# AI Coding Agent Instructions

## 项目概述

这是一个多项目工作空间，包含4个主要系统的开发和维护工作：

1. **DC-API-2018** - 体育赛事/红单推荐微服务系统 (Java Spring/Vue2)
2. **CRM** - 客户关系管理系统 (Spring Boot 后端 + Vue2 前端)
3. **PNG** - 数据聚合系统 (传统 Java Web + Struts)
4. **生产环境文档** - 部署和配置参考

## 架构模式

### DC-API-2018 (微服务架构)
- **分层结构**: dc-api → dc-service → dc-dao → dc-domain
- **15个微服务模块**，主要关注：
  - `dc-api-dcsport` (端口8097) - 体育赛事数据聚合
  - `dc-api-sportcron` (端口8099) - 体育数据定时爬取
  - `dc-api-friend` (端口8081) - 红单推荐/社交功能
  - `dc-modules-office` - Vue2 后台管理前端
- **技术栈**: Spring 4.3.12 + MyBatis + Oracle/MySQL/MongoDB + Redis + Kafka
- **启动方式**: 按 F5 选择对应模块（已配置 launch.json）

### CRM (前后端分离)
- **后端** (`crm-server`): Spring Boot 2.0 + MyBatis + Oracle
- **前端** (`crm-vue`): Vue 2.5.17 + Element UI 2.12 + Axios
- **功能模块**: 额度审核、风控管理、会员管理
- **开发特点**: 需求频繁变更，优先快速迭代

### PNG (传统架构)
- **技术栈**: Java 1.8 + Struts + Oracle
- **部署**: Tomcat 8.5，通过自定义脚本编译部署
- **构建命令**: 使用 `.devtools/build.ps1` 或 VSCode 任务 "PNG: Build Project"
- **调试**: 已配置 F5 热部署调试（见根目录 `.vscode/launch.json`）

## 关键开发工作流

### DC-API-2018 开发
```bash
# 1. 编译整个项目（多模块Maven）
cd DC-Workspace/DC-API-2018
mvn clean install -DskipTests

# 2. 启动单个模块（推荐使用 F5）
# - 选择 "🎯 Launch DcSportApplication" 或其他配置
# - 本地开发 Friend 模块时选择 "🟢 Launch Friend - Local H2"

# 3. 配置切换机制
# Friend 模块通过 spring.profiles.active 参数控制：
# - 本地开发: -local (使用 H2 内存数据库)
# - 生产环境: 默认 (使用加密的 Oracle 配置)
```

### CRM 开发流程
```bash
# 后端启动（Spring Boot）
cd crm-server
mvn spring-boot:run

# 前端开发
cd crm-vue
npm run dev  # 开发模式
npm run build  # 生产构建（使用 gulp）
```

### PNG 开发流程
```powershell
# 使用 VSCode 任务（推荐）
# Ctrl+Shift+P → "Tasks: Run Task" → "PNG: Build Project"

# 或手动编译
.devtools/build.ps1

# 部署到 Tomcat
.devtools/deploy_to_tomcat.bat

# F5 调试
# 使用配置: "PNG - Debug Tomcat (Hot Swap)"
```

## 代码组织约定

### Java 后端模式
- **Controller 层**: 负责请求映射，使用 `@RestController` / `@RequestMapping`
- **Service 层**: 业务逻辑实现，使用 `@Service("beanName")` 注解
- **DAO 层**: 数据访问，MyBatis XML 映射文件与接口分离
- **Domain/POJO**: 实体类在 `dc-domain` / `crm-domain` 中，VO/DTO 按模块分包
- **命名规范**: 
  - Service 实现类后缀 `ServiceImpl`
  - DAO 接口后缀 `Dao`，XML 文件同名放在 resources 下

