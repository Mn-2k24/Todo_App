"""
Chat Service - 7-Step Pipeline

Implements stateless chat API with conversation persistence:
1. Receive & Validate
2. Load Conversation History
3. Persist User Message
4. Invoke AI Agent
5. Execute MCP Tools
6. Persist Assistant Response
7. Return Response
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from phase3.agent.orchestrator import AgentOrchestrator
from phase3.models.conversation import Conversation
from phase3.models.message import Message
from phase3.schemas.chat_schema import ChatRequest, ChatResponse, ErrorResponse, ToolCall
from phase3.services.mcp_client import get_mcp_client

logger = logging.getLogger(__name__)


class ChatServiceError(Exception):
    """Base exception for chat service errors."""

    pass


class ConversationNotFoundError(ChatServiceError):
    """Raised when conversation doesn't exist."""

    pass


class UnauthorizedAccessError(ChatServiceError):
    """Raised when user tries to access conversation they don't own."""

    pass


class ChatService:
    """
    Stateless chat service implementing 7-step pipeline.

    Each request is independent - conversation state is loaded from database.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize chat service.

        Args:
            session: Database session for conversation persistence
        """
        self.session = session
        self.mcp_client = get_mcp_client()

    async def process_chat_message(
        self, user_id: UUID, request: ChatRequest
    ) -> ChatResponse:
        """
        Process a chat message through the 7-step pipeline.

        Args:
            user_id: Authenticated user's UUID
            request: ChatRequest with message and optional conversation_id

        Returns:
            ChatResponse with response, conversation_id, message_id, tool_calls

        Raises:
            ChatServiceError: If processing fails
            UnauthorizedAccessError: If user doesn't own conversation
        """
        try:
            # Step 1: Receive & Validate
            self._validate_request(user_id, request)

            # Step 2: Load Conversation History
            conversation, history = await self._load_conversation_history(
                user_id, request.conversation_id
            )

            # Step 3: Persist User Message
            user_message = await self._persist_user_message(
                conversation.id, request.message
            )

            # Step 4: Invoke AI Agent
            agent_result = await self._invoke_ai_agent(
                user_id, request.message, history
            )

            # Step 5: Execute MCP Tools
            tool_results = await self._execute_mcp_tools(agent_result["tool_calls"])

            # Step 6: Persist Assistant Response
            assistant_message = await self._persist_assistant_response(
                conversation.id, agent_result["message"], tool_results
            )

            # Step 7: Return Response
            return self._build_response(
                conversation.id, assistant_message, agent_result["message"], tool_results
            )

        except UnauthorizedAccessError:
            raise
        except Exception as e:
            logger.error(f"Chat processing failed: {e}", exc_info=True)
            raise ChatServiceError(f"Failed to process chat message: {str(e)}") from e

    # Step 1: Receive & Validate

    def _validate_request(self, user_id: UUID, request: ChatRequest):
        """
        Validate incoming request.

        Args:
            user_id: User UUID from JWT
            request: ChatRequest to validate

        Raises:
            ChatServiceError: If validation fails
        """
        # User ID validation (already done by FastAPI dependency)
        if not user_id:
            raise ChatServiceError("Missing user_id")

        # Message validation (already done by Pydantic, but double-check)
        if not request.message or not request.message.strip():
            raise ChatServiceError("Message cannot be empty")

        if len(request.message) > 2000:
            raise ChatServiceError("Message too long (max 2000 characters)")

        # Conversation ID format validation (if provided)
        if request.conversation_id:
            try:
                UUID(str(request.conversation_id))
            except ValueError:
                raise ChatServiceError("Invalid conversation_id format (must be UUID)")

        logger.info(f"Request validated for user {user_id}")

    # Step 2: Load Conversation History

    async def _load_conversation_history(
        self, user_id: UUID, conversation_id: Optional[UUID]
    ) -> tuple[Conversation, List[Dict[str, str]]]:
        """
        Load existing conversation or create new one.

        Args:
            user_id: User UUID
            conversation_id: Optional existing conversation ID

        Returns:
            Tuple of (Conversation, history messages)

        Raises:
            ConversationNotFoundError: If conversation doesn't exist
            UnauthorizedAccessError: If user doesn't own conversation
        """
        if conversation_id:
            # Load existing conversation
            result = await self.session.execute(
                select(Conversation).where(Conversation.id == conversation_id)
            )
            conversation = result.scalar_one_or_none()

            if not conversation:
                raise ConversationNotFoundError(
                    f"Conversation {conversation_id} not found"
                )

            # Verify ownership
            if conversation.user_id != user_id:
                logger.warning(
                    f"User {user_id} attempted to access conversation {conversation_id} "
                    f"owned by {conversation.user_id}"
                )
                raise UnauthorizedAccessError(
                    "You don't have permission to access this conversation"
                )

            # Load last 10 messages
            messages_result = await self.session.execute(
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.desc())
                .limit(10)
            )
            messages = messages_result.scalars().all()

            # Reverse to chronological order and format for agent
            history = [
                {"role": msg.role, "content": msg.content}
                for msg in reversed(messages)
            ]

            logger.info(
                f"Loaded conversation {conversation_id} with {len(history)} messages"
            )

        else:
            # Create new conversation
            conversation = Conversation(
                id=uuid4(),
                user_id=user_id,
                title=None,  # Will be auto-generated from first message
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            self.session.add(conversation)
            await self.session.flush()  # Get the ID without committing

            history = []
            logger.info(f"Created new conversation {conversation.id}")

        return (conversation, history)

    # Step 3: Persist User Message

    async def _persist_user_message(
        self, conversation_id: UUID, content: str
    ) -> Message:
        """
        Save user's message to database.

        Args:
            conversation_id: Conversation UUID
            content: Message text

        Returns:
            Created Message object
        """
        message = Message(
            id=uuid4(),
            conversation_id=conversation_id,
            role="user",
            content=content,
            tool_calls=None,
            created_at=datetime.utcnow(),
        )

        self.session.add(message)
        await self.session.flush()

        logger.info(f"Persisted user message {message.id} in conversation {conversation_id}")
        return message

    # Step 4: Invoke AI Agent

    async def _invoke_ai_agent(
        self, user_id: UUID, message: str, history: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Invoke AI agent orchestrator with conversation history.

        Args:
            user_id: User UUID
            message: User's message
            history: Previous conversation messages

        Returns:
            Agent result dict with intent, message, tool_calls
        """
        # Create agent orchestrator
        agent = AgentOrchestrator(
            user_id=user_id,
            mcp_client=self.mcp_client,
            use_mock_llm=False,  # Use real Gemini in production
        )

        # Load history into agent
        agent.conversation_history = history

        # Process message
        result = await agent.process_message(message)

        logger.info(
            f"Agent processed message: intent={result['intent']}, "
            f"tools={len(result['tool_calls'])}"
        )

        return result

    # Step 5: Execute MCP Tools

    async def _execute_mcp_tools(
        self, tool_calls: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Execute MCP tools from agent's tool calls.

        Args:
            tool_calls: List of tool calls from agent

        Returns:
            List of tool results
        """
        if not tool_calls:
            return []

        # Extract tool calls for MCP client format
        mcp_calls = []
        for call in tool_calls:
            mcp_calls.append({
                "tool_name": call["tool_name"],
                "parameters": call["parameters"],
            })

        # Execute tools via MCP client
        results = await self.mcp_client.invoke_multiple_tools(mcp_calls)

        logger.info(f"Executed {len(results)} MCP tools")
        return results

    # Step 6: Persist Assistant Response

    async def _persist_assistant_response(
        self, conversation_id: UUID, content: str, tool_results: List[Dict[str, Any]]
    ) -> Message:
        """
        Save assistant's response to database.

        Args:
            conversation_id: Conversation UUID
            content: Response text
            tool_results: Results from MCP tool execution

        Returns:
            Created Message object
        """
        # Serialize tool results to JSON
        tool_calls_json = json.dumps(tool_results) if tool_results else None

        message = Message(
            id=uuid4(),
            conversation_id=conversation_id,
            role="assistant",
            content=content,
            tool_calls=tool_calls_json,
            created_at=datetime.utcnow(),
        )

        self.session.add(message)

        # Update conversation updated_at timestamp
        conversation_result = await self.session.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = conversation_result.scalar_one()
        conversation.updated_at = datetime.utcnow()

        # Commit all changes
        await self.session.commit()

        logger.info(
            f"Persisted assistant message {message.id} in conversation {conversation_id}"
        )
        return message

    # Step 7: Return Response

    def _build_response(
        self,
        conversation_id: UUID,
        message: Message,
        response_text: str,
        tool_results: List[Dict[str, Any]],
    ) -> ChatResponse:
        """
        Build ChatResponse from results.

        Args:
            conversation_id: Conversation UUID
            message: Persisted Message object
            response_text: Natural language response
            tool_results: Tool execution results

        Returns:
            ChatResponse object
        """
        # Convert tool results to ToolCall schema
        tool_calls = []
        for result in tool_results:
            tool_calls.append(
                ToolCall(
                    tool_name=result.get("tool_name", "unknown"),
                    parameters=result.get("parameters", {}),
                    result=result,
                )
            )

        return ChatResponse(
            conversation_id=conversation_id,
            message_id=message.id,
            response=response_text,
            tool_calls=tool_calls,
            created_at=message.created_at,
        )


# Dependency for FastAPI

async def get_chat_service(
    session: AsyncSession = Depends(get_session),
) -> ChatService:
    """
    FastAPI dependency to get ChatService instance.

    Args:
        session: Database session from dependency

    Returns:
        ChatService instance
    """
    return ChatService(session)
