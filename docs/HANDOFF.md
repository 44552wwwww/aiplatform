# HANDOFF.md — InsightForge-AI 项目交接文档

> 生成日期：2026-06-28
> 当前状态：Phase 4.5 完成，全部 21 个测试通过，LLM 真实调用联调成功

---

## 一、当前项目状态

### 1.1 基本信息

| 项目 | 说明 |
|------|------|
| **项目名称** | InsightForge-AI |
| **项目定位** | AI Structured Report Generation Platform（Plugin-based） |
| **开发目标** | 构建可部署上线的 AI 个性化报告生成平台 |
| **当前版本** | v1.0.0-dev |

### 1.2 整体架构

```
┌─────────────────────────────────────────────┐
│                  Frontend                    │
│         Vue3 + Element Plus + Pinia          │
│               (Port 5173)                    │
└──────────────────────┬──────────────────────┘
                       │ REST API (JWT)
┌──────────────────────▼──────────────────────┐
│                  Backend                     │
│            FastAPI (Port 8000)               │
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│  │  Auth     │  │  Report  │  │  Skill    │  │
│  │  Service  │  │  Service │  │  Registry │  │
│  └──────────┘  └──────────┘  └─────┬─────┘  │
│                                    │         │
│  ┌─────────────────────────────────▼──────┐  │
│  │         SkillRuntime                    │  │
│  │  ┌─────────┐  ┌────────────────────┐   │  │
│  │  │ Loader  │  │  Workflow Cache    │   │  │
│  │  └─────────┘  └────────────────────┘   │  │
│  └────────────────────────────────────────┘  │
│                    │                          │
│  ┌─────────────────▼──────────────────────┐  │
│  │         LLM Client (Facade)            │  │
│  │  ┌──────────────────────────────────┐  │  │
│  │  │  OpenAICompatibleProvider         │  │  │
│  │  │  (DeepSeek / OpenAI / Qwen ...)   │  │  │
│  │  └──────────────────────────────────┘  │  │
│  └────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│                 Database                     │
│        SQLite (dev) / PostgreSQL (prod)      │
│              User + Report                   │
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
                    │                  │
                    │  resume/         │
                    │  career/         │
                    │  psychology/     │
                    └──────────────────┘
```

### 1.3 当前目录结构

