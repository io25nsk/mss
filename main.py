from datetime import date

from fastapi import FastAPI, HTTPException
from passlib.context import CryptContext

from models import LoginData, UserData
from database import USERS_COLLECTION


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

NY_BEGIN_DAY = date(2024, 12, 30)
NY_END_DAY = date(2025, 1, 5)
greeting = ("Hello", "Happy New Year")[NY_BEGIN_DAY <= date.today() <= NY_END_DAY]

@app.get("/")
async def index_page():
    return {"Message": "Welcome to My Secret Stash!"}


@app.post("/login")
async def login(login_data: LoginData) -> dict:
    username, password = login_data.model_dump().values()

    if user := await USERS_COLLECTION.find_one({"username": username}):
        if password_context.verify(password, user["password"]):
            return {"Message": f"{greeting} {user['firstname']} {user['lastname']}!"}

    raise HTTPException(status_code=400, detail="Incorrect username or password!")


@app.post("/register")
async def register(register_data: UserData) -> dict:
    if await USERS_COLLECTION.find_one({"username": register_data.username}):
        raise HTTPException(
            status_code=400, detail=f"User {register_data.username} already exist!"
        )

    else:
        user_data = register_data.model_dump()
        user_data["password"] = password_context.hash(user_data["password"])
        await USERS_COLLECTION.insert_one(user_data)

        return {"Message": f"User {user_data['username']} created."}
