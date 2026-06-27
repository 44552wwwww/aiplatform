"""Skill 注册中心 — 启动时扫描一次，运行时零开销查询"""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def _resolve_skills_dir(skills_dir: str) -> Path:
    path = Path(skills_dir)
    if not path.is_absolute():
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        path = project_root / skills_dir
    return path


class SkillRegistry:
    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = _resolve_skills_dir(skills_dir)
        self._skills: dict[str, dict] = {}
        self._scanned = False

    def scan(self) -> None:
        """扫描 skills/ 目录，注册所有 Skill（仅调用一次）"""
        if self._scanned:
            return
        self._skills.clear()
        if not self.skills_dir.exists():
            logger.warning("Skills directory not found: %s", self.skills_dir)
            self._scanned = True
            return
        for manifest_path in sorted(self.skills_dir.rglob("manifest.json")):
            with open(manifest_path, encoding="utf-8") as f:
                manifest = json.load(f)
            skill_id = manifest.get("id", "")
            if skill_id:
                self._skills[skill_id] = manifest
                logger.info(
                    "Registered Skill: [%s] %s v%s",
                    skill_id,
                    manifest.get("display_name", skill_id),
                    manifest.get("version", "?"),
                )
        self._scanned = True
        logger.info("Skill scan complete: %d skills registered", len(self._skills))

    def list_skills(self) -> list[dict]:
        if not self._scanned:
            self.scan()
        return list(self._skills.values())

    def get_skill(self, skill_id: str) -> dict | None:
        if not self._scanned:
            self.scan()
        return self._skills.get(skill_id)

    def is_registered(self, skill_id: str) -> bool:
        if not self._scanned:
            self.scan()
        return skill_id in self._skills


# 全局单例 — 导入时自动扫描
skill_registry = SkillRegistry()
skill_registry.scan()
