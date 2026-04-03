import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

users = [
    {
        "id": 1,
        "first_name": "Rustem",
        "age": 28,
    },
    {
        "id": 2,
        "first_name": "Ilmira",
        "age": 28,
    },
]


@app.get("/", summary="Стартовая страница")
def main():
    return "Qaltamda"


@app.get(
    "/users",
    tags=["Пользователи"],
    summary="Получить всех пользователей"
)
def get_users():
    return users


@app.get(
    "/users/{user_id}",
    tags=["Пользователи"],
    summary="Получить конкретного пользователя"
)
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="Пользователь не найден")


class NewUser(BaseModel):
    first_name: str
    age: int

#Создание нового пользователя
@app.post(
    "/users",
    tags=["Пользователи"],
    summary="Добавить нового пользователя"
)
def create_user(new_user: NewUser):
    users.append({
        "id": len(users) + 1,
        "first_name": new_user.first_name,
        "age": new_user.age,
    })
    return {"success": True, "message": "Пользователь успешно создан"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)