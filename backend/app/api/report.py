"""Report API — 报告生成、列表、详情、删除

所有接口均需 JWT 鉴权。
用户只能访问自己的报告。
"""

import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.skill import SkillRequest, SkillResponse
from app.schemas.report import ReportItem, ReportDetail, ReportListResponse
from app.runtime.skill_runtime import skill_runtime
from app.services.report_service import report_service
from app.core.dependency import get_current_user
from app.models.user import User
from app.types.skill import SkillRequest as InternalSkillRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/report", tags=["report"])


@router.post("/generate", response_model=SkillResponse)
async def generate_report(
    request: SkillRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """生成 AI 报告 → 持久化到数据库 → 返回 report_id

    需要 JWT 鉴权。Skill 不访问数据库，Platform 负责保存 HTML。
    """
    report_id = str(uuid.uuid4())
    logger.info(
        "POST /report/generate: skill=%s user=%s report_id=%s",
        request.skill_id, current_user.id, report_id,
    )

    # 1. 调用 SkillRuntime
    internal_request = InternalSkillRequest(
        skill_id=request.skill_id,
        user_id=current_user.id,
        session_id=report_id,
        parameters=request.parameters,
    )
    result = await skill_runtime.run(internal_request)

    # 2. Platform 负责保存 HTML 到数据库（Skill 不访问数据库）
    if result.success:
        try:
            report = report_service.create(
                db,
                user_id=current_user.id,
                skill_id=request.skill_id,
                result=result,
            )
            report_id = str(report.id)
            logger.info("Report persisted: db_id=%s", report.id)
        except Exception as e:
            logger.exception("Failed to save report to database")
            return SkillResponse(
                report_id=report_id,
                success=False,
                title=result.title,
                html=result.html,
                metadata=result.metadata,
                error=f"报告生成成功但保存失败: {str(e)}",
            )

    return SkillResponse(
        report_id=report_id,
        success=result.success,
        title=result.title,
        html=result.html,
        metadata=result.metadata,
        error=result.error,
    )


@router.get("/list", response_model=ReportListResponse)
async def list_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取当前用户所有报告（需 JWT）"""
    reports = report_service.list_by_user(db, user_id=current_user.id)
    return ReportListResponse(
        reports=[
            ReportItem(
                id=r.id,
                skill_id=r.skill_id,
                title=r.title,
                created_at=r.created_at,
            )
            for r in reports
        ]
    )


@router.get("/{report_id}", response_model=ReportDetail)
async def get_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取报告详情 — 只能查看自己的报告（需 JWT）"""
    report = report_service.get_user_report(db, report_id, current_user.id)
    if report is None:
        raise HTTPException(status_code=404, detail="报告不存在")
    return ReportDetail(
        id=report.id,
        skill_id=report.skill_id,
        title=report.title,
        html=report.html,
        metadata=report.metadata_,
        created_at=report.created_at,
    )


@router.delete("/{report_id}")
async def delete_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """删除报告 — 只能删除自己的报告（需 JWT）"""
    success = report_service.delete(db, report_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="报告不存在")
    return {"message": "报告已删除"}
