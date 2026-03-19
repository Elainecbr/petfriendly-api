from pydantic import BaseModel
from typing import List, Optional

class RouteStep(BaseModel):
    instruction: str
    distance: str
    duration: str
    end_location: dict

class Route(BaseModel):
    total_distance: str
    total_duration: str
    steps: List[RouteStep]

class RouteResponse(BaseModel):
    routes: List[Route]
    status: str