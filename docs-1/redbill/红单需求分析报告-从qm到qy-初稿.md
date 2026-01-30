# 红单需求分析报告（qm → qy）初稿

日期：2026-01-30

## 1. 需求背景与目标
产品诉求：将“红单（PushOrder）”在 qm 产品上的功能完整复制到 qy 产品，保证功能与接口能力对齐，便于后续业务一致运营。

目标：在 qy 产品侧实现与 qm 一致的红单能力，包括后台管理、客户端展示、三方接口与内部服务调用，并保持业务流程一致（创建→生成→发布→展示）。

## 2. 功能范围（基于现有材料）
红单功能是完整后端模块，覆盖推单生成、内容管理、公开展示、第三方接口、内部财务/结算接口。

### 2.1 核心业务链路（四层）
1) 创建：配置 AI 推单用户
2) 生成：触发 AI 内容生成
3) 发布：新增/更新推单内容
4) 展示：用户端查询与展示

### 2.2 功能模块分层
- 基础配置层：参数配置、等级称号、权限记录
- 核心业务层：AI 推单用户管理、推单内容管理
- 数据记录层：内容日志、购买统计
- 对外发布层：客户端与三方公开接口

### 2.3 模块与接口规模
- 组件：dc-api-friend（客户端服务层）+ dc-api-office（后台管理层）
- Controller：9 个
- 接口：约 75 个

## 3. 用户与权限模型
- 后台运营/配置人员：需要认证，管理 AI 用户、内容生成与发布、配置参数
- 客户端用户：无需认证或弱认证，获取推单展示内容
- 第三方系统：可选签名校验，读操作为主
- 内部系统（财务/结算）：WebService 内部调用

## 4. 主要接口类别（高优先级）
- 生成入口：AI 推单触发生成（后台）
- 发布管理：内容新增/更新/发布/下架
- 展示查询：大师列表、排行榜、方案详情

## 5. 现有材料的事实依据
- 红单功能统计与链路说明：docs-1/redbill/红单功能统计报告.md
- 红单架构与接口清单：docs-1/redbill/红单功能完整架构分析（纠正版）.md

## 6. 需求不确定点（待接口抓包确认）
- qm 与 qy 的产品 code 与路由差异（域名、路径前缀、网关）
- 认证方式与 token 策略是否一致
- 内容审核流程是否有差异（人工/自动）
- 三方接口是否需要签名或额外字段
- 与财务/订单系统的集成方式是否一致

## 6.1 APP抓包接口分析（本次新增）
### 6.1.1 红单相关接口统计
- 抓包原始记录中，红单相关接口共 **11 个唯一接口**（均位于 `/api/friend/pushOrder/external/1.0/*`）
- 归属工程模块：**DC-API-2018 / dc-api-friend**
- 归属 Controller：**PushOrderExternalController**

| # | 接口路径 | 模块 | Controller | 说明 |
|---|---------|------|------------|------|
| 1 | `/api/friend/pushOrder/external/1.0/findProgrammePreferredEntity` | dc-api-friend | PushOrderExternalController | 偏好方案实体 |
| 2 | `/api/friend/pushOrder/external/1.0/findMonthlyRankingPageList` | dc-api-friend | PushOrderExternalController | 月榜分页 |
| 3 | `/api/friend/pushOrder/external/1.0/findPersonalInfoPageList` | dc-api-friend | PushOrderExternalController | 大师列表 |
| 4 | `/api/friend/pushOrder/external/1.0/findMonthlyRankingFirstList` | dc-api-friend | PushOrderExternalController | 首页月榜 |
| 5 | `/api/friend/pushOrder/external/1.0/findMatchPreferredPageList` | dc-api-friend | PushOrderExternalController | 偏好赛事分页 |
| 6 | `/api/friend/pushOrder/external/1.0/findMasterDetailed` | dc-api-friend | PushOrderExternalController | 大师详情 |
| 7 | `/api/friend/pushOrder/external/1.0/findMyAttentionPageList` | dc-api-friend | PushOrderExternalController | 我关注的推手 |
| 8 | `/api/friend/pushOrder/external/1.0/pushOrderClickReceive` | dc-api-friend | PushOrderExternalController | 推单点击/埋点 |
| 9 | `/api/friend/pushOrder/external/1.0/findPlanDetailed` | dc-api-friend | PushOrderExternalController | 方案详情 |
|10 | `/api/friend/pushOrder/external/1.0/findProgrammePreferredPageList` | dc-api-friend | PushOrderExternalController | 偏好方案分页 |
|11 | `/api/friend/pushOrder/external/1.0/findMyPurchasePageList` | dc-api-friend | PushOrderExternalController | 我的购买记录 |

### 6.1.2 覆盖情况判断
- 文档《红单功能完整架构分析（纠正版）》中已列出 PushOrderExternalController（19 个接口），上述接口 **属于其子集**。
- 当前仓库未直接检索到对应 Controller 源码路径（可能不在该代码仓库或被排除），**需在实际服务工程确认接口实现是否齐全**。

### 6.1.3 非红单接口（同页面依赖，非本次复制核心）
以下接口出现在同一批抓包中，但不属于红单主链路；可能是页面依赖或通用功能：
- 用户信息与关注：`/api/friend/user/1.0/getUser`、`getMyPraiseCount`、`saveFollow`、`saveFollowNew`、`readCount`
- 等级与板块：`/api/friend/levelSetting/1.0/getLevel`、`/api/friend/board/index/getByLevel`、`/api/friend/board/guess/getByLevel`
- 圈子与动态：`/api/friend/circle/1.0/getCountList`、`/api/friend/circle/2.0/pageList`、`/api/friend/circleComments/1.0/pageList`
- 首页与游戏配置：`/api/friend/indexSetting/1.0/pageList`、`/api/friend/gameSetting/1.0/pageList`
- 任务与话题：`/api/friend/task/1.0/queryTasks`、`/api/friend/topic/1.0/queryTitle`、`/api/friend/topic/1.0/queryDetails`