```
InsightForge-AI/
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── docker-compose.yml
│
├── docs/
│   ├── PRD.md              # 产品需求文档
│   ├── CLAUDE.md            # 开发规范（架构、原则、禁止事项）
│   ├── SKILL_SPEC.md        # Skill 插件协议规范
│   └── HANDOFF.md           # ← 本文档
│
├── backend/
│   ├── .env                 # 含 LLM_API_KEY (DeepSeek)
│   ├── .dockerignore
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   │       └── ...init_users_and_reports_tables.py
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── auth.py      # POST /register, /login; GET /me
│   │   │   ├── report.py    # POST /generate, GET /list, /:id, DELETE /:id
│   │   │   └── skill.py     # GET /list
│   │   ├── core/
│   │   │   ├── config.py    # Pydantic Settings (LLM_PROVIDER, DATABASE_URL...)
│   │   │   ├── security.py  # bcrypt + JWT
│   │   │   └── dependency.py # get_current_user (JWT guard)
│   │   ├── database/
│   │   │   ├── base.py      # SQLAlchemy Base
│   │   │   └── database.py  # Engine + SessionLocal
│   │   ├── models/
│   │   │   ├── user.py      # User: id, username, password_hash, created_at
│   │   │   └── report.py    # Report: id, user_id, skill_id, title, html, metadata(JSON)
│   │   ├── schemas/
│   │   │   ├── auth.py      # RegisterRequest, LoginRequest, TokenResponse, UserInfo
│   │   │   ├── report.py    # ReportItem, ReportDetail, ReportListResponse
│   │   │   └── skill.py     # SkillManifest, SkillRequest, SkillResponse
│   │   ├── services/
│   │   │   ├── auth_service.py    # register, login, get_user_by_id
│   │   │   └── report_service.py # create, list_by_user, get_user_report, delete
│   │   ├── runtime/
│   │   │   └── skill_runtime.py   # 调度 Skill 执行 + Workflow 缓存
│   │   ├── registry/
│   │   │   ├── skill_registry.py  # 扫描 skills/ 注册 Skill
│   │   │   └── loader.py         # importlib 动态加载 Skill 模块
│   │   ├── llm/
│   │   │   ├── base.py           # BaseLLMProvider ABC
│   │   │   ├── client.py         # LLMClient Facade
│   │   │   └── providers/
│   │   │       └── openai_compatible.py  # OpenAI-compatible Provider
│   │   ├── types/
│   │   │   └── skill.py          # SkillRequest, SkillResponse (dataclass)
│   │   └── utils/
│   └── tests/
│       ├── conftest.py           # TestClient + override_get_db
│       ├── test_auth.py          # 8 tests: register/login/me/JWT
│       ├── test_report.py        # 9 tests: list/detail/delete/permission
│       └── test_e2e.py           # 4 tests: full pipeline + real LLM
│
├── frontend/
│   ├── .dockerignore
│   ├── .env                 # VITE_API_URL=http://localhost:8000
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── index.html
│   └── src/
│       ├── App.vue
│       ├── main.ts
│       ├── api/
│       │   ├── client.ts    # JWT 自动注入 + 401 拦截
│       │   ├── auth.ts
│       │   ├── report.ts
│       │   └── skill.ts
│       ├── stores/
│       │   ├── auth.ts      # Pinia: token, user, login/register/logout
│       │   └── skill.ts     # Pinia: skill list
│       ├── router/
│       │   └── index.ts     # 7 routes + auth guard
│       ├── components/
│       │   └── AppHeader.vue
│       ├── pages/
│       │   ├── LoginPage.vue
│       │   ├── RegisterPage.vue
│       │   ├── HomePage.vue      # 动态 Skill 卡片网格
│       │   ├── SkillPage.vue     # 动态参数表单（从 manifest 生成）
│       │   ├── ReportPage.vue    # iframe 渲染 HTML
│       │   ├── HistoryPage.vue   # 报告列表 + 删除
│       │   └── NotFoundPage.vue
│       └── assets/
│           └── main.css
│
├── skills/
│   └── bazi/
│       ├── manifest.json    # id, display_name, version, parameters schema
│       ├── workflow.py      # async run(request) → SkillResponse
│       ├── renderer.py      # HTML 渲染（中国风主题）
│       ├── prompt.md        # 八字分析 Prompt 模板
│       ├── README.md
│       ├── templates/
│       ├── assets/
│       ├── scripts/
│       └── config/
│
└── scripts/
    ├── init_db.py
    └── seed.py
```

### 1.4 开发阶段总览

| Phase | 内容 | 状态 |
|-------|------|:----:|
| **Phase 1** | 项目初始化（目录、FastAPI、Vue3、PostgreSQL、SQLAlchemy、Alembic、Docker） | ✅ |
| **Phase 2** | 接入 Bazi Skill（SkillRuntime、LLM Client、Registry、Loader） | ✅ |
| **Phase 2.5** | 架构优化（async workflow、Provider 抽象、Workflow 缓存、Registry 启动扫描、report_id、统一日志） | ✅ |
| **Phase 3** | 用户与报告系统（注册/登录/JWT/数据库持久化/报告 CRUD） | ✅ |
| **Phase 4** | 前端系统（7 页面、路由守卫、Pinia、动态表单、HTML 渲染） | ✅ |
| **Phase 4.5** | 联调与部署准备（LLM 真实调用、E2E 测试 21/21 通过、问题修复） | ✅ |
| **Phase 5** | 前端测试 + Element Plus 按需导入优化（PRD 未明确，需讨论） | ⏳ |
| **Phase 6** | Docker Compose 一键启动 + Railway 部署 | ⏳ |

### 1.5 下一步计划

**Phase 5（建议）**：前端 Vitest 测试 + Element Plus 按需导入减小打包体积 + UX 细节优化

**Phase 6**：Docker Compose 验证 + PostgreSQL 切换 + Railway 云部署

---

## 二、已完成内容详情

### Phase 1：项目初始化

