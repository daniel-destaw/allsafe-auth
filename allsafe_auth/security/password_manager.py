import bcrypt
import re
from typing import Optional

class PasswordPolicy:
    def __init__(
        self,
        min_length: int = 0,
        require_digit: bool = False,
        require_uppercase: bool = False,
        require_lowercase: bool = False,
        require_special: bool = False,
        custom_regex: Optional[str] = None,
    ):
        self.min_length = min_length
        self.require_digit = require_digit
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_special = require_special
        self.custom_regex = custom_regex

    @staticmethod
    def no_restriction():
        return PasswordPolicy()

    @staticmethod
    def medium():
        return PasswordPolicy(
            min_length=8,
            require_digit=True,
            require_lowercase=True
        )

    @staticmethod
    def strong():
        return PasswordPolicy(
            min_length=12,
            require_digit=True,
            require_uppercase=True,
            require_lowercase=True,
            require_special=True
        )

class PasswordManager:
    def __init__(self, policy: Optional[PasswordPolicy] = None):
        self.policy = policy or PasswordPolicy.medium()  # default to medium

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    def validate_password_strength(self, password: str) -> bool:
        policy = self.policy

        if len(password) < policy.min_length:
            return False
        if policy.require_digit and not re.search(r"\d", password):
            return False
        if policy.require_uppercase and not re.search(r"[A-Z]", password):
            return False
        if policy.require_lowercase and not re.search(r"[a-z]", password):
            return False
        if policy.require_special and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        if policy.custom_regex and not re.match(policy.custom_regex, password):
            return False
        return True