### Vue 前端模式 (DC/CRM 通用)
- **路由**: `src/router/index.js` 定义，按功能模块分组
- **状态管理**: `src/store/` Vuex 模块化
- **API 调用**: `src/utils/request.js` 封装 axios，统一拦截器
- **组件**: `src/views/` 页面级组件，`src/components/` 通用组件
- **Element UI**: 使用千分位格式化金额、日期选择器默认当天时间范围

### CRM 前端特定约定
- **列表页命名**: `transferARM.vue` (列表) + `transferARM-add-or-update.vue` (表单)
- **格式化函数**: 等级显示使用 `levelFormat`，金额使用千分位+两位小数
- **表单校验**: 必填字段前端校验，后端也需幂等性校验（如审核只能操作一次）

## 数据库连接管理

### 开发环境
- **DC Friend 模块**: 本地使用 H2 内存数据库（Oracle 兼容模式），无需 VPN
- **CRM/PNG**: 连接测试库 `pubdbdev` (119.13.81.81:1521)
  - PNG 用户: `pngdev / EO97nh12gloi`
  - Game API 用户: `pubdb / CiuXZ482PZwx`

### 生产环境（只读）
- **PNG 库**: `pngrd@190.92.232.31:1531/pngp` (查询需前缀 `pngdev.`)
- **GAMEAPI 库**: `rdpubdb@190.92.232.31:1561/pubdb` (查询需前缀 `pubdb.`)
- **访问要求**: 需 VPN 连接 (https://18.166.253.125:943/)

### 配置文件加密
DC-API-2018 生产配置使用加密的 `jdbc.properties`，启动时自动解密。本地开发使用 `jdbc-local.properties` 明文配置。

## 常见任务参考

### 查看日志
```bash
# PNG Tomcat 日志
Get-Content C:\apache-tomcat-8.5.100\logs\tomcat-console.log -Tail 100

# 或使用 VSCode 任务: "PNG: 查看控制台日志"
```

### 数据库查询
查询生产表时必须加用户前缀，例如：
```sql
-- PNG 生产库
SELECT * FROM pngdev.KYQP_DATA_ZB WHERE ...

-- GAMEAPI 生产库  
SELECT * FROM pubdb.MEMBER WHERE ...
```

### 需求实现检查清单（CRM 示例）
根据 `0-tech-docs/4-work-tasks.md` 模板：
1. 前端表单校验 + 后端参数验证
2. 列表列宽优化 + 数据格式化（千分位、日期、等级名称）
3. 按钮状态控制（已处理数据禁用操作）
4. 默认值设置（日期范围、全选逻辑）
5. 前后端字段映射确认（新增字段需同步修改 VO/DTO/XML）

## 参考文档位置

- **开发笔记**: `DC-Workspace/README.md` - DC 项目架构和接口梳理
- **本地调试指南**: `DC-Workspace/LOCAL-DEBUG-GUIDE.md` - F5 启动配置
- **Friend 开发指南**: `DC-Workspace/docs/FRIEND-LOCAL-DEVELOPMENT-GUIDE.md` - H2 数据库配置
- **需求任务**: `0-tech-docs/4-work-tasks.md` - CRM 需求拆解和进度跟踪
- **账号密码**: `0-tech-docs/0-账号密码.md` - 数据库/VPN/GitLab 凭证
- **生产文档**: `production-docs-detail/` - 线上服务配置参考

## 特殊注意事项

1. **DC-Workspace 目录结构**: 外层是工作空间（可放个人笔记），内层 `DC-API-2018/` 才是 Git 仓库
2. **主干开发模式**: DC 项目直接在 master 分支开发，小步提交，提交前 `git pull`
3. **模块间依赖**: DC 项目需先 `mvn install` 父模块才能启动子模块
4. **PNG 编译特殊性**: 必须检查 `KYQPDataZB.class` 是否生成，编译失败需查看源文件路径
5. **CRM 需求变更**: 优先看 `4-work-tasks.md` 了解当前开发任务和完成状态
6. **数据库访问限制**: 生产库只读，测试库可写，修改生产数据需联系 SRE

---

*最后更新: 2025-12-23*
