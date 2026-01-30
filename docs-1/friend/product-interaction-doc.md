# 朋友圈产品交互文档

> 基于 API 测试日志 + 后端代码整理，21 个接口的请求/响应字段说明

---

## 架构总览

![朋友圈产品交互架构图](architecture-diagram.png)

---

## 接口规范

| 项目 | 说明 |
|------|------|
| 请求方式 | POST |
| Content-Type | application/json;charset=UTF-8 |
| 成功响应码 | code = "10000" |
| 业务错误码 | code = "10001" |

---

## 1. 个人中心模块

### 1.1 getUser - 获取用户资料

**接口**: `POST /api/friend/user/1.0/getUser`

**请求参数**:
```json
{
  "id": "488714",
  "userId": "488714"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | String | 是 | 要查询的用户ID |
| userId | String | 是 | 当前登录用户ID（用于判断是否已关注） |

**响应示例**:
```json
{
  "code": "10000",
  "data": {
    "id": 488714,
    "userName": "adults123",
    "nickName": "test",
    "headUrl": "https://example.com/new.png",
    "product": "lh",
    "isSpeak": 0,
    "status": "Y",
    "createTime": 1768475918000,
    "followNum": 4,
    "fassNum": 0,
    "isFollow": 0,
    "userLevel": 0,
    "totalPopularityShow": 0,
    "redOrderRateShow": 0,
    "profitRateShow": 0
  },
  "message": "系统成功"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Long | 用户ID |
| userName | String | 用户账号（唯一标识） |
| nickName | String | 用户昵称 |
| headUrl | String | 头像URL |
| product | String | 来源平台（lh=龙虎） |
| isSpeak | Long | 是否禁言：0=正常，1=禁言 |
| status | String | 状态：Y=启用，N=禁用 |
| createTime | Long | 创建时间戳 |
| followNum | Long | 关注数 |
| fassNum | Long | 粉丝数 |
| isFollow | Long | 当前用户是否已关注：0=未关注，1=已关注 |
| userLevel | Integer | 用户等级 |
| totalPopularityShow | Long | 总人气值 |
| redOrderRateShow | Double | 红单率 |
| profitRateShow | Double | 收益率 |

---

### 1.2 update - 更新用户资料

**接口**: `POST /api/friend/user/1.0/update`

**请求参数**:
```json
{
  "id": "488714",
  "nickName": "test",
  "headUrl": "https://example.com/new.png"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | String | 是 | 用户ID |
| nickName | String | 否 | 新昵称 |
| headUrl | String | 否 | 新头像URL |

**响应示例**:
```json
{
  "code": "10000",
  "data": null,
  "message": "系统成功"
}
```

---

### 1.3 getMyPraiseCount - 获取消息计数

**接口**: `POST /api/friend/user/1.0/getMyPraiseCount`

**请求参数**:
```json
{
  "userId": "488714"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| userId | String | 是 | 用户ID |

**响应示例**:
```json
{
  "code": "10000",
  "data": {
    "comments": 0,
    "mentionMe": 0,
    "COMMENTS": 0,
    "PRAISE": 0,
    "praise": 0,
    "MENTIONME": 0
  },
  "message": "系统成功"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| comments / COMMENTS | Long | 未读评论数 |
| praise / PRAISE | Long | 未读点赞数 |
| mentionMe / MENTIONME | Long | 未读@我数 |

---

### 1.4 getLevel - 获取等级权限

**接口**: `POST /api/friend/levelSetting/1.0/getLevel`

**请求参数**:
```json
{
  "account": "adults123",
  "money": 0,
  "levelId": "1"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| account | String | 是 | 用户账号 |
| money | Number | 否 | 充值金额（用于等级计算） |
| levelId | String | 否 | 等级ID |

**响应示例**:
```json
{
  "code": "10000",
  "data": {
    "id": null,
    "name": null,
    "account": null,
    "flag": "Y",
    "isPublish": "Y",
    "isPraise": "Y",
    "isComment": "Y",
    "product": null
  },
  "message": "系统成功"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| flag | String | 是否有效：Y=是，N=否 |
| isPublish | String | 是否可发帖：Y=可以，N=禁止 |
| isPraise | String | 是否可点赞：Y=可以，N=禁止 |
| isComment | String | 是否可评论：Y=可以，N=禁止 |

---

## 2. 社交关系模块

### 2.1 saveFollow - 关注/取消关注

**接口**: `POST /api/friend/user/1.0/saveFollow`

**请求参数**:
```json
{
  "userId": "488714",
  "beUserId": "100001",
  "type": "1"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| userId | String | 是 | 操作人ID（当前登录用户） |
| beUserId | String | 是 | 被关注人ID |
| type | String | 是 | 操作类型：1=关注，2=取消关注 |

**成功响应**:
```json
{
  "code": "10000",
  "data": null,
  "message": "系统成功"
}
```

**业务错误响应**:
```json
{
  "code": "10001",
  "message": "您已关注过该用户"
}
```

---

## 3. 朋友圈动态模块

### 3.1 saveCircle - 发布动态

**接口**: `POST /api/friend/circle/1.0/saveCircle`

**请求参数**:
```json
{
  "userId": "489714",
  "content": "test"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| userId | String | 是 | 发布人ID |
| content | String | 是 | 动态内容 |
| imagePath | String | 否 | 图片路径（多个用逗号分隔） |
| videoPath | String | 否 | 视频路径 |
| videoImg | String | 否 | 视频封面图 |
| topicId | Long | 否 | 关联话题ID |

**响应示例**:
```json
{
  "code": "10000",
  "data": null,
  "message": "系统成功"
}
```

---

### 3.2 pageList - 动态列表

**接口**: `POST /api/friend/circle/2.0/pageList`

**请求参数**:
```json
{
  "pageNum": 1,
  "pageSize": 20
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pageNum | Number | 是 | 页码（从1开始） |
| pageSize | Number | 是 | 每页条数 |
| userId | Long | 否 | 用户ID（查指定用户的动态） |
| topicId | Long | 否 | 话题ID（查指定话题的动态） |

**响应示例**:
```json
{
  "code": "10000",
  "data": {
    "pageNum": 1,
    "pageSize": 20,
    "total": 12337,
    "pages": 617,
    "list": [
      {
        "id": 1692098,
        "userId": 426109,
        "isPaise": "N",
        "userName": "LH867152",
        "userLevel": 15,
        "nickName": "Win哥",
        "headUrl": "https://xxx/avatar.jpeg",
        "content": "动态内容...",
        "commentCount": 4,
        "praiseCount": 16,
        "status": 0,
        "createTime": 1769511496000,
        "showTime": "2026-01-27 18:58:16",
        "videoPath": null,
        "videoImg": null,
        "circleSort": 1,
        "hot": 0,
        "bright": 0,
        "type": 0,
        "topicId": null,
        "topicIcon": null,
        "topicTitle": null,
        "voteThemes": [],
        "imageList": []
      }
    ]
  },
  "message": "系统成功"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Long | 动态ID |
| userId | Long | 发布人ID |
| userName | String | 发布人账号 |
| nickName | String | 发布人昵称 |
| headUrl | String | 发布人头像 |
| userLevel | Integer | 发布人等级 |
| content | String | 动态内容 |
| commentCount | Long | 评论数 |
| praiseCount | Long | 点赞数 |
| status | Long | 审核状态：0=通过，1=未通过 |
| createTime | Long | 创建时间戳 |
| showTime | String | 显示时间（如"1分钟前"） |
| videoPath | String | 视频地址 |
| videoImg | String | 视频封面 |
| imageList | List | 图片列表 |
| circleSort | Long | 排序权重（越大越靠前） |
| hot | Long | 是否热门：0=否，1=是 |
| bright | Long | 是否加亮：0=否，1=是 |
| type | Long | 是否官方发布：0=普通用户，1=官方 |
| topicId | Long | 关联话题ID |
| topicIcon | String | 话题图标 |
| topicTitle | String | 话题标题 |
| isPaise | String | 当前用户是否已点赞：Y=是，N=否 |
| voteThemes | List | 投票选项列表 |

---

### 3.3 readCount - 阅读计数

**接口**: `POST /api/friend/user/1.0/readCount`

**请求参数**:
```json
{
  "type": "1",
  "id": "1689288"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | String | 是 | 类型：1=动态 |
| id | String | 是 | 动态ID |

**响应示例**:
```json
{
  "code": "10000",
  "data": null,
  "message": "系统成功"
}
```

---

### 3.4 getCountList - 获取统计

**接口**: `POST /api/friend/circle/1.0/getCountList`

**请求参数**:
```json
{
  "time": "1706345600000"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| time | String | 是 | 时间戳（获取该时间之后的动态数量） |

**响应示例**:
```json
{
  "code": "10000",
  "data": {
    "count": 16250
  },
  "message": "系统成功"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| count | Long | 新动态数量 |

---

## 4. 互动功能模块

### 4.1 saveChangePraise - 点赞/取消点赞

**接口**: `POST /api/friend/user/1.0/saveChangePraise`

**请求参数**:
```json
{
  "userId": 489714,
  "circleId": 1689288,
  "praiseType": "1",
  "type": "1"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| userId | Long | 是 | 操作人ID |
| circleId | Long | 是 | 动态ID |
| praiseType | String | 是 | 点赞对象类型：1=帖子，2=评论 |
| type | String | 是 | 操作类型：1=点赞，2=取消点赞 |

**响应示例**:
```json
{
  "code": "10000",
  "data": null,
  "message": null
}
```

---

### 4.2 saveComments - 发表评论

**接口**: `POST /api/friend/circleComments/1.0/saveComments`

**请求参数**:
```json
{
  "circleId": "1689288",
  "userId": "489714",
  "content": "test"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| circleId | String | 是 | 动态ID |
| userId | String | 是 | 评论人ID |
| content | String | 是 | 评论内容 |
| bePublishUserId | Long | 否 | 被回复人ID（回复评论时传） |

**响应示例**:
```json
{
  "code": "10000",
  "data": null,
  "message": "系统成功"
}
```

---

### 4.3 pageList - 评论列表

**接口**: `POST /api/friend/circleComments/1.0/pageList`

**请求参数**:
```json
{
  "circleId": 1689288,
  "pageNum": 1,
  "pageSize": 20
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| circleId | Long | 是 | 动态ID |
| pageNum | Number | 是 | 页码 |
| pageSize | Number | 是 | 每页条数 |

**响应示例**:
```json
{
  "code": "10000",
  "data": {
    "pageNum": 1,
    "pageSize": 20,
    "total": 50,
    "list": [
      {
        "id": 12345,
        "fCircleId": 1689288,
        "publishUserId": 489714,
        "userName": "user123",
        "nickName": "用户昵称",
        "userLevel": 5,
        "headUrl": "https://xxx/avatar.png",
        "comments": "评论内容",
        "bePublishUserId": null,
        "beNickName": null,
        "praiseCount": 0,
        "status": 0,
        "createTime": 1769511496000,
        "showTime": "1小时前",
        "isPaise": "N"
      }
    ]
  },
  "message": "系统成功"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Long | 评论ID |
| fCircleId | Long | 动态ID |
| publishUserId | Long | 评论人ID |
| userName | String | 评论人账号 |
| nickName | String | 评论人昵称 |
| userLevel | Integer | 评论人等级 |
| headUrl | String | 评论人头像 |
| comments | String | 评论内容 |
| bePublishUserId | Long | 被回复人ID |
| beNickName | String | 被回复人昵称 |
| praiseCount | Long | 评论点赞数 |
| status | Long | 审核状态：0=通过，1=未通过 |
| createTime | Long | 创建时间戳 |
| showTime | String | 显示时间 |
| isPaise | String | 当前用户是否已点赞：Y=是，N=否 |

---

### 4.4 saveShare - 分享

**接口**: `POST /api/friend/user/1.0/saveShare`

**请求参数**:
```json
{
  "userId": 489714,
  "circleId": 1689288
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| userId | Long | 是 | 分享人ID |
| circleId | Long | 是 | 动态ID |

**响应示例**:
```json
{
  "code": "10000",
  "data": null,
  "message": "系统成功"
}
```

---

### 4.5 saveReport - 举报

**接口**: `POST /api/friend/report/1.0/saveReport`

**请求参数**:
```json
{
  "id": "1689288",
  "userId": "489714",
  "type": "1",
  "reportReason": "test"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | String | 是 | 被举报内容ID（动态ID或评论ID） |
| userId | String | 是 | 举报人ID |
| type | String | 是 | 举报类型：1=举报动态，2=举报评论 |
| reportReason | String | 是 | 举报原因 |

**响应示例**:
```json
{
  "code": "10000",
  "data": null,
  "message": "系统成功"
}
```

---

## 5. 话题广场模块

### 5.1 queryTitle - 话题列表

**接口**: `POST /api/friend/topic/1.0/queryTitle`

**请求参数**:
```json
{}
```

**响应示例**:
```json
{
  "code": "10000",
  "data": [
    {
      "id": 1682,
      "title": "#PG晒图赢彩金#",
      "icon": "https://xxx/topic.png",
      "count": 1000
    }
  ],
  "message": "系统成功"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Long | 话题ID |
| title | String | 话题标题 |
| icon | String | 话题图标 |
| count | Long | 话题下动态数量 |

---

### 5.2 queryDetails - 话题详情

**接口**: `POST /api/friend/topic/1.0/queryDetails`

**请求参数**:
```json
{
  "topicId": 1,
  "pageNum": 1,
  "pageSize": 20
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| topicId | Long | 是 | 话题ID |
| pageNum | Number | 是 | 页码 |
| pageSize | Number | 是 | 每页条数 |

**响应示例**:
```json
{
  "code": "10000",
  "data": {
    "pageNum": 1,
    "pageSize": 20,
    "total": 0,
    "list": []
  },
  "message": "系统成功"
}
```

> 返回的 list 结构同 3.2 动态列表

---

## 6. 任务中心模块

### 6.1 queryTasks - 任务列表

**接口**: `POST /api/friend/task/1.0/queryTasks`

**请求参数**:
```json
{
  "userId": 489714
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| userId | Long | 是 | 用户ID |

**响应示例**:
```json
{
  "code": "10000",
  "data": [
    {
      "id": 1,
      "taskName": "每日签到",
      "taskDesc": "每日签到可获得积分",
      "reward": 10,
      "status": 0
    }
  ],
  "message": "系统成功"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Long | 任务ID |
| taskName | String | 任务名称 |
| taskDesc | String | 任务描述 |
| reward | Long | 奖励值 |
| status | Long | 完成状态：0=未完成，1=已完成 |

---

## 7. 板块功能模块

### 7.1 index/getByLevel - 首页板块

**接口**: `POST /api/friend/board/index/getByLevel`

**请求参数**:
```json
{
  "boardLevel": 1
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| boardLevel | Number | 是 | 板块等级 |

**响应示例**:
```json
{
  "code": "10000",
  "data": [
    { "id": 45, "boardTitle": "老虎机", "boardLevel": 1 },
    { "id": 46, "boardTitle": "棋牌", "boardLevel": 1 },
    { "id": 47, "boardTitle": "真人", "boardLevel": 1 },
    { "id": 48, "boardTitle": "体育", "boardLevel": 1 },
    { "id": 49, "boardTitle": "电竞", "boardLevel": 1 },
    { "id": 50, "boardTitle": "其他", "boardLevel": 1 }
  ],
  "message": "系统成功"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Long | 板块ID |
| boardTitle | String | 板块名称 |
| boardLevel | Long | 板块等级 |

---

### 7.2 guess/getByLevel - 猜你喜欢

**接口**: `POST /api/friend/board/guess/getByLevel`

**请求参数**:
```json
{
  "boardLevel": 1
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| boardLevel | Number | 是 | 板块等级 |

**响应示例**:
```json
{
  "code": "10000",
  "data": [],
  "message": "系统成功"
}
```

---

## 8. 配置管理模块

### 8.1 indexSetting/pageList - 首页配置

**接口**: `POST /api/friend/indexSetting/1.0/pageList`

**请求参数**:
```json
{
  "pageNum": 1,
  "pageSize": 20
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pageNum | Number | 是 | 页码 |
| pageSize | Number | 是 | 每页条数 |

**响应示例**:
```json
{
  "code": "10000",
  "data": {
    "pageNum": 1,
    "pageSize": 20,
    "total": 0,
    "list": []
  },
  "message": "系统成功"
}
```

---

### 8.2 gameSetting/pageList - 游戏配置

**接口**: `POST /api/friend/gameSetting/1.0/pageList`

**请求参数**:
```json
{
  "pageNum": 1,
  "pageSize": 20
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pageNum | Number | 是 | 页码 |
| pageSize | Number | 是 | 每页条数 |

**响应示例**:
```json
{
  "code": "10000",
  "data": {
    "pageNum": 1,
    "pageSize": 20,
    "total": 0,
    "list": []
  },
  "message": "系统成功"
}
```

---

## 接口清单

| # | 模块 | 接口路径 | 说明 |
|---|------|----------|------|
| 1 | 用户 | /api/friend/user/1.0/getUser | 获取用户资料 |
| 2 | 用户 | /api/friend/user/1.0/update | 更新资料 |
| 3 | 用户 | /api/friend/user/1.0/getMyPraiseCount | 消息计数 |
| 4 | 等级 | /api/friend/levelSetting/1.0/getLevel | 等级权限 |
| 5 | 社交 | /api/friend/user/1.0/saveFollow | 关注/取消 |
| 6 | 动态 | /api/friend/circle/1.0/saveCircle | 发布动态 |
| 7 | 动态 | /api/friend/circle/2.0/pageList | 动态列表 |
| 8 | 动态 | /api/friend/user/1.0/readCount | 阅读计数 |
| 9 | 动态 | /api/friend/circle/1.0/getCountList | 统计 |
| 10 | 互动 | /api/friend/user/1.0/saveChangePraise | 点赞 |
| 11 | 互动 | /api/friend/circleComments/1.0/saveComments | 评论 |
| 12 | 互动 | /api/friend/circleComments/1.0/pageList | 评论列表 |
| 13 | 互动 | /api/friend/user/1.0/saveShare | 分享 |
| 14 | 互动 | /api/friend/report/1.0/saveReport | 举报 |
| 15 | 话题 | /api/friend/topic/1.0/queryTitle | 话题列表 |
| 16 | 话题 | /api/friend/topic/1.0/queryDetails | 话题详情 |
| 17 | 任务 | /api/friend/task/1.0/queryTasks | 任务列表 |
| 18 | 板块 | /api/friend/board/index/getByLevel | 首页板块 |
| 19 | 板块 | /api/friend/board/guess/getByLevel | 猜你喜欢 |
| 20 | 配置 | /api/friend/indexSetting/1.0/pageList | 首页配置 |
| 21 | 配置 | /api/friend/gameSetting/1.0/pageList | 游戏配置 |

---

## 附录：实体类源码位置

| 实体类 | 路径 |
|--------|------|
| FUser | `DC-API-2018/dc-domain/.../friend/pojo/FUser.java` |
| FUserVO | `DC-API-2018/dc-domain/.../friend/vo/FUserVO.java` |
| Circle | `DC-API-2018/dc-domain/.../friend/pojo/Circle.java` |
| CircleAppVo | `DC-API-2018/dc-domain/.../friend/vo/CircleAppVo.java` |
| CircleComments | `DC-API-2018/dc-domain/.../friend/pojo/CircleComments.java` |
| CirclePraise | `DC-API-2018/dc-domain/.../friend/pojo/CirclePraise.java` |
| FUserFollow | `DC-API-2018/dc-domain/.../friend/pojo/FUserFollow.java` |
| FReport | `DC-API-2018/dc-domain/.../friend/pojo/FReport.java` |

---

*数据来源: api_test_20260129_204520.log + 后端源码*
