from app.domain.interfaces import RecommendationRepository, RecommenderModelInterface
from app.domain.models import Recommendation, RecommendationSource
from datetime import datetime


class RecommendationService:
    def __init__(self, recommendation_repo: RecommendationRepository, recommender: RecommenderModelInterface):
        self.recommendation_repo = recommendation_repo
        self.recommender = recommender

    def recommend(self, user_id: int, input_text: str) -> list:
        """
        Возвращает рекомендации похожих книг и сохраняет результат в историю.

        Args:
            user_id: ID пользователя
            input_text: Описание книги, которая понравилась

        Returns:
            list: Список рекомендаций (title, author, description, similarity)
        """
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
            self.recommendation_repo.create(recommendation)

        return recommendations

    def get_user_history(self, user_id: int, limit: int = 50) -> list:
        """
        Возвращает историю рекомендаций пользователя.

        Args:
            user_id: ID пользователя
            limit: Максимальное количество записей

        Returns:
            list: Список рекомендаций с полями id, input_text, recommended_book_title,
                  recommended_book_author, similarity_score, created_at
        """
        recommendations = self.recommendation_repo.get_by_user_id(user_id, limit)
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