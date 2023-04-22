from fastapi import APIRouter

router = APIRouter()


@router.get("/client-side")
async def handle_client_side():
    return {"message": "this was called from a client-side route"}


@router.get("/server-side")
async def handle_server_side():
    return {"message": "this was called from a server-side route"}
