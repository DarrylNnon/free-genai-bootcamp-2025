# Role: DevSecOps Engineer

## Task:
Create a secure, multi-stage Dockerfile for a Python Flask web application.

## Context:
The application has a `requirements.txt` file and the main application file is `app.py`. The application listens on port 5000.

## Security Requirements:
1.  **Multi-stage build:** Use a builder stage to install dependencies and a final, smaller stage for the runtime.
2.  **Minimal base image:** Use a minimal, secure base image for the final stage (e.g., `python:3.10-slim`).
3.  **Non-root user:** Create and run the application as a non-root user.
4.  **Pin dependencies:** The `requirements.txt` is assumed to have pinned versions.
5.  **Do not leak secrets:** Ensure no build secrets or credentials are left in the final image.
6.  **Healthcheck:** Add a `HEALTHCHECK` instruction.