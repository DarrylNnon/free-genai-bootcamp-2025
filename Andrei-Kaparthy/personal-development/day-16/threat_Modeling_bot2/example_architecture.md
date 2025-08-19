# Architecture: User Authentication & Profile Service

This document describes a simple microservice for handling user registration, login, and profile management.

## Components

1.  **React Web Client**: A single-page application (SPA) that serves as the user interface. It communicates with the backend via a REST API.
2.  **Auth API (Node.js/Express)**: A backend service that exposes several endpoints:
    *   `POST /register`: Allows new users to sign up with an email and password.
    *   `POST /login`: Authenticates users and returns a JWT.
    *   `GET /profile