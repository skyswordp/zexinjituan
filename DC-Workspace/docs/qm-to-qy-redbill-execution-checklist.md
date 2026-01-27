# qm -> qy 红单复刻执行路径清单（100%覆盖）

> **目标：** 确保qy产品完整支持红单功能，与qm产品数据隔离  
> **执行原则：** 按顺序执行，每项完成后打✅，确保100%覆盖

---

## 📋 执行路径总览

| 序号 | 检查项 | 优先级 | 状态 | 是否需要改造 | 量化说明 |
|------|--------|--------|------|------------|----------|
| 1 | 配置初始化（SQL脚本） | 🔴 必须 | ⬜ | ✅ 需要 | 2个表，2条SQL |
| 2 | 系统参数配置 | 🔴 必须 | ⬜ | ✅ 需要 | 1个参数，1条SQL |
| 3 | 代码改造（PushOrderPublicController） | 🔴 必须 | ⬜ | ✅ 需要 | 1个文件，7个接口，移除硬编码 |
| 4 | 代码确认（PushOrderInsideController） | 🟡 建议 | ⬜ | ⚠️ 需确认 | 1个文件，1处逻辑，确认VIP限制 |
| 5 | 代码验证（PushOrderExternalController） | 🟡 建议 | ⬜ | ❌ 不需要 | 1个文件，18个接口，已支持多产品 |
| 6 | 废弃接口检查 | 🟢 可选 | ⬜ | ⚠️ 需确认 | 1个接口，确认是否使用 |
| 7 | 后台管理接口验证 | 🟡 建议 | ⬜ | ❌ 不需要 | 5个Controller，已支持多产品 |
| 8 | 定时任务验证 | 🟡 建议 | ⬜ | ❌ 不需要 | 2个任务，已支持多产品 |
| 9 | 数据库表检查 | 🟡 建议 | ⬜ | ❌ 不需要 | 7个表，确认有product字段 |
| 10 | DAO层SQL检查 | 🟡 建议 | ⬜ | ❌ 不需要 | 6个DAO文件，确认按product过滤 |
| 11 | 后台管理界面检查 | 🟡 建议 | ⬜ | ❌ 不需要 | 5个页面，确认支持qy |
| 12 | 三方接口调用检查 | 🟢 可选 | ⬜ | ❌ 不需要 | 确认外部系统调用情况 |

**图例：**
- ✅ 需要改造：必须修改代码/配置
- ⚠️ 需确认：需要业务确认或检查是否使用
- ❌ 不需要改造：已支持多产品，只需验证

---

## ✅ 1. 配置初始化（SQL脚本）

### 1.1 推单参数配置初始化

**文件：** 执行SQL脚本  
**表：** `PUSH_ORDER_PARAM_CONFIG`  
**操作：** 复制qm（at）的配置到qy

**SQL脚本：**
```sql
-- 复制qm（at）的推单参数配置到qy
INSERT INTO PUSH_ORDER_PARAM_CONFIG (
    PRODUCT, TYPE, USER_LEVEL, PRICE, CREATE_TIME, OPERATOR, OPERATOR_TIME, DEL
)
SELECT 
    'qy' AS PRODUCT,  -- 改为qy
    TYPE, 
    USER_LEVEL, 
    PRICE, 
    SYSDATE AS CREATE_TIME, 
    'system' AS OPERATOR, 
    SYSDATE AS OPERATOR_TIME, 
    DEL
FROM PUSH_ORDER_PARAM_CONFIG
WHERE PRODUCT = 'at'  -- 从qm（at）复制
AND DEL = '0';
```

**检查点：**
- [ ] SQL执行成功
- [ ] 查询确认qy配置已创建：`SELECT * FROM PUSH_ORDER_PARAM_CONFIG WHERE PRODUCT='qy'`
- [ ] 配置项数量与qm（at）一致

---

### 1.2 等级称号配置初始化

**文件：** 执行SQL脚本  
**表：** `PUSH_ORDER_LEVEL_TITLE_CONFIG`  
**操作：** 复制qm（at）的配置到qy

**SQL脚本：**
```sql
-- 复制qm（at）的等级称号配置到qy
INSERT INTO PUSH_ORDER_LEVEL_TITLE_CONFIG (
    PRODUCT, TYPE, LEVEL, TITLE, SORT, CREATE_TIME, OPERATOR, OPERATOR_TIME, DEL
)
SELECT 
    'qy' AS PRODUCT,  -- 改为qy
    TYPE, 
    LEVEL, 
    TITLE, 
    SORT, 
    SYSDATE AS CREATE_TIME, 
    'system' AS OPERATOR, 
    SYSDATE AS OPERATOR_TIME, 
    DEL
FROM PUSH_ORDER_LEVEL_TITLE_CONFIG
WHERE PRODUCT = 'at'  -- 从qm（at）复制
AND DEL = '0';
```

