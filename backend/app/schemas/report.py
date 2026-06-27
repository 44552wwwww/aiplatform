from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class ReportItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    skill_id: str
    title: str
    created_at: datetime


class ReportDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    skill_id: str
    title: str
    html: Optional[str] = None
    metadata: Optional[dict] = None
    created_at: datetime


class ReportListResponse(BaseModel):
    reports: list[ReportItem]
