import json

from fastapi import FastAPI, HTTPException
from passlib.context import CryptContext

from models import LoginData, UserData


password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

with open ('users.json', 'r') as file_in:
    users = json.load(file_in)

app = FastAPI()


@app.get("/")
async def index_page():
    return {"Message": "Welcome to My Secret Stash!"}


@app.post("/login")
async def login(login_data: LoginData) -> dict:
    username, password = login_data.model_dump().values()

    if user := users.get(username):
        if password_context.verify(password, user['password']):
            return {"Message": f"Hello {user['firstname']} {user['lastname']}!"}

    raise HTTPException(status_code=401, detail="Incorrect username or password!")


@app.post("/register")
async def register(register_data: UserData) -> dict:

    if (user := register_data.username) not in users:
        user_data = register_data.model_dump()
        user_data.pop('username')
        user_data['password'] = password_context.hash(user_data['password'])
        users[user] = user_data

        with open('users.json', 'w') as file_out:
            file_out.write(json.dumps(users))

        return {"Message": f"User {user} created."}

    raise HTTPException(status_code=400, detail=f"User {user} already exist!")