# Python native
import os
# Dependency library
from fastapi import FastAPI
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

app.include_router(auth.router)
app.include_router(protected.router)

origins = [
    "http://localhost:5173",  # The URL where your React app is running
    # You can add other origins here, like production domains
]
app.add_middleware(
     CORSMiddleware,
     allow_origins=origins,  # Allows all origins
    allow_credentials=True,
     allow_methods=["*"],  # Allows all methods
     allow_headers=["*"],  # Allows all headers
)

# templates = Jinja2Templates(directory="backend/public/html")
# app.mount("/asset", StaticFiles(directory="backend/public/asset"), name="asset")

# @app.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request, "title": "Landing", "host": "host"})

# @app.get("/web3", response_class=HTMLResponse)
# async def read_web3(request: Request):
#     return templates.TemplateResponse("web3.html", {"request": request, "title": "Landing", "host": "host"})

@app.get("/react-demo")
async def react_endpoint(request: Request, current_user=Depends(get_current_user)):
    #posts = current_user.posts
    return JSONResponse({"hello": "My name is slim shady"})

@app.get("/user")
async def get_users(request: Request):
    users = await User.all()

    users_response = []
    for user in users: 
        users_response.append({"username": user.username})

