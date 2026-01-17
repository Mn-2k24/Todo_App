# Todo App - Full-Stack Web Application

A complete todo management application demonstrating **Spec-Driven Development (SDD)** principles using Claude Code across two phases: console-based (Phase I) and full-stack web (Phase II).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-15.x-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)

---

## 📋 Overview

This repository showcases a complete evolution from a minimal console application to a professional full-stack web application, entirely built using **Spec-Driven Development** with Claude Code.

**Phase I (Completed):** In-memory console Todo app
**Phase II (Current):** Full-stack web application with:
- Multi-user authentication (Better Auth + JWT)
- RESTful API backend (FastAPI + PostgreSQL)
- Modern frontend (Next.js 15 + React 19 + TypeScript)
- Advanced features (priorities, tags, due dates, search, filters, sorting)
- Professional UI/UX with Tailwind CSS

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+** (for backend)
- **Node.js 18+** (for frontend)
- **PostgreSQL** (local or hosted, e.g., Neon)
- **UV** (Python package manager, recommended)

### Phase I: Console App

```bash
# Run the in-memory console application (Phase I)
python src/main.py
```

### Phase II: Full-Stack Web App

**1. Backend Setup**

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your DATABASE_URL, JWT_SECRET, BETTER_AUTH_SECRET

# Run database migrations
alembic upgrade head

# Start backend server
uvicorn src.main:app --reload
# Backend runs at http://localhost:8000
# API docs at http://localhost:8000/docs
```

**2. Frontend Setup**

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local with NEXT_PUBLIC_API_URL=http://localhost:8000

# Start development server
npm run dev
# Frontend runs at http://localhost:3000
```

**3. Access the App**

- **Frontend**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/docs
- **Phase I Console**: `python src/main.py`

---

## 🏗️ Architecture

### Phase II Stack

**Frontend:**
- Next.js 15 (App Router)
- React 19
- TypeScript
- Tailwind CSS
- Better Auth (authentication)

**Backend:**
- FastAPI (Python)
- SQLModel (ORM)
- Alembic (migrations)
- PostgreSQL (Neon)
- JWT authentication
- Bcrypt password hashing

**Development:**
- Claude Code (AI-assisted development)
- Spec-Kit Plus (specification framework)
- Custom agents & skills (see `.claude/`)

---

## 📂 Project Structure

```
Todo_App/
├── src/                          # Phase I: Console App (PRESERVED)
│   ├── main.py
│   ├── models/
│   ├── services/
│   └── cli/
│
├── backend/                      # Phase II: FastAPI Backend
│   ├── src/
│   │   ├── main.py              # FastAPI app entry
│   │   ├── api/                 # REST endpoints
│   │   ├── models/              # SQLModel database models
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   ├── services/            # Business logic
│   │   ├── auth/                # JWT + Better Auth integration
│   │   └── utils/               # Error handling, helpers
│   ├── alembic/                 # Database migrations
│   ├── tests/                   # Backend tests
│   └── requirements.txt
│
├── frontend/                     # Phase II: Next.js Frontend
│   ├── src/
│   │   ├── app/                 # Next.js App Router pages
│   │   ├── components/          # React components
│   │   ├── lib/                 # API client, auth utilities
│   │   ├── types/               # TypeScript types
│   │   └── styles/              # Global CSS
│   ├── public/                  # Static assets
│   └── package.json
│
├── specs/                        # Feature Specifications
│   ├── 002-phase-i-spec/        # Phase I spec
│   └── 003-phase-ii-full-stack/ # Phase II spec
│
├── .claude/                      # Claude Code Agents & Skills
│   ├── agents/                  # Specialized AI agents
│   └── skills/                  # Reusable agent skills
│
├── history/                      # Prompt History Records (PHRs)
│   └── prompts/                 # Chronological development history
│
├── .specify/                     # Spec-Kit Plus framework
│   ├── memory/                  # Constitution, templates
│   └── scripts/                 # Automation scripts
│
├── README.md                     # This file
├── CLAUDE.md                     # Development rules & workflow
├── constitution.md               # Project principles
└── .gitignore
```

---

## 🎯 Features

### Phase I: Console App
- ✅ Add tasks
- ✅ View all tasks
- ✅ Update task descriptions
- ✅ Delete tasks
- ✅ Mark tasks complete/incomplete

### Phase II: Full-Stack Web App

