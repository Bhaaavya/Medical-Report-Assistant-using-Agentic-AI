from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routes import auth_routes, report_routes, analysis_routes, chat_routes ,audio_routes
from fastapi.staticfiles import StaticFiles


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Medical Report Assistant",
    description="Agentic AI system for medical report understanding",
    version="1.0.0"
)
app.mount(
    "/audio_outputs",
    StaticFiles(directory="audio_outputs"),
    name="audio_outputs"
)

app.include_router(auth_routes.router)
app.include_router(report_routes.router)
app.include_router(analysis_routes.router)
app.include_router(chat_routes.router)
app.include_router(audio_routes.router)


@app.get("/")
def root():
    return {"message": "Medical Report Assistant API is running"}