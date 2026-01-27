# PushOrderExternalController 17个接口操作的数据库表

> **说明：** 这17个接口是**不需要改造**的接口，已支持多产品（动态获取product）

---

## 📋 接口清单

| 序号 | 接口方法 | Service | DAO |
|------|---------|---------|-----|
| 1 | `findPersonalInfoPageList` | `maUsteruserService` | `FUserDao` |
| 2 | `findMonthlyRankingFirstList` | `maUsteruserService` | `FUserDao` |
| 3 | `findMonthlyRankingPageList` | `maUsteruserService` | `FUserDao` |
| 4 | `findMyAttentionPageList` | `maUsteruserService` | `FUserDao` |
| 5 | `findMatchPreferredPageList` | `masterPushOrderContentManagementService` | `PushOrderContentManagementDao` |
| 6 | `findMatchPreferredProgrammePageList` | `masterPushOrderContentManagementService` | `PushOrderContentManagementDao` |
| 7 | `findProgrammePreferredPageList` | `masterPushOrderContentManagementService` | `PushOrderContentManagementDao` |
| 8 | `findMyPurchasePageList` | `masterPushOrderContentManagementService` | `PushOrderContentManagementDao` |
| 9 | `pushOrderClickReceive` | `masterPushOrderContentManagementService` | `PushOrderContentManagementDao` |
| 10 | `findPlanDetailed` | `masterPushOrderContentManagementService` | `PushOrderContentManagementDao` |
| 11 | `findMasterDetailed` | `maUsteruserService` | `FUserDao` |
| 12 | `releasePushOrderContent` | `masterPushOrderContentManagementService` | `PushOrderContentManagementDao` |
| 13 | `findMyPushOrderRecord` | `masterPushOrderContentManagementService` | `PushOrderContentManagementDao` |
| 14 | `findMyPushOrderRecordDetailed` | `masterPushOrderContentManagementService` | `PushOrderContentManagementDao` |
| 15 | `findProgrammePreferredEntity` | `masterPushOrderContentManagementService` | `PushOrderContentManagementDao` |
| 16 | `findProgrammePreferredEntityV1` | `masterPushOrderContentManagementService` | `PushOrderContentManagementDao` |
| 17 | `findPushOrderEventUEDSpecialSubject` | `masterPushOrderContentManagementService` | `PushOrderContentManagementDao` |

---

## 🗄️ 数据库表汇总

### 核心表（主要操作）

| 表名 | 说明 | 操作类型 | 涉及接口数 |
|------|------|---------|-----------|
| **PUSH_ORDER_CONTENT_MANAGEMENT** | 推单内容主表（红单表） | SELECT, INSERT, UPDATE | 15个 |
| **F_USER** | 用户表 | SELECT, JOIN | 12个 |
| **PUSH_ORDER_CONTENT_GENERAL_LOG** | 推单操作日志表（点击、购买、关注） | SELECT, INSERT | 12个 |

### 配置表（只读）

| 表名 | 说明 | 操作类型 | 涉及接口数 |
|------|------|---------|-----------|
| **PUSH_ORDER_PARAM_CONFIG** | 推单参数配置表（价格、奖励配置） | SELECT | 12个 |
| **PUSH_ORDER_LEVEL_TITLE_CONFIG** | 推单等级称号配置表（足球大师、篮球大师） | SELECT | 8个 |

### 关联表（只读）

| 表名 | 说明 | 操作类型 | 涉及接口数 |
|------|------|---------|-----------|
| **F_USER_FOLLOW** | 用户关注表 | SELECT | 5个 |
| **sport_matchs** | 赛事表 | SELECT, JOIN | 10个 |
| **sport_leagues** | 联赛表 | SELECT, JOIN | 10个 |

---

## 📊 详细表操作清单

### 1. PUSH_ORDER_CONTENT_MANAGEMENT（推单内容主表）

**操作类型：** SELECT, INSERT, UPDATE

**涉及的接口：**
- ✅ `findMatchPreferredPageList` - 查询
- ✅ `findMatchPreferredProgrammePageList` - 查询
- ✅ `findProgrammePreferredPageList` - 查询
- ✅ `findMyPurchasePageList` - 查询
- ✅ `pushOrderClickReceive` - 更新（点击统计）
- ✅ `findPlanDetailed` - 查询
- ✅ `releasePushOrderContent` - **INSERT（发布推单）**
- ✅ `findMyPushOrderRecord` - 查询
- ✅ `findMyPushOrderRecordDetailed` - 查询
- ✅ `findProgrammePreferredEntity` - 查询
- ✅ `findProgrammePreferredEntityV1` - 查询
- ✅ `findPushOrderEventUEDSpecialSubject` - 查询
- ✅ `findPersonalInfoPageList` - 子查询（统计）
- ✅ `findMonthlyRankingFirstList` - 子查询（统计）
- ✅ `findMasterDetailed` - 子查询（统计）

