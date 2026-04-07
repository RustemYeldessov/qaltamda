from pydantic import BaseModel, EmailStr, model_validator


# Базовый класс, от него буду наследоваться UserCreate
# и UserOut. Параметры этого класса будут переданы в оба класса-потомка
class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str

# Наследуется от базового класса. Здесь у создаваемого пользователя запрашивается
# информация, которая не будет возвращена после его создания, но нужна для записи в БД
class UserCreate(UserBase):
    password: str
    password_confirm: str

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password_confirm != self.password:
            raise ValueError("Passwords do not match")
        return self

# Информация, которая вернется после создания пользователя помимо той, что
# передается из базового класса UserBase
class UserOut(UserBase):
    id: int
    is_active: bool

    # from_attributes = True позволяет FastAPI работать
    # не только со словарями, но и с объектами ORM
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str