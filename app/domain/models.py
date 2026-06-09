from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class RecommendationSource(Enum):
    ML_MODEL = "ml_model"
    RULE_BASED = "rule_based"


@dataclass
class User:
    id: Optional[int]
    username: str
    hashed_password: str
    created_at: datetime


@dataclass
class Recommendation:
    id: Optional[int]
    user_id: int
    input_text: str
    recommended_book_title: str
    recommended_book_author: str
    similarity_score: float
    source: RecommendationSource
    created_at: datetime