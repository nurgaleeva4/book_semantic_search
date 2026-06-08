from fastapi import FastAPI
from app.api.routes import health, auth, recommend, history

app = FastAPI(title="Book Recommender API", version="1.0.0")

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(recommend.router)
app.include_router(history.router)


@app.get("/")
async def root():
    return {"message": "Book Recommender API", "docs": "/docs"}