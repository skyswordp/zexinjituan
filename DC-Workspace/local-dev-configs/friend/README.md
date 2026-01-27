# Friend 模块本地开发配置文件备份

> 这些是本地开发用的配置文件，**不需要提交到 Git**
>
> 这样做的好处：不影响生产环境的配置文件

## 📁 文件说明

| 文件 | 说明 | 用途 |
|------|------|------|
| `applicationContext-local.xml` | 本地 Spring 配置 | 配置 H2 数据源 |
| `jdbc-local.properties` | H2 数据库连接配置 | 数据库连接参数 |
| `schema.sql` | 数据库初始化脚本 | 自动创建表结构 |

## 🚀 如何使用

### 方式 1: 手动复制（推荐）

当你需要本地开发时，把这些文件复制到 Friend 项目：

```bash
# 复制配置文件
cp applicationContext-local.xml ../DC-API-2018/dc-api/dc-api-friend/src/main/resources/
cp jdbc-local.properties ../DC-API-2018/dc-api/dc-api-friend/src/main/resources/properties/
cp schema.sql ../DC-API-2018/dc-api/dc-api-friend/src/main/resources/

# 修改 web.xml 启用环境切换（手动编辑）
# 把 contextConfigLocation 从：
#   classpath*:applicationContext.xml
# 改成：
#   classpath*:applicationContext${spring.profiles.active:}.xml
```

### 方式 2: 使用符号链接（高级）

```bash
cd DC-API-2018/dc-api/dc-api-friend/src/main/resources/
mklink applicationContext-local.xml ..\..\..\..\..\..\local-dev-configs\friend\applicationContext-local.xml
mklink schema.sql ..\..\..\..\..\..\local-dev-configs\friend\schema.sql

cd properties/
mklink jdbc-local.properties ..\..\..\..\..\..\..\local-dev-configs\friend\jdbc-local.properties
```

## ⚠️ 注意事项

1. **这些文件不要提交到 Git**
2. 使用完本地开发后，可以删除这些文件（不影响生产环境）
3. 如果要恢复 web.xml 的改动：
   ```bash
   git checkout src/main/webapp/WEB-INF/web.xml
   ```

## 📚 相关文档

详细使用说明见：
- [Friend 本地开发指南](../../docs/FRIEND-LOCAL-DEVELOPMENT-GUIDE.md)
- [H2 数据库使用指南](../../docs/FRIEND-H2-DATABASE-GUIDE.md)
