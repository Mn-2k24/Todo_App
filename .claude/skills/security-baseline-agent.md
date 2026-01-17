# Security-Baseline-Agent Skills

## scan_for_secrets

- Checks that code does not contain hardcoded API keys, tokens, passwords
- Blocks commits with exposed secrets
- Allows environment-based secret management

## validate_input_sanitization

- Checks that user inputs are validated and sanitized
- Blocks SQL injection, XSS, command injection vulnerabilities
- Allows parameterized queries and sanitized inputs

## enforce_cors_policy

- Checks that CORS settings are restrictive and intentional
- Blocks permissive CORS (`Access-Control-Allow-Origin: *`) in production
- Allows explicit origin whitelists

## audit_dependency_vulnerabilities

- Checks for known CVEs in dependencies
- Blocks deployment with high/critical severity vulnerabilities
- Allows deployment after vulnerability remediation
