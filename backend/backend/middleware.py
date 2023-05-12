from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
from .database import SQLALCHEMY_DATABASE_URL

def add_middleware(app):
    # Add middleware to handle database sessions
    app.add_middleware(DBSessionMiddleware, db_url=SQLALCHEMY_DATABASE_URL)

    # Add middleware to handle Cross-Origin Resource Sharing (CORS)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
