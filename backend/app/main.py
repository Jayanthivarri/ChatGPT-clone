
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.database.database import Base, engine
from app.database.models import User
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ChatGPT Clone API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
       "https://chatgpt-clone-3-o44o.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chat_router)

@app.get("/")
def home():
    return {
        "message": "ChatGPT Clone Backend is Running 🚀"
    }


if __name__ == "__main__":
    uvicorn.run("app.main:app",host="127.0.0.1",port=8000,reload=True)