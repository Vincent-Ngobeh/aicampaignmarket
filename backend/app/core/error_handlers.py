from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded


async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "error": "Rate limit exceeded",
            "detail": f"Too many requests. Limit: {exc.detail}",
        },
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc) if request.app.debug else "An unexpected error occurred",
        },
    )
