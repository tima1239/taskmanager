from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users, tasks
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager Cloud")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/")
def home():
    return {"message": "☁️ Task Manager Cloud API работает!"}

