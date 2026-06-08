from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models import User, Prediction


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


class PredictionRepository(ABC):
    @abstractmethod
    async def create(self, prediction: Prediction) -> Prediction:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int, limit: int = 50) -> List[Prediction]:
        pass


class MLModelInterface(ABC):
    @abstractmethod
    def predict(self, text: str) -> tuple[str, float]:
        pass