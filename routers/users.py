# from fastapi import APIRouter
# from schemas.user_schema import UserCreate, UserResponse

# router = APIRouter(prefix="/users", tags=["Users"])

# users_db = []

# @router.post("/", response_model=UserResponse)
# def create_user(user: UserCreate):

#     new_user = {
#         "id": len(users_db) + 1,
#         "name": user.name,
#         "age": user.age
#     }

#     users_db.append(new_user)

#     return new_user


# @router.get("/", response_model=list[UserResponse])
# def get_users():
#     return users_db


# @router.get("/{user_id}", response_model=UserResponse)
# def get_user(user_id: int):

#     for user in users_db:
#         if user["id"] == user_id:
#             return user

#     return {"error": "User not found"}

# @router.put("/{user_id}", response_model=UserResponse)
# def update_user(user_id: int, user: UserCreate):

#     for u in users_db:
#         if u["id"] == user_id:
#             u["name"] = user.name
#             u["age"] = user.age
#             return u

#     return {"error": "User not found"}

# @router.delete("/{user_id}")
# def delete_user(user_id: int):

#     for index, user in enumerate(users_db):

#         if user["id"] == user_id:
#             users_db.pop(index)
#             return {"message": "User deleted"}

#     return {"error": "User not found"}

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from models.user_model import User
from schemas.user_schema import UserCreate, UserResponse
from utils.role_checker import require_roles

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    #current_user=Depends(require_roles(["admin"]))   # 👈 RBAC
):
    new_user = User(
        name=user.name,
        age=user.age
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/", response_model=list[UserResponse])
# def get_users(db: Session = Depends(get_db)): list add []
def get_users(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin", "user"]))
):
    users = db.query(User).all()

    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    return user

@router.put("/{user_id}")
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.id == user_id).first()

    db_user.name = user.name
    db_user.age = user.age

    db.commit()

    return {"message": "User updated"}

@router.delete("/{user_id}")
# def delete_user(user_id: int, db: Session = Depends(get_db)):
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))
):
    user = db.query(User).filter(User.id == user_id).first()

    db.delete(user)
    db.commit()

    return {"message": "User deleted"}

