import json

from fastapi import FastAPI

from models import LoginData, UserData


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
        if user['password'] == password:
            return {"Hello": f"{user['firstname']} {user['lastname']}"}

    return {"Error": "Wrong username or password!"}


@app.post("/register")
async def register(register_data: UserData) -> dict:

    if (user := register_data.username) not in users:
        register_dict = register_data.model_dump()
        register_dict.pop('username')
        users[user] = register_dict

        with open('users.json', 'w') as file_out:
            file_out.write(json.dumps(users))

        return {"Message": f"User {user} created."}

    return {"Error": f"User {user} already exist!"}