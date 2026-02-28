from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="AI Cloud Architect Copilot")

app.include_router(router)
