# 🚀 Deployment Guide — InsightForge-AI

> 支持 Docker Compose（含 PostgreSQL）和 Railway 云部署。

---

## 一、环境准备

### 必需软件

| 工具 | 版本 | 用途 |
|------|------|------|
| Docker | 24+ | 容器运行时 |
| Docker Compose | 2.x+ | 服务编排 |
| Git | 任意 | 代码管理 |

---

## 二、Docker Compose 部署

### 1. 获取代码

```bash
git clone <repo-url> InsightForge-AI
cd InsightForge-AI
```

### 2. 配置环境变量

```bash
# 从生产模板创建 .env 文件（项目根目录）
cp .env.production.example .env

# 编辑 .env，替换以下值：
# - SECRET_KEY      → 生成一个随机字符串（至少 32 位）
# - LLM_API_KEY     → 你的 LLM API Key
# - LLM_BASE_URL    → LLM 服务地址
# - LLM_MODEL       → 模型名称
# - POSTGRES_PASSWORD → 数据库密码
# - CORS_ORIGINS    → 生产前端域名
```

### 3. 生成 SECRET_KEY

```bash
# Linux/Mac
openssl rand -hex 32

# Windows PowerShell
[Convert]::ToHexString((1..32 | % { Get-Random -Max 256 }))
```

### 4. 启动服务

```bash
# 构建镜像并启动所有服务
docker compose up -d --build

# 检查服务状态
docker compose ps

# 查看日志
docker compose logs -f
```

### 5. 初始化数据库

```bash
# 在 backend 容器中运行数据库迁移
docker compose exec backend python -m alembic upgrade head

# （可选）创建 demo 用户
docker compose exec backend python ../scripts/seed.py
```

### 6. 验证部署

```bash
# 检查 API 是否正常
curl http://localhost:8000/
# → {"message": "InsightForge-AI API"}

# 检查前端是否正常
curl http://localhost/
# → HTML 页面

# 检查 PostgreSQL
docker compose exec db pg_isready -U user -d insightforge
# → accepting connections
```

### 7. 停止服务

```bash
# 停止（保留数据卷）
docker compose down

# 停止并删除数据卷（重置数据库）
docker compose down -v
```

---

## 三、架构说明

```
┌────────────────────────────────────────────────┐
│  浏览器 :80                                     │
└──────────────────┬─────────────────────────────┘
                   │
┌──────────────────▼─────────────────────────────┐
│  frontend (nginx:alpine)                       │
│  - 静态文件服务                                 │
│  - /auth, /report, /skill → proxy → backend    │
└──────────────────┬─────────────────────────────┘
                   │
┌──────────────────▼─────────────────────────────┐
│  backend (FastAPI + Uvicorn)                   │
│  - REST API                                     │
│  - Skill 执行引擎                               │
│  - 连接 PostgreSQL (db:5432)                    │
│  - 挂载 ./skills:/app/skills                    │
└──────────────────┬─────────────────────────────┘
                   │
┌──────────────────▼─────────────────────────────┐
│  db (PostgreSQL 16)                            │
│  - 数据卷: pgdata:/var/lib/postgresql/data     │
└────────────────────────────────────────────────┘
```

**关键设计要点**：
- 前端通过 nginx 反向代理到后端，无需跨域
- 后端通过 Docker 网络访问 PostgreSQL（hostname: `db`）
- `skills/` 目录通过 bind mount 挂载到后端容器
- 数据库数据通过命名卷 `pgdata` 持久化

---

## 四、环境变量完整说明

| 变量 | 必填 | 默认值 | 说明 |
|------|:--:|--------|------|
| `DATABASE_URL` | ✅ | `sqlite:///./insightforge.db` | 数据库连接字符串。Docker 中自动设为 PostgreSQL |
| `POSTGRES_USER` | — | `user` | PostgreSQL 用户名 |
| `POSTGRES_PASSWORD` | ✅ | — | PostgreSQL 密码 |
| `POSTGRES_DB` | — | `insightforge` | PostgreSQL 数据库名 |
| `LLM_PROVIDER` | ✅ | `openai_compatible` | LLM Provider 类型 |
| `LLM_BASE_URL` | ✅ | — | LLM API 地址 |
| `LLM_API_KEY` | ✅ | — | LLM API 密钥 |
| `LLM_MODEL` | ✅ | `deepseek-chat` | 模型名称 |
| `LLM_TIMEOUT` | — | `120` | LLM 请求超时（秒） |
| `LLM_API_PATH` | — | `/v1/chat/completions` | API 路径 |
| `SECRET_KEY` | ✅ | — | JWT 签名密钥（≥16 字符） |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | — | `30` | JWT 过期时间（分钟） |
| `JWT_ALGORITHM` | — | `HS256` | JWT 签名算法 |
| `DEBUG` | — | `true` | 调试模式（生产设为 false） |
| `CORS_ORIGINS` | ✅ | `http://localhost:5173` | 允许的跨域来源（逗号分隔） |
| `VITE_API_URL` | — | — | 前端 API 地址（Docker 留空） |

