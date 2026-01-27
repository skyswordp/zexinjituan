# 红单后台管理接口检查（qm -> qy 复刻）

> **问题：** 红单相关的后台管理接口检查了吗？qm->qy不需要做什么相应的工作吗？

---

## 📋 后台管理接口清单

### 已发现的Controller（7个）

| Controller | 路径 | 说明 | 接口数 |
|-----------|------|------|--------|
| **PushOrderContentManagementController** | `/api/friend/pushOrder/contentManagement` | 推单内容管理 | 10个 |
| **PushOrderAiUserController** | `/api/friend/pushOrder/aiUser` | AI推单用户管理 | 12个 |
| **PushOrderParamConfigController** | `/api/friend/pushOrder/paramConfig` | 推单参数配置管理 | 3个 |
| **PushOrderLevelTitleConfigController** | `/api/friend/pushOrder/levelTitleConfig` | 推单等级称号配置管理 | 4个 |
| **PushOrderContentGeneralLogController** | `/api/friend/contentGeneralLog` | 推单操作日志管理 | 2个 |
| **PushOrderPermissionRecordController** | `/api/friend/pushOrder/permissionRecord` | 推单权限记录管理 | 1个 |
| **PushOrderPublicController** | `/api/friend/pushOrder/public` | 外部系统接口（已检查） | 7个 |

**总计：** 约39个后台管理接口

---

## ✅ 检查结果

### 1. 大部分接口已支持多产品（使用 `getOperatorProductCode`）

**原理：**
- 后台管理员登录时，系统会根据操作员的 `productCode` 设置session
- 接口通过 `getOperatorProductCode(request)` 从session获取产品代码
- 这样不同产品的管理员登录后，只能看到自己产品的数据

**代码位置：** `BaseController.java` 第50-57行
```java
protected String getOperatorProductCode(HttpServletRequest request) {
    HttpSession session = request.getSession(true);
    Operator operator = (Operator) session.getAttribute("operator");
    return operator.getProductCode();  // ✅ 从session获取产品代码
}
```

**已支持的接口：**
- ✅ `PushOrderContentManagementController` - 大部分接口（8/10）
- ✅ `PushOrderAiUserController` - 大部分接口（10/12）
- ✅ `PushOrderParamConfigController` - 所有接口（3/3）
- ✅ `PushOrderLevelTitleConfigController` - 所有接口（4/4）
- ✅ `PushOrderContentGeneralLogController` - 所有接口（2/2）
- ✅ `PushOrderPermissionRecordController` - 所有接口（1/1）

---

### 2. 需要改造的接口（硬编码 `productCode = "at"`）

#### 2.1 PushOrderContentManagementController

**文件：** `PushOrderContentManagementController.java`

| 接口方法 | 路径 | 问题 | 行号 | 是否需要改造 |
|---------|------|------|------|------------|
| `openPushOrderData` | `/openPushOrderData` | `map.put("product","at")` | 87 | ❌ **已废弃**（@Deprecated） |
| `updateGrantKf` | `/updateGrantKf` | `paramMap.put("productCode", "at")` | 328 | ✅ **需要改造** |
| `findGrantKf` | `/findGrantKf` | `paramMap.put("productCode", "at")` | 364 | ✅ **需要改造** |

**问题代码：**
```java
// 第328行 - updateGrantKf
paramMap.put("productCode", "at");  // ❌ 硬编码

// 第364行 - findGrantKf
paramMap.put("productCode", "at");  // ❌ 硬编码
```

**改造方案：**
```java
// 修改为：
paramMap.put("productCode", getOperatorProductCode(request));  // ✅ 动态获取
```

---

#### 2.2 PushOrderAiUserController

**文件：** `PushOrderAiUserController.java`

| 接口方法 | 路径 | 问题 | 行号 | 是否需要改造 |
|---------|------|------|------|------------|
| `updateGrantKf` | `/updateGrantKf` | `paramMap.put("productCode", "at")` | 323 | ✅ **需要改造** |
| `findGrantKf` | `/findGrantKf` | `paramMap.put("productCode", "at")` | 359 | ✅ **需要改造** |

**问题代码：**
```java
// 第323行 - updateGrantKf
paramMap.put("productCode", "at");  // ❌ 硬编码

// 第359行 - findGrantKf
paramMap.put("productCode", "at");  // ❌ 硬编码
```

**改造方案：**
```java
// 修改为：
paramMap.put("productCode", getOperatorProductCode(request));  // ✅ 动态获取
```

---

## 📊 改造统计

### 需要改造的接口（4个）

