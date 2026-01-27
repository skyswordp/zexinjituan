# 数据库连接快速指南

## 红单系统生产库连接信息

### 方式一：DBeaver（推荐 ⭐⭐⭐⭐⭐）

**下载地址：** https://dbeaver.io/download/

**安装步骤：**
1. 下载并安装 DBeaver（选择 Community Edition，免费）
2. 打开 DBeaver，点击左上角 "新建数据库连接"
3. 选择 "Oracle" → 下一步

**连接配置：**
- **主机：** `190.92.232.31`
- **端口：** `1561`
- **数据库/SID：** `pubdb`
- **用户名：** `rdpubdb`
- **密码：** `E4592gce`
- **连接类型：** 选择 "Service name"（服务名）

**首次连接：**
- DBeaver 会自动下载 Oracle JDBC 驱动，等待下载完成即可
- 如果下载失败，可以手动下载 Oracle JDBC 驱动并配置

**优点：**
- ✅ 免费开源
- ✅ 自带 Oracle 驱动
- ✅ 功能强大，支持 SQL 编辑、数据浏览、导出等
- ✅ 跨平台（Windows/Mac/Linux）

---

### 方式二：Navicat for Oracle（付费，功能最强）

**连接配置：**
- 连接名：红单系统-生产库
- 主机：190.92.232.31
- 端口：1561
- 服务名：pubdb
- 用户名：rdpubdb
- 密码：E4592gce

### 方式三：DBeaver

**连接配置：**
1. 新建连接 → Oracle
2. 主机：190.92.232.31
3. 端口：1561
4. 数据库/SID：pubdb
5. 用户名：rdpubdb
6. 密码：E4592gce

### 方式四：Oracle SQL Developer

**连接配置：**
- 连接名：红单系统-生产库
- 连接类型：Basic
- 主机名：190.92.232.31
- 端口：1561
- 服务名：pubdb
- 用户名：rdpubdb
- 密码：E4592gce

---

## 常用查询示例

### 查询 qm 产品的红单数据
```sql
SELECT * FROM pubdb.PUSH_ORDER_CONTENT_MANAGEMENT 
WHERE product='at' AND state='2'
ORDER BY create_time DESC;
```

### 查询 qy 产品的红单数据
```sql
SELECT * FROM pubdb.PUSH_ORDER_CONTENT_MANAGEMENT 
WHERE product='qy' AND state='2'
ORDER BY create_time DESC;
```

### 查询推单参数配置
```sql
SELECT * FROM pubdb.PUSH_ORDER_PARAM_CONFIG 
WHERE product='at';
```

---

## 注意事项

1. **表名前缀**：查询时必须加上 `pubdb.` 前缀
2. **只读权限**：`rdpubdb` 用户只有查询权限，不能修改数据
3. **产品区分**：通过 `product` 字段区分不同产品
   - qm 产品：`product='at'`
   - qy 产品：`product='qy'`