**影响**：若 qy 产品页面复用相同组件，以上通用接口可能需要同步接入或保持兼容，但不属于红单核心复制范围。

## 6.2 实施评估（是否仅客户端改 code）
结论：**不止是客户端改产品 code**。红单链路依赖后端配置、数据与定时任务，且请求参数存在加密，需要解密对照后端逻辑与数据库字段。

必须完成的后端动作（缺一不可）：
1) **系统参数开通产品**：确认 `PUSHORDER_PRODUCT` 包含 qy（位于 `system_parameter` 表）。
2) **AI 推单用户配置**：`push_order_ai_user` 表需存在 qy 对应用户（含 `product` 字段）。
3) **推单内容落库与展示**：`push_order_content_management`（推单内容表）必须有 qy 数据可供前端展示。
4) **定时任务与 AI 服务**：AI 推单定时任务与 AI 服务调用必须在 qy 环境可用，否则只改前端会导致“空内容”。
5) **外部接口路由**：`/api/friend/pushOrder/external/1.0/*` 必须在 qy 环境可访问且鉴权一致。

### 6.2.1 仅考虑 APP 端“手动推单/展示”场景
若仅评估用户端浏览、详情查看、排行等展示链路，且后端已配置完成，则 **可能只需改产品 code/路由** 即可达成目标。

**前提条件（必须同时满足）：**
1) `/api/friend/pushOrder/external/1.0/*` 在 qy 环境可访问且鉴权一致
2) `PUSHORDER_PRODUCT` 已包含 qy，后端识别该产品
3) 数据库已有 qy 维度的推单内容（否则页面为空）

**结论**：
- 若以上三点成立：**客户端改 code/路由即可**（仅展示链路）
- 若有任一不成立：仍需补齐后端配置或数据

## 6.3 参数解密对照（解密 → 参数 → 接口 → Controller → 数据库）
**解密工具**：使用 [docs-1/aes_decrypt.py](docs-1/aes_decrypt.py) 对 requestData 解密。解密后得到 JSON 参数，再进行字段与接口映射。

建议流程：
1) 抓包获取 requestData（加密）
2) 使用脚本解密得到 JSON 参数（如 `userId`、`pushOrderId`、`pageNum`、`pageSize` 等）
3) 依据接口路径定位 Controller 与业务逻辑
4) 依据参数定位数据库表字段

### 6.3.1 解密参数 → 接口 & Controller 对照（红单 11 接口）
归属：dc-api-friend / PushOrderExternalController
- `/findProgrammePreferredEntity`
- `/findMonthlyRankingPageList`
- `/findPersonalInfoPageList`
- `/findMonthlyRankingFirstList`
- `/findMatchPreferredPageList`
- `/findMasterDetailed`
- `/findMyAttentionPageList`
- `/pushOrderClickReceive`
- `/findPlanDetailed`
- `/findProgrammePreferredPageList`
- `/findMyPurchasePageList`

### 6.3.2 解密参数 → 数据库对照（待实库核对）
以下表与字段来自现有红单数据流文档：
- `push_order_ai_user`：`product`、`user_name`、`user_type`、`league_id`、`status`
- `push_order_content_management`：`match_id`、`league_id`、`match_start_time`、`odds` 等
- `system_parameter`：`PUSHORDER_PRODUCT`（包含 qy）

**影响**：若解密参数中包含 `product` 或隐含产品路由（domain/host），需要确保 qy 的产品 code 能被后端逻辑识别，否则接口返回空或报错。

## 7. 实施建议（原则）
- 以 qm 为事实标准：接口、字段、状态机、权限
- 最小差异迁移：若 qy 有既有约束，做适配而非重写
- 以接口抓包为对齐依据：先对齐“主链路”再补齐外围功能

## 8. 你需要做的 Action（当前阶段）
### A. 需求澄清与对齐
1) 收集 qm 全量接口抓包（请求/响应/错误码）
2) 标注每个接口的使用场景、调用方、频率
3) 确认 qy 侧产品 code 与路由/网关规则
4) 抓包去重：区分“红单核心接口”与“页面通用依赖接口”

### B. 差异分析
5) 建立“接口对照表”（qm ↔ qy）
6) 标注缺失接口/字段/状态机
7) 识别权限与鉴权差异
8) 在 qy 侧核对 PushOrderExternalController 路由是否齐全（11 个外部接口）

### C. 技术落地准备
9) 在 qy 环境确认是否已有对应模块（dc-api-friend / dc-api-office）
10) 若无：规划模块落地路径（复用/迁移/部署）
11) 与数据库对齐：表结构、枚举、状态码
12) 确认 `PUSHORDER_PRODUCT` 包含 qy 产品 code，并校验接口入参里是否需要 product 字段

### D. 交付与验证
13) 优先实现主链路（创建→生成→发布→展示）
14) 用 qm 抓包回放验证 qy 一致性
15) 补齐外围接口（日志、统计、第三方、财务）

## 9. 下一步（已收到抓包）
### 9.1 当前已完成
- 已输出抓包内红单接口清单（11 个外部接口）并归属到模块/Controller
- 已给出“仅 APP 展示链路”的实施前提与结论

### 9.2 仍需补齐（字段级差异需要解密参数样本）
- **详细接口对照表（字段级差异）**：需提供每个接口的 requestData 样本或解密后的 JSON
- **接口优先级与排期建议**：以主链路与产品侧影响为准，需确认 qy 侧页面范围
- **风险清单与回避方案**：基于字段差异、鉴权差异、数据空洞与任务依赖评估
