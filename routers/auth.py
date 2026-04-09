from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from models.user_model import User
from utils.security import hash_password
from utils.security import verify_password
from utils.jwt_handler import create_access_token
from utils.auth_dependency import verify_token
from schemas.user_schema import UserSignup, UserLogin
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

router = APIRouter(prefix="/auth", tags=["Auth"])

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):

    hashed_password = hash_password(user.password)

    new_user = User(
    name=user.name,
    email=user.email,
    password=hashed_password,
    age=user.age,
    role="user"   # 👈 ensure default
)

    db.add(new_user)
    db.commit()

    return {"message": "User created"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        return {"error": "User not found"}

    if not verify_password(user.password, db_user.password):
        return {"error": "Invalid password"}

    token = create_access_token(
    data={
        "user_id": db_user.id,
        "role": db_user.role   # 👈 ADD THIS
    }
)

    return {"access_token": token}

@router.get("/profile")
def get_profile(user=Depends(verify_token)):

    return {
        "message": "Protected API",
        "user": user
    }