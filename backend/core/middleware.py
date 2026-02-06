from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Unhandled exception: {str(e)}")

            # Log the full traceback
            import traceback
            logger.error(traceback.format_exc())

            # Return standardized error response
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": {
                        "code": "GENERAL_001",
                        "message": "Internal server error occurred"
                    }
                }
            )