"""Skill API — 技能列表与查询"""

import logging

from fastapi import APIRouter

from app.registry.skill_registry import skill_registry

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/skill", tags=["skill"])


@router.get("/list")
async def list_skills():
    """列出所有已注册的 Skill"""
    skills = skill_registry.list_skills()
    logger.info("GET /skill/list: %d skills", len(skills))
    return {"skills": skills}