- ✅ 完整目录结构（backend/ + frontend/ + skills/ + docs/ + scripts/）
- ✅ FastAPI 入口 + CORS + 路由注册
- ✅ Vue3 + Vite + TypeScript + Vue Router + Pinia 骨架
- ✅ PostgreSQL 在 docker-compose.yml 中配置（开发阶段使用 SQLite）
- ✅ SQLAlchemy ORM（Base + SessionLocal + get_db 依赖注入）
- ✅ Alembic 迁移工具初始化
- ✅ Docker Compose 三服务编排（backend + frontend + db）
- ✅ .env.example 环境变量模板
- ✅ .gitignore
- ✅ PRD.md / CLAUDE.md / SKILL_SPEC.md 移至 docs/

### Phase 2：接入 Bazi Skill

- ✅ SkillRegistry：启动时自动扫描 `skills/*/manifest.json` 注册 Skill
- ✅ SkillLoader：importlib 动态加载 Skill workflow.py 模块
- ✅ SkillRuntime：调度 Skill 执行 + Workflow 缓存
- ✅ LLM Client：Provider 抽象层，支持 OpenAI-compatible 格式
- ✅ Bazi Skill：workflow.py（异步入口）、renderer.py（HTML 渲染）、prompt.md（模板）
- ✅ `GET /skill/list` 端点实现
- ✅ `POST /report/generate` 端点实现
- ✅ Platform-Skill 完全解耦（grep 验证：backend/ 零八字关键词）
- ✅ types/skill.py 统一定义 SkillRequest / SkillResponse

### Phase 2.5：架构优化

- ✅ workflow.run() 改为 `async def`，移除 asyncio.run()
- ✅ LLM Provider 抽象层：`BaseLLMProvider` ABC → `OpenAICompatibleProvider`
- ✅ SkillRuntime Workflow 缓存（首次加载后缓存 module）
- ✅ Registry 模块导入时自动 scan()，运行时零 I/O
- ✅ SkillResponse 增加 `report_id` 字段
- ✅ 全模块统一 logging

### Phase 3：用户与报告系统

- ✅ 用户注册 → bcrypt 加密 → JWT 签发（注册即登录）
- ✅ 用户登录 → 验证凭证 → JWT 签发
- ✅ `GET /auth/me` 获取当前用户
- ✅ JWT 鉴权依赖（get_current_user → 查 DB 返回 User 对象）
- ✅ User 模型：id, username, password_hash, created_at
- ✅ Report 模型：id, user_id, skill_id, title, html, metadata(JSON), created_at
- ✅ User ↔ Report 一对多关系
- ✅ Alembic 初始迁移（users + reports 表）
- ✅ `POST /report/generate` → JWT 保护 → 生成 → 保存 DB → 返回 report_id
- ✅ `GET /report/list` → 当前用户所有报告
- ✅ `GET /report/{id}` → 仅自己的报告
- ✅ `DELETE /report/{id}` → 仅自己的报告
- ✅ 跨用户权限隔离（grep 验证）
- ✅ 17/17 单元测试通过

### Phase 4：前端系统

- ✅ 7 个页面：Login, Register, Home, Skill, Report, History, 404
- ✅ Vue Router + auth guard（未登录 → 跳转 /login）
- ✅ Pinia stores：auth（JWT + 用户状态）、skill（Skill 列表）
- ✅ 统一 API 客户端（JWT 自动注入 + 401 拦截跳转）
- ✅ 首页动态获取 Skill 列表，卡片自动展示
- ✅ Skill 页动态生成参数表单（从 manifest.json 的 parameters schema）
- ✅ 报告页 iframe sandbox 渲染 HTML
- ✅ 历史页 Element Plus 表格 + 查看/删除操作
- ✅ Element Plus UI + 响应式布局 + 移动端适配
- ✅ 前端零硬编码 Skill（grep 验证：零 bazi/八字 关键词）
- ✅ TypeScript 类型检查通过（vue-tsc --noEmit 零错误）
- ✅ Vite 生产构建通过

### Phase 4.5：联调与部署准备

- ✅ 配置真实 LLM API Key（DeepSeek）
- ✅ LLM 直连测试通过（200 OK，58 chars 响应）
- ✅ 全链路 E2E 测试：注册 → 登录 → 生成报告(真实LLM) → DB保存 → 查询 → 删除
- ✅ HTML 生成验证：5494~5895 chars，含完整 DOCTYPE + CSS + 中文内容
- ✅ 修复 bcrypt 兼容性问题（移除 passlib，直接用 bcrypt）
- ✅ 修复 datetime.utcnow() 弃用警告
- ✅ 修复 Pydantic Config 弃用警告
- ✅ 21/21 全部测试通过（17 单元 + 4 E2E 含真实 LLM）

