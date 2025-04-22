# Unix Task Manager API

A FastAPI-based task management service inspired by Unix process concepts. Supports authentication, task lifecycle control, user ownership, logging, and more.

## Features

- JWT-based Authentication (Login / Register)
- Admin-restricted healthcheck endpoint
- Task CRUD with:
  - Filtering by status and parent
  - Search by name
  - Sorting (created, ended, name, status)
  - Pagination
- Only task owners can view, fork, or delete their tasks
- Centralized logging (~ last 20 API hits)
- CLI tool to create admin user
- Dockerized setup

## API Docs

Available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Quick Start

```bash
git clone https://github.com/yogeeshhk/unix_task_manager.git
cd unix_task_manager
```

### Setup (Local)

```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Run the API

```bash
uvicorn src.main:app --reload
```

## Build Docker Image

```bash
docker-compose build
```

## Run Docker Container

```bash
docker-compose up
```

## Admin CLI

```bash
python create_admin.py create_admin --username your_admin --password your_password
```

## Running Tests

```bash
pytest tests/
```

## Healthcheck (Admin Only)

```http
GET /healthcheck
Authorization: Bearer <admin_token>
```

Returns recent logs and timestamp.

## Authentication

- `/auth/register` - Create a new user
- `/auth/login` - Get JWT token

Use `Authorization: Bearer <token>` header for authenticated requests.

---

## Project Structure

```
src/
│
├── auth/             # Authentication module
├── task/             # Task logic (CRUD, lifecycle)
├── common/           # Shared utils (exceptions, logger)
├── db/               # DB setup and models
├── config.py         # Settings and environment
├── main.py           # Entry point
└── ...
```

## Extra Notes
Some quick context on choices I made while putting this together:

- FastAPI - Picked it because it is lightweight and has great async support. It’s also pretty easy to get up and running with.
- JWT + Custom Exceptions - Instead of throwing HTTPException all over the place, I added a few custom ones to keep responses consistent along with a centralized exception handler - easier to handle in the client (and logs).
- Service Layer - Moved logic out of the route functions and into separate service modules. Keeps the routes cleaner and helps a lot with testing and reuse.
- Typer for CLI - Used Typer for the admin CLI tool, helps build simple command-line stuff quick.
- Rotating Logger - Added rotating file logging for the API. Keeps the logs manageable and makes debugging a lot easier without having to tail a massive file. This can also be accessed by admin using Healthcheck endpoint.
- Swagger Auth Cleanup - Replaced OAuth2PasswordRequestForm with a JSON-based login to avoid the extra fields Swagger adds by default. Simpler and easier to work with on the frontend too.
- Docker Compose - Just a quick setup for local dev.