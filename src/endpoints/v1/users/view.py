from fastapi import APIRouter,Request

router = APIRouter()

@router.get("/profile")  # limit to 5 requests per minute per IP
async def get_profile(request: Request):
    return {"message": "User profile data"}