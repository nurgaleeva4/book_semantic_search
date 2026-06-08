from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.interfaces import UserRepository, RecommendationRepository
from app.domain.models import User, Recommendation, RecommendationSource
from app.infrastructure.database import UserModel, RecommendationModel
from datetime import datetime
from typing import Optional, List


class PostgresUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        user = result.scalar_one_or_none()
        if user:
            return User(
                id=user.id,
                username=user.username,
                hashed_password=user.hashed_password,
                created_at=user.created_at
            )
        return None

    async def create(self, username: str, hashed_password: str) -> User:
        user = UserModel(username=username, hashed_password=hashed_password)
        self.session.add(user)
        await self.session.flush()
        return User(
            id=user.id,
            username=user.username,
            hashed_password=user.hashed_password,
            created_at=user.created_at
        )

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user = result.scalar_one_or_none()
        if user:
            return User(
                id=user.id,
                username=user.username,
                hashed_password=user.hashed_password,
                created_at=user.created_at
            )
        return None


class PostgresRecommendationRepository(RecommendationRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, recommendation: Recommendation) -> Recommendation:
        rec = RecommendationModel(
            user_id=recommendation.user_id,
            input_text=recommendation.input_text,
            recommended_book_title=recommendation.recommended_book_title,
            recommended_book_author=recommendation.recommended_book_author,
            similarity_score=recommendation.similarity_score,
            source=recommendation.source.value,
            created_at=recommendation.created_at or datetime.utcnow()
        )
        self.session.add(rec)
        await self.session.flush()
        recommendation.id = rec.id
        return recommendation

    async def get_by_user_id(self, user_id: int, limit: int = 50) -> List[Recommendation]:
        result = await self.session.execute(
            select(RecommendationModel)
            .where(RecommendationModel.user_id == user_id)
            .order_by(RecommendationModel.created_at.desc())
            .limit(limit)
        )
        recs = result.scalars().all()
        return [
            Recommendation(
                id=r.id,
                user_id=r.user_id,
                input_text=r.input_text,
                recommended_book_title=r.recommended_book_title,
                recommended_book_author=r.recommended_book_author,
                similarity_score=r.similarity_score,
                source=RecommendationSource(r.source),
                created_at=r.created_at
            )
            for r in recs
        ]