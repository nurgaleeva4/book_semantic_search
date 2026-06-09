from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.infrastructure.database import get_db, Session
from app.infrastructure.repositories import PostgresUserRepository, PostgresRecommendationRepository
from app.infrastructure.recommender_model import BookRecommender
from app.services.auth_service import AuthService
from app.services.recommendation_service import RecommendationService
from jose import jwt, JWTError
import os

SECRET_KEY = os.getenv("SECRET_KEY", "secret-key-change-me")
ALGORITHM = "HS256"

security = HTTPBearer()


def get_db_session():
    """Генератор сессий для внедрения зависимостей"""
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


def get_user_repo(session: Session = Depends(get_db_session)):
    return PostgresUserRepository(session)


def get_recommendation_repo(session: Session = Depends(get_db_session)):
    return PostgresRecommendationRepository(session)


def get_auth_service(user_repo: PostgresUserRepository = Depends(get_user_repo)):
    return AuthService(user_repo)


def get_recommendation_service(
    recommendation_repo: PostgresRecommendationRepository = Depends(get_recommendation_repo)
):
    recommender = BookRecommender()
    return RecommendationService(recommendation_repo, recommender)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_repo: PostgresUserRepository = Depends(get_user_repo)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = user_repo.get_by_id(int(user_id))
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user