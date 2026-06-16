"""
Authentication and Authorization Module

Handles user authentication, token validation, and permission checking.
"""

import hashlib
import json
from datetime import datetime, timedelta


class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass


class TokenManager:
    """Manages authentication tokens for the platform."""

    def __init__(self, secret_key=None):
        """Initialize token manager with a secret key."""
        self.secret_key = secret_key or "default-insecure-key"
        self.tokens = {}
        self.token_expiry = timedelta(hours=24)

    def generate_token(self, user_id):
        """Generate an authentication token for a user."""
        token_data = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + self.token_expiry).isoformat(),
        }
        token = hashlib.sha256(
            (user_id + self.secret_key + str(datetime.now())).encode()
        ).hexdigest()
        self.tokens[token] = token_data
        return token

    def validate_token(self, token):
        """Validate an authentication token."""
        if token not in self.tokens:
            raise AuthenticationError("Invalid token")

        token_data = self.tokens[token]
        if datetime.fromisoformat(token_data["expires_at"]) < datetime.now():
            del self.tokens[token]
            raise AuthenticationError("Token expired")

        return token_data["user_id"]

    def revoke_token(self, token):
        """Revoke an authentication token."""
        if token in self.tokens:
            del self.tokens[token]


class PermissionManager:
    """Manages user permissions and access control."""

    def __init__(self):
        """Initialize permission manager."""
        self.roles = {
            "admin": ["read", "write", "delete", "audit"],
            "user": ["read", "write"],
            "viewer": ["read"],
        }

    def has_permission(self, user_role, action):
        """Check if a user has permission to perform an action."""
        if user_role not in self.roles:
            return False
        return action in self.roles[user_role]

    def grant_permission(self, user_role, action):
        """Grant a new permission to a role."""
        if user_role not in self.roles:
            self.roles[user_role] = []
        if action not in self.roles[user_role]:
            self.roles[user_role].append(action)
