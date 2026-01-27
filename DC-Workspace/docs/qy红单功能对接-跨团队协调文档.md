# qy 红单功能对接 - 跨团队协调文档

## 📋 背景

将 `qm` 产品的红单功能复制到 `qy` 产品，需要解决两个问题：

1. **用户数据同步**：`qy` 用户需要同步到 `F_USER` 表
2. **接口加密对接**：`qy` 客户端访问红单接口需要实现加密

**当前状态**：✅ 已通过测试验证，技术方案可行。

---

## 🎯 问题一：qy 用户同步到 F_USER 表

### 问题
红单功能依赖 `F_USER` 表，但 `qy` 用户目前在 MySQL 的 `game_user` 表中。

### 解决方案
调用接口同步用户数据到 `F_USER` 表。

### 接口信息
- **地址**：`https://pt777aiguo.mypengyouquan.com/api/friend/user/1.0/inerst`
- **方式**：`POST`
- **参数**：`requestData`（AES 加密的 JSON 字符串）

### 请求格式

**明文 JSON**：
{
  "sid": "设备唯一标识（UUID）",
  "product": "qy",
  "data": {
    "userName": "用户登录名（必须与 game_user.loginname 一致）",
    "nickName": "用户昵称",
    "product": "qy"
  }
}**加密方式**：
1. AES 加密（密钥：`smkldospdosldaaa`，IV：`0000000000000000`）
2. Base64 编码
3. URL 编码（`+`→`%2B`，`/`→`%2F`，`=`→`%3D`）

### 需要 qy 系统团队完成
1. 新用户创建时，调用接口同步到 `F_USER` 表
2. 处理存量用户（批量或按需同步）
3. 实现加密逻辑（参考 `dc-common` 模块的 `AESUtil` 类）

**参考代码**：`DC-API-2018/dc-api/dc-api-friend/src/test/java/com/dc/it/test/AESHelper.java`

---

## 🎯 问题二：qy 客户端访问红单接口的加密

### 问题
红单接口要求所有请求参数必须 AES 加密 + URL 编码，否则无法访问。

### 解决方案
前端实现加密逻辑，将请求参数加密后发送。

### 请求格式

**所有红单接口都需要这样调用**：
- 接口地址：`https://pt777aiguo.mypengyouquan.com/api/friend/xxx`
- 请求方式：`POST`
- Content-Type：`application/x-www-form-urlencoded`
- 参数：`requestData`（加密后的字符串）

**请求参数 JSON 结构**：
{
  "sid": "设备唯一标识（UUID）",
  "product": "qy",
  "token": "用户登录后的 token（从 qy 登录接口获取）",
  "data": {
    // 具体业务参数
  }
}**加密方式**：同问题一（AES + Base64 + URL 编码）

### 需要 qy 前端团队完成
1. 实现 AES 加密工具类（参考 `AESUtil`）
2. 修改所有红单接口请求，添加加密逻辑
3. 确保 `token` 正确传递到加密参数中

**说明**：
- ✅ 后端会自动解析和验证 `token`（已有 `getTokenUser()` 和 `getLoginNamePlayer()` 方法，在 `dc-api-friend` 的 `BaseController` 中）
- ✅ 前端只需实现加密，无需后端额外对接

---

## ✅ 验证结果

- ✅ 成功创建 3 个测试用户（`adults123`, `adults124`, `adults125`）
- ✅ 用户数据正确写入 `F_USER` 表，`product = 'qy'`
- ✅ 接口加密逻辑已验证通过

---

## 📝 总结

**需要配合的团队**：
1. **qy 系统团队**：实现用户数据同步（问题一）
2. **qy 前端团队**：实现接口加密（问题二）

**预计工作量**：
- 问题一：1-2 个工作日
- 问题二：2-3 个工作日

**阻塞风险**：不完成这两项工作，qy 红单功能无法正常使用。