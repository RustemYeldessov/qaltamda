from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, DeclarativeBase
from src.database import get_db
from src.auth import models, schemas, service

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=schemas.UserOut)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # Проверяем, нет ли уже такого email
    user = db.query(models.UserModel).filter(models.UserModel.email == user_in.email).first()

    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pwd = service.hash_password(user_in.password)
    db_user = models.UserModel(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed_pwd
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user