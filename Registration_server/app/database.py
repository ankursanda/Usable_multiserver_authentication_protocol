from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
from .models import db, RegisteredUser, RegisteredServer  # Import your models

class Storage:
    def __init__(self):
        pass  # SQLAlchemy handles the database connection

    def add_user(self, user: RegisteredUser):
        try:
            db.session.add(user)
            db.session.commit()
            print(f"User {user.user_id} added successfully.")
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error adding user {user.user_id}: {str(e)}")

    def add_server(self, server: RegisteredServer):
        try:
            db.session.add(server)
            db.session.commit()
            print(f"Server {server.server_id} added successfully.")
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error adding server {server.server_id}: {str(e)}")

    def get_user(self, user_id: str) -> Optional[RegisteredUser]:
        try:
            return RegisteredUser.query.get(user_id)
        except SQLAlchemyError as e:
            print(f"Error retrieving user {user_id}: {str(e)}")
            return None

    def get_server(self, server_id: str) -> Optional[RegisteredServer]:
        try:
            return RegisteredServer.query.get(server_id)
        except SQLAlchemyError as e:
            print(f"Error retrieving server {server_id}: {str(e)}")
            return None

# Initialize the storage instance
storage = Storage()
