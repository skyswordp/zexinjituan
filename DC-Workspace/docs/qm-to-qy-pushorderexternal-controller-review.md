# PushOrderExternalController 代码走查（qm -> qy 复刻）

> **目标：** 确认 `PushOrderExternalController` 是否需要改造以支持 qy 产品

---

## 📋 代码走查结果

### ✅ 结论：**不需要改造，已支持多产品**

---

## 🔍 详细分析

### 1. Controller 基本信息

**文件位置：**
- `DC-API-2018/dc-api/dc-api-friend/src/main/java/com/dc/it/controller/PushOrderExternalContoller.java`

**接口路径：**
- `/api/friend/pushOrder/external/1.0/`

**接口数量：** 18个

**继承关系：**
- 继承 `BaseController`
- 使用 `this.getProduct(request)` 获取产品代码

---

### 2. getProduct 方法实现

**代码位置：** `BaseController.java` 第138-151行

```java
public String getProduct(HttpServletRequest request) {
    String reqJsonStr = request.getAttribute("requestJsonData").toString();
    String data = null;
    if (!StringUtils.isBlank(reqJsonStr)) {
        try {
            JSONObject reqJson = JSONObject.fromObject(reqJsonStr);
            data = reqJson.getString("product");  // ⭐ 从请求JSON中动态获取
        } catch (Exception e) {
            logger.warn("参数有误", e);
        }
    }
    return data;
}
```

**说明：**
- ✅ 从请求JSON中动态获取 `product` 字段
- ✅ 没有硬编码，支持任意产品代码
- ✅ 只要请求中传了 `product='qy'`，就能正常工作

---

### 3. 所有接口的 product 获取方式

**统一模式：**
```java
String product = this.getProduct(request);  // 动态获取
if (StringUtils.isBlank(product)) {
    return resultMap(ErrorCode.SC_31005.getCode(), "获取product失败.", null);
}
map.put("product", product);  // 传递给Service层
```

**检查结果：**
- ✅ 所有18个接口都使用 `this.getProduct(request)` 动态获取
- ✅ 没有硬编码 `product = "at"` 或 `product = "qm"`
- ✅ 所有接口都把 `product` 传递给Service层

---

### 4. 接口清单（18个）

| 序号 | 接口方法 | 路径 | product获取方式 | 是否需要改造 |
|------|---------|------|---------------|------------|
| 1 | `findPersonalInfoPageList` | `/1.0/findPersonalInfoPageList` | `this.getProduct(request)` | ❌ 不需要 |
| 2 | `findMonthlyRankingFirstList` | `/1.0/findMonthlyRankingFirstList` | `this.getProduct(request)` | ❌ 不需要 |
| 3 | `findMonthlyRankingPageList` | `/1.0/findMonthlyRankingPageList` | `this.getProduct(request)` | ❌ 不需要 |
| 4 | `findMyAttentionPageList` | `/1.0/findMyAttentionPageList` | `this.getProduct(request)` | ❌ 不需要 |
| 5 | `findMatchPreferredPageList` | `/1.0/findMatchPreferredPageList` | `this.getProduct(request)` | ❌ 不需要 |
| 6 | `findMatchPreferredProgrammePageList` | `/1.0/findMatchPreferredProgrammePageList` | `this.getProduct(request)` | ❌ 不需要 |
| 7 | `findProgrammePreferredPageList` | `/1.0/findProgrammePreferredPageList` | `this.getProduct(request)` | ❌ 不需要 |
| 8 | `findMyPurchasePageList` | `/1.0/findMyPurchasePageList` | `this.getProduct(request)` | ❌ 不需要 |
| 9 | `pushOrderClickReceive` | `/1.0/pushOrderClickReceive` | `this.getProduct(request)` | ❌ 不需要 |
| 10 | `findPlanDetailed` | `/1.0/findPlanDetailed` | `this.getProduct(request)` | ❌ 不需要 |
| 11 | `findMasterDetailed` | `/1.0/findMasterDetailed` | `this.getProduct(request)` | ❌ 不需要 |
| 12 | `releasePushOrderContent` | `/1.0/releasePushOrderContent` | `this.getProduct(request)` | ❌ 不需要 |
| 13 | `findMyPushOrderRecord` | `/1.0/findMyPushOrderRecord` | `this.getProduct(request)` | ❌ 不需要 |
| 14 | `findMyPushOrderRecordDetailed` | `/1.0/findMyPushOrderRecordDetailed` | `this.getProduct(request)` | ❌ 不需要 |
| 15 | `findProgrammePreferredEntity` | `/1.0/findProgrammePreferredEntity` | `this.getProduct(request)` | ❌ 不需要 |
| 16 | `findProgrammePreferredEntityV1` | `/1.1/findProgrammePreferredEntity` | `this.getProduct(request)` | ❌ 不需要 |
| 17 | `findPushOrderEventUEDSpecialSubject` | `/1.0/findPushOrderEventUEDSpecialSubject` | `this.getProduct(request)` | ❌ 不需要 |
| 18 | `findPushOrderFiveEvent` | `/1.0/findPushOrderFiveEvent` | ❌ **硬编码product='at'** | ✅ **需要改造** |

