from fastapi.responses import JSONResponse

def error_response(message: str, code: int = 400) -> JSONResponse:
    return JSONResponse(
        status_code=code,
        content={"error": message, "code": code, "detail": "An error occurred"}
    )