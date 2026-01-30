# 🔧 红单定时任务流程图完整指南

## 📋 概述

本目录包含红单（推单）功能的 **5个定时任务** 的详细流程图和文档。这些流程图通过 **Mermaid** 绘制，并通过 **Python 脚本** 转换为易读的可视化流程图。

---

## 📁 文件清单

### Mermaid 源文件（基于代码一比一还原）
| 文件 | 任务 | 执行时间 |
|------|------|---------|
| `task-01-ai-pushorder.mmd` | AI推单任务 | 每天 21:00:00 |
| `task-02-repair-pushorder.mmd` | AI补救推单 | 每天 23:00:00 |
| `task-03-restock-pushorder.mmd` | AI补单 | 每天 00:00:01 |
| `task-04-user-fire.mmd` | 月度用户火标志 | 每月5日 00:00:00 |
| `task-05-real-pushorder.mmd` | 真实玩家推单 | 每天 20:00:00 |

### HTML 可视化流程图
| 文件 | 说明 |
|------|------|
| `task-01-flow.html` | 📊 AI推单任务流程图（可交互） |
| `task-02-flow.html` | 📊 AI补救推单流程图（可交互） |
| `task-03-flow.html` | 📊 AI补单流程图（可交互） |
| `task-04-flow.html` | 📊 月度用户火标志流程图（可交互） |
| `task-05-flow.html` | 📊 真实玩家推单流程图（可交互） |
| `index.html` | 🎯 **总览页面**（任务导航中心） |

### 辅助文件
| 文件 | 说明 |
|------|------|
| `generate_task_flows.py` | 🐍 Python 脚本（生成 HTML 流程图） |
| `红单定时任务和数据交互报告.md` | 📄 详细的任务分析报告 |
| `红单功能统计报告.md` | 📄 红单功能整体统计 |

---

## 🚀 快速开始

### 方法1：查看 HTML 流程图（推荐）
```bash
# 1. 打开总览页面
docs-1/redbill/index.html

# 2. 在浏览器中点击任务卡片查看具体流程图
# 3. 鼠标悬停可以查看更多细节
```

### 方法2：查看 Mermaid 源文件
```bash
# 用任何支持 Mermaid 的编辑器打开 .mmd 文件
# 推荐：VS Code + Mermaid 扩展
```

### 方法3：重新生成流程图
```bash
cd c:\Users\DEVTrump\projects\docs-1\redbill
python generate_task_flows.py
```

---

## 📊 5个定时任务详解

### 1️⃣ AI推单任务（task-01）
**执行时间**：每天 21:00:00  
**流程图**：`task-01-flow.html`

**主要功能**：
- ✅ 根据未来2天内即将开赛的体育赛事生成推单
- ✅ 调用豆包AI或KIMI AI进行分析
- ✅ 生成标题和分析结果

**关键步骤**：
1. 获取系统配置的推单产品列表
2. 查询每个产品下的AI推单用户
3. 获取未来2天内的赛事信息
4. 过滤有效的赔率数据
5. 调用AI生成推单内容
6. 保存到数据库

**流程图查看**：[task-01-flow.html](task-01-flow.html)

---

### 2️⃣ AI补救推单任务（task-02）
**执行时间**：每天 23:00:00  
**流程图**：`task-02-flow.html`

**主要功能**：
- ✅ 21点推单失败时的保险机制
- ✅ 检查当日推单是否已成功
- ✅ 失败则重新执行推单

**关键步骤**：
1. 查询当日AI生成的推单总数
2. 如果 count > 0，则跳过（说明今日推单成功）
3. 如果 count = 0，则执行补救推单逻辑

**特点**：
- 智能判断：不会重复生成已成功的推单
- 防护机制：确保每日都有推单产出

**流程图查看**：[task-02-flow.html](task-02-flow.html)

---

### 3️⃣ AI补单任务（task-03）
**执行时间**：每天 00:00:01  
**流程图**：`task-03-flow.html`

**主要功能**：
- ✅ 为针对特定联赛的推单用户补充推单
- ✅ 对比2天前和今天的推单情况
- ✅ 避免重复推同一赛事给同一用户

**关键步骤**（最复杂）：
1. 查询设置了「联赛限制」的用户
2. 提取这些用户针对的联赛ID列表
3. 查询2天前这些联赛的已推赛事
4. 查询今天特定联赛未推过的赛事
5. 第1步过滤：排除 odds 无效的赛事
6. 第2步过滤：排除 odds 盘口不足3个的赛事
7. 扣减2天前推过的用户的推单数量
8. 执行补单逻辑（按剩余推单数）

**特殊处理**：
- 联赛级别的精细化管理
- 用户历史对比（避免重复）
- 推单数量的动态调整

