# Import python core libary dependices
import os

# Imports from project or 3rd party libary dependices
from fastapi import APIRouter, Request, HTTPException
from starlette.responses import HTMLResponse, RedirectResponse
from src.core.config import get_settings

settings = get_settings()

USERNAME = settings.dash_username
PASSWORD = settings.dash_password

router = APIRouter(include_in_schema=False)

@router.get("/dev_dash/login")
async def dash_login_page():
    return HTMLResponse("""
    <h2>Developer Dashboard Login</h2>
    <form action='/dev_dash/login/check' method='get'>
        <input name='username' placeholder='Username' required/>
        <input name='password' type='password' placeholder='Password' required/>
        <button type='submit'>Login</button>
    </form>
    """)

@router.get("/dev_dash/login/check")
async def dash_login_check(request: Request):
    username = request.query_params.get("username")
    password = request.query_params.get("password")

    if username != USERNAME or password != PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid Dash credentials")

    request.session["dash_logged_in"] = True
    # Redirect to trailing slash so Dash loads correctly
    return RedirectResponse(url="/dev_dash/", status_code=303)

@router.get("/dev_dash/logout")
async def dash_logout(request: Request):
    request.session.pop("dash_logged_in", None)
    return HTMLResponse("<h3>Logged out. <a href='/dev_dash/login'>Login again</a></h3>")