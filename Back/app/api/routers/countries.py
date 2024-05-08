from fastapi import APIRouter

from app.api.deps import CountryServiceDep

router = APIRouter(prefix="/countries", tags=["Countries"])


@router.get("/", response_model=list[str])
async def read_countries(
    *, country_service: CountryServiceDep
):
    """
    Retrieve a list of all countries
    """
    return country_service.get_all()
