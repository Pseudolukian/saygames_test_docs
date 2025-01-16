from fastapi import FastAPI, APIRouter
from Routers.GAME import game_router
from Routers.USER import user_router
from oapi import custom_openapi, export_open_api_to_yaml
import uvicorn


main_api_router = APIRouter()
app = FastAPI()


main_api_router.include_router(game_router)
main_api_router.include_router(user_router)
app.include_router(main_api_router)
#app.openapi = custom_openapi
open_api_scheme = app.openapi()

export_open_api_to_yaml(fast_api_openapi=open_api_scheme, file_name="open_api.yaml")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8003, reload=True)