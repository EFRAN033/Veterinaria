from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_services():
    return {"message": "Services endpoint - Coming soon"}
