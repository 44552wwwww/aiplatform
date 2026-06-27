"""Skill Runtime — 平台运行时，负责调度 Skill 执行

Platform 唯一调用入口：await skill_runtime.run(request)
Platform 不直接访问 Skill 内部代码。
"""

import logging
from typing import Any

from app.types.skill import SkillRequest, SkillResponse
from app.registry.loader import skill_loader

logger = logging.getLogger(__name__)


class SkillRuntime:
    """Skill 调度运行时 — 含 Workflow 缓存"""

    def __init__(self):
        self._cache: dict[str, Any] = {}

    async def run(self, request: SkillRequest) -> SkillResponse:
        logger.info("SkillRuntime.run: skill_id=%s user_id=%s", request.skill_id, request.user_id)

        # 缓存命中检查
        workflow = self._cache.get(request.skill_id)
        if workflow is None:
            logger.info("Cache miss, loading: %s", request.skill_id)
            workflow = skill_loader.load_workflow(request.skill_id)
            if workflow is None:
                logger.error("Skill not found: %s", request.skill_id)
                return SkillResponse(
                    success=False,
                    title="",
                    html="",
                    metadata={},
                    error=f"Skill not found: {request.skill_id}",
                )
            self._cache[request.skill_id] = workflow
            logger.info("Skill cached: %s", request.skill_id)
        else:
            logger.info("Cache hit: %s", request.skill_id)

        try:
            result = await workflow.run(request)
            return result
        except Exception as e:
            logger.exception("Skill execution error: %s", request.skill_id)
            return SkillResponse(
                success=False,
                title="",
                html="",
                metadata={},
                error=str(e),
            )


skill_runtime = SkillRuntime()