---

### 5. 特殊接口检查

#### 5.1 `findPushOrderFiveEvent`（第587-597行）

**代码：**
```java
@PostMapping(value = "/1.0/findPushOrderFiveEvent")
public String findPushOrderFiveEvent(HttpServletRequest request) {
    try {
        List result = masterPushOrderContentManagementService.findPushOrderFiveEvent();
        return resultMap(ErrorCode.SC_10000.getCode(), ErrorCode.SC_10000.getMessage(), result);
    } catch (Exception e) {
        e.printStackTrace();
        log.error("推单5大赛事赛事UED专题查询 1.0执行异常.", e);
    }
    return resultMapMsg(ErrorCode.SC_10001.getCode(), ErrorCode.SC_10001.getMessage());
}
```

**分析：**
- ❌ 没有获取 `product`
- ❌ 没有传递 `product` 给Service
- ⚠️ 需要检查Service层是否按product过滤

**建议：**
- 检查 `masterPushOrderContentManagementService.findPushOrderFiveEvent()` 方法
- 确认是否需要按product过滤数据
- 如果需要，需要修改接口添加product参数

---

### 6. 与 PushOrderPublicController 对比

| 对比项 | PushOrderExternalController | PushOrderPublicController |
|--------|---------------------------|--------------------------|
| **product获取方式** | ✅ `this.getProduct(request)` 动态获取 | ❌ 硬编码 `product = "at"` |
| **是否支持多产品** | ✅ 支持 | ❌ 不支持（需要改造） |
| **是否需要改造** | ❌ 不需要 | ✅ 需要 |
| **接口数量** | 18个 | 7个 |
| **调用方** | App客户端（需要登录） | 外部系统（无需登录） |

---

## ✅ 最终结论

### 不需要改造的接口（17个）

**原因：**
- ✅ 所有接口都使用 `this.getProduct(request)` 动态获取product
- ✅ 没有硬编码，支持任意产品代码
- ✅ 只要请求中传了 `product='qy'`，就能正常工作

**验证方式：**
- 测试时在请求JSON中传入 `"product": "qy"`
- 确认返回的数据是qy产品的数据

---

### 需要确认的接口（1个）

**接口：** `findPushOrderFiveEvent` - 推单5大赛事赛事UED专题查询

**业务特点：**
- 查询固定的5大联赛：西班牙甲级联赛、英格兰超级联赛、意大利甲级联赛、德国甲级联赛、法国甲级联赛
- SQL硬编码 `product = 'at'`（第733行和第756行）
- 接口注释：**"推单5大赛事赛事UED专题查询"**

**可能的情况：**
1. **UED专题专用** - 如果这个接口是专门给UED产品用的，可能不需要改造
2. **5大联赛共享** - 如果5大联赛的数据是所有产品共享的，可能不需要按product隔离
3. **业务需求** - 如果业务上就是只查at产品的5大联赛数据，可能不需要改造

**需要确认：**
- ⚠️ qy产品是否需要这个"5大赛事UED专题"功能？
- ⚠️ 如果需要，qy产品是否也需要查询5大联赛的数据？
- ⚠️ 如果不需要，可以保持现状，不改造

**建议：**
- 先与产品/业务确认：qy产品是否需要这个功能
- 如果需要 → 需要改造（添加product参数）
- 如果不需要 → 保持现状，不改造

---

### 需要改造的接口（如果确认qy需要5大赛事功能）

**问题：**
- ❌ Controller层没有获取product参数
- ❌ Service层没有接收product参数
- ❌ DAO层SQL硬编码 `product = 'at'`（第733行和第756行）

**需要改造：**

#### 1. Controller层改造
**文件：** `PushOrderExternalContoller.java` 第587-597行

**修改前：**
```java
@PostMapping(value = "/1.0/findPushOrderFiveEvent")
public String findPushOrderFiveEvent(HttpServletRequest request) {
    try {
        List result = masterPushOrderContentManagementService.findPushOrderFiveEvent();
        return resultMap(ErrorCode.SC_10000.getCode(), ErrorCode.SC_10000.getMessage(), result);
    } catch (Exception e) {
        // ...
    }
}
```

