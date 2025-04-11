from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy (assume db is initialized in your Flask app)
db = SQLAlchemy()

class RegisteredUser(db.Model):
    __tablename__ = 'registered_users'
    
    user_id = db.Column(db.String(128), primary_key=True, nullable=False)  # Unique identifier for the user
    D_i = db.Column(db.LargeBinary, nullable=False)  # Storing bytes securely
    registration_date = db.Column(
        db.DateTime, 
        nullable=False, 
        default=datetime.utcnow
    )
    last_updated = db.Column(
        db.DateTime, 
        nullable=False, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )

    def __init__(self, user_id: str, D_i: bytes):
        self.user_id = user_id
        self.D_i = D_i

    def __repr__(self):
        return f"<RegisteredUser(user_id={self.user_id})>"


class RegisteredServer(db.Model):
    __tablename__ = 'registered_servers'
    
    server_id = db.Column(db.String(128), primary_key=True, nullable=False)  # Unique identifier for the server
    SB_j = db.Column(db.LargeBinary, nullable=False)  # Storing bytes securely
    SM_j = db.Column(db.LargeBinary, nullable=False)  # Storing bytes securely
    registration_date = db.Column(
        db.DateTime, 
        nullable=False, 
        default=datetime.utcnow
    )
    last_updated = db.Column(
        db.DateTime, 
        nullable=False, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )

    def __init__(self, server_id: str, SB_j: bytes, SM_j: bytes):
        self.server_id = server_id
        self.SB_j = SB_j
        self.SM_j = SM_j

    def __repr__(self):
        return f"<RegisteredServer(server_id={self.server_id})>"
