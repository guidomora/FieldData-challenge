from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def _build_error_response(
    *,
    status_code: int,
    code: str,
    message: str,
    details: list[dict[str, str]] | None = None,
) -> JSONResponse:
    payload: dict[str, object] = {
        "error": {
            "code": code,
            "message": message,
        }
    }
    if details:
        payload["error"]["details"] = details

    return JSONResponse(status_code=status_code, content=payload)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        detail = exc.detail
        if isinstance(detail, dict):
            return _build_error_response(
                status_code=exc.status_code,
                code=str(detail.get("code", "http_error")),
                message=str(detail.get("message", "Request failed.")),
                details=detail.get("details"),
            )

        return _build_error_response(
            status_code=exc.status_code,
            code="http_error",
            message=str(detail),
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        _: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        details: list[dict[str, str]] = []
        for error in exc.errors():
            location = ".".join(str(item) for item in error["loc"] if item != "body")
            details.append(
                {
                    "field": location or "request",
                    "message": error["msg"],
                }
            )

        return _build_error_response(
            status_code=422,
            code="validation_error",
            message="The request contains invalid or missing data.",
            details=details,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_: Request, __: Exception) -> JSONResponse:
        return _build_error_response(
            status_code=500,
            code="internal_error",
            message="An internal error occurred while processing the request.",
        )