**修改后：**
```java
@PostMapping(value = "/1.0/findPushOrderFiveEvent")
public String findPushOrderFiveEvent(HttpServletRequest request) {
    try {
        String product = this.getProduct(request);  // 添加：获取product
        if (StringUtils.isBlank(product)) {
            return resultMap(ErrorCode.SC_31005.getCode(), ErrorCode.SC_31005.getMessage() + "获取product失败.", null);
        }
        List result = masterPushOrderContentManagementService.findPushOrderFiveEvent(product);  // 修改：传入product
        return resultMap(ErrorCode.SC_10000.getCode(), ErrorCode.SC_10000.getMessage(), result);
    } catch (Exception e) {
        // ...
    }
}
```

#### 2. Service层改造
**文件：** `IMasterPushOrderContentManagementService.java` 和 `MasterPushOrderContentManagementImpl.java`

**修改：**
- 接口方法签名：`findPushOrderFiveEvent()` → `findPushOrderFiveEvent(String product)`
- 实现方法：添加product参数，传递给DAO

#### 3. DAO层改造
**文件：** `PushOrderContentManagementDao.xml` 第721-780行

**修改：**
- 第733行：`AND cm.product = 'at'` → `AND cm.product = #{product}`
- 第756行：`AND cm.product = 'at'` → `AND cm.product = #{product}`

**完整改造SQL：**
```xml
<select id="findPushOrderFiveEvent" resultType="com.dc.it.friend.vo.MatchCurrencyVo" parameterType="String">
    WITH ranked_matches AS (
        SELECT cm.*,
            ROW_NUMBER() OVER (
                PARTITION BY cm.home_team
                ORDER BY cm.match_start_time ASC, cm.id ASC
            ) AS rn
        FROM PUSH_ORDER_CONTENT_MANAGEMENT cm
        WHERE cm.competition_results = '0'
            AND cm.state = '2'
            AND cm.product = #{product}  -- 修改：动态参数
            AND (cm.size_handicap_id IS NOT NULL OR cm.let_ball_handicap_id IS NOT NULL)
            AND cm.match_name IN (
                '西班牙甲级联赛', '英格兰超级联赛', '意大利甲级联赛',
                '德国甲级联赛', '法国甲级联赛'
            )
            AND cm.match_start_time > SYSDATE
    ),
    filtered_matches AS (
        SELECT * FROM ranked_matches WHERE rn = 1
    ),
    top_5_per_match AS (
        SELECT cm.*,
            ROW_NUMBER() OVER (
                PARTITION BY cm.match_id
                ORDER BY cm.match_start_time ASC, cm.id ASC
            ) AS match_row_num
        FROM PUSH_ORDER_CONTENT_MANAGEMENT cm
        JOIN filtered_matches fm ON cm.match_id = fm.match_id
        WHERE cm.competition_results = '0'
            AND cm.state = '2'
            AND cm.product = #{product}  -- 修改：动态参数
    )
    SELECT
        sm.home_team_name AS homeTeamName,
        sm.away_team_name AS awayTeamName,
        sm.home_logo_url AS homeLogoUrl,
        sm.away_logo_url AS awayLogoUrl,
        sm.odds AS odds,
        t5.match_name AS leagueName,
        t5.match_start_time AS matchTime,
        t5.push_order_option AS pushOrderOption,
        t5.match_id AS matchId,
        t5.league_match_id AS leagueId,
        t5.let_ball_competition_results AS letBallCompetitionResults,
        t5.win_alone_competition_results AS winAloneCompetitionResults,
        t5.size_competition_results AS sizeCompetitionResults,
        t5.let_ball_price_rate AS letBallPriceRate,
        t5.win_alone_price_rate AS winAlonePriceRate,
        t5.size_price_rate AS sizePriceRate
    FROM top_5_per_match t5
    JOIN sport_matchs sm ON sm.match_id = t5.match_id AND sm.league_id = t5.league_match_id
    WHERE t5.match_row_num <= 5
    ORDER BY t5.match_start_time ASC
</select>
```

---

## 📋 验证建议

### 测试方式

1. **正常接口测试（17个）：**
   ```json
   {
     "product": "qy",
     "data": {
       // 其他参数
     }
   }
   ```

2. **特殊接口测试（1个）：**
   - 先测试当前实现，看返回什么数据
   - 确认是否需要按product过滤

---

## 🎯 总结

**PushOrderExternalController：**
- ✅ **17个接口不需要改造** - 已支持多产品
- ❌ **1个接口需要改造** - `findPushOrderFiveEvent`（SQL硬编码 `product='at'`）

**改造范围：**
- Controller层：1个方法（添加product参数获取）
- Service层：1个方法（添加product参数）
- DAO层：1个SQL（2处硬编码改为动态参数）

**对比 PushOrderPublicController：**
- PushOrderExternalController：✅ 17个接口已支持，1个需要改造
- PushOrderPublicController：❌ 7个接口都需要改造（硬编码 `product = "at"`）

