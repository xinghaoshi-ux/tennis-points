from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.exceptions import AppException, app_exception_handler
from app.routers import (
    auth,
    dashboard,
    health,
    players,
    points_rules,
    public,
    rankings,
    seasons,
    tournaments,
    uploads,
)

app = FastAPI(title="THA Tennis Points API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppException, app_exception_handler)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(seasons.router)
app.include_router(players.router)
app.include_router(tournaments.router)
app.include_router(points_rules.router)
app.include_router(uploads.router)
app.include_router(rankings.router)
app.include_router(public.router)
app.include_router(dashboard.router)
