"""Auth API 测试"""


class TestRegister:
    def test_register_success(self, client):
        resp = client.post(
            "/auth/register", json={"username": "alice", "password": "secret123"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["username"] == "alice"

    def test_register_duplicate(self, client):
        client.post("/auth/register", json={"username": "bob", "password": "pass1"})
        resp = client.post("/auth/register", json={"username": "bob", "password": "pass2"})
        assert resp.status_code == 400
        assert "已存在" in resp.json()["detail"]

    def test_register_missing_password(self, client):
        resp = client.post("/auth/register", json={"username": "test"})
        assert resp.status_code == 422


class TestLogin:
    def test_login_success(self, client):
        client.post("/auth/register", json={"username": "charlie", "password": "mypass"})
        resp = client.post("/auth/login", json={"username": "charlie", "password": "mypass"})
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["user"]["username"] == "charlie"

    def test_login_wrong_password(self, client):
        client.post("/auth/register", json={"username": "dave", "password": "correct"})
        resp = client.post("/auth/login", json={"username": "dave", "password": "wrong"})
        assert resp.status_code == 401

    def test_login_nonexistent_user(self, client):
        resp = client.post("/auth/login", json={"username": "nobody", "password": "x"})
        assert resp.status_code == 401


class TestMe:
    def test_me_with_token(self, client, auth_headers):
        resp = client.get("/auth/me", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["username"] == "testuser"

    def test_me_without_token(self, client):
        resp = client.get("/auth/me")
        assert resp.status_code == 401
