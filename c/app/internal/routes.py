from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def handle_health():
    return {"message": "health check"}
