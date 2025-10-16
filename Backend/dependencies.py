from fastapi import FastAPI, Depends
from starlette.requests import Request
from tortoise.exceptions import DoesNotExist

# Custom Code
from backend.redis import RedisAdapter
from backend.session import Session, SessionManager

def get_kv_store(request: Request) -> RedisAdapter:
    return request.app.state.kv_store

def get_session_manager(request: Request) -> SessionManager:
    return request.app.state.session_manager

def get_session(
    request: Request, session_manager: SessionManager = Depends(get_session_manager)
) -> Session:
    if not hasattr(request.state, "session"):
        request.state.session = Session(
            request=request, session_manager=session_manager
        )
    return request.state.session

async def get_current_user(request: Request, session: Session = Depends(get_session)):
    await session.load()
    if not session.data or not session.data.get("user_id"):
        logger.warning("Session has not user id")
        raise HTTPException(status_code=303, headers={"location": "/"})

    try:
        user = await User.get(user_id=session.data["user_id"])
        user = UserCtx(user, session)

    except DoesNotExist as e:
        logger.warning(f"User does not exist {e}")
        raise HTTPException(status_code=303, headers={"location": "/"}) from e
    return user

def get_admin(request: Request, ctx: UserCtx = Depends(get_current_user)):
    try:
        admin = AdminCtx(ctx.user, ctx.session)
    except PermissionError as e:
        logger.critical(
            "Insufficient privilege request on admin from IP: %s (%s)",
            request.client.host,
            e,
        )
        raise HTTPException(status_code=401, detail="Not authenticated") from e
    return admin

def get_superuser(request: Request, ctx: User = Depends(get_current_user)):
    try:
        su = SuperUserCtx(ctx.user, ctx.session)
    except PermissionError as e:
        logger.critical(
            "Insufficient privilege request on superuser from IP: %s (%s)",
            request.client.host,
            e,
        )
        raise HTTPException(status_code=401, detail="Not authenticated") from e
    return su