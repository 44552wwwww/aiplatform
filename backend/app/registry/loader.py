"""Skill 动态加载器 — 负责从 skills/ 目录动态加载 Skill 模块"""

import sys
import importlib.util
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def _resolve_skills_dir(skills_dir: str) -> Path:
    path = Path(skills_dir)
    if not path.is_absolute():
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        path = project_root / skills_dir
    return path


class SkillLoader:
    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = _resolve_skills_dir(skills_dir)

        backend_root = self.skills_dir.parent / "backend"
        if str(backend_root) not in sys.path:
            sys.path.insert(0, str(backend_root))

        if str(self.skills_dir.parent) not in sys.path:
            sys.path.insert(0, str(self.skills_dir.parent))

        logger.info("SkillLoader ready: skills_dir=%s", self.skills_dir)

    def load_workflow(self, skill_id: str) -> Optional[object]:
        workflow_path = self.skills_dir / skill_id / "workflow.py"
        if not workflow_path.exists():
            logger.warning("Workflow not found: %s", workflow_path)
            return None
        spec = importlib.util.spec_from_file_location(
            f"skill_{skill_id}", str(workflow_path)
        )
        if spec is None or spec.loader is None:
            logger.error("Failed to create module spec for: %s", skill_id)
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        logger.info("Skill loaded: %s → %s", skill_id, workflow_path)
        return module


skill_loader = SkillLoader()