---

## 五、Railway 部署

Railway 是一个支持 Docker 的云平台，提供一键部署和托管 PostgreSQL。

### 方式一：Docker Compose on Railway

1. **准备项目**
   - 将 `.env.production.example` 中的变量添加到 Railway 的 "Variables" 面板
   - Railway 自动提供 `DATABASE_URL`（覆盖你在 .env 中的设置）

2. **创建 railway.toml**（可选，Railway 也能自动检测 docker-compose.yml）

3. **部署**
   ```bash
   # 安装 Railway CLI
   npm install -g @railway/cli
   
   # 登录
   railway login
   
   # 初始化项目
   railway init
   
   # 部署
   railway up
   ```

4. **设置环境变量**
   - 在 Railway Dashboard → Variables 中添加所有必填变量
   - `DATABASE_URL` 由 Railway PostgreSQL 插件自动注入

### 方式二：单服务 Dockerfile

如果 Railway 不支持 Compose，可以分别部署：

1. **backend** — 使用 `backend/Dockerfile`
2. **frontend** — 使用 `frontend/Dockerfile`（需要构建参数 `VITE_API_URL=`）
3. **db** — 使用 Railway PostgreSQL 插件

每个服务通过 Railway 的环境变量配置。

### Railway 环境变量要点

- `DATABASE_URL` — 由 Railway PostgreSQL 插件自动设置，**不要手动覆盖**
- `SECRET_KEY` — 手动设置强随机字符串
- `LLM_API_KEY` — 你的 LLM API 密钥
- `VITE_API_URL` — 留空（前端使用 nginx 反向代理）
- `CORS_ORIGINS` — 设为 Railway 分配的前端域名（如 `https://xxx.up.railway.app`）

---

## 六、常见问题

### Q1: 前端 404 错误
确保 nginx 配置中的 `try_files $uri $uri/ /index.html` 存在（SPA 路由回退）。

### Q2: 后端无法连接数据库
```bash
# 检查 db 服务是否健康
docker compose ps db
# 检查数据库是否接受连接
docker compose exec db pg_isready -U user -d insightforge
# 检查 backend 能否 ping 通 db
docker compose exec backend ping db
```

### Q3: Skill 列表为空
检查 `skills/` 目录是否正确挂载：
```bash
docker compose exec backend ls /app/skills/
```
应看到 `bazi` 目录。如果为空，确认 `docker-compose.yml` 中 `volumes: - ./skills:/app/skills` 存在。

### Q4: 数据库迁移失败
```bash
# 进入容器手动运行迁移
docker compose exec backend python -m alembic upgrade head
# 或重置数据库
docker compose down -v
docker compose up -d
docker compose exec backend python -m alembic upgrade head
```

### Q5: LLM 调用超时
增大 `LLM_TIMEOUT` 环境变量（默认 120 秒），或使用更快的模型。

---

## 七、备份与恢复

### 备份数据库

```bash
# PostgreSQL 备份
docker compose exec db pg_dump -U user insightforge > backup.sql
```

### 恢复数据库

```bash
# PostgreSQL 恢复
cat backup.sql | docker compose exec -T db psql -U user -d insightforge
```

### 数据卷备份

```bash
# 备份整个 pgdata 卷
docker run --rm -v insightforge-ai_pgdata:/data -v $(pwd):/backup alpine tar czf /backup/pgdata-backup.tar.gz -C /data .
```

---

## 八、安全建议

- [ ] 生产环境 `DEBUG=false`
- [ ] `SECRET_KEY` ≥ 32 随机字符
- [ ] 定期轮换 `LLM_API_KEY`
- [ ] 启用 HTTPS（Railway 默认支持）
- [ ] 限制 `CORS_ORIGINS` 为具体的生产域名
- [ ] 定期备份数据库
- [ ] 监控日志中的异常
