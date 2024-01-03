from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from validation import Trade, User
from typing import List
from fastapi.exception_handlers import RequestValidationError
from fastapi import Request, status
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


app = FastAPI(
    title="Trading App"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"

@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"



#
# @app.exception_handler(ResponseValidationError)
# async def validation_exception_handler(request: Request, exc: ResponseValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail": exc.errors()})
#     )
#
#
#
# fake_users = [
#     {"id": 1, "role": "admin", "name": ["Bob"]},
#     {"id": 2, "role": "investor", "name": "John"},
#     {"id": 3, "role": "trader", "name": "Matt"},
#     {"id": 4, "role": "investor", "name": "John", "degree": [
#         {"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": "expert"}
#     ]},
#
# ]
#
#
# @app.get("/users/{user_id}", response_model=List[User])
# def get_user(user_id: int):
#     return [user for user in fake_users if user.get("id") == user_id]
#
#
# fake_trades = [
#     {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
#     {"id": 2, "user_id": 1, "currency": "BTC", "side": "sell", "price": 125, "amount": 2.12},
# ]
#
#
# @app.get("/trades")
# def get_trades(limit: int = 1, offset: int = 1):
#     return fake_trades[offset:][:limit]
#
#
# fake_users2 = [
#     {"id": 1, "role": "admin", "name": "Bob"},
#     {"id": 2, "role": "investor", "name": "John"},
#     {"id": 3, "role": "trader", "name": "Matt"},
# ]
#
#
# @app.post("/user/{user_id}")
# def change_user_name(user_id: int, new_name: str):
#     current_user = list(filter(lambda user: user.get("id") == user_id, fake_users2))[0]
#     current_user["name"] = new_name
#     return {"status": 200, "data": current_user}
#
#
#
# @app.post("/trades")
# def add_trades(trades: List[Trade]):
#     fake_trades.extend(trades)
#     return {"status": 200, "data": fake_trades}


