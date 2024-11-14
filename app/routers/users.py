from fastapi import APIRouter

router = APIRouter()

@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "coolGuy0"}

@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}

# @app.get(path="/users/me")
# async def read_user_me():
#     return {"user_id": "current_foo"}

# @app.get("/users/{user_id}")
# async def read_user(user_id: str):
#     if user_id != "current_foo":
#         raise HTTPException(status_code=404, detail=f"User '{user_id}' not found!")
#     return {"user_id": user_id}
