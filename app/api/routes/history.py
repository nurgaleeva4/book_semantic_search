from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Annotated, List
from app.api.dependencies import get_recommendation_service, get_current_user
from app.services.recommendation_service import RecommendationService
from app.domain.models import User

router = APIRouter(tags=["history"])


class HistoryItem(BaseModel):
    id: int
    input_text: str
    recommended_book_title: str
    recommended_book_author: str
    similarity_score: float
    created_at: str


class HistoryResponse(BaseModel):
    recommendations: List[HistoryItem]


@router.get("/recommendations/history", response_model=HistoryResponse)
async def get_history(
    current_user: Annotated[User, Depends(get_current_user)],
    recommendation_service: Annotated[RecommendationService, Depends(get_recommendation_service)]
):
    recommendations = await recommendation_service.get_user_history(current_user.id)
    return HistoryResponse(recommendations=recommendations)