**检查点：**
- [ ] SQL执行成功
- [ ] 查询确认qy配置已创建：`SELECT * FROM PUSH_ORDER_LEVEL_TITLE_CONFIG WHERE PRODUCT='qy'`
- [ ] 配置项数量与qm（at）一致

---

## ✅ 2. 系统参数配置

**文件：** 数据库表 `SYSTEM_PARAMETER`  
**参数名：** `PUSHORDER_PRODUCT`  
**操作：** 添加qy到产品列表

**当前值（示例）：** `at,ql,uf`  
**修改后：** `at,ql,uf,qy`

**SQL脚本：**
```sql
-- 查询当前配置
SELECT * FROM SYSTEM_PARAMETER WHERE PARAMETER_NAME = 'PUSHORDER_PRODUCT';

-- 更新配置（添加qy）
UPDATE SYSTEM_PARAMETER 
SET PARAMETER_VALUE = PARAMETER_VALUE || ',qy'
WHERE PARAMETER_NAME = 'PUSHORDER_PRODUCT'
AND PARAMETER_VALUE NOT LIKE '%qy%';  -- 避免重复添加

-- 验证
SELECT * FROM SYSTEM_PARAMETER WHERE PARAMETER_NAME = 'PUSHORDER_PRODUCT';
```

**检查点：**
- [ ] 查询确认当前值
- [ ] 执行更新SQL
- [ ] 验证qy已添加到参数值中
- [ ] 确认参数值格式正确（逗号分隔）

---

## ✅ 3. 代码改造：PushOrderPublicController

**文件：** `DC-API-2018/dc-api/dc-api-office/src/main/java/com/dc/it/friend/controller/PushOrderPublicController.java`  
**问题：** 第40行硬编码 `private String product = "at"`  
**操作：** 移除硬编码，支持动态获取productCode

### 3.1 修改步骤

**步骤1：删除硬编码**
```java
// 删除这行
private String product = "at";//对外的就查AT的
```

**步骤2：添加获取产品代码方法**
```java
/**
 * 获取产品代码
 * 优先级：请求参数 productCode > header productCode > 默认值 "at"（兼容老调用）
 */
private String getProductCode(HttpServletRequest request, Map<String, Object> map) {
    // 1. 优先从请求参数获取
    if (map != null && map.containsKey("productCode")) {
        String productCode = (String) map.get("productCode");
        if (StringUtils.isNotBlank(productCode)) {
            return productCode;
        }
    }
    
    // 2. 从header获取
    String headerProduct = request.getHeader("productCode");
    if (StringUtils.isNotBlank(headerProduct)) {
        return headerProduct;
    }
    
    // 3. 默认值（兼容老调用）
    return "at";
}
```

**步骤3：修改所有接口方法**
在每个接口方法中，将：
```java
map.put("product", product);
```
改为：
```java
String product = getProductCode(request, map);
map.put("product", product);
```

**涉及接口（7个）：**
1. `findPersonalInfoPageList` - 第81行
2. `findMasterDetailed` - 第102行
3. `findPushUserInfo` - 第120行
4. `findMonthlyRankingPageList` - 第138行
5. `findPlanDetailed` - 第158行
6. `findProgrammePreferredPageList` - 第177行
7. `findMatchPreferredPageList` - 第195行

### 3.2 检查点

- [ ] 删除硬编码 `product = "at"`
- [ ] 添加 `getProductCode` 方法
- [ ] 修改7个接口方法，使用动态product
- [ ] 编译通过，无语法错误
- [ ] 代码review通过

---

## ✅ 4. 代码确认：PushOrderInsideController（需确认）

**文件：** `DC-API-2018/dc-api/dc-api-friend/src/main/java/com/dc/it/controller/PushOrderInsideContoller.java`  
**路径：** `/api/friend/pushOrder/inside/1.0/`  
**接口数量：** 4个  
**状态：** ✅ 已支持多产品，但**有qm特殊逻辑需要确认**  
**是否需要改造：** ⚠️ 需确认（取决于业务需求）

**文件：** `DC-API-2018/dc-api/dc-api-friend/src/main/java/com/dc/it/controller/PushOrderInsideContoller.java`  
**问题：** 第90行硬编码VIP限制逻辑  
**操作：** 确认qy产品的VIP限制要求

