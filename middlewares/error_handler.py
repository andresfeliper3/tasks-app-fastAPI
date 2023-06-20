from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        try:
            # Call the next middleware or route handler
            return await call_next(request)
        except Exception as e:
            # If an exception occurs, handle it and return a JSON response with the error message
            return JSONResponse(content={"error": str(e)}, status_code=500)
