#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
朋友圈产品交互架构图生成器
使用现代化设计风格，清晰展示模块关系
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

def draw_rounded_box(ax, x, y, w, h, color, edge_color, title, items, title_size=14):
    """绘制圆角模块框"""
    # 主框
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.15",
        facecolor=color,
        edgecolor=edge_color,
        linewidth=2.5,
        alpha=0.95
    )
    ax.add_patch(box)

    # 标题栏背景
    title_bar = FancyBboxPatch(
        (x, y + h - 0.6), w, 0.6,
        boxstyle="round,pad=0.02,rounding_size=0.15",
        facecolor=edge_color,
        edgecolor=edge_color,
        linewidth=0,
        alpha=0.3
    )
    ax.add_patch(title_bar)

    # 标题文字
    ax.text(x + w/2, y + h - 0.3, title,
            ha='center', va='center',
            fontsize=title_size, fontweight='bold',
            color='#2c3e50')

    # 内容列表
    y_pos = y + h - 0.9
    for item in items:
        ax.text(x + 0.2, y_pos, item,
                ha='left', va='center',
                fontsize=10, color='#34495e')
        y_pos -= 0.4

def draw_arrow(ax, start, end, color='#7f8c8d', width=2, style='arc3,rad=0.1'):
    """绘制箭头"""
    arrow = FancyArrowPatch(
        start, end,
        arrowstyle='->,head_width=0.3,head_length=0.2',
        color=color,
        linewidth=width,
        connectionstyle=style,
        mutation_scale=15
    )
    ax.add_patch(arrow)

# 创建画布
fig, ax = plt.subplots(figsize=(20, 14), facecolor='#fafbfc')
ax.set_xlim(-1, 19)
ax.set_ylim(-1, 14)
ax.axis('off')
ax.set_facecolor('#fafbfc')

# ========== 标题 ==========
ax.text(9, 13, '朋友圈产品交互架构图',
        ha='center', va='center',
        fontsize=28, fontweight='bold', color='#1a1a2e')
ax.text(9, 12.4, 'FriendController API Architecture Overview',
        ha='center', va='center',
        fontsize=12, color='#6c757d', style='italic')

# ========== 用户入口 ==========
user_circle = Circle((9, 10.5), 0.6,
                      facecolor='#4361ee', edgecolor='#3a0ca3', linewidth=3)
ax.add_patch(user_circle)
ax.text(9, 10.5, 'USER', ha='center', va='center', fontsize=12, color='white', fontweight='bold')
ax.text(9, 9.7, '用户入口', ha='center', va='center', fontsize=12, fontweight='bold', color='#1a1a2e')

# ========== 核心功能模块（第一行） ==========
modules_core = [
    {
        'pos': (0.5, 6.5), 'size': (4, 2.5),
        'color': '#fff3e0', 'edge': '#ff9800',
        'title': '[1] 个人中心',
        'items': ['getUser - 查看资料', 'update - 编辑资料', 'getMyPraiseCount - 点赞数', 'getLevel - 用户等级']
    },
    {
        'pos': (5, 6.5), 'size': (4, 2.5),
        'color': '#e8f5e9', 'edge': '#4caf50',
        'title': '[2] 社交关系',
        'items': ['saveFollow - 关注/取消', 'getList - 关注/粉丝列表']
    },
    {
        'pos': (9.5, 6.5), 'size': (4, 2.5),
        'color': '#ede7f6', 'edge': '#673ab7',
        'title': '[3] 朋友圈动态',
        'items': ['saveCircle - 发布动态', 'pageList - 动态列表', 'readCount - 阅读计数', 'getCountList - 统计']
    },
    {
        'pos': (14, 6.5), 'size': (4, 2.5),
        'color': '#fce4ec', 'edge': '#e91e63',
        'title': '[4] 互动功能',
        'items': ['saveChangePraise - 点赞', 'saveComments - 评论', 'saveShare - 分享', 'saveReport - 举报']
    },
]

# ========== 扩展功能模块（第二行） ==========
modules_extend = [
    {
        'pos': (2, 3), 'size': (4, 2),
        'color': '#e0f7fa', 'edge': '#00bcd4',
        'title': '[5] 话题广场',
        'items': ['queryTitle - 话题列表', 'queryDetails - 话题详情']
    },
    {
        'pos': (7, 3), 'size': (4, 2),
        'color': '#fffde7', 'edge': '#ffc107',
        'title': '[6] 任务中心',
        'items': ['queryTasks - 任务列表']
    },
    {
        'pos': (12, 3), 'size': (4, 2),
        'color': '#fff8e1', 'edge': '#ff9800',
        'title': '[7] 板块功能',
        'items': ['index/getByLevel', 'guess/getByLevel']
    },
]