### 4.1 当前代码

```java
//球盟需求 VIP1以上的才可以购买
if ("at".equalsIgnoreCase(product)){
    int userLevel=Integer.parseInt((String)map.get("userLevel"));
    if (userLevel<1){
        return resultMap(ErrorCode.SC_20000.getCode(),"VIP1以上才可以购买",null);
    }
}
```

### 4.2 确认选项

**选项A：qy也需要VIP限制**
```java
if ("at".equalsIgnoreCase(product) || "qy".equalsIgnoreCase(product)){
    int userLevel=Integer.parseInt((String)map.get("userLevel"));
    if (userLevel<1){
        return resultMap(ErrorCode.SC_20000.getCode(),"VIP1以上才可以购买",null);
    }
}
```

**选项B：qy不需要VIP限制**
- 保持现状，qy产品不检查VIP等级

**选项C：qy有不同限制**
- 需要确认qy的VIP要求，单独处理

### 4.3 检查点

- [ ] 与产品/业务确认qy的VIP限制要求
- [ ] 根据确认结果修改代码（如需要）
- [ ] 编译通过，无语法错误

---

## ✅ 5. 废弃接口检查

**文件：** `DC-API-2018/dc-api/dc-api-office/src/main/java/com/dc/it/friend/controller/PushOrderContentManagementController.java`  
**接口：** `openPushOrderData`（第52行，@Deprecated）  
**问题：** 第87行硬编码 `map.put("product","at")`

### 5.1 处理方案

**选项A：接口已废弃，忽略**
- 接口标记为@Deprecated，可能已不再使用
- 建议：保持现状，不修改

**选项B：接口仍在使用，需要改造**
```java
// 修改第87行
String product = getProductCode(request, map);  // 需要添加getProductCode方法
map.put("product", product);
```

### 5.2 检查点

- [ ] 确认接口是否仍在使用（查看调用日志/代码搜索）
- [ ] 如仍在使用，按选项B改造
- [ ] 如已废弃，记录说明

---

## ✅ 5. 代码验证：PushOrderExternalController（不需要改造）

**文件：** `DC-API-2018/dc-api/dc-api-friend/src/main/java/com/dc/it/controller/PushOrderExternalContoller.java`  
**路径：** `/api/friend/pushOrder/external/1.0/`  
**接口数量：** 18个  
**状态：** ✅ 已支持多产品（从header获取product）  
**是否需要改造：** ❌ 不需要

### 5.1 代码检查

**验证点：** 所有接口都从header获取product，无硬编码

**代码证据：**
```java
// 所有接口都使用这种方式获取product（第47行等）
String product = this.getProduct(request);//产品编号
```

**18个接口列表：**
1. `findPersonalInfoPageList` - 大师列表
2. `findMonthlyRankingFirstList` - 首页月榜
3. `findMonthlyRankingPageList` - 月榜列表
4. `findMyAttentionPageList` - 我的关注
5. `findMatchPreferredPageList` - 赛事优选
6. `findMatchPreferredProgrammePageList` - 赛事优选方案
7. `findProgrammePreferredPageList` - 方案优选
8. `findMyPurchasePageList` - 我的购买
9. `pushOrderClickReceive` - 推单点击统计
10. `findPlanDetailed` - 方案详细
11. `findMasterDetailed` - 大师详细
12. `releasePushOrderContent` - 发布推单
13. `findMyPushOrderRecord` - 我的推单记录
14. `findMyPushOrderRecordDetailed` - 推单记录详细
15. `findProgrammePreferredEntity` (v1.0) - 方案优选实体（APP）
16. `findProgrammePreferredEntity` (v1.1) - 方案优选实体（PC）
17. `findPushOrderEventUEDSpecialSubject` - UED专题查询
18. `findPushOrderFiveEvent` - 5大赛事查询

### 5.2 验证步骤

**代码检查：**
- [ ] 确认所有18个接口都使用 `this.getProduct(request)` 获取product
- [ ] 确认无硬编码 `product = "at"` 或类似代码
- [ ] 确认所有接口都正确传递product到Service层

**功能测试（可选，建议执行）：**
- [ ] `findPersonalInfoPageList` - 使用productCode='qy'测试
- [ ] `findMonthlyRankingPageList` - 使用productCode='qy'测试
- [ ] `findPlanDetailed` - 使用productCode='qy'测试
- [ ] `releasePushOrderContent` - 使用productCode='qy'测试
- [ ] 数据隔离验证（qy数据不包含qm数据）

