from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_adoptions():
    return {"message": "Adoptions endpoint - Coming soon"}