---

## 三、当前技术栈

| 层级 | 技术 | 版本 | 说明 |
|------|------|------|------|
| **Backend** | FastAPI | 0.115+ | 异步 Web 框架 |
| | Uvicorn | 0.30+ | ASGI Server |
| | Pydantic | v2 | 数据校验 |
| | Python | 3.12+ | |
| **Frontend** | Vue | 3.5+ | Composition API |
| | Vite | 5.4+ | 构建工具 |
| | TypeScript | 5.6+ | 类型检查 |
| | Element Plus | 2.8+ | UI 组件库 |
| | Pinia | 2.2+ | 状态管理 |
| | Vue Router | 4.4+ | 路由 |
| **Database** | SQLAlchemy | 2.0+ | ORM |
| | Alembic | 1.13+ | 数据库迁移 |
| | SQLite | — | 开发环境（零配置） |
| | PostgreSQL | 16 | 生产环境（Docker Compose） |
| **LLM** | DeepSeek-Chat | — | 当前配置（OpenAI-compatible） |
| | 可切换 | — | OpenAI / Qwen / OpenRouter / vLLM |
| **Auth** | bcrypt | 4.2+ | 密码哈希 |
| | python-jose | 3.3+ | JWT 签发与验证 |
| **部署** | Docker Compose | 3.9 | 三服务编排 |
| | Railway | — | 目标部署平台 |

---

## 四、当前项目规范（核心约束摘要）

### 4.1 PRD.md 核心约束

- 项目定位：AI Structured Report Generation Platform，**不是算命网站**
- 架构：插件化（Plugin），Platform + Skill 分离
- 第一版 Skill：仅 Bazi（命运双鉴），其他显示 "Coming Soon"
- 用户系统：注册 / 登录 / JWT / 安全退出
- 数据库：User + Report 一对多
- API：全部 RESTful — `POST /register` `/login` `/report/generate` `GET /report/list` `/:id` `DELETE /:id`
- MVP：注册、登录、JWT、Bazi Skill、HTML 报告、保存数据库、历史记录、删除、Docker、Railway
- **V1 禁止**：Redis、MQ、微服务、RAG、LangGraph、Multi-Agent、支付、邮箱验证、OAuth、API Key、多模型切换、后台管理
- 开发阶段：Phase 1→6，每阶段停止等待确认
- 扩展：新增 Skill 只需在 `skills/` 下新增目录，无需修改 Platform

### 4.2 CLAUDE.md 核心约束

- 原则：KISS、YAGNI、DRY、SOLID
- **Platform 禁止出现任何业务逻辑**（八字、紫微、简历...）
- **Skill 禁止访问数据库、登录信息、API、JWT**
- 所有 AI 调用统一经过 `llm/client.py`
- 命名：Python snake_case，Vue PascalCase，数据库 snake_case，API RESTful
- 分层：Repository → Service → API
- 密码 bcrypt，JWT FastAPI 官方方案
- 用户只能访问自己的 Report
- 配置全部走 .env
- **禁止**：print()（用 logging）、硬编码、业务层直接 SQL
- 每 Phase 一次 Commit，禁止一次上千行修改
- 未经允许不得重写已有代码

### 4.3 SKILL_SPEC.md 核心约束

- Skill 是 Platform 的最小业务单元
- **Platform 永远不关心 Skill 内部实现**
- **Platform 只调用 `workflow.run(request) → SkillResponse`**
- Skill 目录：`manifest.json`、`workflow.py`、`renderer.py`、`prompt.md`、`README.md`
- manifest.json 字段：`id, display_name, version, author, description, icon, category, entry, output, parameters`
- SkillRequest 字段：`skill_id, user_id, session_id, parameters`
- SkillResponse 字段：`success, title, html, metadata, error`
- workflow.run() 是 Skill 唯一入口
- Skill 不允许抛未处理异常 → 返回 `success=false` + `error`
- 所有 Skill 统一输出 HTML
- Skill 不依赖其他 Skill，不修改 Platform