**主要字段：**
- `id`, `user_name`, `product`, `title`, `match_id`, `league_match_id`
- `state`, `competition_results`, `price`, `number_click`, `number_buyer`
- `create_time`, `update_time`

---

### 2. F_USER（用户表）

**操作类型：** SELECT, JOIN

**涉及的接口：**
- ✅ `findPersonalInfoPageList` - 查询用户信息
- ✅ `findMonthlyRankingFirstList` - 查询用户信息
- ✅ `findMonthlyRankingPageList` - 查询用户信息
- ✅ `findMyAttentionPageList` - 查询关注用户
- ✅ `findMatchPreferredProgrammePageList` - JOIN用户信息
- ✅ `findProgrammePreferredPageList` - JOIN用户信息
- ✅ `findMyPurchasePageList` - JOIN用户信息
- ✅ `findPlanDetailed` - JOIN用户信息
- ✅ `findMasterDetailed` - 查询用户详细信息
- ✅ `findMyPushOrderRecordDetailed` - JOIN用户信息
- ✅ `findProgrammePreferredEntity` - JOIN用户信息
- ✅ `findPushOrderEventUEDSpecialSubject` - 间接关联

**主要字段：**
- `id`, `user_name`, `nick_name`, `head_url`, `product`
- `authentication`, `fire_icon`, `level_config_id`
- `red_order_rate`, `red_order_rate_type`, `total_popularity`

---

### 3. PUSH_ORDER_CONTENT_GENERAL_LOG（推单操作日志表）

**操作类型：** SELECT, INSERT

**涉及的接口：**
- ✅ `pushOrderClickReceive` - **INSERT（记录点击）**
- ✅ `findMatchPreferredProgrammePageList` - 统计点击、购买、关注数
- ✅ `findProgrammePreferredPageList` - 统计点击、购买、关注数
- ✅ `findMyPurchasePageList` - 查询购买记录
- ✅ `findPlanDetailed` - 统计点击、购买、关注数
- ✅ `findMasterDetailed` - 统计点击、购买、关注数
- ✅ `findMyPushOrderRecord` - 统计点击、购买、关注数
- ✅ `findMyPushOrderRecordDetailed` - 统计点击、购买、关注数
- ✅ `findProgrammePreferredEntity` - 统计点击、购买、关注数
- ✅ `findPersonalInfoPageList` - 子查询（统计）
- ✅ `findMonthlyRankingFirstList` - 子查询（统计购买）
- ✅ `findMasterDetailed` - 子查询（统计）

**主要字段：**
- `id`, `content_management_id`, `user_name`, `operator_user_name`, `product`
- `type` (0=点击, 1=购买, 2=关注, 3=审核)
- `create_time`, `remarks`

---

### 4. PUSH_ORDER_PARAM_CONFIG（推单参数配置表）

**操作类型：** SELECT（只读）

**涉及的接口：**
- ✅ `findMatchPreferredPageList` - 查询价格配置
- ✅ `findMatchPreferredProgrammePageList` - 查询奖励配置
- ✅ `findProgrammePreferredPageList` - 查询奖励配置
- ✅ `findMyPurchasePageList` - 查询奖励配置
- ✅ `findPlanDetailed` - 查询奖励配置
- ✅ `findMasterDetailed` - 查询奖励配置
- ✅ `findMyPushOrderRecord` - 查询奖励配置
- ✅ `findMyPushOrderRecordDetailed` - 查询奖励配置
- ✅ `findProgrammePreferredEntity` - 查询奖励配置
- ✅ `findPersonalInfoPageList` - 查询奖励配置（人气计算）
- ✅ `findMonthlyRankingFirstList` - 查询奖励配置（人气计算）
- ✅ `findMasterDetailed` - 查询奖励配置

**主要字段：**
- `id`, `product`, `type` (0=默认配置)
- `purchase_bonus` (购买奖励), `click_count_bonus` (点击奖励)
- `fan_bonus` (粉丝奖励), `push_order_bonus` (推单奖励)

---

### 5. PUSH_ORDER_LEVEL_TITLE_CONFIG（推单等级称号配置表）

**操作类型：** SELECT（只读）

**涉及的接口：**
- ✅ `findPersonalInfoPageList` - 查询称号（足球大师、篮球大师）
- ✅ `findMyAttentionPageList` - 查询称号
- ✅ `findMatchPreferredProgrammePageList` - 查询称号
- ✅ `findProgrammePreferredPageList` - 查询称号
- ✅ `findPlanDetailed` - 查询称号
- ✅ `findMyPushOrderRecordDetailed` - 查询称号
- ✅ `findProgrammePreferredEntity` - 查询称号
- ✅ `findMasterDetailed` - 查询称号

**主要字段：**
- `id`, `name` (称号名称，如"足球大师"、"篮球大师")
- `product` (产品代码)

---

