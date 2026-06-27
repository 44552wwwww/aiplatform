"""全项目统一的 Skill 请求/响应类型定义

所有模块引用 SkillRequest / SkillResponse 必须从此文件导入，
不得重复定义。
"""

from dataclasses import dataclass, field


@dataclass
class SkillRequest:
    """Platform → Skill 的统一请求"""
    skill_id: str
    user_id: int
    session_id: str
    parameters: dict = field(default_factory=dict)


@dataclass
class SkillResponse:
    """Skill → Platform 的统一响应"""
    success: bool
    title: str
    html: str
    metadata: dict = field(default_factory=dict)
    error: str | None = None
