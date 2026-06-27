"""Bazi Skill — HTML 渲染器

负责将 AI 分析结果渲染为最终 HTML。
Renderer 不负责 AI 调用、不负责数据存储。
"""

import re


def _md_to_html(md_text: str) -> str:
    """简易 Markdown → HTML 转换"""
    # 标题 ### → <h3>
    md_text = re.sub(r"^### (.+)$", r"<h3>\1</h3>", md_text, flags=re.MULTILINE)
    # 标题 ## → <h2>
    md_text = re.sub(r"^## (.+)$", r"<h2>\1</h2>", md_text, flags=re.MULTILINE)
    # 标题 # → <h1>
    md_text = re.sub(r"^# (.+)$", r"<h1>\1</h1>", md_text, flags=re.MULTILINE)
    # 粗体 **text**
    md_text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", md_text)
    # 换行保留
    md_text = re.sub(r"\n\n", "</p><p>", md_text)
    md_text = f"<p>{md_text}</p>"
    md_text = md_text.replace("<p></p>", "<br>")
    return md_text


def render(title: str, params: dict, ai_content: str) -> str:
    """生成最终 HTML 报告"""
    body = _md_to_html(ai_content)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif;
            background: linear-gradient(135deg, #f5f0eb 0%, #e8e0d5 100%);
            min-height: 100vh;
            color: #3d3226;
            line-height: 1.8;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        .header {{
            text-align: center;
            padding: 48px 20px;
            background: linear-gradient(135deg, #8b4513 0%, #a0522d 50%, #6b3410 100%);
            color: #f5e6d3;
            border-radius: 16px;
            margin-bottom: 32px;
            box-shadow: 0 8px 32px rgba(107, 52, 16, 0.3);
        }}
        .header h1 {{
            font-size: 2.2em;
            letter-spacing: 0.08em;
            margin-bottom: 8px;
        }}
        .header .subtitle {{
            font-size: 0.95em;
            opacity: 0.8;
        }}
        .content {{
            background: #fffef9;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 2px 16px rgba(0,0,0,0.06);
        }}
        .content h1 {{ font-size: 1.6em; color: #8b4513; margin: 32px 0 16px; border-bottom: 2px solid #e8d5c4; padding-bottom: 8px; }}
        .content h2 {{ font-size: 1.3em; color: #a0522d; margin: 28px 0 14px; }}
        .content h3 {{ font-size: 1.1em; color: #6b3410; margin: 20px 0 10px; }}
        .content p {{ margin: 10px 0; text-indent: 1em; }}
        .content strong {{ color: #8b4513; }}
        .footer {{
            text-align: center;
            margin-top: 32px;
            color: #a09080;
            font-size: 0.85em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔮 {title}</h1>
            <div class="subtitle">
                出生于 {params.get('year')}年{params.get('month')}月{params.get('day')}日 {params.get('hour')}时 · {params.get('gender')}
            </div>
        </div>
        <div class="content">
            {body}
        </div>
        <div class="footer">
            <p>Powered by InsightForge AI · 仅供参考</p>
        </div>
    </div>
</body>
</html>"""
    return html
