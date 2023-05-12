from .database import Base, engine
from .api import app
from .middleware import add_middleware
from .websocket import close_websockets

add_middleware(app)

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

@app.on_event("shutdown")
async def shutdown_event():
    Base.metadata.drop_all(bind=engine)
    await close_websockets()
