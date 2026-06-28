# 🔮 InsightForge-AI

> AI结构化报告生成平台 — 基于插件架构，可扩展的AI报告系统。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Vue 3.5+](https://img.shields.io/badge/Vue-3.5+-green.svg)](https://vuejs.org)
[![Tests](https://img.shields.io/badge/Tests-45%2F45%20passed-brightgreen.svg)](.)

---

## 📖 项目介绍

InsightForge-AI 是一个**基于插件的AI结构化报告生成平台**。它不是算命网站 — 八字只是第一个技能（Skill）示例。

平台提供通用基础设施（用户系统、JWT认证、数据库、技能调度、大模型抽象层），每个**技能（Skill）**封装一个特定的AI能力（提示词、分析、HTML渲染）。新增一种AI报告类型**不需要修改平台代码** — 只需在 `skills/` 目录下新建一个文件夹即可。

### 核心设计原则

```
平台 ← 技能请求/技能响应 → 技能
```

- **平台**：用户、JWT、REST API、数据库、技能注册/运行时、大模型服务、部署
- **技能**：业务逻辑、提示词、AI分析、HTML渲染
- **平台不关心技能内部做什么。技能不接触数据库或认证。**

---

## 🏗 架构

```
┌─────────────────────────────────────────────┐
│                  前端                         │
│         Vue3 + Element Plus + Pinia          │
│               (端口 5173)                    │
└──────────────────────┬──────────────────────┘
                       │ REST API (JWT)
┌──────────────────────▼──────────────────────┐
│                  后端                         │
│            FastAPI (端口 8000)                │
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│  │  认证     │  │  报告     │  │  技能     │  │
│  │  服务     │  │  服务     │  │  注册中心  │  │
│  └──────────┘  └──────────┘  └─────┬─────┘  │
│                                    │         │
│  ┌─────────────────────────────────▼──────┐  │
│  │         技能运行时                        │  │
│  │  ┌─────────┐  ┌────────────────────┐   │  │
│  │  │ 加载器   │  │  工作流缓存         │   │  │
│  │  └─────────┘  └────────────────────┘   │  │
│  └────────────────────────────────────────┘  │
│                    │                          │
│  ┌─────────────────▼──────────────────────┐  │
│  │         大模型客户端（外观模式）          │  │
│  │  ┌──────────────────────────────────┐  │  │
│  │  │  OpenAI兼容提供商                  │  │  │
│  │  │  (DeepSeek / OpenAI / Qwen ...)   │  │  │
│  │  └──────────────────────────────────┘  │  │
│  └────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│                 数据库                        │
│        SQLite (开发) / PostgreSQL (生产)     │
│              用户 + 报告                     │
└─────────────────────────────────────────────┘

                    ┌──────────────────┐
                    │   skills/        │
                    │   (独立目录)     │
                    │                  │
                    │  bazi/           │
                    │    workflow.py   │
                    │    renderer.py   │
                    │    prompt.md     │
                    │    manifest.json │
                    └──────────────────┘
```

### 完整请求流程

```
POST /report/generate  { skill_id, parameters }
    │
    ▼
api/report.py          JWT认证 → 用户对象
    │
    ▼
SkillRuntime.run()     缓存查找 → 加载工作流 → 执行
    │
    ▼
workflow.py            校验 → 加载提示词 → 填充模板
    │
    ▼
大模型客户端             POST DeepSeek/OpenAI → AI响应
    │
    ▼
renderer.py            AI内容 → HTML
    │
    ▼
ReportService          存入数据库 (user_id, skill_id, html)
    │
    ▼
响应                    SkillResponse { report_id, title, html }
```

---

## 🛠 技术栈

| 层级 | 技术 | 版本 |
|-------|-----------|---------|
| **后端** | FastAPI | 0.115+ |
| | Uvicorn | 0.30+ |
| | Pydantic | v2 |
| | Python | 3.12+ |
| **前端** | Vue | 3.5+ (组合式API) |
| | Vite | 5.4+ |
| | TypeScript | 5.6+ |
| | Element Plus | 2.8+ (按需导入) |
| | Pinia | 2.2+ |
| | Vue Router | 4.4+ |
| **数据库** | SQLAlchemy | 2.0+ |
| | Alembic | 1.13+ |
| | SQLite | 开发环境 (零配置) |
| | PostgreSQL | 16 (生产环境) |
| **大模型** | DeepSeek-Chat | OpenAI兼容 |
| | 可切换 | OpenAI / Qwen / OpenRouter / vLLM |
| **认证** | bcrypt | 4.2+ |
| | python-jose | 3.3+ (JWT) |
| **测试** | Pytest | 9.1+ (后端) |
| | Vitest | 2.1+ (前端) |
| **部署** | Docker Compose | 3.9 |
| | Railway | 目标平台 |

---

## 🚀 快速开始

### 前置条件

- Python 3.12+
- Node.js 22+
- Docker（可选，用于PostgreSQL/生产环境）

### 1. 克隆与配置

```bash
git clone <仓库地址> InsightForge-AI
cd InsightForge-AI
cp .env.example .env
# 编辑 .env — 设置你的 LLM_API_KEY 和 SECRET_KEY
```

### 2. 后端

```bash
cd backend
pip install -r requirements.txt
python -m alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### 3. 前端

```bash
cd frontend
npm install
npm run dev
```

访问 **http://localhost:5173**

### 4. 创建演示数据（可选）

```bash
cd backend
python ../scripts/seed.py
# 创建演示用户：用户名=demo，密码=demo123
```

---

## 🐳 Docker部署

```bash
docker compose up -d
docker compose ps
docker compose logs -f
```

---

## ☁️ Railway部署

1. 将项目推送到GitHub
2. 在Railway中关联仓库
3. 根据 `.env.example` 设置环境变量
4. 部署 — Railway自动检测Dockerfile
5. 添加PostgreSQL服务

---

## 🧩 添加新技能

添加新技能**不需要修改任何平台代码**。

### 分步指南

1. **创建技能目录**

```bash
mkdir -p skills/career
```

2. **编写 `manifest.json`**

```json
{
  "id": "career",
  "display_name": "职业规划",
  "version": "1.0.0",
  "description": "AI 职业发展规划分析",
  "icon": "career",
  "category": "career",
  "entry": "workflow.py",
  "output": "html",
  "parameters": {
    "industry": {
      "type": "select",
      "label": "目标行业",
      "required": true,
      "options": ["互联网", "金融", "医疗", "教育"],
      "default": "互联网"
    },
    "years_experience": {
      "type": "number",
      "label": "工作年限",
      "required": true,
      "min": 0,
      "max": 50,
      "default": 3
    }
  }
}
```

3. **编写 `workflow.py`**

```python
import logging
from app.types.skill import SkillRequest, SkillResponse

logger = logging.getLogger(__name__)

async def run(request: SkillRequest) -> SkillResponse:
    try:
        params = request.parameters
        # 校验、构建提示词、调用大模型、渲染HTML……
        return SkillResponse(
            success=True,
            title="职业规划报告",
            html="<html>...</html>",
            metadata={"skill": "career", "version": "1.0.0"},
        )
    except Exception as e:
        logger.exception("职业规划技能出错")
        return SkillResponse(
            success=False, title="", html="", metadata={}, error=str(e)
        )
```

4. **编写 `prompt.md`** — AI提示词模板

5. **编写 `renderer.py`** — HTML渲染器

6. **重启后端** — 技能在启动时自动发现

### 技能目录结构

```
skills/my_skill/
├── manifest.json    # 必填：技能元数据 + 参数定义
├── workflow.py      # 必填：async def run(request) -> SkillResponse
├── renderer.py      # 必填：HTML生成
├── prompt.md        # 必填：AI提示词模板
├── README.md        # 可选：技能说明文档
├── templates/       # 可选：额外模板
├── assets/          # 可选：静态资源
└── scripts/         # 可选：工具脚本
```

---

## 📡 API示例

### 注册

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "demo", "password": "demo123"}'
```

### 登录

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "demo", "password": "demo123"}'
# 返回：{ "access_token": "...", "user": { "id": 1, "username": "demo" } }
```

### 获取技能列表

```bash
curl http://localhost:8000/skill/list
```

### 生成报告

```bash
curl -X POST http://localhost:8000/report/generate \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"skill_id": "bazi", "parameters": {"year": 1990, "month": 6, "day": 15, "hour": 8, "gender": "男"}}'
```

### 获取报告列表

```bash
curl -H "Authorization: Bearer <token>" http://localhost:8000/report/list
```

### 获取报告详情

```bash
curl -H "Authorization: Bearer <token>" http://localhost:8000/report/1
```

### 删除报告

```bash
curl -X DELETE -H "Authorization: Bearer <token>" http://localhost:8000/report/1
```

---

## 📁 项目结构

```
InsightForge-AI/
├── README.md
├── LICENSE (MIT)
├── .env.example
├── docker-compose.yml
│
├── docs/
│   ├── PRD.md              # 产品需求文档
│   ├── CLAUDE.md           # 开发规范与约束
│   ├── SKILL_SPEC.md       # 技能插件协议规范
│   ├── HANDOFF.md          # 项目交接文档
│   └── assets/             # 截图与架构图
│
├── backend/
│   ├── app/
│   │   ├── main.py         # FastAPI入口 + 日志 + 异常处理
│   │   ├── api/            # REST接口 (auth, report, skill)
│   │   ├── core/           # 配置、安全 (bcrypt+JWT)、依赖注入
│   │   ├── database/       # SQLAlchemy引擎 + 会话
│   │   ├── models/         # ORM模型 (User, Report)
│   │   ├── schemas/        # Pydantic请求/响应模型
│   │   ├── services/       # 业务逻辑层
│   │   ├── runtime/        # 技能执行引擎
│   │   ├── registry/       # 技能自动发现
│   │   ├── llm/            # 大模型抽象层（提供商模式）
│   │   └── types/          # 内部类型定义
│   ├── tests/              # pytest (21个测试，全部通过)
│   └── alembic/            # 数据库迁移
│
├── frontend/
│   ├── src/
│   │   ├── main.ts         # Vue入口 (Pinia + Router + 全局错误处理)
│   │   ├── App.vue         # 根组件
│   │   ├── api/            # HTTP客户端 (JWT注入、ApiError、类型化API)
│   │   ├── components/     # 共享组件：AppHeader、LoadingOverlay、ErrorDisplay、StateWrapper
│   │   ├── pages/          # 7个页面：首页、登录、注册、技能、报告、历史、404
│   │   ├── stores/         # Pinia状态管理：auth、skill
│   │   └── router/         # Vue Router + 路由守卫
│   └── __tests__/          # Vitest (24个测试，全部通过)
│
├── skills/
│   └── bazi/               # 第一个技能：八字命理分析
│       ├── manifest.json
│       ├── workflow.py
│       ├── renderer.py
│       └── prompt.md
│
└── scripts/
    ├── init_db.py
    └── seed.py
```

---

## 🖼 截图

> 截图待补充 — 将图片添加到 `docs/assets/` 目录后在此处引用。

| 页面 | 截图 |
|------|-----------|
| 首页 | ![首页](docs/assets/screenshot-home.png) |
| 技能表单 | ![技能](docs/assets/screenshot-skill.png) |
| 报告 | ![报告](docs/assets/screenshot-report.png) |
| 历史 | ![历史](docs/assets/screenshot-history.png) |

---

## 🧪 测试

```bash
# 后端测试 (21个测试)
cd backend
python -m pytest tests/ -v

# 前端测试 (24个测试)
cd frontend
npx vitest run
```

**测试状态：45/45 全部通过 ✅**

---

## 📜 许可证

MIT — 详见 [LICENSE](LICENSE)。

---

## 🔮 路线图

- [x] 第一阶段：项目初始化 (FastAPI + Vue3 + Docker)
- [x] 第二阶段：八字技能集成 (技能运行时 + 大模型客户端)
- [x] 第三阶段：用户系统 (注册/登录/JWT/报告增删改查)
- [x] 第四阶段：前端 (7个页面、Pinia、动态表单)
- [x] 第五阶段：产品化 (测试、日志、文档、用户体验打磨)
- [ ] 第六阶段：部署 (Docker Compose验证 + Railway)
- [ ] 更多技能 (职业规划、简历分析、心理测评……)
- [ ] PDF导出
- [ ] 暗色模式
- [ ] 多语言国际化
