from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.infrastructure.database import get_db, AsyncSession
from app.infrastructure.repositories import PostgresUserRepository, PostgresRecommendationRepository
from app.infrastructure.recommender_model import BookRecommender
from app.services.auth_service import AuthService
from app.services.recommendation_service import RecommendationService
from jose import jwt, JWTError
import os

SECRET_KEY = os.getenv("SECRET_KEY", "secret-key-change-me")
ALGORITHM = "HS256"

security = HTTPBearer()


async def get_db_session():
    async for session in get_db():
        yield session


async def get_user_repo(session: Annotated[AsyncSession, Depends(get_db_session)]):
    return PostgresUserRepository(session)


async def get_recommendation_repo(session: Annotated[AsyncSession, Depends(get_db_session)]):
    return PostgresRecommendationRepository(session)


async def get_auth_service(user_repo: Annotated[PostgresUserRepository, Depends(get_user_repo)]):
    return AuthService(user_repo)


async def get_recommendation_service(
    recommendation_repo: Annotated[PostgresRecommendationRepository, Depends(get_recommendation_repo)]
):
    recommender = BookRecommender()
    return RecommendationService(recommendation_repo, recommender)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_repo: Annotated[PostgresUserRepository, Depends(get_user_repo)]
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await user_repo.get_by_id(int(user_id))
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user