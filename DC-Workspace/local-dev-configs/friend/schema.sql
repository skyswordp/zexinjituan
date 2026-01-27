-- ==========================================
-- Friend 工程 H2 数据库初始化脚本
-- ==========================================
--
-- 说明:
-- 1. 本脚本用于 H2 数据库的表结构初始化
-- 2. 应用启动时自动执行（仅当表不存在时）
-- 3. 根据实际需要的表逐步添加
--
-- ==========================================

-- 创建 DUAL 表（Oracle 兼容）
CREATE TABLE IF NOT EXISTS DUAL (
    DUMMY VARCHAR(1)
);

-- 插入一行数据到 DUAL
MERGE INTO DUAL KEY(DUMMY) VALUES ('X');

-- ==========================================
-- 示例表：用户红单记录表
-- ==========================================
CREATE TABLE IF NOT EXISTS F_USER_FRIEND (
    ID NUMBER(19) PRIMARY KEY,
    USER_ID NUMBER(19) NOT NULL,
    FRIEND_TYPE NUMBER(2) DEFAULT 0,
    MATCH_ID VARCHAR(50),
    MATCH_NAME VARCHAR(200),
    CREATE_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UPDATE_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    STATUS NUMBER(2) DEFAULT 1
);

-- 创建索引
CREATE INDEX IF NOT EXISTS IDX_USER_FRIEND_UID ON F_USER_FRIEND(USER_ID);
CREATE INDEX IF NOT EXISTS IDX_USER_FRIEND_MID ON F_USER_FRIEND(MATCH_ID);

-- ==========================================
-- 示例表：红单配置表
-- ==========================================
CREATE TABLE IF NOT EXISTS F_FRIEND_CONFIG (
    ID NUMBER(19) PRIMARY KEY,
    CONFIG_KEY VARCHAR(100) NOT NULL UNIQUE,
    CONFIG_VALUE VARCHAR(500),
    CONFIG_DESC VARCHAR(200),
    CREATE_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UPDATE_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 插入默认配置
MERGE INTO F_FRIEND_CONFIG KEY(CONFIG_KEY) VALUES
(1, 'friend.enabled', '1', '红单功能开关', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- ==========================================
-- 系统序列（Oracle 兼容）
-- ==========================================
CREATE SEQUENCE IF NOT EXISTS SEQ_FRIEND_ID START WITH 1000 INCREMENT BY 1;

-- ==========================================
-- 注意事项
-- ==========================================
-- 1. 如果启动时报错提示缺少某个表，在此脚本中添加对应的 CREATE TABLE 语句
-- 2. H2 的 NUMBER 类型对应 Oracle 的 NUMBER
-- 3. TIMESTAMP 对应 Oracle 的 DATE/TIMESTAMP
-- 4. 主键使用 NUMBER(19) 存储长整型 ID
--
-- 如何添加新表:
-- a) 从 Oracle 生产库导出表结构: SHOW CREATE TABLE table_name;
-- b) 将 Oracle DDL 转换为 H2 语法（通常很接近）
-- c) 添加到本文件并重启应用
-- ==========================================
