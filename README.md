# Unix Task Manager

A FastAPI-based task manager that mimics a simplified Linux process manager. Spawn (fork) tasks, kill them, filter them, sort them, and pretend you're doing something important.

## Features

-  Create tasks (automatically start in `running` status)
-  Fork existing tasks (child inherits name and status)
-  Kill tasks (mark as `killed` and set `ended_at`)
-  Filter by `status`, `parent_id`, or `name`
-  Paginated and sortable task listing
-  Parent-child relationships with recursive grace
-  Full test coverage (kind of)
-  Custom exception handling
-  SQLAlchemy + Alembic + PostgreSQL

## Tech Stack

- **Python 3.11**
- **FastAPI**
- **SQLAlchemy**
- **Alembic**
- **PostgreSQL**
- **Docker + Docker Compose**
- **Pytest**

## Setup

```bash
# Clone the repo
git clone https://github.com/yogeeshhk/unix_task_manager.git
cd unix-task-manager

# Create a .env file
cp .env.example .env

# add your database URL to the .env file
# Example: DATABASE_URL=postgresql://postgres:postgres@db:5432/task_manager 

# build and run the docker containers
docker-compose up --build
```


### API Docs

Available at: [http://localhost:8000/docs](http://localhost:8000/docs)

##  Running Tests

```bash
pytest tests/
```

## Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "your message"

# Apply migration
alembic upgrade head
```
## Troubleshooting

If PostgreSQL enum issues occur:

```sql
DROP TYPE IF EXISTS taskstatus;
```

Ensure the database schema aligns with updated models.


## Example Task

```json
{
  "name": "Compile"
}
```

Response:

```json
{
  "id": 1,
  "name": "Compile",
  "status": "running",
  "created_at": "...",
  "started_at": "...",
  "ended_at": null,
  "parent_id": null
}
