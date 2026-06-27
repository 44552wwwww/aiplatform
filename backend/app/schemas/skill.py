from pydantic import BaseModel


class SkillRequest(BaseModel):
    """API 层 Skill 执行请求"""
    skill_id: str
    parameters: dict = {}


class SkillResponse(BaseModel):
    """API 层 Skill 执行响应（含 report_id 用于后续持久化）"""
    report_id: str
    success: bool
    title: str
    html: str
    metadata: dict = {}
    error: str | None = None
