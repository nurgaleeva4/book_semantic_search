from app.domain.interfaces import UserRepository
from app.domain.models import User
from passlib.context import CryptContext
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def hash_password(self, password: str) -> str:
        """Хеширует пароль с помощью bcrypt"""
        return pwd_context.hash(password)

    def verify_password(self, plain: str, hashed: str) -> bool:
        """Проверяет, соответствует ли пароль хешу"""
        return pwd_context.verify(plain, hashed)

    def register(self, username: str, password: str) -> User:
        """Регистрирует нового пользователя"""
        existing = self.user_repo.get_by_username(username)
        if existing:
            raise ValueError("Username already exists")
        hashed = self.hash_password(password)
        return self.user_repo.create(username, hashed)

    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Аутентифицирует пользователя по логину и паролю"""
        user = self.user_repo.get_by_username(username)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user