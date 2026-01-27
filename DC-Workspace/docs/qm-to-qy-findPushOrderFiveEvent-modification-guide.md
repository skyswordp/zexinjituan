# findPushOrderFiveEvent 改造指南（qy 需要5大赛事功能时）

> **前提：** 如果 qy 产品也需要"5大赛事专题"功能，才需要改造。如果不需要，可以不改。

---

## 📋 这句话的意思（大白话）

### 当前情况：
- 这个接口现在**只查 at（亚博）产品的数据**
- SQL 里写死了 `product = 'at'`
- qy 产品调用这个接口，也只会返回 at 的数据

### 两种选择：

**选择1：qy 不需要这个功能**
- ✅ **不改代码**，保持现状
- qy 产品不调用这个接口，或者调用后返回 at 的数据（如果业务允许）

**选择2：qy 也需要这个功能**
- ❌ **必须改代码**，让接口支持动态 product
- qy 产品调用时传入 `product='qy'`，返回 qy 的5大联赛数据
- at 产品调用时传入 `product='at'`，返回 at 的5大联赛数据

---

## 🔧 改造步骤（如果 qy 需要这个功能）

### 改造范围：3层（Controller → Service → DAO）

---

### 1️⃣ Controller 层改造

**文件：** `DC-API-2018/dc-api/dc-api-friend/src/main/java/com/dc/it/controller/PushOrderExternalContoller.java`

**位置：** 第587-597行