---

## 五、当前项目架构（调用流程）

### 5.1 平台组件关系

```
Platform (Backend)
│
├── api/           ← REST 端点，无业务逻辑
│   ├── auth.py    → AuthService
│   ├── report.py  → SkillRuntime + ReportService
│   └── skill.py   → SkillRegistry
│
├── services/      ← 业务逻辑 + 数据库操作
│   ├── auth_service.py
│   └── report_service.py
│
├── runtime/       ← Skill 调度引擎
│   └── skill_runtime.py  → SkillLoader + Workflow Cache
│
├── registry/      ← Skill 发现与管理
│   ├── skill_registry.py  → 扫描 manifest.json
│   └── loader.py          → importlib 动态加载 workflow.py
│
├── llm/           ← LLM 调用抽象
│   ├── base.py    → Provider ABC
│   ├── client.py  → Facade
│   └── providers/ → 具体实现 (OpenAI-compatible...)
│
├── types/         ← 全项目统一类型
│   └── skill.py   → SkillRequest / SkillResponse (dataclass)
│
└── models/        ← ORM 模型
    ├── user.py
    └── report.py

Skills (独立目录，位于项目根)
│
└── skills/
    └── bazi/
        ├── manifest.json    ← Registry 读取
        ├── workflow.py      ← Runtime 调用 entry
        ├── renderer.py      ← 生成 HTML
        └── prompt.md        ← AI Prompt 模板
```

### 5.2 完整调用流程

```
POST /report/generate   { skill_id: "bazi", parameters: {...} }
    │
    ▼
api/report.py
    ├── get_current_user()  → JWT 鉴权 → User 对象
    ├── SkillRequest(skill_id, user_id, session_id, parameters)
    │
    ▼
runtime/skill_runtime.py  →  skill_runtime.run(request)
    ├── 缓存命中？→ 直接用
    ├── 缓存未命中 → loader.load_workflow("bazi")
    │       └── importlib 动态加载 skills/bazi/workflow.py
    │       └── 存入缓存
    ├── await workflow.run(request)
    │       │
    │       ▼
    │   skills/bazi/workflow.py
    │       ├── 1. _validate_params()
    │       ├── 2. _load_prompt() → prompt.md
    │       ├── 3. _fill_template() → 填入参数
    │       ├── 4. await llm_client.generate(prompt, system)
    │       │       │
    │       │       ▼
    │       │   llm/client.py (Facade)
    │       │       └── OpenAICompatibleProvider.generate()
    │       │           └── POST https://api.deepseek.com/v1/chat/completions
    │       │
    │       ├── 5. renderer.render(ai_content) → HTML
    │       └── 6. return SkillResponse(success=True, title, html, metadata)
    │
    ▼
api/report.py (续)
    ├── if success:
    │       report_service.create(db, user_id, skill_id, result) → DB
    │       report_id = report.id
    └── return SkillResponse(report_id, success, title, html, metadata)
```

### 5.3 Platform ↔ Skill 边界

```
Platform 负责：                    Skill 负责：
┌─────────────────────┐           ┌─────────────────────┐
│ 用户系统             │           │ Prompt (prompt.md)   │
│ JWT 鉴权             │           │ Workflow (业务逻辑)  │
│ REST API             │           │ AI 调用 (via client)│
│ 数据库存储           │           │ HTML 生成 (renderer) │
│ Skill 注册与调度     │           │ 参数校验             │
│ HTML 展示            │           │                      │
│ Docker / Railway     │           │                      │
└─────────────────────┘           └─────────────────────┘
         │                                  │
         └──── SkillRequest ────→ SkillResponse
              (唯一通信协议)
```

---

## 六、当前待完成事项（TODO）

### 6.1 必须完成

| # | 事项 | Phase | 说明 |
|---|------|:-----:|------|
| 1 | Docker Compose 端到端验证 | 6 | `docker compose up` 一键启动全栈 |
| 2 | PostgreSQL 切换 + 数据迁移 | 6 | 当前开发 SQLite，生产需 PG |
| 3 | Railway 云部署 | 6 | 目标部署平台 |
| 4 | 生产环境 SECRET_KEY 更换 | 6 | 当前为开发密钥 |

### 6.2 建议完成

