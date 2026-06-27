# CLAUDE.md

# InsightForge AI

> Plugin-based AI Structured Report Generation Platform

---

# 一、项目定位

## 项目目标

InsightForge AI 是一个基于插件（Plugin）的 AI 个性化报告生成平台。

本项目不是算命网站。

命理分析（Bazi）只是第一个 Skill。

未来平台可以扩展：

- 简历分析
- 职业规划
- 学习规划
- 心理测评
- PPT生成
- 商业分析
- 更多 AI 报告

平台负责基础能力。

Skill 负责业务能力。

平台永远保持通用。

---

# 二、开发目标

本项目主要用于：

- AI 全栈开发学习
- AI 全栈开发作品集
- AI 全栈开发实习求职

目标：

构建一个真正可以部署上线的 AI Web 应用。

而不是 Demo。

---

# 三、开发原则

始终遵循：

## KISS

Keep It Simple.

保持简单。

不要过度设计。

---

## YAGNI

You Aren't Gonna Need It.

不要为了未来可能出现的需求增加复杂度。

---

## DRY

Don't Repeat Yourself.

避免重复代码。

公共逻辑统一抽象。

---

## SOLID

遵循基本的软件设计原则。

保持模块独立。

---

## 优先原则

优先保证：

可维护性

可扩展性

可读性

而不是：

炫技。

---

# 四、整体架构

Platform

↓

Skill Registry

↓

Skill Runtime

↓

Skill

↓

LLM Service

↓

HTML Report

↓

Database

Platform 永远不知道 Skill 内部如何实现。

Platform 只负责：

调度。

---

# 五、Platform 职责

Platform 负责：

- 用户系统
- JWT
- REST API
- Skill 注册
- Skill 调度
- LLM Service
- 数据库存储
- HTML 展示
- 历史记录
- Docker
- Railway

Platform 不允许出现任何业务逻辑。

例如：

不得出现：

八字

紫微

简历

职业规划

这些业务代码。

---

# 六、Skill 职责

所有业务能力必须封装成 Skill。

例如：

skills/

    bazi/

    resume/

    career/

    psychology/

Skill 负责：

- Workflow
- Prompt
- AI分析
- HTML生成
- Validator
- Renderer
- Metadata

Skill 不负责：

登录

数据库

API

JWT

网页

Docker

这些全部属于 Platform。

---

# 七、Skill Registry

平台启动时：

自动扫描：

skills/*

读取：

manifest.json

自动注册。

禁止：

手动写死：

if skill == "bazi"

以后新增：

skills/new_skill

平台无需修改即可识别。

---

# 八、Skill Runtime

Platform 调用：

Skill Runtime

Skill Runtime：

读取 Skill

↓

构造 SkillRequest

↓

调用：

workflow.run()

↓

获得：

SkillResponse

↓

返回 Platform

Platform 不直接调用 Skill 内部任何文件。

---

# 九、LLM Service

所有 Skill 必须统一调用：

services/llm_service.py

禁止：

Skill 内：

直接调用 OpenAI SDK。

统一：

LLMService.generate()

以后如果：

更换模型

增加Provider

增加缓存

Skill 无需修改。

---

# 十、数据库

数据库仅负责：

User

Report

后续可增加：

SkillLog

AuditLog

目前不需要。

---

# 十一、Report

Platform 保存：

Skill 返回的 HTML。

Platform 不关心 HTML 如何生成。

Platform 不解析 HTML。

Platform 不修改 HTML。

直接保存。

直接展示。

---

# 十二、目录规范

backend/

    api/

    core/

    database/

    models/

    schemas/

    services/

    skills/

    utils/

frontend/

docs/

docker/

目录职责必须单一。

不得混乱。

---

# 十三、Skill目录规范

每个 Skill：

skills/

    xxx/

        manifest.json

        workflow.py

        prompt.md

        renderer.py

        README.md

允许增加：

templates/

assets/

styles/

scripts/

Platform 不读取这些目录。

Platform 只读取：

manifest

workflow

---

# 十四、命名规范

统一采用：

snake_case

Python：

snake_case

Vue：

PascalCase

数据库：

snake_case

API：

RESTful

---

# 十五、REST API

统一：

GET

POST

PUT

DELETE

禁止：

/getUser

/createReport

统一：

/report

/report/{id}

---

# 十六、数据库规范

使用：

SQLAlchemy ORM

禁止：

业务层直接 SQL。

统一：

Repository

Service

API

分层。

---

# 十七、前端规范

Vue3

Composition API

TypeScript

Pinia

统一：

API调用：

services/api.ts

不要：

页面直接 axios。

---

# 十八、错误处理

统一：

HTTPException

统一返回：

错误码

错误信息

不要：

print。

不要：

裸异常。

---

# 十九、日志

统一：

logging

不要：

print()

生产环境：

禁止 print。

---

# 二十、配置

所有配置：

.env

例如：

DATABASE_URL

OPENAI_API_KEY

BASE_URL

MODEL_NAME

禁止：

硬编码。

---

# 二十一、安全

密码：

bcrypt

JWT：

FastAPI官方方案

用户：

只能访问自己的 Report。

任何查询必须校验 user_id。

---

# 二十二、Docker

必须支持：

docker compose up

即可运行。

开发环境：

Docker。

生产：

Railway。

---

# 二十三、Railway

最终部署：

Frontend

↓

Backend

↓

PostgreSQL

所有数据必须持久化。

重新部署不得丢失数据。

---

# 二十四、Git

每完成一个阶段：

一次 Commit。

Commit 尽量小。

禁止：

一次 Commit 上千行修改。

---

# 二十五、开发流程

必须严格按照 Phase 开发。

Phase 1

项目初始化。

停止。

等待确认。

Phase 2

接入 Bazi Skill。

停止。

等待确认。

Phase 3

用户系统。

停止。

等待确认。

Phase 4

数据库。

停止。

等待确认。

Phase 5

前端。

停止。

等待确认。

Phase 6

部署。

停止。

等待确认。

未经确认不得继续。

---

# 二十六、重构原则

未经允许：

不得：

重写已有代码。

已有 Skill：

优先：

重构

封装

解耦

不要：

推倒重写。

如果必须修改：

先说明原因。

等待确认。

---

# 二十七、代码原则

优先：

低耦合

高内聚

模块化

统一接口

避免重复

不要：

为了优雅而复杂。

---

# 二十八、禁止事项

不要：

- 引入微服务
- 引入Redis
- 引入MQ
- 引入RAG
- 引入LangGraph
- 引入Multi-Agent
- 引入支付
- 引入OAuth
- 引入邮箱验证
- 引入后台管理
- 引入用户API Key
- 引入多模型切换

这些都属于 V2。

V1 保持简单。

---

# 二十九、Claude Code 工作原则

每次开发：

1.

先阅读：

PRD.md

CLAUDE.md

SKILL_SPEC.md

2.

理解当前 Phase。

3.

只完成当前任务。

4.

完成立即停止。

5.

输出：

- 修改内容
- 新增文件
- 修改原因
- 下一阶段建议

6.

等待用户确认。

不得自动进入下一阶段。

---

# 三十、最终目标

完成一个真正可以部署到 Railway 的：

Plugin-based AI Structured Report Generation Platform。

平台：

负责：

用户

权限

数据库

调度

Skill：

负责：

AI能力

HTML报告

未来新增任何 AI 能力，都应该通过新增 Skill 实现，而无需修改 Platform 核心。