### 5.3 检查点

- [ ] 代码review确认支持多产品（无硬编码）
- [ ] 功能测试通过（使用productCode='qy'）
- [ ] 数据隔离验证通过

---

## ✅ 6. 废弃接口检查

---

## ✅ 7. 后台管理接口验证（不需要改造）

**说明：** 后台管理Controller已支持多产品（使用`getOperatorProductCode(request)`），只需验证

**Controller列表（5个）：**
1. `PushOrderContentManagementController` - 推单内容管理
2. `PushOrderParamConfigController` - 推单参数配置
3. `PushOrderLevelTitleConfigController` - 等级称号配置
4. `PushOrderAiUserController` - AI用户管理
5. `PushOrderPermissionRecordController` - 权限记录

**是否需要改造：** ❌ 不需要（已支持多产品）

**Controller列表：**
1. `PushOrderContentManagementController` - 推单内容管理
2. `PushOrderParamConfigController` - 推单参数配置
3. `PushOrderLevelTitleConfigController` - 等级称号配置
4. `PushOrderAiUserController` - AI用户管理
5. `PushOrderPermissionRecordController` - 权限记录

### 7.1 验证步骤

**检查所有Controller是否使用 `getOperatorProductCode(request)`：**

```java
// 正确示例（PushOrderParamConfigController）
pushOrderParamConfig.setProduct(getOperatorProductCode(request));
```

**检查点：**
- [ ] `PushOrderContentManagementController` - 确认使用getOperatorProductCode
- [ ] `PushOrderParamConfigController` - 确认使用getOperatorProductCode
- [ ] `PushOrderLevelTitleConfigController` - 确认使用getOperatorProductCode
- [ ] `PushOrderAiUserController` - 确认使用getOperatorProductCode
- [ ] `PushOrderPermissionRecordController` - 确认使用getOperatorProductCode

### 7.2 功能测试

- [ ] 后台登录qy产品账号
- [ ] 测试推单内容管理（查询、审核、删除）
- [ ] 测试推单参数配置（查询、修改）
- [ ] 测试等级称号配置（查询、修改）
- [ ] 测试AI用户管理（查询、创建推单）
- [ ] 确认数据隔离（qy后台只能看到qy数据）

---

## ✅ 8. 定时任务验证（不需要改造）

**说明：** 定时任务已支持多产品，通过系统参数配置，只需验证

**是否需要改造：** ❌ 不需要（已支持多产品）

### 8.1 AI推单任务

**文件：** `DC-API-2018/dc-api/dc-api-office/src/main/java/com/dc/it/friend/quartz/AIPushOrderTask.java`  
**状态：** ✅ 已支持多产品，通过系统参数 `PUSHORDER_PRODUCT` 配置

**验证步骤：**
1. 确认系统参数 `PUSHORDER_PRODUCT` 包含qy（已在步骤2完成）
2. 查看定时任务日志，确认qy产品被处理

**检查点：**
- [ ] 系统参数已包含qy
- [ ] 定时任务日志显示qy产品被处理
- [ ] qy产品成功生成AI推单

### 8.2 红单结算任务

**文件：** `DC-API-2018/dc-api/dc-api-sportcron/src/main/resources/mapper/ob/OBEventDao.xml`  
**方法：** `queryObMatchDataList`  
**状态：** ⚠️ SQL未按product过滤，但不影响功能（更新时按ID更新）

**检查点：**
- [ ] 确认SQL查询逻辑（虽然不按product过滤，但更新时按ID更新，不影响数据隔离）
- [ ] 查看结算任务日志，确认qy红单正常结算

---

## ✅ 9. 数据库表检查（不需要改造）

**说明：** 所有表都有product字段，只需确认

**是否需要改造：** ❌ 不需要（表结构已支持）

**需要检查的表：**

| 表名 | 是否有product字段 | 状态 |
|------|------------------|------|
| `PUSH_ORDER_CONTENT_MANAGEMENT` | ✅ 有 | 核心表 |
| `PUSH_ORDER_PARAM_CONFIG` | ✅ 有 | 配置表 |
| `PUSH_ORDER_LEVEL_TITLE_CONFIG` | ✅ 有 | 配置表 |
| `PUSH_ORDER_AI_USER` | ✅ 有 | AI用户表 |
| `PUSH_ORDER_PERMISSION_RECORD` | ✅ 有 | 权限记录表 |
| `PUSH_ORDER_CONTENT_GENERAL_LOG` | ✅ 有 | 日志表 |
| `F_USER` | ✅ 有 | 用户表（间接隔离） |