**流程图查看**：[task-03-flow.html](task-03-flow.html)

---

### 4️⃣ 月度用户火标志设置（task-04）
**执行时间**：每月5日 00:00:00  
**流程图**：`task-04-flow.html`

**主要功能**：
- ✅ 每月初重置用户的「火」标志
- ✅ 清空月度统计数据
- ✅ 为排行榜更新做准备

**关键步骤**：
1. 调用 `IMasterUserService.setUserFire()`
2. 循环所有推单用户
3. 更新 fire = 1（用户火标志）
4. 重置月度统计数据：
   - monthlyWinCount = 0（月度胜场数）
   - monthlyHotCount = 0（月度热度数）
   - monthlyRankRing = 0（月度排名环）

**应用场景**：
- 月度排行榜重置
- 用户称号/等级更新
- 推单人气值清零

**流程图查看**：[task-04-flow.html](task-04-flow.html)

---

### 5️⃣ 真实玩家推单任务（task-05）
**执行时间**：每天 20:00:00  
**流程图**：`task-05-flow.html`

**主要功能**：
- ✅ 基于真实玩家历史注单数据生成推单
- ✅ 半AI模式（真实用户 + AI分析）
- ✅ 提高推单的真实性和可信度

**关键步骤**：
1. 查询所有「半AI」(userType=1) 推单用户
2. 查询该用户过去30天的历史注单
3. 分析用户的投注习惯：
   - 胜率/中奖率
   - 偏好赛事类型
   - 常用投注方式
4. 获取即将开赛的赛事（优先用户偏好类型）
5. 准备AI分析上下文（融入用户历史风格）
6. 调用AI生成推单（基于用户特征）
7. 保存真实推单

**特点**：
- 个性化推单：每个用户的推单风格不同
- 数据驱动：基于历史注单数据分析
- 提高可信度：展现真实玩家的投注思路

**流程图查看**：[task-05-flow.html](task-05-flow.html)

---

## 🎨 流程图图例

在每个 HTML 流程图中，节点颜色代表不同的含义：

| 颜色 | 含义 | 示例 |
|------|------|------|
| 🟢 绿色 | 开始/结束节点 | START, END |
| 🔴 红色 | 错误/异常处理 | ERROR, 【被迫结束】 |
| 🔵 蓝色 | 外部服务调用 | 调用AI接口、调用服务 |
| 🟠 橙色 | 数据库操作 | 查询数据库、保存数据 |
| 🟡 黄色 | 条件判断 | if/else 判断 |
| 🟣 紫色 | 复杂业务逻辑 | 数据转换、统计计算 |

---

## 💾 源代码位置

所有定时任务的源代码位于：
```
DC-API-2018/dc-api/dc-api-office/src/main/java/com/dc/it/friend/
├── quartz/
│   └── AIPushOrderTask.java          ← 定时任务主类
├── service/interfaces/
│   └── IAIPushOrderService.java      ← 服务接口
├── service/impl/
│   └── AIPushOrderServiceImpl.java    ← 服务实现类（2172行）
└── controller/
    └── PushOrderAiUserController.java ← 后台控制器

Spring配置：
DC-API-2018/dc-api/dc-api-office/src/main/resources/
├── applicationContext.xml             ← Quartz 定时任务配置
└── applicationContext-quartz.xml      ← 触发器配置
```

---

## 🔍 源代码与流程图对应关系

### task-01-ai-pushorder.mmd
对应源代码方法：
- `AIPushOrderTask.aiPushOrder()` → `IAIPushOrderService.taskCreatePushOrder()` → `createPushOrder(uuid, null)`
- 源文件：`AIPushOrderServiceImpl.java` 第532行

### task-02-repair-pushorder.mmd
对应源代码方法：
- `AIPushOrderTask.aiRepairPushOrder()` → `IAIPushOrderService.taskRepairCreatePushOrder()`
- 源文件：`AIPushOrderServiceImpl.java` 第544行

### task-03-restock-pushorder.mmd
对应源代码方法：
- `AIPushOrderTask.aiRestockPushOrder()` → `IAIPushOrderService.taskRestockPushOrder()` → `restockPushOrder(uuid, null)`
- 源文件：`AIPushOrderServiceImpl.java` 最复杂，涉及多个方法

### task-04-user-fire.mmd
对应源代码方法：
- `AIPushOrderTask.userFire()` → `IMasterUserService.setUserFire(null)`
- 位置：Friend模块的 UserService

### task-05-real-pushorder.mmd
对应源代码方法：
- `AIPushOrderTask.aiRealPushOrder()` → `IAIPushOrderService.taskCreateRealPushOrder()` → `createRealPushOrder(uuid, null)`
- 源文件：`AIPushOrderServiceImpl.java`

