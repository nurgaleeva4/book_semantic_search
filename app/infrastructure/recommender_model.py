import json
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from app.domain.interfaces import RecommenderModelInterface

BOOKS_DATA_PATH = os.getenv("BOOKS_DATA_PATH", "data/books_metadata.json")
EMBEDDINGS_PATH = os.getenv("EMBEDDINGS_PATH", "data/embeddings.npy")


class BookRecommender(RecommenderModelInterface):
    def __init__(self):
        self.model = None
        self.books = []
        self.embeddings = None
        self.is_loaded = False

    def load(self):
        """Загружает модель и данные о книгах"""
        print("Загрузка нейросети для рекомендаций...")
        self.model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

        print("Загрузка базы книг...")
        with open(BOOKS_DATA_PATH, "r", encoding="utf-8") as f:
            self.books = json.load(f)

        print("Загрузка эмбеддингов книг...")
        self.embeddings = np.load(EMBEDDINGS_PATH)

        self.is_loaded = True
        print(f"Загружено {len(self.books)} книг. Рекомендательная система готова!")

    def recommend(self, text: str) -> list:
        """Возвращает список рекомендаций (похожих книг)"""
        if not self.is_loaded:
            self.load()

        query_embedding = self.model.encode([text])
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]

        indexed = list(enumerate(similarities))
        indexed.sort(key=lambda x: x[1], reverse=True)

        results = []
        for idx, score in indexed[:10]:
            if score > 0.2 and len(results) < 5:
                book = self.books[idx]
                results.append({
                    "title": book["title"],
                    "author": book["author"],
                    "description": book["description"][:200] + "..." if len(book["description"]) > 200 else book["description"],
                    "similarity": round(float(score), 3)
                })
        return results