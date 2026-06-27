# ✅ Deployment Checklist — InsightForge-AI

> 每次部署前/后逐项检查，确保无遗漏。

---

## 一、部署前检查 (Pre-Deploy)

### 代码质量

- [ ] 所有测试通过：`cd backend && python -m pytest tests/ -v`
- [ ] 所有测试通过：`cd frontend && npx vitest run`
- [ ] TypeScript 类型检查零错误：`cd frontend && npx vue-tsc --noEmit`
- [ ] 前端构建成功：`cd frontend && npm run build`
- [ ] Platform-Skill 解耦验证：grep backend/app/ 无业务关键词

### 安全配置

- [ ] SECRET_KEY 已更换为非默认值（≥32 字符随机字符串）
- [ ] LLM_API_KEY 已配置真实的 API Key
- [ ] DEBUG=false（生产环境）
- [ ] CORS_ORIGINS 已设为生产域名（非 localhost）
- [ ] .env 文件不在 Git 版本控制中
- [ ] 无真实 API Key 出现在代码文件或文档中

### 环境变量检查

- [ ] `.env` 文件存在于项目根目录
- [ ] `DATABASE_URL` 指向 PostgreSQL（Docker）或有值（Railway 自动注入）
- [ ] `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB` 已设置
- [ ] `LLM_PROVIDER` / `LLM_BASE_URL` / `LLM_API_KEY` / `LLM_MODEL` 正确
- [ ] `VITE_API_URL` 留空（Docker）或设为正确的后端地址

---

## 二、Docker Compose 部署验证

### 启动检查

- [ ] `docker compose up -d --build` 无错误
- [ ] `docker compose ps` 显示 3 个服务均为 healthy/running
- [ ] backend 容器日志无异常：`docker compose logs backend`
- [ ] frontend 容器日志无异常：`docker compose logs frontend`
- [ ] db 容器健康检查通过：`docker compose ps db | grep healthy`

### 数据库检查

- [ ] PostgreSQL 可连接：`docker compose exec db pg_isready -U user -d insightforge`
- [ ] 数据库迁移成功：`docker compose exec backend python -m alembic upgrade head`
- [ ] 数据库表已创建：`docker compose exec db psql -U user -d insightforge -c "\dt"`

### 服务连通性

- [ ] Backend API 响应：`curl http://localhost:8000/` → `{"message":"InsightForge-AI API"}`
- [ ] Skill 列表可获取：`curl http://localhost:8000/skill/list` → 包含 bazi
- [ ] 前端页面可访问：`curl http://localhost/` → HTML（非 502/504）
- [ ] Nginx API 代理正常：`curl http://localhost/auth/login -X POST -H "Content-Type: application/json" -d '{"username":"test","password":"test"}'` → JSON 响应
- [ ] Skills 目录已挂载：`docker compose exec backend ls /app/skills/bazi/manifest.json`

### 持久化验证

- [ ] 注册用户后重启服务，用户数据仍存在
- [ ] 生成报告后重启服务，报告数据仍存在
- [ ] `docker compose down && docker compose up -d` 后数据不丢失

---

## 三、线上 E2E 测试

按顺序执行，每步确认成功：

### 用户系统

- [ ] **注册**：POST /auth/register → 200，返回 token
- [ ] **登录**：POST /auth/login → 200，返回 token
- [ ] **获取用户信息**：GET /auth/me → 200，返回用户名
- [ ] **未登录拦截**：无 token 访问 /report/list → 401

### Skill 系统

- [ ] **Skill 列表**：GET /skill/list → 返回 bazi（命运双鉴）

### 报告系统（需真实 LLM）

- [ ] **生成报告**：POST /report/generate → 200，返回 HTML 报告
- [ ] **报告列表**：GET /report/list → 200，包含已生成的报告
- [ ] **报告详情**：GET /report/{id} → 200，HTML 内容完整
- [ ] **删除报告**：DELETE /report/{id} → 200
- [ ] **权限隔离**：用户 A 无法查看/删除用户 B 的报告

### 前端验证

- [ ] 首页正常加载，显示 Skill 卡片
- [ ] 点击 Skill 进入参数表单页
- [ ] 填写参数点击生成，跳转到报告页
- [ ] 报告页正常渲染 HTML
- [ ] 历史页正常显示报告列表
- [ ] 登录/注册页正常跳转

---

## 四、Railway 部署额外检查

- [ ] Railway PostgreSQL 插件已附加
- [ ] `DATABASE_URL` 由 Railway 自动注入（不要手动设置）
- [ ] 所有环境变量已在 Railway Variables 面板设置
- [ ] `railway up` 部署成功
- [ ] 分配的前端域名可访问
- [ ] CORS_ORIGINS 包含 Railway 分配的域名
- [ ] 生产环境 HTTPS 已启用（Railway 默认支持）

---

## 五、安全终检

- [ ] `.env` 和 `backend/.env` 均已 gitignored
- [ ] `*.db` 文件均已 gitignored
- [ ] `node_modules/` 和 `__pycache__/` 均已 gitignored
- [ ] git 历史中无明文 API Key（`git log -p | grep -i api_key`）
- [ ] Docker 镜像中无 .env 文件（检查 Dockerfile 的 COPY 指令）
- [ ] SECRET_KEY 强度足够（≥32 字符，非字典词）
- [ ] 生产环境 DEBUG=false

---

## 六、监控与日志（生产环境）

- [ ] 应用日志正常输出（无异常 ERROR）
- [ ] LLM 调用正常完成（无超时、无 5xx）
- [ ] 数据库连接池正常（无连接泄漏）
- [ ] 磁盘空间充足（数据库卷大小在增长）

---

## 七、回滚计划

如部署出现问题：

```bash
# 1. 回滚到上一个稳定版本的代码
git checkout <previous-tag>

# 2. 重建并启动
docker compose up -d --build

# 3. 如果数据库出现问题，从备份恢复
docker compose down
docker compose up -d db
cat backup.sql | docker compose exec -T db psql -U user -d insightforge
docker compose up -d
```

---

## 八、签署

| 检查项 | 状态 | 签名 | 日期 |
|--------|:----:|------|------|
| 部署前检查 | ☐ | | |
| Docker Compose 验证 | ☐ | | |
| 线上 E2E | ☐ | | |
| Railway（如使用） | ☐ | | |
| 安全终检 | ☐ | | |
