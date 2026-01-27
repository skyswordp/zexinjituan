# qm -> qy 红单复刻 Action 清单

> **执行原则：** 按顺序执行，每项完成后打✅

---

## 📋 配置项说明（为什么需要这些配置？）

| 配置项 | 表名 | 解决什么问题 | 代码位置 | 不配置会怎样 |
|--------|------|------------|---------|------------|
| **1. 系统参数** | `S_SYSTEM_PARAMETER` | **告诉定时任务要为哪些产品生成推单** | `AIPushOrderServiceImpl.java:812` | ❌ 定时任务不会处理qy，直接跳过 |
| **2. AI推单用户** | `PUSH_ORDER_AI_USER` | **定时任务需要知道为哪些用户生成推单** | `AIPushOrderServiceImpl.java:915` | ❌ 没有用户，定时任务会跳过qy产品（日志：`没有找到任何启用的推单用户`） |
| **3. AI用户文案** | `PUSH_ORDER_AI_USER_COPYWRITE` | **AI生成推单时使用的文案模板** | `AIPushOrderServiceImpl.java:1078` | ❌ 没有文案，AI无法生成推单内容，推单生成失败 |
| **4. 推单价格配置** | `PUSH_ORDER_PARAM_CONFIG` | **推单的售价（用户购买红单的价格）** | `AIPushOrderServiceImpl.java:933` | ❌ 没有价格配置，推单无法定价，生成失败 |
| **5. 等级称号配置** | `PUSH_ORDER_LEVEL_TITLE_CONFIG` | **用户等级称号（足球大师/篮球大师）** | 前端展示用 | ⚠️ 不影响定时任务，但前端显示会缺失 |

**定时任务执行流程（代码逻辑）：**
```
1. 读取系统参数（S_SYSTEM_PARAMETER）
   → 获取产品列表 ['at', 'qy']
   → 如果没有qy，直接跳过

2. 循环处理每个产品
   → 查询AI用户（PUSH_ORDER_AI_USER）
   → 如果没有用户，跳过该产品（日志：没有找到任何启用的推单用户）

3. 查询推单价格（PUSH_ORDER_PARAM_CONFIG）
   → 用于给推单定价

4. 查询AI用户文案（PUSH_ORDER_AI_USER_COPYWRITE）
   → AI生成推单内容时使用

5. 生成推单
   → 插入 PUSH_ORDER_CONTENT_MANAGEMENT 表
```

**执行流程：**
```
定时任务启动
  ↓
读取系统参数（S_SYSTEM_PARAMETER）→ 获取产品列表 ['at', 'qy']
  ↓
循环处理每个产品
  ↓
查询AI用户（PUSH_ORDER_AI_USER）→ 如果没有用户，跳过该产品
  ↓
查询推单价格（PUSH_ORDER_PARAM_CONFIG）→ 如果没有价格，推单无法定价
  ↓
查询AI用户文案（PUSH_ORDER_AI_USER_COPYWRITE）→ 如果没有文案，AI无法生成内容
  ↓
生成推单 → 插入 PUSH_ORDER_CONTENT_MANAGEMENT 表
```

---

## 🔴 必须执行（5项配置 + 1项代码改造）

### ✅ Action 1: 数据库配置初始化（3个表）

**执行位置：** 数据库客户端（Query1.sql）

#### 1.1 推单参数配置
```sql
INSERT INTO pubdb.PUSH_ORDER_PARAM_CONFIG (
    PRODUCT, TYPE, USER_LEVEL, PRICE, CREATE_TIME, OPERATOR, OPERATOR_TIME, DEL
)
SELECT 
    'qy' AS PRODUCT,
    TYPE, USER_LEVEL, PRICE,
    SYSDATE AS CREATE_TIME,
    'system' AS OPERATOR,
    SYSDATE AS OPERATOR_TIME,
    DEL
FROM pubdb.PUSH_ORDER_PARAM_CONFIG
WHERE PRODUCT = 'at' AND DEL = '0';
```

**验证：**
```sql
SELECT COUNT(*) FROM pubdb.PUSH_ORDER_PARAM_CONFIG WHERE PRODUCT='qy';
```

