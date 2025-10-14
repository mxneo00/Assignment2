import os
from passlib.hash import bcrypt

from fastapi import FastAPI, Form, Depends
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse

# Custom Code
from backend.session import Session
from backend.lifespan import lifespan
from backend.app.models import User
from backend.config import app

router = APIRouter(
    prefix="/auth",
    tags=['auth'],
)

@router.get("/signup")
async def get_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup")
async def post_signup(
    fname = Form(...),
    lname = Form(...),
    email = Form(...),
    username = Form(...),
    password = Form(...),
    password_confirmation = Form(...)
):
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
        print("\033")
    return templates.TemplateResponse("dashboard.html", {"request": request})

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

@router.get("/me")
async def get_me(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# @router.post("/login")
# async def post_login(
#     request: Request,
#     email: str = Form(...),
#     password: str = Form(...)
# ):
