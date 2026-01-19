from fastapi import APIRouter, Request

from app.core.rate_limit import limiter
from app.schemas.image import (
    ImageGenerationRequest,
    ImageGenerationResponse,
)
from app.services.dalle_service import generate_image


router = APIRouter(prefix="/images", tags=["images"])


@router.post(
    "/generate",
    response_model=ImageGenerationResponse,
    summary="Generate marketing image",
    description="Generate a promotional image using DALL-E",
)
@limiter.limit("3/minute")
async def generate_marketing_image(
    request: Request,
    image_request: ImageGenerationRequest,
) -> ImageGenerationResponse:
    result = await generate_image(prompt=image_request.prompt, size=image_request.size)
    return ImageGenerationResponse(
        success=True,
        image_url=result["image_url"],
        revised_prompt=result["revised_prompt"],
    )
