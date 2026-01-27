# qm -> qy 红单复刻执行顺序总结

> **核心目标：** 让qy产品支持红单功能，数据与qm完全隔离

---

## 📋 docs目录文档清单

| 文档名 | 说明 | 用途 |
|--------|------|------|
| `qm-to-qy-redbill.md` | 技术方案文档 | 整体方案和业务流程 |
| `qm-to-qy-redbill-action.md` | **Action执行清单** | ⭐ **核心执行文档** |
| `qm-to-qy-redbill-execution-checklist.md` | 执行检查清单 | 详细检查项 |
| `qm-to-qy-redbill-timer-task-review.md` | 定时任务代码审查 | 定时任务详细分析 |
| `qm-to-qy-config-init-verification.sql` | 配置初始化验证SQL | 验证配置是否初始化成功 |
| `qm-to-qy-timer-task-data-verification.sql` | 定时任务数据验证SQL | 验证定时任务是否生成qy数据 |
| `qm-to-qy-timer-task-tables-summary.md` | 定时任务操作表总结 | 定时任务操作哪些表 |
| `qm-to-qy-pushorderexternal-controller-review.md` | App接口代码审查 | 17个接口检查结果 |
| `qm-to-qy-backend-admin-controllers-review.md` | 后台管理接口审查 | 39个后台管理接口检查 |
| `qm-to-qy-backend-admin-vs-app-interfaces-tables-comparison.md` | 表操作对比 | 后台管理 vs App接口 vs 定时任务 |
| `qm-to-qy-17-interfaces-data-isolation-verification.md` | 数据隔离验证 | 17个接口数据隔离机制 |
| `qm-to-qy-pushorderexternal-17-interfaces-tables.md` | 17个接口操作表 | 17个接口操作哪些表 |
| `qm-to-qy-findPushOrderFiveEvent-modification-guide.md` | 5大赛事接口改造指南 | 1个接口改造方案 |
| `account-passwd.md` | 账号密码汇总 | 各种账号密码信息 |
| `database-connection-guide.md` | 数据库连接指南 | 如何连接数据库 |
| `redbill-verification-queries.sql` | 红单验证SQL | 通用验证SQL |

---

## 🎯 执行顺序（核心问题：第一步是什么？）

### ✅ 正确顺序：先配置，后代码，再验证

```
第一步：数据库配置初始化（让定时任务有数据可生成）
  ↓
第二步：系统参数配置（让定时任务知道要处理qy）
  ↓
第三步：等待定时任务执行（生成qy数据）
  ↓
第四步：代码改造（接口支持qy）
  ↓
第五步：测试验证（验证数据和接口）
```

---

## 📊 详细执行步骤

### 🔴 第一步：数据库配置初始化（必须先做！）

**目的：** 让定时任务有数据可生成

**为什么必须先做？**
- 定时任务需要AI用户配置才能生成推单
- 定时任务需要价格配置才能给推单定价
- 定时任务需要文案配置才能生成推单内容
- **没有这些配置，定时任务会跳过qy产品**

**执行内容：**

#### 1.1 推单参数配置（PUSH_ORDER_PARAM_CONFIG）
```sql
-- 复制at的推单参数配置到qy
INSERT INTO pubdb.PUSH_ORDER_PARAM_CONFIG (...)
SELECT ..., 'qy' AS PRODUCT, ...
FROM pubdb.PUSH_ORDER_PARAM_CONFIG
WHERE PRODUCT = 'at' AND DEL = '0';
```

#### 1.2 等级称号配置（PUSH_ORDER_LEVEL_TITLE_CONFIG）
```sql
-- 复制at的等级称号配置到qy
INSERT INTO pubdb.PUSH_ORDER_LEVEL_TITLE_CONFIG (...)
SELECT ..., 'qy' AS PRODUCT, ...
FROM pubdb.PUSH_ORDER_LEVEL_TITLE_CONFIG
WHERE PRODUCT = 'at' AND DEL = '0';
```

#### 1.3 AI推单用户配置（PUSH_ORDER_AI_USER）⭐ **关键！**
```sql
-- 复制at的AI用户配置到qy
INSERT INTO pubdb.PUSH_ORDER_AI_USER (...)
SELECT ..., 'qy' AS PRODUCT, ...
FROM pubdb.PUSH_ORDER_AI_USER
WHERE PRODUCT = 'at' AND STATUS = 0;
```

