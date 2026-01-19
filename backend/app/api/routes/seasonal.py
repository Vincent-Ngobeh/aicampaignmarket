from fastapi import APIRouter

from app.schemas.seasonal import SeasonalResponse
from app.services.seasonal_service import get_seasonal_suggestions


router = APIRouter(prefix="/seasonal", tags=["seasonal"])


@router.get(
    "/suggestions",
    response_model=SeasonalResponse,
    summary="Get UK seasonal marketing suggestions",
)
async def get_suggestions() -> SeasonalResponse:
    data = get_seasonal_suggestions()
    return SeasonalResponse(
        success=True,
        current_season=data["current_season"],
        active_events=data["active_events"],
        upcoming_events=data["upcoming_events"],
        suggestions=data["suggestions"],
    )
