from fastapi import FastAPI, HTTPException, Path, Body
from pydantic import BaseModel

app = FastAPI()

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get('/users')
async def get_users() -> list:
    return users

@app.post('/user/{username}/{age}')
async def create_user(user: User):
    if not users:
        user.id = 1
    else:
        user.id = users[-1].id + 1
    users.append(user)
    return user

@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int, user: str = Body()):
    try:
        edit_user = users[user_id]
        edit_user.username = username
        edit_user.age = age
        return edit_user
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    try:
        user_out = users.pop(user_id-1)
        return user_out
    except:
        raise HTTPException(status_code=404, detail='Users not found')

