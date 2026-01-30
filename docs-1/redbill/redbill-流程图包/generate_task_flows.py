#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
红单定时任务流程图可视化生成脚本
将 Mermaid 图转换为更易读的流程图（使用 graphviz）
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple
import subprocess
import json

# 配置
REDBILL_DIR = r"c:\Users\DEVTrump\projects\docs-1\redbill"
OUTPUT_DIR = REDBILL_DIR
TASKS = {
    "01": {
        "name": "AI推单任务",
        "mermaid": "task-01-ai-pushorder.mmd",
        "time": "21:00:00",
        "description": "根据未来2天内即将开赛的体育赛事生成单关推单"
    },
    "02": {
        "name": "AI补救推单任务",
        "mermaid": "task-02-repair-pushorder.mmd",
        "time": "23:00:00",
        "description": "如果21点推单任务失败，则进行补救"
    },
    "03": {
        "name": "AI补单任务",
        "mermaid": "task-03-restock-pushorder.mmd",
        "time": "00:00:01",
        "description": "为针对特定联赛的推单用户补充推单"
    },
    "04": {
        "name": "月度用户火标志设置",
        "mermaid": "task-04-user-fire.mmd",
        "time": "每月5日 00:00:00",
        "description": "每月初重置推单用户的火标志和统计数据"
    },
    "05": {
        "name": "真实玩家推单任务",
        "mermaid": "task-05-real-pushorder.mmd",
        "time": "20:00:00",
        "description": "基于真实玩家历史注单数据生成推单（半AI模式）"
    }
}

