#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
红单（PushOrder）产品交互流程图 - 手绘风格
生成位置：docs-1/redbill/
同时输出 Mermaid 流程描述
"""

import math
import os
import re
import textwrap
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

# 手绘/自由风格
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['path.sketch'] = (1, 120, 2.0)  # (scale, length, randomness)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKGROUND = '#fff8f0'
MERMAID_PATH = os.path.join(BASE_DIR, 'redbill-flow.mmd')


def draw_box(ax, x, y, w, h, title, items, face, edge, title_size=12, text_size=8.5):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.03,rounding_size=0.25",
        facecolor=face,
        edgecolor=edge,
        linewidth=2.2,
        alpha=0.95
    )
    ax.add_patch(box)

    title_bar = FancyBboxPatch(
        (x, y + h - 0.55), w, 0.55,
        boxstyle="round,pad=0.02,rounding_size=0.25",
        facecolor=edge,
        edgecolor=edge,
        linewidth=0,
        alpha=0.2
    )
    ax.add_patch(title_bar)

    ax.text(x + w/2, y + h - 0.28, title,
            ha='center', va='center',
            fontsize=title_size, fontweight='bold', color='#2b2d42')

    y_pos = y + h - 0.85
    for item in items:
        ax.text(x + 0.18, y_pos, item,
                ha='left', va='center',
                fontsize=text_size, color='#3a3d46')
        y_pos -= 0.32


def draw_arrow(ax, start, end, color='#6c757d', width=1.8, style='arc3,rad=0.1', linestyle='-'):
    arrow = FancyArrowPatch(
        start, end,
        arrowstyle='->,head_width=0.28,head_length=0.22',
        color=color,
        linewidth=width,
        connectionstyle=style,
        mutation_scale=12,
        linestyle=linestyle
    )
    ax.add_patch(arrow)


def calc_height(items_count, base=1.4, line_h=0.32, title_h=0.6):
    return base + title_h + items_count * line_h


def build_mermaid(nodes, edges):
    lines = ['flowchart LR']
    for key, node in nodes.items():
        label = node['label']
        lines.append(f"  {key}[{label}]")
    for edge in edges:
        label = edge.get('label')
        if label:
            lines.append(f"  {edge['from']} -->|{label}| {edge['to']}")
        else:
            lines.append(f"  {edge['from']} --> {edge['to']}")
    return '\n'.join(lines)


def get_center(node_key, node_positions, node_types, circle_positions):
    if node_types.get(node_key) == 'circle':
        return circle_positions[node_key]
    x, y, w, h = node_positions[node_key]
    return (x + w / 2, y + h - 0.3)


def draw_edge_label(ax, start, end, text, color='#6c757d'):
    if not text:
        return
    mx = (start[0] + end[0]) / 2
    my = (start[1] + end[1]) / 2
    ax.text(mx, my, text, ha='center', va='center', fontsize=8, color=color, alpha=0.85)


def parse_mermaid(path):
    node_pattern = re.compile(r'^\s*([A-Za-z0-9_]+)\[(.+)\]\s*$')
    edge_pattern = re.compile(r'^\s*([A-Za-z0-9_]+)\s*-->\s*(?:\|([^|]+)\|\s*)?([A-Za-z0-9_]+)\s*$')

    nodes = {}
    edges = []
    with open(path, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('flowchart'):
                continue
            m = node_pattern.match(line)
            if m:
                key, label = m.group(1), m.group(2)
                nodes[key] = {'label': label}
                continue
            m = edge_pattern.match(line)
            if m:
                src, label, dst = m.group(1), m.group(2), m.group(3)
                edges.append({'from': src, 'to': dst, 'label': label})
    return nodes, edges


def build_layers(nodes, edges):
    incoming = {k: 0 for k in nodes}
    outgoing = {k: [] for k in nodes}
    for e in edges:
        if e['from'] not in outgoing:
            outgoing[e['from']] = []
        outgoing[e['from']].append(e['to'])
        incoming[e['to']] = incoming.get(e['to'], 0) + 1

    layers = []
    current = [k for k, v in incoming.items() if v == 0]
    seen = set(current)
    while current:
        layers.append(current)
        nxt = []
        for node in current:
            for to in outgoing.get(node, []):
                incoming[to] -= 1
                if incoming[to] == 0 and to not in seen:
                    seen.add(to)
                    nxt.append(to)
        current = nxt

    # 未连接节点放在最后一层
    dangling = [k for k in nodes if k not in seen]
    if dangling:
        layers.append(dangling)
    return layers


# ===== 数据 =====
controllers = [
    {
        'title': 'PushOrderPublicController（对外接口）',
        'items': [
            '/findPersonalInfoPageList',
            '/findMasterDetailed',
            '/findPushUserInfo',
            '/findMonthlyRankingPageList',
            '/findPlanDetailed',
            '/findProgrammePreferredPageList',
            '/findMatchPreferredPageList',
        ],
        'color': '#e7f0ff', 'edge': '#3a86ff'
    },
    {
        'title': 'PushOrderAiUserController（AI用户管理）',
        'items': [
            '/leagueList',
            '/testAi',
            '/backPushOrder',
            '/backRestockPushOrder',
            '/list',
            '/checkPlayers',
            '/checkAIUser',
            '/save',
            '/update',
            '/del',
            '/updateGrantKf',
            '/findGrantKf',
            '/queryHalfAIApplyProduct',
            '/saveHalfAI',
            '/updateHalfAI',
        ],
        'color': '#fff1e6', 'edge': '#ff7f50'
    },
    {
        'title': 'PushOrderContentManagementController（内容管理）',
        'items': [
            '/pageList',
            '/pageListOne',
            '/insert',
            '/update',
            '/updateState',
            '/openPushOrderData',
            '/findDetectingUsername',
            '/findGeneralLogPageList',
            '/updatePartialFields',
            '/findMatchFootBasketBall',
            '/updateGrantKf',
            '/findGrantKf',
        ],
        'color': '#e8f8f1', 'edge': '#2a9d8f'
    },
    {
        'title': 'PushOrderParamConfigController（参数配置）',
        'items': [
            '/list',
            '/update',
            '/findPushOrdersPrice',
        ],
        'color': '#f6f7ff', 'edge': '#7b6ed6'
    },
    {
        'title': 'PushOrderLevelTitleConfigController（等级称号）',
        'items': [
            '/list',
            '/insert',
            '/update',
            '/findIdNameList',
        ],
        'color': '#fff6db', 'edge': '#f4a261'
    },
    {
        'title': 'PushOrderContentGeneralLogController（内容日志）',
        'items': [
            '/pageList',
            '/purchaseStatisticsPageList',
        ],
        'color': '#f3f3f3', 'edge': '#6c757d'
    },
    {
        'title': 'PushOrderPermissionRecordController（权限记录）',
        'items': [
            '/pageList',
        ],
        'color': '#ffeef3', 'edge': '#e76f51'
    },
]

# ===== 节点/连线数据（作为 Mermaid 源） =====
nodes = {
    'User': {'label': '外部用户'},
    'Admin': {'label': '后台运营'},
    'AI': {'label': 'AI任务'},
    'Public': {'label': 'PushOrderPublicController'},
    'AiUser': {'label': 'PushOrderAiUserController'},
    'Content': {'label': 'PushOrderContentManagementController'},
    'Param': {'label': 'PushOrderParamConfigController'},
    'Level': {'label': 'PushOrderLevelTitleConfigController'},
    'Log': {'label': 'PushOrderContentGeneralLogController'},
    'Perm': {'label': 'PushOrderPermissionRecordController'},
}

edges = [
    {'from': 'User', 'to': 'Public', 'label': '查询大师/榜单/方案', 'color': '#ff7f50', 'rad': 0.15},
    {'from': 'Public', 'to': 'Content', 'label': '拉取公开推单', 'color': '#3a86ff', 'rad': -0.25, 'style': '--'},
    {'from': 'Admin', 'to': 'AiUser', 'label': 'AI用户配置', 'color': '#52b788', 'rad': 0.12},
    {'from': 'Admin', 'to': 'Content', 'label': '内容运营', 'color': '#52b788', 'rad': -0.18},
    {'from': 'Admin', 'to': 'Param', 'label': '参数配置', 'color': '#52b788', 'rad': 0.22},
    {'from': 'Admin', 'to': 'Level', 'label': '等级称号', 'color': '#52b788', 'rad': -0.12},
    {'from': 'Admin', 'to': 'Perm', 'label': '授权与权限', 'color': '#52b788', 'rad': 0.25},
    {'from': 'AI', 'to': 'Content', 'label': '任务创建/补单', 'color': '#3a86ff', 'rad': 0.1},
    {'from': 'AiUser', 'to': 'Content', 'label': '推单生产', 'color': '#ff7f50', 'rad': 0.1},
    {'from': 'Param', 'to': 'Content', 'label': '价格/产品影响', 'color': '#7b6ed6', 'rad': 0.2, 'style': '--'},
    {'from': 'Level', 'to': 'Content', 'label': '称号影响', 'color': '#f4a261', 'rad': -0.2, 'style': '--'},
    {'from': 'Perm', 'to': 'Content', 'label': '权限影响', 'color': '#e76f51', 'rad': 0.2, 'style': '--'},
    {'from': 'Content', 'to': 'Log', 'label': '日志/统计', 'color': '#6c757d', 'rad': -0.2},
]

# ===== Mermaid 输出 =====
with open(MERMAID_PATH, 'w', encoding='utf-8') as f:
    f.write(build_mermaid(nodes, edges))

# ===== 读取 Mermaid 做绘图对齐 =====
nodes, edges = parse_mermaid(MERMAID_PATH)

# ===== 画布 =====
fig, ax = plt.subplots(figsize=(24, 17), facecolor=BACKGROUND)
ax.set_xlim(-1, 24)
ax.set_ylim(-2, 17)
ax.axis('off')
ax.set_facecolor(BACKGROUND)

# 标题
ax.text(11.5, 16.1, '红单（PushOrder）产品交互流程图',
        ha='center', va='center', fontsize=26, fontweight='bold', color='#22223b')
ax.text(11.5, 15.4, 'Freehand / Excalidraw Style',
        ha='center', va='center', fontsize=11, color='#6c757d', style='italic')

# 入口节点位置（从 Mermaid 的“圆形节点”推断）
circle_positions = {}
circle_styles = {
    'User': {'face': '#ffd166', 'edge': '#f4a261'},
    'Admin': {'face': '#caffbf', 'edge': '#52b788'},
    'AI': {'face': '#bde0fe', 'edge': '#3a86ff'},
}

layers = build_layers(nodes, edges)
layer_x = [2.0 + i * 7.0 for i in range(len(layers))]
node_positions = {}

for li, layer in enumerate(layers):
    for idx, key in enumerate(layer):
        if key in circle_styles:
            circle_positions[key] = (layer_x[li], 13.6 - idx * 2.2)
        else:
            node_positions[key] = (layer_x[li] - 1.4, 9.0 - idx * 3.0, 6.6, 2.6)

for key, (cx, cy) in circle_positions.items():
    style = circle_styles.get(key, {'face': '#e9ecef', 'edge': '#6c757d'})
    circle = Circle((cx, cy), 0.75, facecolor=style['face'], edgecolor=style['edge'], linewidth=2.5)
    ax.add_patch(circle)
    ax.text(cx, cy, nodes[key]['label'], ha='center', va='center', fontsize=11, fontweight='bold')

# 布局：两列+中列
x_left = 0.8
x_mid = 8.2
x_right = 15.8
w = 6.6

# 计算高度
heights = [calc_height(len(c['items'])) for c in controllers]

# 绘制模块
controller_map = {
    'Public': controllers[0],
    'AiUser': controllers[1],
    'Content': controllers[2],
    'Param': controllers[3],
    'Level': controllers[4],
    'Log': controllers[5],
    'Perm': controllers[6],
}

for key, (x, y, bw, bh) in node_positions.items():
    if key in controller_map:
        c = controller_map[key]
        draw_box(ax, x, y, bw, bh, c['title'], c['items'], c['color'], c['edge'])
    else:
        draw_box(ax, x, y, bw, bh, nodes[key]['label'], [], '#f8f9fa', '#6c757d')

# 箭头连接（完全由 Mermaid 数据驱动）
default_edge_style = {
    ('User', 'Public'): {'color': '#ff7f50', 'rad': 0.15},
    ('Public', 'Content'): {'color': '#3a86ff', 'rad': -0.25, 'style': '--'},
    ('Admin', 'AiUser'): {'color': '#52b788', 'rad': 0.12},
    ('Admin', 'Content'): {'color': '#52b788', 'rad': -0.18},
    ('Admin', 'Param'): {'color': '#52b788', 'rad': 0.22},
    ('Admin', 'Level'): {'color': '#52b788', 'rad': -0.12},
    ('Admin', 'Perm'): {'color': '#52b788', 'rad': 0.25},
    ('AI', 'Content'): {'color': '#3a86ff', 'rad': 0.1},
    ('AiUser', 'Content'): {'color': '#ff7f50', 'rad': 0.1},
    ('Param', 'Content'): {'color': '#7b6ed6', 'rad': 0.2, 'style': '--'},
    ('Level', 'Content'): {'color': '#f4a261', 'rad': -0.2, 'style': '--'},
    ('Perm', 'Content'): {'color': '#e76f51', 'rad': 0.2, 'style': '--'},
    ('Content', 'Log'): {'color': '#6c757d', 'rad': -0.2},
}

for edge in edges:
    style_conf = default_edge_style.get((edge['from'], edge['to']), {})
    start = get_center(edge['from'], node_positions, {'User': 'circle', 'Admin': 'circle', 'AI': 'circle'}, circle_positions)
    end = get_center(edge['to'], node_positions, {'User': 'circle', 'Admin': 'circle', 'AI': 'circle'}, circle_positions)
    style = style_conf.get('style', '-')
    color = style_conf.get('color', '#6c757d')
    rad = style_conf.get('rad', 0.1)
    draw_arrow(
        ax,
        start,
        end,
        color=color,
        width=2.0 if style == '-' else 1.4,
        style=f"arc3,rad={rad}",
        linestyle=style
    )
    draw_edge_label(ax, start, end, edge.get('label'), color=color)

# 小说明
ax.text(1.0, -0.8, '说明：节点内列出该Controller下的全部接口；虚线代表弱依赖/配置影响。',
        ha='left', va='center', fontsize=9, color='#6c757d')

# 保存
plt.tight_layout()
output_path = os.path.join(BASE_DIR, 'redbill-flow.png')
plt.savefig(output_path, dpi=220, bbox_inches='tight', facecolor=BACKGROUND, edgecolor='none')

# 另存中文名
import shutil
output_path_cn = os.path.join(BASE_DIR, '红单产品交互流程图.png')
shutil.copy(output_path, output_path_cn)

print('Done:', output_path)
print('Done:', output_path_cn)
print('Done:', MERMAID_PATH)

plt.close()