**修改前：**
```java
@PostMapping(value = "/1.0/findPushOrderFiveEvent", produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
public String findPushOrderFiveEvent(HttpServletRequest request) throws Exception {
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

**修改后：**
```java
@PostMapping(value = "/1.0/findPushOrderFiveEvent", produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
public String findPushOrderFiveEvent(HttpServletRequest request) throws Exception {
    try {
        // ✅ 添加：从请求中获取 product 参数
        String product = this.getProduct(request);
        if (StringUtils.isBlank(product)) {
            return resultMap(ErrorCode.SC_31005.getCode(), ErrorCode.SC_31005.getMessage() + "获取product失败.", null);
        }
        // ✅ 修改：传入 product 参数给 Service
        List result = masterPushOrderContentManagementService.findPushOrderFiveEvent(product);
        return resultMap(ErrorCode.SC_10000.getCode(), ErrorCode.SC_10000.getMessage(), result);
    } catch (Exception e) {
        e.printStackTrace();
        log.error("推单5大赛事赛事UED专题查询 1.0执行异常.", e);
    }
    return resultMapMsg(ErrorCode.SC_10001.getCode(), ErrorCode.SC_10001.getMessage());
}
```

**改动说明：**
- ✅ 添加 `String product = this.getProduct(request);` 获取产品代码
- ✅ 添加 product 为空判断
- ✅ 修改 Service 调用，传入 product 参数

---

### 2️⃣ Service 接口层改造

**文件：** `DC-API-2018/dc-service/src/main/java/com/dc/it/friend/service/interfaces/IMasterPushOrderContentManagementService.java`

**位置：** 第132行

**修改前：**
```java
/**
 * 推单5大赛事UED专题查询
 * @return
 */
List<Map<String,Object>> findPushOrderFiveEvent();
```

**修改后：**
```java
/**
 * 推单5大赛事UED专题查询
 * @param product 产品代码（如：at、qy）
 * @return
 */
List<Map<String,Object>> findPushOrderFiveEvent(String product);
```

**改动说明：**
- ✅ 方法签名添加 `String product` 参数

---

### 3️⃣ Service 实现层改造

**文件：** `DC-API-2018/dc-service/src/main/java/com/dc/it/friend/service/impl/MasterPushOrderContentManagementImpl.java`

**位置：** 第2392行

**修改前：**
```java
@Override
public List<Map<String, Object>> findPushOrderFiveEvent() {
    List<MatchCurrencyVo> matchCurrencyVoList = pushOrderContentManagementDao.findPushOrderFiveEvent();
    // ... 后续处理
}
```

**修改后：**
```java
@Override
public List<Map<String, Object>> findPushOrderFiveEvent(String product) {
    // ✅ 修改：传入 product 参数给 DAO
    List<MatchCurrencyVo> matchCurrencyVoList = pushOrderContentManagementDao.findPushOrderFiveEvent(product);
    // ... 后续处理（不变）
}
```

**改动说明：**
- ✅ 方法签名添加 `String product` 参数
- ✅ DAO 调用时传入 product 参数

---

### 4️⃣ DAO 接口层改造

**文件：** `DC-API-2018/dc-dao/src/main/java/com/dc/it/friend/dao/PushOrderContentManagementDao.java`

**位置：** 第126行

**修改前：**
```java
List<MatchCurrencyVo> findPushOrderFiveEvent();
```

**修改后：**
```java
List<MatchCurrencyVo> findPushOrderFiveEvent(String product);
```

**改动说明：**
- ✅ 方法签名添加 `String product` 参数

---

### 5️⃣ DAO XML 层改造（最关键！）

**文件：** `DC-API-2018/dc-dao/src/main/java/com/dc/it/friend/dao/PushOrderContentManagementDao.xml`

**位置：** 第721-780行

**修改前：**
```xml
<select id="findPushOrderFiveEvent" resultType="com.dc.it.friend.vo.MatchCurrencyVo">
    WITH ranked_matches AS (
        SELECT cm.*,
            ROW_NUMBER() OVER (
                PARTITION BY cm.home_team
                ORDER BY cm.match_start_time ASC, cm.id ASC
            ) AS rn
        FROM PUSH_ORDER_CONTENT_MANAGEMENT cm
        WHERE cm.competition_results = '0'
            AND cm.state = '2'
            AND cm.product = 'at'  -- ❌ 硬编码：只查 at 产品
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
            AND cm.product = 'at'  -- ❌ 硬编码：只查 at 产品
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
    JOIN sport_matchs sm
    ON sm.match_id = t5.match_id AND sm.league_id = t5.league_match_id
    WHERE t5.match_row_num <= 5
    ORDER BY t5.match_start_time ASC
</select>
```

**修改后：**
```xml
<!-- ✅ 添加 parameterType="String" -->
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
            AND cm.product = #{product}  -- ✅ 修改：动态参数，支持任意产品
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
            AND cm.product = #{product}  -- ✅ 修改：动态参数，支持任意产品
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
    JOIN sport_matchs sm
    ON sm.match_id = t5.match_id AND sm.league_id = t5.league_match_id
    WHERE t5.match_row_num <= 5
    ORDER BY t5.match_start_time ASC
</select>
```

**改动说明：**
- ✅ 添加 `parameterType="String"` 声明参数类型
- ✅ 第733行：`AND cm.product = 'at'` → `AND cm.product = #{product}`
- ✅ 第756行：`AND cm.product = 'at'` → `AND cm.product = #{product}`

---

## ✅ 改造后的效果

### 改造前：
- qy 产品调用 → 返回 at 产品的数据（错误）
- at 产品调用 → 返回 at 产品的数据（正确）

### 改造后：
- qy 产品调用（传入 `product='qy'`）→ 返回 qy 产品的5大联赛数据（正确）
- at 产品调用（传入 `product='at'`）→ 返回 at 产品的5大联赛数据（正确）

---

## 📋 改造检查清单

- [ ] Controller 层：添加 product 参数获取
- [ ] Service 接口层：方法签名添加 product 参数
- [ ] Service 实现层：方法签名添加 product 参数，传递给 DAO
- [ ] DAO 接口层：方法签名添加 product 参数
- [ ] DAO XML 层：添加 `parameterType="String"`，2处 `product='at'` 改为 `product=#{product}`
- [ ] 编译测试：确保代码能编译通过
- [ ] 功能测试：qy 产品调用返回 qy 数据，at 产品调用返回 at 数据

---

## ⚠️ 注意事项

1. **必须5层都改** - Controller、Service接口、Service实现、DAO接口、DAO XML，缺一不可
2. **SQL 改2处** - 第733行和第756行都要改
3. **测试验证** - 改造后必须测试 qy 和 at 两个产品都能正常返回数据

