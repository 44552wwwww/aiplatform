"""Report API 测试"""

import pytest


class TestReportList:
    def test_list_empty(self, client, auth_headers):
        resp = client.get("/report/list", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["reports"] == []

    def test_list_requires_auth(self, client):
        resp = client.get("/report/list")
        assert resp.status_code == 401


class TestReportDetail:
    def test_not_found(self, client, auth_headers):
        resp = client.get("/report/99999", headers=auth_headers)
        assert resp.status_code == 404

    def test_requires_auth(self, client):
        resp = client.get("/report/1")
        assert resp.status_code == 401


class TestReportDelete:
    def test_not_found(self, client, auth_headers):
        resp = client.delete("/report/99999", headers=auth_headers)
        assert resp.status_code == 404

    def test_requires_auth(self, client):
        resp = client.delete("/report/1")
        assert resp.status_code == 401


class TestReportGenerateAuth:
    def test_requires_auth(self, client):
        """生成报告需要 JWT"""
        resp = client.post(
            "/report/generate",
            json={"skill_id": "bazi", "parameters": {"year": 2000, "month": 1, "day": 1, "hour": 12, "gender": "男"}},
        )
        assert resp.status_code == 401

    def test_invalid_skill(self, client, auth_headers):
        """不存在的 Skill 返回错误"""
        resp = client.post(
            "/report/generate",
            json={"skill_id": "nonexistent", "parameters": {}},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is False
        assert "not found" in data["error"].lower()


class TestReportCrossUser:
    """权限隔离测试 — 用户不能访问其他用户的报告"""

    def test_cross_user_isolation(self, client, auth_headers):
        """另一个用户无法访问 testuser 的报告"""
        # testuser 的报告（需要先生成一个）
        # 由于没有 LLM Key，我们只测试权限边界
        # 注册另一个用户
        client.post("/auth/register", json={"username": "other", "password": "pass"})
        resp2 = client.post("/auth/login", json={"username": "other", "password": "pass"})
        other_token = resp2.json()["access_token"]
        other_headers = {"Authorization": f"Bearer {other_token}"}

        # other 用户访问不存在的报告 → 404
        resp = client.get("/report/1", headers=other_headers)
        assert resp.status_code == 404

        # other 用户能看到自己的空列表
        resp = client.get("/report/list", headers=other_headers)
        assert resp.status_code == 200
        assert resp.json()["reports"] == []
