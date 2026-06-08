from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated, List
from app.api.dependencies import get_recommendation_service, get_current_user
from app.services.recommendation_service import RecommendationService
from app.domain.models import User

router = APIRouter(tags=["recommend"])


class RecommendRequest(BaseModel):
    text: str


class RecommendItem(BaseModel):
    title: str
    author: str
    description: str
    similarity: float


class RecommendResponse(BaseModel):
    query: str
    recommendations: List[RecommendItem]


@router.post("/recommend", response_model=RecommendResponse)
async def recommend(
    request: RecommendRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    recommendation_service: Annotated[RecommendationService, Depends(get_recommendation_service)]
):
    if not request.text or len(request.text.strip()) < 3:
        raise HTTPException(status_code=400, detail="Text must be at least 3 characters")

    recommendations = await recommendation_service.recommend(current_user.id, request.text)

    return RecommendResponse(
        query=request.text,
        recommendations=[RecommendItem(**r) for r in recommendations]
    )