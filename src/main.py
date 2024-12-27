import uvicorn
from fastapi import FastAPI

from src.endpoints.youtube import router as youtube_router

app = FastAPI()
app.include_router(youtube_router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, workers=2)
