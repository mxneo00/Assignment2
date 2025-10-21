# Libraries
from passlib.hash import bcrypt
from fastapi import FastAPI, Form, Depends
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from tortoise.exceptions import IntegrityError
# Application Code
from backend.session import Session
from backend.lifespan import lifespan
from backend.app.models import User
from backend.config import app

router = APIRouter(prefix="",tags=['auth'])
templates = Jinja2Templates(directory="backend/public/html")
#----------------------SIGNUP-------------------------------
@router.post("/signup")
async def post_signup(
    fname = Form(...),
    lname = Form(...),
    email = Form(...),
    username = Form(...),
    password = Form(...),
    password_confirmation = Form(...),
):
    if password != password_confirmation:
        print("Invalid Password Combination")
    try:
        user = await User.create(
            username=username,
            fname=fname, 
            lname=lname, 
            email=email,
            digest=bcrypt.hash(password),
            role="temp",
            tier="free",
        )
    except IntegrityError as e:
        return JSONResponse({"error": "Failed to create user"})
    return RedirectResponse(url = "/dashboard")
#-----------------------LOGIN/LOGOUT---------------------------------
@router.post("/login")
async def post_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    user = await User.get_or_none(email=email)
    if not user or not bcrypt.verify(password, user.digest):
        return JSONResponse({"error": "Invalid login credentials"})
    session = Session(request)
    await session.create_session({"user_id": user.user_id, "username": user.username})
    return RedirectResponse(url = "/dashboard")

@router.get("/logout")
async def logout(request: Request):
    session = Session(request)
    await session.delete_session()
    return RedirectResponse(url = "/")
#------------------------USERDATA------------------------------------
@router.get("/me")
async def get_me(request: Request):
    session = Session(request)
    data = await session.get_session()
    if not data: 
        return JSONResponse({"error": "Failed to get user data"})
    return JSONResponse({"user": data})

@router.get("/change-password")
async def changePass(request: Request):
    return {"msg": "TODO"}
#----------------------REDIS TEST-----------------------------------
@router.get("/redis-set-test")
async def redis_ping(request: Request):
    redis_conn = router.state.kv_store
    await redis_conn.set("user:var1:3458343", "HELLOW WORLD")
    return {"msg":"Key successfully set"}

    
@router.get("/redis-get-test")
async def redis_ping(request: Request):
    redis_conn = app.state.kv_store
    list_of_keys = await redis_conn.keys("user:var1:*")
    return {"redis_keys": list_of_keys}