**Authentication & Security:**
- ✅ User registration with email + password
- ✅ Secure login with JWT tokens
- ✅ httpOnly cookies for token storage
- ✅ Session persistence
- ✅ Password hashing (bcrypt)
- ✅ Data isolation (users only see their tasks)

**Task Management:**
- ✅ Create, read, update, delete tasks
- ✅ Priority levels (High, Medium, Low)
- ✅ Tags for categorization
- ✅ Due dates with overdue indicators
- ✅ Mark tasks complete/incomplete
- ✅ Immediate UI updates (optimistic rendering)

**Organization & Discovery:**
- ✅ Search tasks by description
- ✅ Filter by priority, tags, status
- ✅ Sort by newest, title, due date, priority
- ✅ Sort preference persistence

**User Experience:**
- ✅ Professional, responsive UI (Tailwind CSS)
- ✅ Loading states for all operations
- ✅ Error handling with user-friendly messages
- ✅ Success/error toast notifications
- ✅ Empty states with helpful guidance
- ✅ Confirmation dialogs for destructive actions

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/                    # Run all tests
pytest tests/unit/              # Unit tests only
pytest tests/integration/       # Integration tests only
pytest tests/contract/          # API contract tests
```

### Frontend Tests

```bash
cd frontend
npm test                        # Run all tests
npm run test:watch             # Watch mode
```

---

## 🔧 Development Workflow

This project follows **Spec-Driven Development (SDD)** principles:

1. **Specify First**: Write detailed specifications before code
2. **Agent-Driven**: Use Claude Code agents for all code generation
3. **No Manual Coding**: All code generated via AI workflows
4. **Quality Gates**: Automated validation at each phase

### Key Commands

```bash
# Specification workflow
/sp.specify       # Create feature specification
/sp.plan          # Generate implementation plan
/sp.tasks         # Break down into tasks
/sp.implement     # Execute implementation

# Quality assurance
/sp.analyze       # Cross-artifact consistency check
/sp.adr           # Create Architecture Decision Record
```

See `CLAUDE.md` for complete workflow documentation.

---

## 📚 Documentation

**Project Documentation:**
- `README.md` - This file (overview & quick start)
- `CLAUDE.md` - Development rules, agent usage, SDD workflow
- `constitution.md` - Project principles, quality standards, constraints

**Specifications:**
- `specs/002-phase-i-spec/spec.md` - Phase I feature specification
- `specs/003-phase-ii-full-stack/spec.md` - Phase II feature specification
- `specs/003-phase-ii-full-stack/plan.md` - Phase II implementation plan

**Agent Documentation:**
- `.claude/agents/` - Specialized AI agents for specific tasks
- `.claude/skills/` - Reusable skills for common operations

**Development History:**
- `history/prompts/` - Complete record of all AI interactions (PHRs)

---

## 🔐 Environment Variables

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/database

# Authentication
JWT_SECRET=your-secret-key-here  # Generate: openssl rand -hex 32
BETTER_AUTH_SECRET=your-auth-secret-here  # Generate: openssl rand -hex 32
JWT_EXPIRATION_HOURS=24

# CORS (optional)
ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**⚠️ SECURITY:** Never commit `.env` or `.env.local` files. Use `.env.example` templates only.

---

## 🚢 Deployment

### Backend (FastAPI)

**Option 1: Railway**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

**Option 2: Render**
- Connect GitHub repository
- Set environment variables
- Deploy with Render.yaml

### Frontend (Next.js)

**Option 1: Vercel** (Recommended)
```bash
npm install -g vercel
vercel
```

**Option 2: Netlify**
- Connect GitHub repository
- Configure build settings
- Deploy

---

## 🤝 Contributing

This repository demonstrates Spec-Driven Development. To contribute:

1. Fork the repository
2. Create a feature branch
3. Follow SDD principles (specify → plan → implement)
4. Use Claude Code agents for code generation
5. Submit pull request with specification

---

## 📜 License

MIT License

Copyright (c) 2026 Mn-2k24

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

---

## 📞 Contact

**GitHub**: [@Mn-2k24](https://github.com/Mn-2k24)

**Project Repository**: [Todo_App](https://github.com/Mn-2k24/Todo_App)

---

## 🎓 Learning Resources

This project demonstrates:
- Spec-Driven Development methodology
- Claude Code agent-based workflows
- Full-stack TypeScript application architecture
- RESTful API design
- Modern authentication patterns
- Professional UI/UX implementation

Explore the `specs/` and `.claude/` directories to see how features were specified and implemented entirely through AI-assisted development.

---

**Built with Claude Code** 🤖