| Controller | 接口方法 | 问题 | 优先级 |
|-----------|---------|------|--------|
| PushOrderContentManagementController | `updateGrantKf` | 硬编码 `productCode="at"` | ⚠️ **中**（授权客服标识） |
| PushOrderContentManagementController | `findGrantKf` | 硬编码 `productCode="at"` | ⚠️ **中**（授权客服标识） |
| PushOrderAiUserController | `updateGrantKf` | 硬编码 `productCode="at"` | ⚠️ **中**（授权客服标识） |
| PushOrderAiUserController | `findGrantKf` | 硬编码 `productCode="at"` | ⚠️ **中**（授权客服标识） |

### 不需要改造的接口（35个）

- ✅ 所有接口都使用 `getOperatorProductCode(request)` 动态获取产品代码
- ✅ 后台管理员登录后，系统会根据操作员的 `productCode` 自动过滤数据

---

## 🔧 改造方案

### 改造文件1：PushOrderContentManagementController.java

**文件位置：** `DC-API-2018/dc-api/dc-api-office/src/main/java/com/dc/it/friend/controller/PushOrderContentManagementController.java`

#### 修改1：updateGrantKf 方法（第328行）

**修改前：**
```java
@RequestMapping(value = "/updateGrantKf", method = RequestMethod.POST, produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
public String updateGrantKF(@RequestBody Map<String, Object> mapEntity, HttpServletRequest request) throws Exception {
    Map<String, Object> paramMap = new HashMap<>();
    paramMap.put("category", "PUSHORDER");
    paramMap.put("code", "GRANT_PUSHORDER_CONTENT");
    paramMap.put("productCode", "at");  // ❌ 硬编码
    // ...
}
```

**修改后：**
```java
@RequestMapping(value = "/updateGrantKf", method = RequestMethod.POST, produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
public String updateGrantKF(@RequestBody Map<String, Object> mapEntity, HttpServletRequest request) throws Exception {
    Map<String, Object> paramMap = new HashMap<>();
    paramMap.put("category", "PUSHORDER");
    paramMap.put("code", "GRANT_PUSHORDER_CONTENT");
    paramMap.put("productCode", getOperatorProductCode(request));  // ✅ 动态获取
    // ...
}
```

#### 修改2：findGrantKf 方法（第364行）

**修改前：**
```java
@RequestMapping(value = "/findGrantKf", method = RequestMethod.POST, produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
public String findGrantKf(HttpServletRequest request) throws Exception {
    Map<String, Object> paramMap = new HashMap<>();
    paramMap.put("category", "PUSHORDER");
    paramMap.put("code", "GRANT_PUSHORDER_CONTENT");
    paramMap.put("productCode", "at");  // ❌ 硬编码
    // ...
}
```

**修改后：**
```java
@RequestMapping(value = "/findGrantKf", method = RequestMethod.POST, produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
public String findGrantKf(HttpServletRequest request) throws Exception {
    Map<String, Object> paramMap = new HashMap<>();
    paramMap.put("category", "PUSHORDER");
    paramMap.put("code", "GRANT_PUSHORDER_CONTENT");
    paramMap.put("productCode", getOperatorProductCode(request));  // ✅ 动态获取
    // ...
}
```

---

### 改造文件2：PushOrderAiUserController.java

**文件位置：** `DC-API-2018/dc-api/dc-api-office/src/main/java/com/dc/it/friend/controller/PushOrderAiUserController.java`

#### 修改1：updateGrantKf 方法（第323行）

**修改前：**
```java
@RequestMapping(value = "/updateGrantKf", method = RequestMethod.POST, produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
public String updateGrantKF(@RequestBody Map<String, Object> mapEntity, HttpServletRequest request) throws Exception {
    Map<String, Object> paramMap = new HashMap<>();
    paramMap.put("category", "PUSHORDER");
    paramMap.put("code", "GRANT_PUSHORDER_AIUSER");
    paramMap.put("productCode", "at");  // ❌ 硬编码
    // ...
}
```

**修改后：**
```java
@RequestMapping(value = "/updateGrantKf", method = RequestMethod.POST, produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
public String updateGrantKF(@RequestBody Map<String, Object> mapEntity, HttpServletRequest request) throws Exception {
    Map<String, Object> paramMap = new HashMap<>();
    paramMap.put("category", "PUSHORDER");
    paramMap.put("code", "GRANT_PUSHORDER_AIUSER");
    paramMap.put("productCode", getOperatorProductCode(request));  // ✅ 动态获取
    // ...
}
```

#### 修改2：findGrantKf 方法（第359行）

**修改前：**
```java
@RequestMapping(value = "/findGrantKf", method = RequestMethod.POST, produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
public String findGrantKf(HttpServletRequest request) throws Exception {
    Map<String, Object> paramMap = new HashMap<>();
    paramMap.put("category", "PUSHORDER");
    paramMap.put("code", "GRANT_PUSHORDER_AIUSER");
    paramMap.put("productCode", "at");  // ❌ 硬编码
    // ...
}
```