---

## 📈 任务执行时间表

```
00:00:01
   └─ 🌙 AI补单任务（task-03）

20:00:00
   └─ 🌃 真实玩家推单任务（task-05）

21:00:00
   └─ 🌙 AI推单任务（task-01）← 最重要

23:00:00
   └─ 🌙 AI补救推单任务（task-02）← 保险机制

每月5日 00:00:00
   └─ 📅 月度用户火标志设置（task-04）
```

---

## 🛠️ Python 脚本使用说明

### generate_task_flows.py

**功能**：
- 自动读取所有 Mermaid .mmd 文件
- 生成对应的 HTML 可视化流程图
- 生成索引页面（总览）

**使用方法**：
```bash
cd c:\Users\DEVTrump\projects\docs-1\redbill
python generate_task_flows.py
```

**输出**：
- `task-01-flow.html` 至 `task-05-flow.html`（5个流程图）
- `index.html`（索引总览页面）

**自定义**：
修改脚本中的 `TASKS` 字典来添加新任务或修改配置。

---

## 📚 相关文档

### 主文档
- **红单定时任务和数据交互报告.md** - 完整的任务分析报告
  - 包含所有5个任务的详细说明
  - 数据来源和抓取逻辑
  - 27+交互接口列表
  - 故障排查指南

- **红单功能统计报告.md** - 红单功能整体统计
  - 7个Controller统计
  - 44个接口统计
  - 核心服务和DAO类

---

## 🎯 推荐使用场景

| 场景 | 推荐使用 |
|------|---------|
| 快速了解任务流程 | 📊 打开 `index.html` |
| 详细研究某个任务 | 📊 打开对应的 `task-XX-flow.html` |
| 学习代码逻辑 | 🔗 查看 .mmd 文件 + 源代码 |
| 培训新人 | 🎓 展示 HTML 流程图 |
| 编写文档 | 📄 参考 .md 报告文件 |
| 系统架构分析 | 🏗️ 参考完整的定时任务结构 |

---

## 💡 关键要点

### AI推单的核心特点
✅ **双AI模式**：豆包AI（0号）和KIMI AI（1号）  
✅ **多层次保障**：创建→补救→补单三步机制  
✅ **精细化管理**：支持联赛级别的推单限制  
✅ **真实性融合**：半AI模式融入真实用户数据  
✅ **月度重置**：定期清空统计数据，保持系统活性  

### 推单产品配置
- 系统参数 `PUSHORDER_PRODUCT` 配置可用产品
- 示例：`yl,at,qy,e68`（各产品可独立配置）
- 支持动态添加新产品

### 推单用户类型
| 类型 | 说明 | 推单方式 |
|------|------|---------|
| 全AI(0) | 纯AI分析 | 基于赛事+赔率+历史 |
| 半AI(1) | 真实用户+AI | 基于用户历史注单+AI分析 |

---

## 🚀 快速命令参考

```bash
# 查看总览
start index.html

# 查看具体任务（以第1个为例）
start task-01-flow.html

# 查看Mermaid源文件
code task-01-ai-pushorder.mmd

# 重新生成所有流程图
python generate_task_flows.py

# 查看完整的任务分析报告
code 红单定时任务和数据交互报告.md
```

---

## ❓ 常见问题

**Q: 如何修改流程图？**
A: 编辑对应的 .mmd 文件，然后重新运行 `generate_task_flows.py` 脚本。

**Q: 可以添加新的任务吗？**
A: 可以。创建新的 .mmd 文件，并在 `generate_task_flows.py` 的 `TASKS` 字典中添加配置。

**Q: HTML 流程图可以导出吗？**
A: 可以。在浏览器中右键点击 Mermaid 图表，选择「保存为图片」。

**Q: 我可以离线使用这些流程图吗？**
A: 可以。所有 HTML 文件都是独立的，可以离线打开和使用。

---

## 📝 更新日志

- **2026-01-30** - 初始版本
  - ✅ 创建5个 Mermaid 流程图
  - ✅ 生成 Python 脚本
  - ✅ 生成 HTML 可视化
  - ✅ 完成本说明文档

---

## 👨‍💻 开发者信息

**创建者**：GitHub Copilot  
**创建时间**：2026年1月30日  
**项目**：DC-API 红单（推单）功能梳理  
**参考源代码**：DC-API-2018 项目

---

## 📞 技术支持

如有问题或建议，请参考：
- 📄 `红单定时任务和数据交互报告.md` - 详细分析
- 🔗 源代码位置：`DC-API-2018/dc-api/dc-api-office/`
- 💻 源代码文件：`AIPushOrderTask.java`、`AIPushOrderServiceImpl.java`

---

**🎉 享受高效的流程可视化体验！**
