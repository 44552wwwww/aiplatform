"""全链路端到端测试：注册 → 登录 → 生成报告 → 数据库验证 → 查询报告

使用 conftest.py 的 fixtures（client, setup_db, TestingSessionLocal），
避免重复的数据库配置。
"""

import logging

import pytest

from app.models.report import Report
from tests.conftest import TestingSessionLocal

logger = logging.getLogger(__name__)


class TestE2EBazi:
    """真实 LLM 端到端测试"""

    def test_full_pipeline(self, client):
        # 1. 注册
        register_resp = client.post(
            "/auth/register", json={"username": "e2euser", "password": "e2epass"}
        )
        assert register_resp.status_code == 200, f"注册失败: {register_resp.text}"
        token = register_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        logger.info("E2E: 1. Register passed")

        # 2. 获取当前用户
        me_resp = client.get("/auth/me", headers=headers)
        assert me_resp.status_code == 200
        assert me_resp.json()["username"] == "e2euser"
        logger.info("E2E: 2. /me JWT auth passed")

        # 3. 生成 Bazi 报告（真实 LLM 调用）
        generate_resp = client.post(
            "/report/generate",
            json={
                "skill_id": "bazi",
                "parameters": {
                    "year": 1990,
                    "month": 6,
                    "day": 15,
                    "hour": 8,
                    "gender": "male",
                },
            },
            headers=headers,
        )
        assert generate_resp.status_code == 200, f"Generate failed: {generate_resp.text}"
        data = generate_resp.json()
        logger.info("E2E: 3. Report generated: success=%s, title=%s", data["success"], data["title"])

        if data["success"]:
            assert len(data["html"]) > 100, f"HTML too short: {len(data['html'])} chars"
            logger.info("    HTML size: %d chars", len(data["html"]))
            assert data["report_id"].isdigit(), f"report_id not numeric: {data['report_id']}"
            report_id = int(data["report_id"])

            # 4. 验证数据库持久化
            db = TestingSessionLocal()
            report = db.query(Report).filter(Report.id == report_id).first()
            db.close()
            assert report is not None, "Report not saved to DB"
            assert report.skill_id == "bazi"
            assert report.user_id == 1
            assert len(report.html) > 100
            logger.info(
                "E2E: 4. DB saved: id=%d, skill=%s, html=%d chars",
                report.id, report.skill_id, len(report.html),
            )

            # 5. 获取报告详情
            detail_resp = client.get(f"/report/{report_id}", headers=headers)
            assert detail_resp.status_code == 200
            detail = detail_resp.json()
            assert detail["title"] == data["title"]
            assert detail["html"] == data["html"]
            logger.info("E2E: 5. Report detail retrieved")

            # 6. 报告列表
            list_resp = client.get("/report/list", headers=headers)
            assert list_resp.status_code == 200
            reports = list_resp.json()["reports"]
            assert len(reports) == 1
            assert reports[0]["id"] == report_id
            logger.info("E2E: 6. Report list: %d entries", len(reports))

            # 7. 删除报告
            del_resp = client.delete(f"/report/{report_id}", headers=headers)
            assert del_resp.status_code == 200
            logger.info("E2E: 7. Report deleted")

            # 8. 验证数据库删除
            db = TestingSessionLocal()
            deleted = db.query(Report).filter(Report.id == report_id).first()
            db.close()
            assert deleted is None
            logger.info("E2E: 8. DB deletion confirmed")
        else:
            pytest.fail(f"Report generation returned error: {data.get('error')}")

    def test_html_contains_keywords(self, client):
        """验证生成的 HTML 包含完整结构"""
        # 注册
        resp = client.post("/auth/register", json={"username": "htmltest", "password": "pass"})
        assert resp.status_code == 200
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 生成
        resp = client.post(
            "/report/generate",
            json={
                "skill_id": "bazi",
                "parameters": {"year": 2000, "month": 1, "day": 1, "hour": 12, "gender": "female"},
            },
            headers=headers,
        )
        data = resp.json()
        if data["success"]:
            html = data["html"]
            # 验证 HTML 结构完整性
            assert "<!DOCTYPE html>" in html
            assert "</html>" in html
            assert "InsightForge" in html or "命运双鉴" in html or "analysis" in html.lower()
            logger.info("E2E: HTML structure valid: %d chars, DOCTYPE + title present", len(html))
        else:
            pytest.fail(f"Report failed: {data.get('error')}")


class TestE2EErrorHandling:
    """错误处理测试"""

    def test_unauthorized_access(self, client):
        resp = client.post("/report/generate", json={"skill_id": "bazi", "parameters": {}})
        assert resp.status_code == 401
        logger.info("E2E: Unauthorized access blocked")

    def test_invalid_skill(self, client):
        resp = client.post("/auth/register", json={"username": "err", "password": "p"})
        assert resp.status_code == 200
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        resp = client.post(
            "/report/generate",
            json={"skill_id": "no_such_skill", "parameters": {}},
            headers=headers,
        )
        data = resp.json()
        assert data["success"] is False
        logger.info("E2E: Invalid skill handled: %s", data["error"])