**修改后：**
```java
@RequestMapping(value = "/findGrantKf", method = RequestMethod.POST, produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
public String findGrantKf(HttpServletRequest request) throws Exception {
    Map<String, Object> paramMap = new HashMap<>();
    paramMap.put("category", "PUSHORDER");
    paramMap.put("code", "GRANT_PUSHORDER_AIUSER");
    paramMap.put("productCode", getOperatorProductCode(request));  // ✅ 动态获取
    // ...
}
```

---

## ⚠️ 注意事项

### 1. 系统参数配置

**这些接口操作的是系统参数表（S_SYSTEM_PARAMETER）：**

- `GRANT_PUSHORDER_CONTENT` - 推单内容授权客服标识
- `GRANT_PUSHORDER_AIUSER` - AI用户授权客服标识

**需要确认：**
- ⚠️ qy产品是否需要独立的授权客服标识？
- ⚠️ 如果需要，需要在 `S_SYSTEM_PARAMETER` 表中为qy创建对应的系统参数
- ⚠️ 如果不需要，改造后qy会使用qy产品的系统参数（如果存在）

### 2. 系统参数初始化

**如果qy需要独立的授权客服标识，需要初始化：**

```sql
-- 推单内容授权客服标识（qy）
INSERT INTO pubdb.S_SYSTEM_PARAMETER (
    ID, CATEGORY, CODE, VALUE, PRODUCT_CODE, CREATE_TIME, CREATE_USER
)
SELECT 
    SEQ_S_SYSTEM_PARAMETER.NEXTVAL,
    'PUSHORDER',
    'GRANT_PUSHORDER_CONTENT',
    '0',  -- 默认未授权
    'qy',
    SYSDATE,
    'system'
FROM DUAL
WHERE NOT EXISTS (
    SELECT 1 FROM pubdb.S_SYSTEM_PARAMETER 
    WHERE CATEGORY = 'PUSHORDER' 
    AND CODE = 'GRANT_PUSHORDER_CONTENT' 
    AND PRODUCT_CODE = 'qy'
);

-- AI用户授权客服标识（qy）
INSERT INTO pubdb.S_SYSTEM_PARAMETER (
    ID, CATEGORY, CODE, VALUE, PRODUCT_CODE, CREATE_TIME, CREATE_USER
)
SELECT 
    SEQ_S_SYSTEM_PARAMETER.NEXTVAL,
    'PUSHORDER',
    'GRANT_PUSHORDER_AIUSER',
    '0',  -- 默认未授权
    'qy',
    SYSDATE,
    'system'
FROM DUAL
WHERE NOT EXISTS (
    SELECT 1 FROM pubdb.S_SYSTEM_PARAMETER 
    WHERE CATEGORY = 'PUSHORDER' 
    AND CODE = 'GRANT_PUSHORDER_AIUSER' 
    AND PRODUCT_CODE = 'qy'
);
```

---

## ✅ 最终结论

### 需要改造的接口（4个）

1. ✅ `PushOrderContentManagementController.updateGrantKf` - 修改授权客服标识
2. ✅ `PushOrderContentManagementController.findGrantKf` - 查询授权客服标识
3. ✅ `PushOrderAiUserController.updateGrantKf` - 修改授权客服标识
4. ✅ `PushOrderAiUserController.findGrantKf` - 查询授权客服标识

### 不需要改造的接口（35个）

- ✅ 所有其他接口都使用 `getOperatorProductCode(request)` 动态获取产品代码
- ✅ 后台管理员登录后，系统会根据操作员的 `productCode` 自动过滤数据

### 改造工作量

- **代码改造：** 4个接口，2个文件，每处修改1行代码（共4处）
- **系统参数初始化：** 如果qy需要独立的授权客服标识，需要初始化2个系统参数

---

## 📋 改造检查清单

- [ ] PushOrderContentManagementController.updateGrantKf - 修改 `productCode="at"` → `getOperatorProductCode(request)`
- [ ] PushOrderContentManagementController.findGrantKf - 修改 `productCode="at"` → `getOperatorProductCode(request)`
- [ ] PushOrderAiUserController.updateGrantKf - 修改 `productCode="at"` → `getOperatorProductCode(request)`
- [ ] PushOrderAiUserController.findGrantKf - 修改 `productCode="at"` → `getOperatorProductCode(request)`
- [ ] 系统参数初始化（可选）- 如果qy需要独立的授权客服标识，初始化 `GRANT_PUSHORDER_CONTENT` 和 `GRANT_PUSHORDER_AIUSER`

