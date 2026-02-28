from pydantic import BaseModel
from typing import List


class ArchitectureRequest(BaseModel):
    use_case: str


class ArchitectureResponse(BaseModel):
    services: List[str]
    security: List[str]
    scalability: List[str]
    cost_optimization: List[str]
