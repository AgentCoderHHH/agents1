from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@dataclass
class User:
    id: str
    username: str
    email: str
    hashed_password: str
    roles: List[str]
    is_active: bool = True
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

@dataclass
class Token:
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600  # 1 hour

class AuthManager:
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 60

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Generate password hash."""
        return pwd_context.hash(password)

    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify a JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            logger.error("Token has expired")
            return None
        except jwt.JWTError:
            logger.error("Invalid token")
            return None

    def has_permission(self, user: User, permission: str) -> bool:
        """Check if a user has a specific permission."""
        # In a real implementation, this would check against a permissions database
        # For now, we'll use a simple role-based check
        if "admin" in user.roles:
            return True
        
        # Define role-based permissions
        role_permissions = {
            "manager": ["read", "write", "delete"],
            "user": ["read"],
            "analyst": ["read", "write"]
        }
        
        for role in user.roles:
            if role in role_permissions and permission in role_permissions[role]:
                return True
        
        return False

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user."""
        # In a real implementation, this would query a user database
        # For now, we'll use a mock user
        mock_user = User(
            id="1",
            username="test_user",
            email="test@example.com",
            hashed_password=self.get_password_hash("password"),
            roles=["user"]
        )
        
        if username == mock_user.username and self.verify_password(password, mock_user.hashed_password):
            return mock_user
        return None

    def create_user(self, username: str, email: str, password: str, roles: List[str]) -> User:
        """Create a new user."""
        # In a real implementation, this would save to a user database
        hashed_password = self.get_password_hash(password)
        return User(
            id=str(len(self._mock_users) + 1),
            username=username,
            email=email,
            hashed_password=hashed_password,
            roles=roles
        )

    def get_user(self, username: str) -> Optional[User]:
        """Get a user by username."""
        # In a real implementation, this would query a user database
        if username == "test_user":
            return User(
                id="1",
                username="test_user",
                email="test@example.com",
                hashed_password=self.get_password_hash("password"),
                roles=["user"]
            )
        return None

    def update_user(self, user: User) -> User:
        """Update a user."""
        # In a real implementation, this would update a user database
        user.updated_at = datetime.utcnow()
        return user

    def delete_user(self, username: str) -> bool:
        """Delete a user."""
        # In a real implementation, this would delete from a user database
        return True 