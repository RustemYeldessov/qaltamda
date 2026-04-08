from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session, DeclarativeBase
from src.auth.schemas import UserLogin
from src.database import get_db
from src.auth import models, schemas, service
from src.config import settings
from authx import AuthX, AuthXConfig

router = APIRouter(prefix="/auth", tags=["Authentication"])

config = AuthXConfig()
config.JWT_SECRET_KEY = settings.JWT_SECRET_KEY
config.JWT_ACCESS_COOKIE_NAME = settings.JWT_ACCESS_COOKIE_NAME
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

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


@router.post("/login")
def login(creds: UserLogin, response: Response, db: Session = Depends(get_db)):
    # 1. Поиск пользователя в БД
    user = db.query(models.UserModel).filter(models.UserModel.username == creds.username).first()

    # 2. Если пользователь не найден
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    # 3. Проверка пароля
    is_verified = service.verify_password(creds.password, user.hashed_password)

    if not is_verified:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # 4. Создание токена, привязанного к реальному ID пользователя
    token = security.create_access_token(uid=str(user.id))

    # 5. Устанавливаем токен в куки через AuthX
    security.set_access_cookies(token, response=response)

    return {"message": "Logged in successfully"}


@router.post("/logout")
def logout(response: Response):
    security.unset_access_cookies(response)
    return {"message": "Logged out successfully"}