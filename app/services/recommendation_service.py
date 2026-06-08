from app.domain.interfaces import RecommendationRepository, RecommenderModelInterface
from app.domain.models import Recommendation, RecommendationSource
from datetime import datetime


class RecommendationService:
    def __init__(self, recommendation_repo: RecommendationRepository, recommender: RecommenderModelInterface):
        self.recommendation_repo = recommendation_repo
        self.recommender = recommender

    async def recommend(self, user_id: int, input_text: str) -> list:
        """Возвращает рекомендации и сохраняет результат"""
        recommendations = self.recommender.recommend(input_text)

        for rec in recommendations:
            recommendation = Recommendation(
                id=None,
                user_id=user_id,
                input_text=input_text[:500],
                recommended_book_title=rec["title"],
                recommended_book_author=rec["author"],
                similarity_score=rec["similarity"],
                source=RecommendationSource.ML_MODEL,
                created_at=datetime.utcnow()
            )
            await self.recommendation_repo.create(recommendation)

        return recommendations

    async def get_user_history(self, user_id: int, limit: int = 50) -> list:
        recommendations = await self.recommendation_repo.get_by_user_id(user_id, limit)
        return [
            {
                "id": r.id,
                "input_text": r.input_text,
                "recommended_book_title": r.recommended_book_title,
                "recommended_book_author": r.recommended_book_author,
                "similarity_score": r.similarity_score,
                "created_at": r.created_at.isoformat()
            }
            for r in recommendations
        ]