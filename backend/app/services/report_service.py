"""Report Service — 报告持久化、查询、删除

所有数据库操作在此层完成。
API 层不直接操作数据库。
"""

import logging

from sqlalchemy.orm import Session

from app.models.report import Report
from app.types.skill import SkillResponse as InternalSkillResponse

logger = logging.getLogger(__name__)


class ReportService:
    def create(
        self,
        db: Session,
        user_id: int,
        skill_id: str,
        result: InternalSkillResponse,
    ) -> Report:
        """保存 Skill 执行结果到数据库"""
        report = Report(
            user_id=user_id,
            skill_id=skill_id,
            title=result.title,
            html=result.html,
            metadata_=result.metadata,
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        logger.info(
            "Report saved: id=%s user_id=%s skill=%s", report.id, user_id, skill_id
        )
        return report

    def list_by_user(self, db: Session, user_id: int) -> list[Report]:
        """获取用户的所有报告"""
        return (
            db.query(Report)
            .filter(Report.user_id == user_id)
            .order_by(Report.created_at.desc())
            .all()
        )

    def get_by_id(self, db: Session, report_id: int) -> Report | None:
        """获取单条报告（不做权限校验）"""
        return db.query(Report).filter(Report.id == report_id).first()

    def get_user_report(self, db: Session, report_id: int, user_id: int) -> Report | None:
        """获取用户自己的报告（含权限校验）"""
        return (
            db.query(Report)
            .filter(Report.id == report_id, Report.user_id == user_id)
            .first()
        )

    def delete(self, db: Session, report_id: int, user_id: int) -> bool:
        """删除用户自己的报告，返回是否成功"""
        report = self.get_user_report(db, report_id, user_id)
        if report is None:
            return False
        db.delete(report)
        db.commit()
        logger.info("Report deleted: id=%s user_id=%s", report_id, user_id)
        return True


report_service = ReportService()