| # | 事项 | 说明 |
|---|------|------|
| 1 | Element Plus 按需导入 | 当前全量导入，打包 ~1MB，可减小至 ~300KB |
| 2 | 前端 Vitest 测试 | 目前仅后端有 pytest 测试 |
| 3 | 报告分页 | `GET /report/list?page=1&size=20` |
| 4 | 前端 Loading/Error 状态优化 | 当前基本覆盖，可加强边界情况 |
| 5 | Skill manifest parameters 支持更多类型 | 当前支持 number/string/select |

### 6.3 以后优化

| # | 事项 | 说明 |
|---|------|------|
| 1 | Anthropic Provider | 新增 `llm/providers/anthropic.py` |
| 2 | 多模型切换 UI | 用户可选模型 |
| 3 | 报告导出 PDF | Platform 层实现 |
| 4 | 深色模式 | CSS 变量切换 |
| 5 | 国际化 i18n | vue-i18n |
| 6 | Skill 热加载 | 不重启后端加载新 Skill |

---

## 七、当前已知问题

| # | 问题 | 影响 | 解决方案 |
|---|------|------|----------|
| 1 | **SQLite 开发，PostgreSQL 未实际连接** | 仅开发环境 | Docker Compose 已配置 PG，Phase 6 切换 |
| 2 | **psycopg2 在 Windows 上未安装** | Windows 开发无法连 PG | Docker 内构建无此问题 |
| 3 | **LLM API Key 在 backend/.env 中** | 仅本地有效 | .gitignore 已排除，不会提交 |
| 4 | **前端无自动化测试** | 质量保障不完整 | Phase 5 可加 Vitest |
| 5 | **Element Plus 全量导入** | 首屏加载 ~1MB | Phase 5 按需导入 |
| 6 | **Railway 部署未执行** | 未上线 | Phase 6 |
| 7 | **Docker Compose 未端到端验证** | 可能需调试 | Phase 6 |
| 8 | **Starlette TestClient httpx 弃用警告** | 无实际影响 | 等待上游更新 |

---

## 八、新对话启动提示词

**将以下内容复制到新的 Claude Code 对话中：**

```
你现在接手 InsightForge-AI 项目的开发。

## 必须阅读的文档

请按顺序严格阅读以下文档：

1. docs/PRD.md          — 产品需求与功能定义
2. docs/CLAUDE.md        — 开发规范、架构约束、禁止事项
3. docs/SKILL_SPEC.md    — Skill 插件协议规范
4. docs/HANDOFF.md       — 项目交接文档（当前状态）

以上四份文档是项目的唯一开发规范，必须完全遵守。

## 项目当前状态

- Phase 1~4.5 已完成
- 21/21 测试全部通过（含真实 LLM 端到端测试）
- LLM 已配置 DeepSeek API，调用正常
- 前端 7 页面构建通过，vue-tsc 零错误
- 后端完整业务闭环：注册 → 登录 → 生成报告 → 数据库保存 → 历史管理

## 开发原则（不可违反）

1. Platform 与 Skill 完全解耦
2. Platform 不允许出现任何业务逻辑（八字、紫微、简历等）
3. Skill 不允许访问数据库、JWT、API
4. 所有 AI 请求统一经过 llm/client.py
5. 新增 Skill 只需在 skills/ 下新增目录
6. 未经允许不得重写已有代码
7. 每完成一个 Phase 立即停止，等待确认
8. 保持 KISS 原则，不过度设计
9. 所有数据操作放到 Service 层
10. API 层不写业务逻辑

## 当前后端 .env 配置

LLM_PROVIDER=openai_compatible
LLM_BASE_URL=https://api.deepseek.com
LLM_API_KEY=<YOUR_DEEPSEEK_API_KEY>
LLM_MODEL=deepseek-chat
DATABASE_URL=sqlite:///./insightforge.db

## 启动方式

Backend:  cd backend && uvicorn app.main:app --reload --port 8000
Frontend: cd frontend && npm run dev
Tests:    cd backend && python -m pytest tests/ -v

## 下一步

从 Phase 5 或 Phase 6 开始，请阅读 HANDOFF.md 了解当前进度后向我确认计划。
```

---

**文档结束。保存于 docs/HANDOFF.md**