### 6. F_USER_FOLLOW（用户关注表）

**操作类型：** SELECT（只读）

**涉及的接口：**
- ✅ `findPersonalInfoPageList` - 统计粉丝数、关注数
- ✅ `findMonthlyRankingFirstList` - 统计粉丝数
- ✅ `findMyAttentionPageList` - 查询关注列表
- ✅ `findPlanDetailed` - 查询是否关注
- ✅ `findMasterDetailed` - 统计粉丝数

**主要字段：**
- `id`, `user_id` (关注者ID), `be_user_id` (被关注者ID)
- `create_time`

---

### 7. sport_matchs（赛事表）

**操作类型：** SELECT, JOIN

**涉及的接口：**
- ✅ `findMatchPreferredPageList` - JOIN赛事信息
- ✅ `findMatchPreferredProgrammePageList` - JOIN赛事信息
- ✅ `findProgrammePreferredPageList` - JOIN赛事信息
- ✅ `findMyPurchasePageList` - JOIN赛事信息
- ✅ `findPlanDetailed` - JOIN赛事信息
- ✅ `findMasterDetailed` - JOIN赛事信息
- ✅ `findMyPushOrderRecordDetailed` - JOIN赛事信息
- ✅ `findProgrammePreferredEntity` - JOIN赛事信息
- ✅ `findPushOrderEventUEDSpecialSubject` - JOIN赛事信息
- ✅ `findPushOrderFiveEvent` - JOIN赛事信息

**主要字段：**
- `match_id`, `league_id`, `home_team_name`, `away_team_name`
- `home_logo_url`, `away_logo_url`, `match_time`, `odds`, `score`

---

### 8. sport_leagues（联赛表）

**操作类型：** SELECT, JOIN

**涉及的接口：**
- ✅ `findMatchPreferredPageList` - 查询联赛名称
- ✅ `findMatchPreferredProgrammePageList` - 查询联赛名称
- ✅ `findProgrammePreferredPageList` - 查询联赛名称
- ✅ `findMyPurchasePageList` - 查询联赛名称
- ✅ `findPlanDetailed` - 查询联赛名称
- ✅ `findMasterDetailed` - 查询联赛名称
- ✅ `findMyPushOrderRecord` - 查询联赛名称
- ✅ `findMyPushOrderRecordDetailed` - 查询联赛名称
- ✅ `findProgrammePreferredEntity` - 查询联赛名称
- ✅ `findPushOrderEventUEDSpecialSubject` - 查询联赛名称

**主要字段：**
- `league_id`, `league_name`, `product`

---

## 📈 表操作统计

### 按操作类型统计

| 操作类型 | 表名 | 接口数 |
|---------|------|--------|
| **SELECT** | 所有表 | 17个接口 |
| **INSERT** | PUSH_ORDER_CONTENT_MANAGEMENT, PUSH_ORDER_CONTENT_GENERAL_LOG | 2个接口 |
| **UPDATE** | PUSH_ORDER_CONTENT_MANAGEMENT | 1个接口 |

### 按表统计

| 表名 | 涉及接口数 | 主要用途 |
|------|----------|---------|
| PUSH_ORDER_CONTENT_MANAGEMENT | 15个 | 推单内容主表，核心业务表 |
| F_USER | 12个 | 用户信息表 |
| PUSH_ORDER_CONTENT_GENERAL_LOG | 12个 | 操作日志表（点击、购买、关注） |
| PUSH_ORDER_PARAM_CONFIG | 12个 | 参数配置表（价格、奖励） |
| sport_matchs | 10个 | 赛事信息表 |
| sport_leagues | 10个 | 联赛信息表 |
| PUSH_ORDER_LEVEL_TITLE_CONFIG | 8个 | 等级称号配置表 |
| F_USER_FOLLOW | 5个 | 用户关注关系表 |

---

## ✅ 总结

**这17个接口一共操作了 8 张数据库表：**

1. **PUSH_ORDER_CONTENT_MANAGEMENT** - 推单内容主表（核心表）
2. **F_USER** - 用户表
3. **PUSH_ORDER_CONTENT_GENERAL_LOG** - 推单操作日志表
4. **PUSH_ORDER_PARAM_CONFIG** - 推单参数配置表
5. **PUSH_ORDER_LEVEL_TITLE_CONFIG** - 推单等级称号配置表
6. **F_USER_FOLLOW** - 用户关注表
7. **sport_matchs** - 赛事表
8. **sport_leagues** - 联赛表

**操作类型：**
- **查询（SELECT）**：所有接口都有
- **插入（INSERT）**：2个接口（`releasePushOrderContent`, `pushOrderClickReceive`）
- **更新（UPDATE）**：1个接口（`pushOrderClickReceive`）

**数据隔离：**
- ✅ 所有表都通过 `product` 字段进行数据隔离
- ✅ 所有接口都动态获取 `product` 参数，支持多产品

