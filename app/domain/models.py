from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class PredictionSource(Enum):
    ML_MODEL = "ml_model"
    RULE_BASED = "rule_based"


@dataclass
class User:
    id: Optional[int]
    username: str
    hashed_password: str
    created_at: datetime


@dataclass
class Prediction:
    id: Optional[int]
    user_id: int
    input_text: str
    predicted_genre: str
    confidence: float
    source: PredictionSource
    created_at: datetime