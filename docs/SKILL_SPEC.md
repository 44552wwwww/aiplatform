# SKILL_SPEC.md

# InsightForge Skill Specification

Version: 1.0

---

# 一、Skill 的定义

Skill 是 InsightForge AI 的最小业务单元。

一个 Skill 代表一种完整的 AI 能力。

例如：

- 八字分析
- 简历分析
- 职业规划
- 心理测评
- PPT生成
- 商业分析

平台只负责：

- 用户
- 权限
- 数据库
- AI调度
- 报告管理

Skill 负责：

- 数据处理
- Prompt
- AI分析
- HTML生成

Platform 永远不关心 Skill 的内部实现。

---

# 二、Skill 生命周期

Platform

↓

Skill Registry

↓

加载 Skill

↓

创建 SkillRequest

↓

workflow.run(request)

↓

SkillResponse

↓

Platform

↓

保存数据库

↓

网页展示

Platform 永远不会访问 Skill 内部代码。

Platform 只调用：

workflow.run()

---

# 三、Skill 标准目录

每一个 Skill 必须遵循统一目录。

```

skills/

    bazi/

        manifest.json

        workflow.py

        renderer.py

        prompt.md

        README.md

        templates/

        assets/

        scripts/

```

其中：

manifest.json

描述 Skill。

workflow.py

Skill 唯一入口。

renderer.py

负责 HTML。

prompt.md

Prompt。

README.md

Skill 说明。

Platform 只依赖：

manifest

workflow

其它目录完全属于 Skill。

---

# 四、manifest.json

每个 Skill 必须提供：

```json
{
    "id":"bazi",

    "name":"命运双鉴",

    "version":"1.0.0",

    "author":"Your Name",

    "description":"八字与紫微斗数分析",

    "entry":"workflow.py",

    "output":"html"
}
```

字段说明：

id

Skill 唯一标识。

name

显示名称。

version

版本。

entry

入口文件。

output

目前固定：

html。

---

# 五、SkillRequest

Platform 调用 Skill 时：

统一传入：

```python
class SkillRequest:

    skill_id:str

    user_id:int

    session_id:str

    parameters:dict
```

例如：

```json
{
    "skill_id":"bazi",

    "user_id":1,

    "session_id":"uuid",

    "parameters":{

        "year":2002,

        "month":5,

        "day":18,

        "hour":14,

        "gender":"男"

    }

}
```

Skill 不允许：

访问数据库。

Skill 不允许：

读取登录信息。

Skill 所有输入：

全部来自：

SkillRequest。

---

# 六、SkillResponse

Skill 必须返回：

```python
class SkillResponse:

    success:bool

    title:str

    html:str

    metadata:dict

    error:str|None
```

示例：

```json
{
    "success":true,

    "title":"命运双鉴",

    "html":"<html>......</html>",

    "metadata":{

        "skill":"bazi",

        "version":"1.0.0"

    },

    "error":null
}
```

Platform：

统一保存：

html。

Platform：

不会解析：

html。

---

# 七、workflow.py

每个 Skill 必须提供：

```python
def run(request:SkillRequest)->SkillResponse:
```

Platform：

永远调用：

```python
workflow.run(request)
```

禁止：

Platform 调用：

任何其它 Python 文件。

---

# 八、Workflow 职责

workflow.py：

负责：

1.

读取参数。

2.

调用内部模块。

3.

调用 Prompt。

4.

调用 AI。

5.

调用 Renderer。

6.

返回：

SkillResponse。

Workflow 不负责：

数据库。

登录。

API。

网页。

---

# 九、Renderer

Renderer：

负责：

最终 HTML。

例如：

```python
html=renderer.render(...)
```

Renderer 不负责：

AI。

Prompt。

数据库。

---

# 十、Prompt

Prompt：

统一放：

prompt.md

Prompt 可以：

引用模板。

引用配置。

引用脚本。

Prompt 不直接访问数据库。

---

# 十一、Metadata

metadata：

用于：

记录：

Skill 信息。

例如：

```json
{
    "skill":"bazi",

    "version":"1.0.0",

    "model":"deepseek-chat",

    "duration":12.3
}
```

Platform：

可以保存。

但：

不参与业务。

---

# 十二、HTML

所有 Skill：

统一输出：

HTML。

原因：

Platform：

无需关心：

Markdown。

PDF。

JSON。

网页直接展示。

以后：

导出 PDF。

也由 Platform 完成。

Skill：

只负责 HTML。

---

# 十三、错误处理

发生错误：

返回：

```json
{
    "success":false,

    "title":"",

    "html":"",

    "metadata":{},

    "error":"错误信息"
}
```

禁止：

抛出未处理异常。

Platform：

统一处理错误。

---

# 十四、Skill Version

每个 Skill：

必须维护：

version。

例如：

```
1.0.0
```

以后：

升级：

```
1.1.0

2.0.0
```

Platform：

读取：

manifest。

---

# 十五、兼容性

Platform：

只依赖：

SkillRequest。

SkillResponse。

workflow.run()

其它实现：

全部允许自由修改。

因此：

Skill 可以：

完全重构内部。

Platform：

无需修改。

---

# 十六、新增 Skill

新增 Skill：

只需要：

```
skills/

    new_skill/
```

完成：

manifest。

workflow。

renderer。

prompt。

即可。

Platform：

自动扫描。

自动注册。

无需修改源码。

---

# 十七、Skill 开发原则

每个 Skill：

必须：

低耦合。

高内聚。

独立运行。

不得依赖其它 Skill。

不得修改 Platform。

---

# 十八、Platform 与 Skill 的边界

Platform 负责：

✓ 用户

✓ JWT

✓ API

✓ 数据库

✓ 调度

✓ HTML展示

✓ Docker

✓ Railway

Skill 负责：

✓ Prompt

✓ Workflow

✓ AI分析

✓ HTML生成

✓ Validator

✓ Renderer

两者禁止相互侵入。

---

# 十九、最佳实践

推荐：

Workflow

↓

Service

↓

Renderer

↓

Response

不要：

Workflow

↓

直接拼接 HTML。

保持模块清晰。

---

# 二十、最终原则

Platform 永远保持稳定。

Skill 可以无限扩展。

新增任何 AI 能力：

都应该通过新增 Skill 实现。

而不是修改 Platform。

InsightForge 的核心竞争力不是某一个 Skill。

而是：

统一的平台能力 + 可扩展的 Skill 插件体系。