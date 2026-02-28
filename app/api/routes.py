from fastapi import APIRouter
from app.domain.models import ArchitectureRequest, ArchitectureResponse
from app.application.architect_service import ArchitectService

router = APIRouter()
service = ArchitectService()


@router.post("/architect", response_model=ArchitectureResponse)
async def architect(request: ArchitectureRequest):
    result = await service.generate_architecture(request.use_case)
    return result
