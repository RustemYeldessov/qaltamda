from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, DeclarativeBase
from src.database import get_db
from src.auth import models, schemas, service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get(
    "/users",
    response_model=list[schemas.UserOut],
    summary="All users list"
)
def read_users(
        skip: int = 0,
        limit: int = 50,
        db: Session = Depends(get_db)
):
    users = db.query(models.UserModel).offset(skip).limit(limit).all()

    return users

@router.post("/register", response_model=schemas.UserOut, status_code=201)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # Проверяем, нет ли уже такого email
    user = db.query(models.UserModel).filter(models.UserModel.email == user_in.email).first()

    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pwd = service.hash_password(user_in.password)

    db_user = models.UserModel(
        username=user_in.username,
        email=user_in.email,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        hashed_password=hashed_pwd
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user