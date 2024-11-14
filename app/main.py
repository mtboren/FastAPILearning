from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .routers import items, users
from .internal import admin

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()

for module in [items, users]:
    app.include_router(module.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}}
)

@app.get("/")
async def get_root():
    return {"message": "Hello, Biggie applications!"}