#### 1.2 等级称号配置
```sql
INSERT INTO pubdb.PUSH_ORDER_LEVEL_TITLE_CONFIG (
    PRODUCT, TYPE, LEVEL, TITLE, SORT, CREATE_TIME, OPERATOR, OPERATOR_TIME, DEL
)
SELECT 
    'qy' AS PRODUCT,
    TYPE, LEVEL, TITLE, SORT,
    SYSDATE AS CREATE_TIME,
    'system' AS OPERATOR,
    SYSDATE AS OPERATOR_TIME,
    DEL
FROM pubdb.PUSH_ORDER_LEVEL_TITLE_CONFIG
WHERE PRODUCT = 'at' AND DEL = '0';
```

**验证：**
```sql
SELECT COUNT(*) FROM pubdb.PUSH_ORDER_LEVEL_TITLE_CONFIG WHERE PRODUCT='qy';
```

#### 1.3 AI推单用户配置（关键！）
```sql
-- 复制qm（at）的AI用户配置到qy
INSERT INTO pubdb.PUSH_ORDER_AI_USER (
    ID, USER_NAME, PRODUCT, PUSH_QUANTITY, STATUS, CREATE_TIME, CREATE_BY,
    MATCH_TYPE, HANDICAP_ITEM, LEAGUE_ID, USER_TYPE, SKIP_APPROVE, PUSH_SERIES_QUANTITY
)
SELECT 
    SEQ_PUSH_ORDER_AI_USER.NEXTVAL,
    USER_NAME,
    'qy' AS PRODUCT,
    PUSH_QUANTITY,
    STATUS,
    SYSDATE AS CREATE_TIME,
    'system' AS CREATE_BY,
    MATCH_TYPE,
    HANDICAP_ITEM,
    LEAGUE_ID,
    USER_TYPE,
    SKIP_APPROVE,
    PUSH_SERIES_QUANTITY
FROM pubdb.PUSH_ORDER_AI_USER
WHERE PRODUCT = 'at' AND STATUS = 0;
```

**验证：**
```sql
SELECT COUNT(*) FROM pubdb.PUSH_ORDER_AI_USER WHERE PRODUCT='qy' AND STATUS=0;
```

#### 1.4 AI用户文案配置（关键！）
```sql
-- 复制qm（at）的AI用户文案配置到qy
-- 注意：需要先执行1.3，获取新插入的qy用户ID
INSERT INTO pubdb.PUSH_ORDER_AI_USER_COPYWRITE (
    CWID, POAUID, MATCH_TYPE, HANDICAP, AI_TYPE, COPYWRITE, HANDICAP_TYPE
)
SELECT 
    SEQ_PUSH_ORDER_AI_USER_COPYWRITE.NEXTVAL,
    qy_user.ID AS POAUID,  -- 使用qy用户的新ID
    at_copywrite.MATCH_TYPE,
    at_copywrite.HANDICAP,
    at_copywrite.AI_TYPE,
    at_copywrite.COPYWRITE,
    at_copywrite.HANDICAP_TYPE
FROM pubdb.PUSH_ORDER_AI_USER_COPYWRITE at_copywrite
INNER JOIN pubdb.PUSH_ORDER_AI_USER at_user 
    ON at_copywrite.POAUID = at_user.ID
INNER JOIN pubdb.PUSH_ORDER_AI_USER qy_user 
    ON at_user.USER_NAME = qy_user.USER_NAME 
    AND qy_user.PRODUCT = 'qy'
WHERE at_user.PRODUCT = 'at';
```

**验证：**
```sql
SELECT COUNT(*) FROM pubdb.PUSH_ORDER_AI_USER_COPYWRITE cw
INNER JOIN pubdb.PUSH_ORDER_AI_USER u ON cw.POAUID = u.ID
WHERE u.PRODUCT = 'qy';
```

---

### ✅ Action 2: AI用户文案配置（关键！）

**执行位置：** 数据库客户端（Query1.sql）

**说明：** AI生成推单时需要文案模板，没有文案无法生成推单内容

