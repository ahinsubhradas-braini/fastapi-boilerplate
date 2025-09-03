from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse

class DashAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        path = request.url.path
        # Allow login and logout routes
        if path.startswith("/dev_dash") and not path.startswith("/dev_dash/login") and not path.startswith("/dev_dash/logout"):
            if not request.session.get("dash_logged_in"):
                # Redirect to login page instead of showing HTML directly
                return RedirectResponse(url="/dev_dash/login")
        return await call_next(request)