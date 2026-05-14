#!/usr/bin/env python3
import json
import os
from datetime import datetime

DOCS_DIR = 'docs'

def load_history():
    history_file = f'{DOCS_DIR}/history.json'
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            return json.load(f)
    return []

def generate_html():
    history = load_history()
    last_update = history[0] if history else None
    
    html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Proxy</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        h1 {{
            color: #667eea;
            margin-bottom: 10px;
        }}
        .status {{
            display: inline-block;
            padding: 5px 15px;
            background: #10b981;
            color: white;
            border-radius: 20px;
            font-size: 14px;
        }}
        .content-frame {{
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        iframe {{
            width: 100%;
            height: 80vh;
            border: none;
        }}
        .controls {{
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .input-group {{
            display: flex;
            gap: 10px;
        }}
        input {{
            flex: 1;
            padding: 12px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            font-size: 16px;
        }}
        button {{
            padding: 12px 30px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        }}
        button:hover {{
            background: #5568d3;
        }}
        .info {{
            margin-top: 15px;
            padding: 15px;
            background: #f3f4f6;
            border-radius: 8px;
            font-size: 14px;
        }}
        .history {{
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            margin-top: 20px;
        }}
        .history-item {{
            padding: 10px;
            border-bottom: 1px solid #e5e7eb;
        }}
        .history-item:last-child {{
            border-bottom: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌐 Web Proxy</h1>
            <span class="status">● فعال</span>
            {f'<p style="margin-top: 10px; color: #6b7280;">آخرین بروزرسانی: {last_update["timestamp"][:19]}</p>' if last_update else ''}
        </div>

        <div class="controls">
            <form action="https://github.com/{os.environ.get('GITHUB_REPOSITORY', 'USER/REPO')}/actions/workflows/fetch.yml" method="get" target="_blank">
                <div class="input-group">
                    <input type="text" id="urlInput" placeholder="https://example.com" value="{last_update['url'] if last_update else ''}">
                    <button type="button" onclick="updateURL()">تغییر سایت</button>
                </div>
            </form>
            <div class="info">
                <strong>نحوه استفاده:</strong>
                <ol style="margin-right: 20px; margin-top: 10px;">
                    <li>URL مورد نظر را وارد کنید</li>
                    <li>روی "تغییر سایت" کلیک کنید</li>
                    <li>در صفحه GitHub Actions روی "Run workflow" کلیک کنید</li>
                    <li>URL را در فیلد وارد کرده و اجرا کنید</li>
                    <li>بعد از 1-2 دقیقه صفحه را رفرش کنید</li>
                </ol>
            </div>
        </div>

        <div class="content-frame">
            <iframe src="content.html" title="Proxied Content"></iframe>
        </div>

        <div class="history">
            <h3>📜 تاریخچه</h3>
            {''.join([f'<div class="history-item">🔗 {item["url"]}<br><small>{item["timestamp"][:19]} - {item["status"]}</small></div>' for item in history[:10]])}
        </div>
    </div>

    <script>
        function updateURL() {{
            const url = document.getElementById('urlInput').value;
            if (!url) {{
                alert('لطفاً یک URL وارد کنید');
                return;
            }}
            alert('URL کپی شد. حالا به صفحه GitHub Actions بروید و workflow را اجرا کنید.');
            navigator.clipboard.writeText(url);
            window.open('https://github.com/{os.environ.get('GITHUB_REPOSITORY', 'USER/REPO')}/actions/workflows/fetch.yml', '_blank');
        }}
    </script>
</body>
</html>"""
    
    with open(f'{DOCS_DIR}/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ Index generated")

if __name__ == '__main__':
    generate_html()
