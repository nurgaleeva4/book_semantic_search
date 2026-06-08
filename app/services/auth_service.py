from app.domain.interfaces import UserRepository
from app.domain.models import User
from passlib.context import CryptContext
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    async def register(self, username: str, password: str) -> User:
        existing = await self.user_repo.get_by_username(username)
        if existing:
            raise ValueError("Username already exists")
        hashed = self.hash_password(password)
        return await self.user_repo.create(username, hashed)

    async def authenticate(self, username: str, password: str) -> Optional[User]:
        user = await self.user_repo.get_by_username(username)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user