import sys

import typer
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.auth.models import User
from src.auth.service import get_password_hash
from src.common.logger import get_logger
from src.db.database import SessionLocal
from src.db.utils import check_db_connection

app = typer.Typer()
logger = get_logger(__name__)


@app.callback()
def validate_db():
    if not check_db_connection():
        typer.echo("Database is not available. Please ensure it's running.")
        raise typer.Exit(code=1)


@app.command()
def create_admin(
        username: str = typer.Option(..., "--username", "-u", help="Username for the admin user."),
        password: str = typer.Option(
            ..., "--password", "-p",
            help="Password for the admin user.",
            prompt=True, hide_input=True, confirmation_prompt=True
        ),
):
    try:
        db: Session = SessionLocal()

        existing = db.query(User).filter(User.username == username).first()
        if existing:
            msg = f"Admin with username '{username}' already exists."
            logger.error(msg)
            typer.echo(msg)
            sys.exit(1)

        hashed_password = get_password_hash(password)
        admin = User(username=username, hashed_password=hashed_password, is_admin=True)

        db.add(admin)
        db.commit()
        db.refresh(admin)

        logger.info(f"Admin created: {username}")
        typer.echo(f"Admin user '{username}' created successfully.")

    except SQLAlchemyError:
        logger.exception("Database error while creating admin user.")
        typer.echo("An error occurred while accessing the database.")
        sys.exit(1)

    except Exception:
        logger.exception("Unexpected error occurred.")
        typer.echo("Something went wrong. Check the logs for more details.")
        sys.exit(1)


if __name__ == "__main__":
    app()
