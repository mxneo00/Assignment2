# Python native
import os
# Dependency library
from fastapi import FastAPI, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from passlib.hash import bcrypt
# Application Code
from backend.session import Session
from backend.lifespan import lifespan
from backend.app.models import User
from backend.app.router import (auth, protected)
from backend.config import app
from backend.context import UserCtx, AdminCtx
from backend.dependencies import get_current_user

app.include_router(auth.router)
app.include_router(protected.router)
templates = Jinja2Templates(directory="backend/public/html")


origins = [
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/signup")
async def get_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/login")
async def get_signup(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request, user: UserCtx = Depends(get_current_user)):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/react")
async def react_endpoint(request: Request, current_user=Depends(get_current_user)):
    #posts = current_user.posts
    return JSONResponse({})

@app.get("/user")
async def get_users(request: Request):
    users = await User.all()
    users_response = []
    for user in users: 
        users_response.append({"username": user.username})
    return JSONResponse({"users": users_response})

