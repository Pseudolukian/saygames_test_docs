from fastapi import FastAPI, APIRouter
from Routers.GAME import game_router
from Routers.USER import user_router
from Routers.AUTH import auth_router
from fastapi.responses import HTMLResponse
from oapi import custom_openapi, export_open_api_to_yaml
import uvicorn
tags_metadata = [
    {
        "name": "Game",
        "description": "This tag provides endpoints related to game operations."
    }
]
main_api_router = APIRouter()
app = FastAPI(root_path="/api",
        docs_url="/")

main_api_router.include_router(game_router)
main_api_router.include_router(user_router)
main_api_router.include_router(auth_router)

app.include_router(main_api_router)
open_api_scheme = app.openapi()

export_open_api_to_yaml(fast_api_openapi=open_api_scheme, file_name="open_api.yaml")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8003, reload=True)