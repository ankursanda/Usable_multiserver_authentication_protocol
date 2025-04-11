from datetime import datetime
from typing import Tuple
from flask import current_app  # To access the Flask app context
from .cryptoUtils import CryptoUtils
import logging
from app.models import RegisteredUser, RegisteredServer
from app.database import storage  # Import the storage instance

logger = logging.getLogger(__name__)

class RegistrationCenter:
    def __init__(self, secret_key):
        # Access SECRET_KEY from the Flask app context
        self._secret_key = secret_key
        if not self._secret_key:
            raise ValueError("SECRET_KEY is not set in the app configuration.")
        logger.info("Registration Center initialized")
        
    def register_user(self, user_id: str, A_i: bytes) -> Tuple[bytes, bytes]:
        """Register a new user following the protocol."""
        try:
            # Calculate B_i = h(x||ID_i)
            B_i = CryptoUtils.hash_value(self._secret_key.encode() + user_id.encode())
            
            # Calculate D_i = B_i ⊕ h(h(x)||ID_i)
            D_i = CryptoUtils.xor_bytes(
                B_i,
                CryptoUtils.hash_value(CryptoUtils.hash_value(self._secret_key.encode()) + user_id.encode())
            )
            
            # Calculate C_i = h(h(x)||A_i||ID_i)
            C_i = CryptoUtils.hash_value(
                CryptoUtils.hash_value(self._secret_key.encode()) +
                A_i +
                user_id.encode()
            )
            
            # Store user registration in the database
            # user = RegisteredUser(
            #     user_id=user_id,
            #     D_i=D_i,
            #     # registration_date=datetime.utcnow(),
            #     # last_updated=datetime.utcnow()
            # )
            # storage.add_user(user)  # Persist user data to the database
            
            logger.info(f"User {user_id} registered successfully")
            return C_i, CryptoUtils.hash_value(self._secret_key.encode())
            
        except Exception as e:
            logger.error(f"Error registering user {user_id}: {str(e)}")
            raise

    def register_server(self, server_id: str, Q_j: bytes, V_j: bytes) -> Tuple[bytes, bytes]:
        """Register a new server following the protocol."""
        try:
            # Calculate SB_j = (x||SID_j)
            SB_j = self._secret_key.encode() + server_id.encode()
            
            # Calculate SM_j = SB_j ⊕ h(h(x)||Q_j||SID_j)
            SM_j = CryptoUtils.xor_bytes(
                SB_j,
                CryptoUtils.hash_value(
                    CryptoUtils.hash_value(self._secret_key.encode()) +
                    Q_j +
                    server_id.encode()
                )
            )
            
            # Calculate SV_j = Q_j ⊕ h(SID_j)
            SV_j = CryptoUtils.xor_bytes(
                Q_j,
                CryptoUtils.hash_value(server_id.encode())
            )
            
            # Store server registration in the database
            server = RegisteredServer(
                server_id=server_id,
                SB_j=SB_j,
                SM_j=SM_j,
                registration_date=datetime.utcnow(),
                last_updated=datetime.utcnow()
            )
            storage.add_server(server)  # Persist server data to the database
            
            logger.info(f"Server {server_id} registered successfully")
            return SM_j, SV_j
            
        except Exception as e:
            logger.error(f"Error registering server {server_id}: {str(e)}")
            raise