#### 1.4 AI用户文案配置（PUSH_ORDER_AI_USER_COPYWRITE）⭐ **关键！**
```sql
-- 复制at的AI用户文案配置到qy
-- 注意：必须先执行1.3，获取新插入的qy用户ID
INSERT INTO pubdb.PUSH_ORDER_AI_USER_COPYWRITE (...)
SELECT ..., qy_user.ID AS POAUID, ...
FROM pubdb.PUSH_ORDER_AI_USER_COPYWRITE at_copywrite
INNER JOIN pubdb.PUSH_ORDER_AI_USER at_user ON ...
INNER JOIN pubdb.PUSH_ORDER_AI_USER qy_user ON ...
WHERE at_user.PRODUCT = 'at';
```

**验证SQL：**
```sql
-- 执行 docs/qm-to-qy-config-init-verification.sql
```

**时间：** 10-15分钟

---

### 🔴 第二步：系统参数配置（让定时任务知道要处理qy）

**目的：** 让定时任务知道要为qy产品生成推单

**执行内容：**
```sql
-- 更新系统参数，添加qy
UPDATE pubdb.S_SYSTEM_PARAMETER 
SET VALUE = 'at,qy'  -- 如果原来只有at，就改成at,qy
WHERE CATEGORY = 'PUSHORDER' 
  AND CODE = 'PUSHORDER_PRODUCT';
```

**验证SQL：**
```sql
SELECT VALUE FROM pubdb.S_SYSTEM_PARAMETER
WHERE CATEGORY = 'PUSHORDER' AND CODE = 'PUSHORDER_PRODUCT';
-- 应该返回：at,qy
```

**时间：** 1分钟

---

### 🟡 第三步：等待定时任务执行（生成qy数据）

**目的：** 让定时任务为qy生成推单数据

**执行时间：**
- AI推单任务：每天21:00执行
- 或者：通过后台管理接口手动触发

**验证SQL：**
```sql
-- 执行 docs/qm-to-qy-timer-task-data-verification.sql
-- 检查是否有 product='qy' 的数据生成
SELECT COUNT(*) FROM pubdb.PUSH_ORDER_CONTENT_MANAGEMENT 
WHERE PRODUCT = 'qy' AND OPERATION_PORT = '2';  -- OPERATION_PORT='2'表示AI生成
```

**时间：** 等待定时任务执行（或手动触发）

---

### 🔴 第四步：代码改造（接口支持qy）

**目的：** 让接口支持qy产品

**执行内容：**

#### 4.1 PushOrderPublicController（7个外部接口）
- 移除硬编码 `product = "at"`
- 添加动态获取 `productCode` 的方法
- 7个接口都改为动态获取

#### 4.2 后台管理接口（4个接口）
- `PushOrderContentManagementController.updateGrantKf`
- `PushOrderContentManagementController.findGrantKf`
- `PushOrderAiUserController.updateGrantKf`
- `PushOrderAiUserController.findGrantKf`

**时间：** 1-2小时

---

### 🟡 第五步：测试验证

**目的：** 验证数据和接口

**测试内容：**
1. 验证配置完整性
2. 验证定时任务数据生成
3. 验证接口返回qy数据
4. 验证数据隔离（qy和at数据不串）

**时间：** 1-2天

---

## ❓ 核心问题：第一步是不是先搞定时任务？

### ✅ 答案：不是！必须先配置，定时任务才能生成数据

**正确理解：**

1. **定时任务不需要改代码** - 定时任务已经支持多产品，只需要配置
2. **必须先配置** - 没有配置，定时任务会跳过qy产品
3. **配置完成后，定时任务自动生效** - 定时任务会读取配置，自动为qy生成数据

**执行顺序：**
```
❌ 错误顺序：
  先改代码 → 再配置 → 定时任务生成数据

✅ 正确顺序：
  先配置 → 系统参数 → 定时任务生成数据 → 再改代码 → 测试验证
```

**为什么必须先配置？**