```sql
-- 复制qm（at）的AI用户文案配置到qy
-- 注意：必须先执行1.3（AI用户配置），获取新插入的qy用户ID
INSERT INTO pubdb.PUSH_ORDER_AI_USER_COPYWRITE (
    CWID, POAUID, MATCH_TYPE, HANDICAP, AI_TYPE, COPYWRITE, HANDICAP_TYPE
)
SELECT 
    SEQ_PUSH_ORDER_AI_USER_COPYWRITE.NEXTVAL,
    qy_user.ID AS POAUID,  -- 使用qy用户的新ID
    at_copywrite.MATCH_TYPE,
    at_copywrite.HANDICAP,
    at_copywrite.AI_TYPE,
    at_copywrite.COPYWRITE,
    at_copywrite.HANDICAP_TYPE
FROM pubdb.PUSH_ORDER_AI_USER_COPYWRITE at_copywrite
INNER JOIN pubdb.PUSH_ORDER_AI_USER at_user 
    ON at_copywrite.POAUID = at_user.ID
INNER JOIN pubdb.PUSH_ORDER_AI_USER qy_user 
    ON at_user.USER_NAME = qy_user.USER_NAME 
    AND qy_user.PRODUCT = 'qy'
WHERE at_user.PRODUCT = 'at';
```

**验证：**
```sql
SELECT COUNT(*) FROM pubdb.PUSH_ORDER_AI_USER_COPYWRITE cw
INNER JOIN pubdb.PUSH_ORDER_AI_USER u ON cw.POAUID = u.ID
WHERE u.PRODUCT = 'qy';
```

---

### ✅ Action 3: 系统参数配置

**执行位置：** 数据库客户端（Query1.sql）

```sql
-- 查询当前值
SELECT CATEGORY, CODE, VALUE 
FROM pubdb.S_SYSTEM_PARAMETER
WHERE CATEGORY = 'PUSHORDER' AND CODE = 'PUSHORDER_PRODUCT';

-- 更新配置（添加qy）
UPDATE pubdb.S_SYSTEM_PARAMETER 
SET VALUE = VALUE || ',qy',
    UPDATE_TIME = SYSDATE
WHERE CATEGORY = 'PUSHORDER'
  AND CODE = 'PUSHORDER_PRODUCT'
  AND VALUE NOT LIKE '%qy%';
```

**验证：**
```sql
SELECT VALUE FROM pubdb.S_SYSTEM_PARAMETER 
WHERE CATEGORY = 'PUSHORDER' AND CODE = 'PUSHORDER_PRODUCT';
-- 结果应包含 'qy'
```

---

### ✅ Action 4: 代码改造 - PushOrderPublicController

**执行位置：** `DC-API-2018/dc-api/dc-api-office/src/main/java/com/dc/it/friend/controller/PushOrderPublicController.java`

#### 3.1 删除第40行硬编码
```java
// 删除这行
private String product = "at";//对外的就查AT的
```

#### 3.2 添加方法（放在类中任意位置）
```java
private String getProductCode(HttpServletRequest request, Map<String, Object> map) {
    if (map != null && map.containsKey("productCode")) {
        String productCode = (String) map.get("productCode");
        if (StringUtils.isNotBlank(productCode)) {
            return productCode;
        }
    }
    String headerProduct = request.getHeader("productCode");
    if (StringUtils.isNotBlank(headerProduct)) {
        return headerProduct;
    }
    return "at";  // 默认值，兼容老调用
}
```

#### 3.3 修改7个接口方法
在每个方法中，找到：
```java
map.put("product", product);
```
改为：
```java
String product = getProductCode(request, map);
map.put("product", product);
```

**涉及方法：**
- `findPersonalInfoPageList` (约第81行)
- `findMasterDetailed` (约第102行)
- `findPushUserInfo` (约第120行)
- `findMonthlyRankingPageList` (约第138行)
- `findPlanDetailed` (约第158行)
- `findProgrammePreferredPageList` (约第177行)
- `findMatchPreferredPageList` (约第195行)

**验证：** 编译通过，无语法错误

---

### ✅ Action 5: 代码确认 - PushOrderInsideController

**执行位置：** `DC-API-2018/dc-api/dc-api-friend/src/main/java/com/dc/it/controller/PushOrderInsideContoller.java`

