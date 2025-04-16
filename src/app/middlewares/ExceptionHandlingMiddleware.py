from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except StarletteHTTPException as exc:
            # Handling specific HTTP middlewares (e.g., 404 Not Found, 400 Bad Request)
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "status_code": exc.status_code,
                    "detail": exc.detail,
                    "message": "Custom Error: HTTPException"
                }
            )
        except Exception as exc:
            logging.error(f"Unhandled error: {str(exc)}")
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal Server Error",
                    "message": str(exc)
                }
            )