**检查点：**
- [ ] 确认所有表都有product字段
- [ ] 确认product字段类型正确（VARCHAR2）
- [ ] 确认product字段有索引（如需要）

---

## ✅ 10. DAO层SQL检查（不需要改造）

**说明：** DAO层SQL已按product过滤，只需确认

**是否需要改造：** ❌ 不需要（SQL已支持多产品）

**需要检查的DAO文件：**

1. `PushOrderContentManagementDao.xml`
2. `PushOrderParamConfigDao.xml`
3. `PushOrderLevelTitleConfigDao.xml`
4. `PushOrderAiUserDao.xml`
5. `PushOrderPermissionRecordDao.xml`
6. `PushOrderContentGeneralLogDao.xml`

**检查点：**
- [ ] 所有SELECT查询都包含 `WHERE product = #{product}`
- [ ] 所有INSERT都包含 `product` 字段
- [ ] 所有UPDATE都包含 `WHERE product = #{product}`
- [ ] 所有DELETE都包含 `WHERE product = #{product}`

**示例检查：**
```xml
<!-- 正确示例 -->
<select id="findList" resultType="...">
    SELECT ... FROM PUSH_ORDER_PARAM_CONFIG
    WHERE product = #{product}
    AND del = '0'
</select>
```

---

## ✅ 11. 后台管理界面检查（不需要改造）

**说明：** 后台管理界面已支持多产品，只需验证

**是否需要改造：** ❌ 不需要（界面已支持多产品）

**模块：** `dc-modules-office`  
**需要检查的页面：**

1. 推单内容管理页面
2. 推单参数配置页面
3. 等级称号配置页面
4. AI用户管理页面
5. 权限记录页面

**检查点：**
- [ ] 后台登录qy产品账号
- [ ] 确认所有页面都能正常访问
- [ ] 确认所有页面显示qy产品数据（不显示qm数据）
- [ ] 确认所有操作（增删改查）都按product隔离
- [ ] 确认下拉框/选择器支持qy产品

---

## ✅ 12. 三方接口调用检查

**接口：** `/api/public/pushOrder/*`（7个对外接口）

### 12.1 检查步骤

1. **日志检查：** 查看是否有外部系统调用这些接口
2. **代码搜索：** 搜索是否有其他系统调用这些接口
3. **文档检查：** 查看API文档，确认接口使用情况

### 12.2 处理方案

**如有外部系统调用：**
- 通知外部系统，接口已支持productCode参数
- 提供接口文档，说明如何使用productCode='qy'

**如无外部系统调用：**
- 记录说明，接口已改造，支持多产品

**检查点：**
- [ ] 确认是否有外部系统调用
- [ ] 如有，通知外部系统并提供文档
- [ ] 记录接口改造说明

---

## 🎯 执行总结

### 必须完成项（🔴）- 需要改造

- [ ] 1. 配置初始化（SQL脚本）- 2个表，2条SQL
- [ ] 2. 系统参数配置 - 1个参数，1条SQL
- [ ] 3. 代码改造（PushOrderPublicController）- 1个文件，7个接口

### 建议完成项（🟡）- 需确认或验证

- [ ] 4. 代码确认（PushOrderInsideController）- 1处逻辑，需确认VIP限制
- [ ] 5. 代码验证（PushOrderExternalController）- 18个接口，验证支持多产品
- [ ] 7. 后台管理接口验证 - 5个Controller，验证支持多产品
- [ ] 8. 定时任务验证 - 2个任务，验证支持多产品
- [ ] 9. 数据库表检查 - 7个表，确认有product字段
- [ ] 10. DAO层SQL检查 - 6个DAO文件，确认按product过滤
- [ ] 11. 后台管理界面检查 - 5个页面，验证支持qy

### 可选完成项（🟢）- 可选验证

- [ ] 6. 废弃接口检查 - 1个接口，确认是否使用
- [ ] 12. 三方接口调用检查 - 确认外部系统调用情况

---

## 📝 执行记录

**执行人：** _______________  
**开始时间：** _______________  
**完成时间：** _______________  

**问题记录：**
1. 
2. 
3. 

**备注：**
- 

---

## ✅ 最终验收

- [ ] 所有必须完成项已完成
- [ ] 所有建议完成项已完成（或已确认不需要）
- [ ] 功能测试通过
- [ ] 数据隔离验证通过
- [ ] 代码review通过
- [ ] 文档已更新

**验收人：** _______________  
**验收时间：** _______________