**第90行代码：**
```java
if ("at".equalsIgnoreCase(product)){
    int userLevel=Integer.parseInt((String)map.get("userLevel"));
    if (userLevel<1){
        return resultMap(ErrorCode.SC_20000.getCode(),"VIP1以上才可以购买",null);
    }
}
```

**执行动作：**
- [ ] 与产品/业务确认：qy产品是否需要VIP1限制？
- [ ] 如果需要：修改为 `if ("at".equalsIgnoreCase(product) || "qy".equalsIgnoreCase(product))`
- [ ] 如果不需要：保持现状，无需修改

---

## 🟡 验证执行（2项）

### ✅ Action 6: 验证配置完整性

**执行位置：** 数据库客户端（Query1.sql）

```sql
-- 综合验证
SELECT '推单参数配置' AS item, COUNT(*) AS qy_count
FROM pubdb.PUSH_ORDER_PARAM_CONFIG WHERE PRODUCT='qy'
UNION ALL
SELECT '等级称号配置', COUNT(*)
FROM pubdb.PUSH_ORDER_LEVEL_TITLE_CONFIG WHERE PRODUCT='qy'
UNION ALL
SELECT 'AI推单用户', COUNT(*)
FROM pubdb.PUSH_ORDER_AI_USER WHERE PRODUCT='qy' AND STATUS=0
UNION ALL
SELECT '系统参数', 
    CASE WHEN VALUE LIKE '%qy%' THEN 1 ELSE 0 END
FROM pubdb.S_SYSTEM_PARAMETER 
WHERE CATEGORY='PUSHORDER' AND CODE='PUSHORDER_PRODUCT';
```

**预期结果：** 前3项数量 > 0，最后1项 = 1

---

### ✅ Action 7: 验证定时任务数据生成

**执行位置：** 数据库客户端（Query1.sql）

**等待时间：** 定时任务每天21:00执行，执行后验证

```sql
-- 验证qy是否有AI生成的推单
SELECT 
    PRODUCT,
    COUNT(*) AS total,
    COUNT(CASE WHEN OPERATION_PORT='2' THEN 1 END) AS ai_generated,
    MAX(CREATE_TIME) AS last_create_time
FROM pubdb.PUSH_ORDER_CONTENT_MANAGEMENT
WHERE PRODUCT IN ('at', 'qy')
GROUP BY PRODUCT;
```

**预期结果：** qy的 `ai_generated` > 0

---

## 📋 执行顺序

1. ✅ Action 1: 数据库配置初始化（4个表）
   - 1.1 推单参数配置
   - 1.2 等级称号配置
   - 1.3 AI推单用户配置（关键！）
   - 1.4 AI用户文案配置（关键！）
2. ✅ Action 2: AI用户文案配置（必须在1.3之后执行）
3. ✅ Action 3: 系统参数配置
4. ✅ Action 4: 代码改造
5. ✅ Action 5: 代码确认
6. ✅ Action 6: 验证配置完整性
7. ✅ Action 7: 验证定时任务数据生成（等待21:00执行后）

---

## ⚠️ 关键点

1. **系统参数必须包含qy** - 定时任务从这里读取产品列表，没有qy直接跳过
2. **AI推单用户配置必须要有** - 没有用户，定时任务会跳过qy产品（日志：`没有找到任何启用的推单用户`）
3. **AI用户文案配置必须要有** - 没有文案，AI无法生成推单内容，推单生成失败
4. **推单价格配置必须要有** - 没有价格，推单无法定价，生成失败
5. **代码改造必须完成** - 否则7个对外接口不支持qy
6. **定时任务执行时间** - 每天21:00，需要等待执行后才能验证数据

---

## ✅ 最终确认清单

**所有定时任务已检查：**
- ✅ AI推单（每天21:00）
- ✅ AI补救推单（每天23:00）
- ✅ AI补单（每天00:00:01）
- ✅ 用户火标设置（每月5号00:00）
- ✅ AI真实推单（每天20:00）
- ✅ 红单结算（每3分钟）

**结论：所有定时任务都只依赖这5个配置项，无需其他配置。**

