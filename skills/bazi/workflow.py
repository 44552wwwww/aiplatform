"""Bazi Skill — 八字命理分析工作流

此文件是 Platform 调用 Bazi Skill 的唯一入口。
Platform 永远只调用：await workflow.run(request) → SkillResponse
"""

import logging
import re
from pathlib import Path

from app.llm.client import llm_client
from app.types.skill import SkillRequest, SkillResponse
from skills.bazi.renderer import render

logger = logging.getLogger(__name__)

_SKILL_DIR = Path(__file__).parent


def _load_prompt() -> str:
    prompt_path = _SKILL_DIR / "prompt.md"
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")
    return ""


def _extract_system_user(prompt_template: str) -> tuple[str, str]:
    system = ""
    match = re.search(
        r"##\s*系统指令\s*\n(.*?)(?=##\s*分析要求)", prompt_template, re.DOTALL
    )
    if match:
        system = match.group(1).strip()
    return system, prompt_template


def _fill_template(template: str, params: dict) -> str:
    try:
        return template.format(**params)
    except KeyError as e:
        raise ValueError(f"缺少必要参数: {e}")


def _validate_params(params: dict) -> dict:
    required = ["year", "month", "day", "hour", "gender"]
    missing = [k for k in required if k not in params]
    if missing:
        raise ValueError(f"缺少必要参数: {', '.join(missing)}")
    return {
        "year": int(params["year"]),
        "month": int(params["month"]),
        "day": int(params["day"]),
        "hour": int(params["hour"]),
        "gender": str(params["gender"]),
    }


async def run(request: SkillRequest) -> SkillResponse:
    """Bazi Skill 统一入口（异步）"""
    logger.info("Bazi workflow started: user_id=%s", request.user_id)

    try:
        # 1. 验证参数
        params = _validate_params(request.parameters)
        logger.info("Params validated: %s", params)

        # 2. 加载并填充 prompt
        prompt_template = _load_prompt()
        if not prompt_template:
            return SkillResponse(
                success=False,
                title="命运双鉴",
                html="",
                metadata={"skill": "bazi", "version": "1.0.0"},
                error="Prompt 模板未找到",
            )

        system, template = _extract_system_user(prompt_template)
        user_prompt = _fill_template(template, params)

        # 3. 调用 LLM（直接 await，无 asyncio.run）
        ai_result = await llm_client.generate(user_prompt, system=system)

        # 4. 渲染 HTML
        html = render(
            title="命运双鉴 — 八字命理分析",
            params=params,
            ai_content=ai_result,
        )

        logger.info("Bazi workflow completed successfully")

        return SkillResponse(
            success=True,
            title="命运双鉴",
            html=html,
            metadata={
                "skill": "bazi",
                "version": "1.0.0",
                "model": llm_client.model,
            },
        )

    except ValueError as e:
        logger.warning("Bazi validation error: %s", e)
        return SkillResponse(
            success=False,
            title="命运双鉴",
            html="",
            metadata={"skill": "bazi", "version": "1.0.0"},
            error=str(e),
        )
    except Exception as e:
        logger.exception("Bazi workflow error")
        return SkillResponse(
            success=False,
            title="命运双鉴",
            html="",
            metadata={"skill": "bazi", "version": "1.0.0"},
            error=f"分析过程出错: {str(e)}",
        )