定时任务执行流程：
```
1. 读取系统参数 PUSHORDER_PRODUCT → 获取产品列表
   → 如果没有qy，直接跳过 ❌

2. 查询AI用户（PUSH_ORDER_AI_USER）
   → 如果没有qy的AI用户，跳过qy产品 ❌

3. 查询价格配置（PUSH_ORDER_PARAM_CONFIG）
   → 如果没有qy的价格配置，推单无法定价 ❌

4. 查询文案配置（PUSH_ORDER_AI_USER_COPYWRITE）
   → 如果没有qy的文案配置，AI无法生成内容 ❌

5. 生成推单 → 插入 PUSH_ORDER_CONTENT_MANAGEMENT
```

**结论：必须先配置，定时任务才能生成qy数据！**

---

## 📋 快速执行清单（按顺序）

### ✅ Step 1: 数据库配置初始化（必须先做！）

**执行文件：** `docs/qm-to-qy-redbill-action.md` - Action 1

**执行内容：**
1. ✅ 推单参数配置（PUSH_ORDER_PARAM_CONFIG）
2. ✅ 等级称号配置（PUSH_ORDER_LEVEL_TITLE_CONFIG）
3. ✅ AI推单用户配置（PUSH_ORDER_AI_USER）⭐ **关键！**
4. ✅ AI用户文案配置（PUSH_ORDER_AI_USER_COPYWRITE）⭐ **关键！**

**验证：** 执行 `docs/qm-to-qy-config-init-verification.sql`

**时间：** 10-15分钟

---

### ✅ Step 2: 系统参数配置

**执行文件：** `docs/qm-to-qy-redbill-action.md` - Action 2

**执行内容：**
```sql
UPDATE pubdb.S_SYSTEM_PARAMETER 
SET VALUE = 'at,qy'
WHERE CATEGORY = 'PUSHORDER' AND CODE = 'PUSHORDER_PRODUCT';
```

**验证：** 查询系统参数，确认包含qy

**时间：** 1分钟

---

### ✅ Step 3: 等待定时任务执行（或手动触发）

**执行方式：**
- 等待定时任务执行（每天21:00）
- 或通过后台管理接口手动触发：`/api/friend/pushOrder/aiUser/backPushOrder`

**验证：** 执行 `docs/qm-to-qy-timer-task-data-verification.sql`

**时间：** 等待执行（或手动触发）

---

### ✅ Step 4: 代码改造

**执行文件：** `docs/qm-to-qy-redbill-action.md` - Action 4

**执行内容：**
1. PushOrderPublicController（7个接口）
2. 后台管理接口（4个接口）

**时间：** 1-2小时

---

### ✅ Step 5: 测试验证

**执行内容：**
1. 验证配置完整性
2. 验证定时任务数据生成
3. 验证接口返回qy数据
4. 验证数据隔离

**时间：** 1-2天

---

## 🎯 总结

### 核心问题答案

**Q: 第一步是不是先搞定时任务，让定时任务生效，把qy的数据先爬下来？**

**A: 不是！必须先配置，定时任务才能生成数据。**

**正确顺序：**
1. ✅ **先配置**（数据库配置初始化 + 系统参数配置）
2. ✅ **定时任务自动生效**（读取配置，自动为qy生成数据）
3. ✅ **再改代码**（接口支持qy）
4. ✅ **最后测试**（验证数据和接口）

**为什么？**
- 定时任务不需要改代码，已经支持多产品
- 但必须先有配置（AI用户、价格、文案），定时任务才能生成数据
- 没有配置，定时任务会跳过qy产品（日志：`没有找到任何启用的推单用户`）

---

## 📋 推荐执行文档

**核心执行文档：**
- ⭐ `docs/qm-to-qy-redbill-action.md` - **Action执行清单**（最详细）

**参考文档：**
- `docs/qm-to-qy-redbill.md` - 技术方案（整体方案）
- `docs/qm-to-qy-redbill-execution-checklist.md` - 执行检查清单（详细检查项）

**验证SQL：**
- `docs/qm-to-qy-config-init-verification.sql` - 配置初始化验证
- `docs/qm-to-qy-timer-task-data-verification.sql` - 定时任务数据验证