class TaskFlowGenerator:
    """流程图生成器"""
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.mermaid_to_graphviz_map = {}
        
    def generate_graphviz_dot(self, task_id: str, task_info: Dict) -> str:
        """生成 Graphviz DOT 格式的流程图"""
        
        task_name = task_info["name"]
        task_time = task_info["time"]
        task_desc = task_info["description"]
        
        dot_content = f"""
digraph G {{
    rankdir=TD;
    bgcolor="white";
    node [shape=box, style="rounded,filled", fillcolor=white, fontname="Microsoft YaHei", fontsize=10];
    edge [fontname="Microsoft YaHei", fontsize=9];
    
    // 标题信息
    title [label="{task_id}. {task_name}\\n{task_time}\\n{task_desc}", 
           shape=box, style="filled", fillcolor="#4CAF50", fontcolor=white, fontsize=12, fontweight=bold];
    
    // 定义节点和边
"""
        return dot_content
        
    def parse_mermaid_to_graphviz(self, mermaid_file: str) -> str:
        """解析 Mermaid 文件并转换为 Graphviz DOT"""
        
        try:
            with open(mermaid_file, 'r', encoding='utf-8') as f:
                mermaid_content = f.read()
            
            # 简单的转换逻辑
            # 这里可以添加更复杂的解析逻辑
            return mermaid_content
            
        except Exception as e:
            print(f"❌ 读取文件失败: {mermaid_file}")
            print(f"   错误: {e}")
            return ""
    
    def generate_html_preview(self, task_id: str, task_info: Dict) -> str:
        """生成 HTML 预览页面"""
        
        task_name = task_info["name"]
        task_time = task_info["time"]
        task_desc = task_info["description"]
        mermaid_file = task_info["mermaid"]
        
        mermaid_path = os.path.join(self.output_dir, mermaid_file)
        
        try:
            with open(mermaid_path, 'r', encoding='utf-8') as f:
                mermaid_graph = f.read()
        except:
            mermaid_graph = "graph TD\\n    A[读取失败]"
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{task_id}. {task_name}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: "Microsoft YaHei", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        
        .header .task-id {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 20px;
            margin-right: 10px;
            font-size: 12px;
        }}
        
        .header .task-time {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
        }}
        
        .header p {{
            margin-top: 15px;
            font-size: 14px;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .mermaid {{
            display: flex;
            justify-content: center;
            background: #f9f9f9;
            border-radius: 8px;
            padding: 20px;
            overflow-x: auto;
        }}
        
        .legend {{
            margin-top: 30px;
            padding: 20px;
            background: #f5f5f5;
            border-left: 4px solid #667eea;
            border-radius: 5px;
        }}
        
        .legend h3 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 16px;
        }}
        
        .legend-items {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 3px;
            flex-shrink: 0;
        }}
        
        .color-green {{ background: #4CAF50; }}
        .color-red {{ background: #f44336; }}
        .color-blue {{ background: #2196F3; }}
        .color-orange {{ background: #FF9800; }}
        .color-yellow {{ background: #FFC107; }}
        .color-purple {{ background: #9C27B0; }}
        
        .footer {{
            padding: 20px;
            text-align: center;
            border-top: 1px solid #eee;
            background: #f9f9f9;
            font-size: 12px;
            color: #666;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 20px;
            }}
            
            .content {{
                padding: 20px;
            }}
            
            .legend-items {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔧 {task_name}</h1>
            <div>
                <span class="task-id">任务 {task_id}</span>
                <span class="task-time">⏰ {task_time}</span>
            </div>
            <p>{task_desc}</p>
        </div>
        
        <div class="content">
            <div class="mermaid">
{mermaid_graph}
            </div>
            
            <div class="legend">
                <h3>图例说明</h3>
                <div class="legend-items">
                    <div class="legend-item">
                        <div class="legend-color color-green"></div>
                        <span>开始/结束节点</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color color-blue"></div>
                        <span>外部服务调用（AI）</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color color-orange"></div>
                        <span>数据库操作</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color color-yellow"></div>
                        <span>条件判断</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color color-purple"></div>
                        <span>复杂业务逻辑</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color color-red"></div>
                        <span>错误/异常处理</span>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>💻 红单定时任务流程图 | 生成时间: 2026-01-30 | 图表自动生成版本</p>
        </div>
    </div>
    
    <script>
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
        mermaid.contentLoaded();
    </script>
</body>
</html>
"""
        return html_content
    
    def generate_all(self):
        """生成所有任务的流程图"""
        
        print("🚀 开始生成红单定时任务流程图...")
        print("=" * 60)
        
        for task_id, task_info in TASKS.items():
            print(f"\n📋 处理任务 {task_id}: {task_info['name']}")
            print(f"   ⏰ 执行时间: {task_info['time']}")
            
            # 生成 HTML 预览
            mermaid_file = os.path.join(self.output_dir, task_info['mermaid'])
            html_content = self.generate_html_preview(task_id, task_info)
            
            html_output = os.path.join(
                self.output_dir, 
                f"task-{task_id}-flow.html"
            )
            
            try:
                with open(html_output, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"   ✅ HTML预览已生成: {os.path.basename(html_output)}")
            except Exception as e:
                print(f"   ❌ 生成HTML失败: {e}")
        
        print("\n" + "=" * 60)
        self._generate_index_html()
        print("\n🎉 所有流程图生成完成！")
    
    def _generate_index_html(self):
        """生成索引页面"""
        
        tasks_html = ""
        for task_id, task_info in TASKS.items():
            tasks_html += f"""
            <div class="task-card">
                <div class="task-header">
                    <h3>任务 {task_id}: {task_info['name']}</h3>
                    <span class="task-time">⏰ {task_info['time']}</span>
                </div>
                <p class="task-desc">{task_info['description']}</p>
                <a href="task-{task_id}-flow.html" class="task-link">查看流程图 →</a>
            </div>
"""
        
        index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>红单定时任务流程图</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: "Microsoft YaHei", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }}
        
        .header h1 {{
            font-size: 36px;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 16px;
            opacity: 0.9;
        }}
        
        .tasks-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        
        .task-card {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .task-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        }}
        
        .task-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }}
        
        .task-header h3 {{
            color: #333;
            font-size: 18px;
            flex: 1;
        }}
        
        .task-time {{
            background: #667eea;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            white-space: nowrap;
            margin-left: 10px;
        }}
        
        .task-desc {{
            color: #666;
            font-size: 14px;
            line-height: 1.5;
            margin-bottom: 15px;
        }}
        
        .task-link {{
            display: inline-block;
            color: #667eea;
            text-decoration: none;
            font-weight: bold;
            transition: color 0.3s;
        }}
        
        .task-link:hover {{
            color: #764ba2;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: white;
            opacity: 0.8;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔧 红单定时任务流程图</h1>
            <p>5个定时任务的详细流程和执行逻辑</p>
        </div>
        
        <div class="tasks-grid">
{tasks_html}
        </div>
        
        <div class="footer">
            <p>💻 自动生成于 2026-01-30 | 基于 Quartz 定时任务框架</p>
        </div>
    </div>
</body>
</html>
"""
        
        index_file = os.path.join(self.output_dir, "index.html")
        try:
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(index_html)
            print(f"✅ 索引页面已生成: {os.path.basename(index_file)}")
        except Exception as e:
            print(f"❌ 生成索引页面失败: {e}")

def main():
    """主函数"""
    
    # 检查输出目录
    if not os.path.exists(OUTPUT_DIR):
        print(f"❌ 输出目录不存在: {OUTPUT_DIR}")
        return
    
    # 创建生成器并生成所有流程图
    generator = TaskFlowGenerator(OUTPUT_DIR)
    generator.generate_all()
    
    print("\n📂 所有文件位置:")
    print(f"   {OUTPUT_DIR}")
    print("\n💡 使用说明:")
    print("   1. 用浏览器打开 index.html 查看所有任务列表")
    print("   2. 点击任务卡片查看详细流程图")
    print("   3. 每个流程图都有详细的图例说明")

if __name__ == "__main__":
    main()
