# Resume Insight — 简历洞察

基于 AI 的简历分析报告生成器。

## Skill 功能

用户输入**求职岗位**和**简历内容**，AI 自动生成专业分析报告，包括：

- 综合评分（百分制）
- 岗位匹配度分析
- 优势分析
- 不足分析
- 缺失技能
- 简历优化建议
- 面试官可能追问的问题
- 综合建议

## 输入

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| job | text | 是 | 求职岗位名称 |
| resume | textarea | 是 | 完整简历内容 |

## 输出

HTML 格式的专业简历分析报告。

## 目录结构

```
skills/resume/
├── manifest.json      # Skill 元数据 + 参数定义
├── workflow.py        # 工作流入口（参数校验 → Prompt → LLM → Renderer）
├── prompt.md          # AI Prompt 模板
├── renderer.py        # HTML 渲染器
└── README.md          # 本文件
```

## 调用流程

```
POST /report/generate { skill_id: "resume", parameters: { job, resume } }
  → SkillRuntime.run()
    → skill_loader.load_workflow("resume")
    → workflow.run(request)
      → _validate_params()      # 校验 job + resume
      → _load_prompt()          # 读取 prompt.md
      → _extract_system_user()  # 分离系统指令 + 用户提示
      → _fill_template()        # 用参数填充 {job} {resume}
      → llm_client.generate()   # 调用 AI
      → render()                # 生成 HTML
    → SkillResponse { html }
  → report_service.create()     # 存入数据库
  → 返回 report_id
```

## 架构说明

本 Skill 100% 遵循命运双鉴（bazi）Skill 的架构模式。

新增本 Skill 不需要修改任何平台代码（Registry / Runtime / API / Database / Router 全部零修改）。
