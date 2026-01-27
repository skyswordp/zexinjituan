# 定时任务操作的表总结（qm -> qy 验证）

## 问题1：定时任务总共操作哪些表？

### 主要操作的表（写入）

| 表名 | 操作类型 | 代码位置 | 说明 |
|------|---------|---------|------|
| **PUSH_ORDER_CONTENT_MANAGEMENT** | INSERT | `AIPushOrderServiceImpl.java:1364` | ⭐ **核心表**：定时任务生成的推单数据插入到这里 |

### 查询的表（只读）

| 表名 | 查询目的 | 代码位置 | 说明 |
|------|---------|---------|------|
| **S_SYSTEM_PARAMETER** | 获取产品列表 | `AIPushOrderServiceImpl.java:78` | 查询 `PUSHORDER_PRODUCT` 参数，获取需要生成推单的产品列表 |
| **PUSH_ORDER_AI_USER** | 查询AI推单用户 | `AIPushOrderServiceImpl.java:915` | 查询每个产品下的AI推单用户配置 |
| **PUSH_ORDER_PARAM_CONFIG** | 查询推单价格 | `AIPushOrderServiceImpl.java:933` | 查询每个产品下的推单价格配置 |
| **F_USER** | 查询用户信息 | 间接查询 | AI用户信息（可能通过其他DAO查询） |
| **赛事相关表** | 查询未来比赛 | `AIPushOrderServiceImpl.java:823` | 查询未来第2天的足球/篮球比赛 |

### 总结

**写入操作：只有1个表**
- ✅ `PUSH_ORDER_CONTENT_MANAGEMENT` - 插入推单数据

**查询操作：多个表**
- `S_SYSTEM_PARAMETER` - 系统参数
- `PUSH_ORDER_AI_USER` - AI用户配置
- `PUSH_ORDER_PARAM_CONFIG` - 推单价格配置
- 赛事相关表 - 比赛数据

---

## 问题2：为什么查询结果只有 at，没有 qy？

### 可能的原因

#### 1. 系统参数未配置 qy（最可能）
- **检查点：** `S_SYSTEM_PARAMETER` 表中 `PUSHORDER_PRODUCT` 参数是否包含 `qy`
- **代码逻辑：** `AIPushOrderServiceImpl.java:812` - 从系统参数获取产品列表
- **如果未配置：** 定时任务不会为 qy 生成推单

#### 2. qy 产品没有AI推单用户
- **检查点：** `PUSH_ORDER_AI_USER` 表中是否有 `product='qy'` 且 `status=0` 的用户
- **代码逻辑：** `AIPushOrderServiceImpl.java:915-920` - 如果没有AI用户，会跳过该产品
- **日志提示：** `"系统生成推单【直接跳过】，原因：没有找到任何启用的推单用户"`

#### 3. qy 产品没有推单价格配置
- **检查点：** `PUSH_ORDER_PARAM_CONFIG` 表中是否有 `product='qy'` 的配置
- **代码逻辑：** `AIPushOrderServiceImpl.java:933` - 查询推单价格配置

#### 4. 定时任务还未执行
- **执行时间：** 每天21:00
- **如果当前时间未到21:00：** 今天的数据还未生成

#### 5. 定时任务执行失败
- **需要查看日志：** 检查定时任务执行日志是否有错误

---

## 验证 SQL（快速检查）

```sql
-- ==========================================
-- 1. 检查系统参数（最关键）
-- ==========================================
SELECT 
    VALUE,
    CASE 
        WHEN VALUE LIKE '%qy%' THEN '✅ qy已配置'
        ELSE '❌ qy未配置（定时任务不会为qy生成推单）'
    END AS status
FROM pubdb.S_SYSTEM_PARAMETER
WHERE CATEGORY = 'PUSHORDER'
  AND CODE = 'PUSHORDER_PRODUCT';

-- ==========================================
-- 2. 检查AI推单用户配置
-- ==========================================
SELECT 
    PRODUCT,
    COUNT(*) AS ai_user_count
FROM pubdb.PUSH_ORDER_AI_USER
WHERE PRODUCT IN ('at', 'qy')
  AND STATUS = 0  -- 启用状态
GROUP BY PRODUCT
ORDER BY PRODUCT;

-- ==========================================
-- 3. 检查推单价格配置
-- ==========================================
SELECT 
    PRODUCT,
    COUNT(*) AS price_config_count
FROM pubdb.PUSH_ORDER_PARAM_CONFIG
WHERE PRODUCT IN ('at', 'qy')
GROUP BY PRODUCT
ORDER BY PRODUCT;

-- ==========================================
-- 4. 检查推单数据（最终结果）
-- ==========================================
SELECT 
    PRODUCT,
    COUNT(*) AS total,
    COUNT(CASE WHEN OPERATION_PORT = '2' THEN 1 END) AS ai_generated
FROM pubdb.PUSH_ORDER_CONTENT_MANAGEMENT
WHERE PRODUCT IN ('at', 'qy')
GROUP BY PRODUCT
ORDER BY PRODUCT;
```

---

## 结论

### 问题1答案
**定时任务主要操作1个表（写入）：**
- `PUSH_ORDER_CONTENT_MANAGEMENT` - 插入推单数据

**查询多个表（只读）：**
- 系统参数、AI用户配置、推单价格配置、赛事数据等

### 问题2答案
**查询结果只有 at 没有 qy，说明：**
1. ✅ **最可能：系统参数未配置 qy** → 定时任务不会为 qy 生成推单
2. ⚠️ **可能：qy 没有AI推单用户配置** → 定时任务会跳过 qy
3. ⚠️ **可能：定时任务还未执行** → 今天的数据还未生成

**建议：先执行上面的验证SQL，按顺序检查每个环节。**

