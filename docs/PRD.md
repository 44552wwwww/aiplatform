# PRD（Product Requirements Document）

# InsightForge AI

副标题：

AI Structured Report Generation Platform

版本：

v1.0

---

# 一、项目简介

## 1.1 项目背景

随着大语言模型的发展，越来越多的 AI 应用开始围绕"输入数据 → AI 分析 → 输出报告"这一模式展开。

例如：

- 命理分析
- 简历分析
- 职业规划
- 心理测评
- 学习规划
- 商业分析

这些业务虽然内容不同，但本质工作流程一致。

因此，本项目希望实现一个可扩展的 AI 报告生成平台。

平台负责：

- 用户系统
- 报告管理
- AI 调用
- 数据库存储
- HTML 展示

具体业务通过 Skill 插件扩展。

---

# 二、项目定位

本项目不是算命网站。

而是：

> AI Structured Report Generation Platform

目前仅实现：

Bazi Skill（命运双鉴）

未来支持：

- Resume Skill
- Career Skill
- Study Skill
- Psychology Skill

任何新业务都应该通过新增 Skill 完成，而不是修改平台。

---

# 三、项目目标

本项目主要用于：

- AI 全栈开发学习
- AI 全栈开发实习作品集
- 展示现代 AI Web 应用开发能力

目标：

构建一个真正可以部署上线的 AI Web 应用。

---

# 四、目标用户

第一阶段：

普通用户。

用户可以：

- 注册
- 登录
- 生成 AI 报告
- 查看历史报告

---

# 五、产品功能

## 用户系统

支持：

- 注册
- 登录
- JWT 登录状态
- 安全退出

---

## AI 报告

用户：

选择 Skill

↓

填写数据

↓

生成报告

↓

查看 HTML

↓

保存历史

↓

删除历史

---

## 我的报告

用户可以：

查看：

所有历史报告。

支持：

- 查看
- 删除

---

# 六、Skill

第一版：

仅提供：

命运双鉴（八字+紫微）

首页展示：

```
命运双鉴

Coming Soon

Coming Soon
```

以后：

直接增加新的 Skill。

---

# 七、页面设计

## 首页

展示：

平台介绍。

Skill 列表。

---

## 登录

用户名

密码

---

## 注册

用户名

密码

---

## Skill 页面

填写参数。

点击生成。

显示生成状态。

---

## 报告详情

直接展示 HTML。

---

## 我的报告

列表：

标题

创建时间

查看

删除

---

# 八、工作流程

用户

↓

登录

↓

首页

↓

选择 Skill

↓

填写参数

↓

提交

↓

Skill 生成 HTML

↓

保存数据库

↓

网页展示

↓

历史记录

---

# 九、数据库

第一版：

User

Report

即可。

用户与 Report 建立一对多关系。

一个用户拥有多个报告。

---

# 十、API

用户：

POST /register

POST /login

报告：

POST /report/generate

GET /report/list

GET /report/{id}

DELETE /report/{id}

全部采用 RESTful。

---

# 十一、部署

项目最终部署到 Railway。

数据库使用 PostgreSQL。

所有用户数据必须持久化。

支持 Docker 部署。

---

# 十二、MVP

第一版必须完成：

✅ 注册

✅ 登录

✅ JWT

✅ Bazi Skill

✅ HTML 报告

✅ 保存数据库

✅ 历史记录

✅ 删除报告

✅ Docker

✅ Railway

---

# 十三、非目标

第一版不实现：

- Redis
- MQ
- 微服务
- RAG
- LangGraph
- Multi-Agent
- 支付
- 邮箱验证
- 第三方登录
- 用户 API Key
- 多模型切换
- 后台管理

保持简单。

---

# 十四、扩展性要求

平台必须支持：

新增一个 Skill。

无需修改：

- 用户系统
- 数据库
- API
- 前端框架
- 平台核心

仅新增：

```
skills/

    new_skill/
```

即可完成扩展。

---

# 十五、项目原则

项目采用：

插件化（Plugin）架构。

平台负责：

- 用户
- 数据
- AI 调度
- 报告管理

Skill 负责：

- 业务逻辑
- AI 分析
- HTML 报告

平台与 Skill 解耦。

所有 Skill 统一遵循 Skill Contract。

---

# 十六、开发阶段

Phase 1

项目初始化。

完成：

- 项目结构
- FastAPI
- Vue
- PostgreSQL
- Docker

---

Phase 2

接入现有 Bazi Skill。

---

Phase 3

完成用户系统。

---

Phase 4

完成报告存储。

---

Phase 5

完成前端页面。

---

Phase 6

完成部署。

每完成一个阶段：

停止开发。

等待确认。

不得自动继续下一阶段。

---

# 十七、最终目标

完成一个真正可以部署上线的 AI 个性化报告生成平台。

平台支持：

- 用户注册
- 用户登录
- AI 报告生成
- HTML 展示
- 历史管理

未来新增任何 AI 能力，都应通过新增 Skill 实现，而无需修改平台核心。