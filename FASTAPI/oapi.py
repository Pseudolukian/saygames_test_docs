from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI
import json
from pathlib import Path
import yaml

def custom_openapi(application: FastAPI):
    if application.openapi_schema:
        return application.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=application.routes,
    )
    application.openapi_schema = openapi_schema
    return application.openapi_schema

def export_open_api_to_yaml(fast_api_openapi: json, file_name: str):
    openapi_yaml = yaml.dump(fast_api_openapi, allow_unicode=True)
    path_to_file = Path(f"./{file_name}")
     
    with open(path_to_file, "w", encoding='utf-8') as file:
        file.write(openapi_yaml)
