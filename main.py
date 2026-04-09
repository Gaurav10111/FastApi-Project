from fastapi import FastAPI
from routers import users
from database.db import engine
from models import user_model
from routers import auth
from models import qr_models
from routers import qr_routes
from fastapi.staticfiles import StaticFiles


user_model.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/qrs", StaticFiles(directory="qrs"), name="qrs")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(qr_routes.router)
