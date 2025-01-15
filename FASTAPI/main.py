from fastapi import FastAPI, APIRouter
from Routers.GAME import game_router
import uvicorn

main_api_router = APIRouter()
app = FastAPI()

main_api_router.include_router(game_router)
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8003, reload=True)