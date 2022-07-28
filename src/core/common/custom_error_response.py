from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from src.core.common.dto.exception_response_dto import ExceptionResponseDto


def custom_error_response(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # not quite the ideal scenario but this is the best we can do to override the default
    # error schema. See
    from fastapi.openapi.constants import REF_PREFIX
    import pydantic.schema

    paths = openapi_schema["paths"]
    for path in paths:
        for method in paths[path]:
            if paths[path][method]["responses"].get("422"):
                paths[path][method]["responses"]["422"] = {
                    "description": "Validation Error",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": f"{REF_PREFIX}ExceptionResponseDto"}
                        }
                    },
                }

    error_response_defs = pydantic.schema.schema(
        (ExceptionResponseDto,), ref_prefix=REF_PREFIX, ref_template=f"{REF_PREFIX}{{model}}"
    )
    openapi_schemas = openapi_schema["components"]["schemas"]
    openapi_schemas.update(error_response_defs["definitions"])
    openapi_schemas.pop("ValidationError")
    openapi_schemas.pop("HTTPValidationError")

    app.openapi_schema = openapi_schema