# 绘制核心模块
for m in modules_core:
    draw_rounded_box(ax, *m['pos'], *m['size'], m['color'], m['edge'], m['title'], m['items'])

# 绘制扩展模块
for m in modules_extend:
    draw_rounded_box(ax, *m['pos'], *m['size'], m['color'], m['edge'], m['title'], m['items'])

# ========== 绘制箭头 ==========
# 用户到核心模块
arrows_to_core = [
    ((9, 9.9), (2.5, 9)),   # 到个人中心
    ((9, 9.9), (7, 9)),     # 到社交关系
    ((9, 9.9), (11.5, 9)),  # 到朋友圈（主流程）
    ((9, 9.9), (16, 9)),    # 到互动
]

for i, (start, end) in enumerate(arrows_to_core):
    if i == 2:  # 主流程用粗蓝色
        draw_arrow(ax, start, end, color='#4361ee', width=3.5, style='arc3,rad=0.15')
    else:
        draw_arrow(ax, start, end, color='#adb5bd', width=2, style='arc3,rad=0.15')

# 核心模块到扩展模块
arrows_to_extend = [
    ((11.5, 6.5), (4, 5)),    # 朋友圈到话题
    ((11.5, 6.5), (9, 5)),    # 朋友圈到任务
    ((11.5, 6.5), (14, 5)),   # 朋友圈到板块
]

for start, end in arrows_to_extend:
    draw_arrow(ax, start, end, color='#adb5bd', width=1.5, style='arc3,rad=0.2')

# ========== 接口规范框 ==========
spec_box = FancyBboxPatch(
    (0.5, -0.5), 7, 3,
    boxstyle="round,pad=0.02,rounding_size=0.15",
    facecolor='#f8f9fa',
    edgecolor='#6c757d',
    linewidth=2
)
ax.add_patch(spec_box)

ax.text(4, 2.2, '[ API Spec ]', ha='center', va='center', fontsize=13, fontweight='bold', color='#495057')
ax.text(4, 1.5, 'Method: POST', ha='center', va='center', fontsize=11, color='#6c757d')
ax.text(4, 1.0, 'Content-Type: application/json', ha='center', va='center', fontsize=11, color='#6c757d')
ax.text(4, 0.5, 'Response: { code, message, data }', ha='center', va='center', fontsize=11, color='#6c757d')
ax.text(4, 0.0, 'Params: product, userId, pageNum/Size', ha='center', va='center', fontsize=11, color='#6c757d')

# ========== 图例 ==========
legend_box = FancyBboxPatch(
    (8.5, -0.5), 10, 3,
    boxstyle="round,pad=0.02,rounding_size=0.15",
    facecolor='#f8f9fa',
    edgecolor='#6c757d',
    linewidth=2
)
ax.add_patch(legend_box)

ax.text(13.5, 2.2, '[ Legend ]', ha='center', va='center', fontsize=13, fontweight='bold', color='#495057')

legend_items = [
    (9.2, 1.4, '#ff9800', '[1] 个人中心 - 用户资料管理'),
    (9.2, 0.9, '#4caf50', '[2] 社交关系 - 关注/粉丝'),
    (9.2, 0.4, '#673ab7', '[3] 朋友圈 - 动态发布浏览'),
    (9.2, -0.1, '#e91e63', '[4] 互动功能 - 点赞评论分享'),
    (14, 1.4, '#00bcd4', '[5] 话题广场'),
    (14, 0.9, '#ffc107', '[6] 任务中心'),
    (14, 0.4, '#ff9800', '[7] 板块功能'),
    (14, -0.1, '#4361ee', '━━ 主流程'),
]

for x, y, color, text in legend_items:
    circle = Circle((x, y), 0.12, facecolor=color, edgecolor='none')
    ax.add_patch(circle)
    ax.text(x + 0.3, y, text, ha='left', va='center', fontsize=9, color='#495057')

# ========== 保存 ==========
plt.tight_layout()
output_path = r'C:\Users\DEVTrump\projects\docs-1\FriendController\architecture-diagram.png'
plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='#fafbfc', edgecolor='none')
print('Done: ' + output_path)

# 同时保存一份中文名的
import shutil
output_path_cn = r'C:\Users\DEVTrump\projects\docs-1\FriendController\朋友圈产品交互架构图.png'
shutil.copy(output_path, output_path_cn)
print('Done: architecture-diagram.png copied')

plt.close()
