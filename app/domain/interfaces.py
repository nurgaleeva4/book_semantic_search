from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models import User, Recommendation, RecommendationSource


class UserRepository(ABC):
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    async def create(self, username: str, hashed_password: str) -> User:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass


class RecommendationRepository(ABC):
    @abstractmethod
    async def create(self, recommendation: Recommendation) -> Recommendation:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int, limit: int = 50) -> List[Recommendation]:
        pass


class RecommenderModelInterface(ABC):
    @abstractmethod
    def recommend(self, text: str) -> List[dict]:
        """Возвращает список рекомендаций: list of {title, author, description, similarity}"""
        pass