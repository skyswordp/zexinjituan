# 三方依赖 & 全局共享配置

红单功能涉及的配置分两类：全局共享的（不用管）和按产品隔离的（需要初始化）。

---

## 一、全局共享（QY不用管）

这些数据所有产品共用，QY自动继承，不需要单独配置。

### 1. 热门联赛 - OB_NAMI_LEAGUE_R
```
作用：标记哪些联赛是热门（英超、西甲、NBA等）
AI推单会优先选这些联赛的比赛生成推单
SQL：select ob_league_id from OB_NAMI_LEAGUE_R where is_hot=1
特点：没有product字段，全局共享
```

### 2. 体育赛事数据 - SPORT_LEAGUES / SPORT_MATCHS
```
作用：联赛信息、比赛信息
来源：体育数据抓取服务自动同步
特点：基础数据，全局共享
```

---

## 二、按产品隔离（QY需要初始化）

这些数据按product字段隔离，QY需要单独配置。

### 1. 推单参数配置 - PUSH_ORDER_PARAM_CONFIG
```
作用：VIP等级要求、每日推单次数限制、售价等
初始化：SQL复制QM数据，改product='qy'
```

### 2. 等级称号配置 - PUSH_ORDER_LEVEL_TITLE_CONFIG
```
作用：足球大师、篮球大师等称号配置
初始化：SQL复制QM数据，改product='qy'
```

### 3. 系统参数 - SYSTEM_PARAMETER
```
作用：告诉定时任务要处理哪些产品
初始化：PUSHORDER_PRODUCT 值改成 'at,qy'
```

### 4. 推单AI用户 - PUSH_ORDER_AI_USER
```
作用：配置哪些用户参与AI自动推单
初始化：登录QY后台手动配置
```

### 5. 联赛类型 - SPORT_LEAGUES_TYPE
```
作用：联赛分类tab（五大联赛、FIFA、欧冠等）
初始化：登录QY后台手动配置
```

---

## 三、后台管理接口（不用改代码）

这些后台接口已支持多产品，登录对应产品后台自动隔离数据。

```
/api/friend/pushOrder/permissionRecord/pageList  → 推单权限记录
/api/friend/pushOrder/contentManagement/*        → 推单内容管理
/api/friend/pushOrder/paramConfig/*              → 推单参数配置
/api/friend/pushOrder/aiUser/*                   → AI用户管理
/api/friend/pushOrder/levelTitleConfig/*         → 等级称号配置
/api/sport/hotLegues/*                           → 热门联赛配置
/api/sport/leaguesType/*                         → 联赛类型配置
```

**原理：** 都通过 `getOperatorProductCode(request)` 从登录session获取product

---

## 四、总结

```
QY要做的事：
├── SQL初始化（3个）
│   ├── PUSH_ORDER_PARAM_CONFIG - 复制数据
│   ├── PUSH_ORDER_LEVEL_TITLE_CONFIG - 复制数据
│   └── SYSTEM_PARAMETER - 更新PUSHORDER_PRODUCT
│
└── 后台手动配置（2个）
    ├── 推单AI用户 - 配置哪些用户自动推单
    └── 联赛类型 - 配置联赛分类tab

QY不用管的事：
├── 热门联赛配置 - 全局共享
├── 体育赛事数据 - 全局共享
└── 后台管理接口 - 已支持多产品
```
