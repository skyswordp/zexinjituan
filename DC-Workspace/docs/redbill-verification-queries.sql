-- ==========================================
-- 红单系统数据库验证查询 SQL
-- 数据库: pubdb (生产库)
-- 用户: rdpubdb (只读)
-- 注意: 查询表时需要加前缀 pubdb.<表名>
-- ==========================================

-- ==========================================
-- 1. 连接验证 - 测试数据库连接是否正常
-- ==========================================
SELECT '数据库连接成功！' AS status, 
       SYSDATE AS current_time,
       USER AS current_user
FROM dual;

-- ==========================================
-- 2. 查看当前用户权限和 Schema 信息
-- ==========================================
SELECT username, 
       default_tablespace,
       created
FROM user_users;

-- ==========================================
-- 3. 查看 pubdb schema 下的所有表
-- ==========================================
SELECT table_name,
       num_rows,
       last_analyzed
FROM all_tables
WHERE owner = 'PUBDB'
ORDER BY table_name;

-- ==========================================
-- 4. 查看红单系统相关表的结构
-- ==========================================
-- 4.1 红单主表结构
SELECT column_name,
       data_type,
       data_length,
       nullable,
       data_default
FROM all_tab_columns
WHERE owner = 'PUBDB'
  AND table_name = 'PUSH_ORDER_CONTENT_MANAGEMENT'
ORDER BY column_id;

-- 4.2 推单参数配置表结构
SELECT column_name,
       data_type,
       data_length
FROM all_tab_columns
WHERE owner = 'PUBDB'
  AND table_name = 'PUSH_ORDER_PARAM_CONFIG'
ORDER BY column_id;

-- 4.3 推单等级称号配置表结构
SELECT column_name,
       data_type,
       data_length
FROM all_tab_columns
WHERE owner = 'PUBDB'
  AND table_name = 'PUSH_ORDER_LEVEL_TITLE_CONFIG'
ORDER BY column_id;

-- ==========================================
-- 5. 查询 qm 产品（product='at'）的红单数据
-- ==========================================
-- 5.1 统计 qm 产品的红单总数
SELECT COUNT(*) AS total_count,
       COUNT(CASE WHEN state = '2' THEN 1 END) AS approved_count,
       COUNT(CASE WHEN state = '1' THEN 1 END) AS pending_count,
       COUNT(CASE WHEN state = '0' THEN 1 END) AS draft_count
FROM pubdb.PUSH_ORDER_CONTENT_MANAGEMENT
WHERE product = 'at';

-- 5.2 查询 qm 产品最近 10 条已审核通过的红单
SELECT id,
       user_name,
       title,
       match_name,
       price,
       number_buyer,
       lian_hong,
       competition_results,
       profit,
       state,
       product,
       create_time
FROM pubdb.PUSH_ORDER_CONTENT_MANAGEMENT
WHERE product = 'at'
  AND state = '2'  -- 2=审核通过
ORDER BY create_time DESC
FETCH FIRST 10 ROWS ONLY;

-- 5.3 查询 qm 产品的红单赛果统计
SELECT competition_results,
       CASE competition_results
           WHEN '0' THEN '未结束'
           WHEN '1' THEN '红（赢）'
           WHEN '2' THEN '黑（输）'
           WHEN '3' THEN '和'
           WHEN '4' THEN '取消'
           ELSE '未知'
       END AS result_desc,
       COUNT(*) AS count
FROM pubdb.PUSH_ORDER_CONTENT_MANAGEMENT
WHERE product = 'at'
  AND state = '2'
GROUP BY competition_results
ORDER BY competition_results;

-- ==========================================
-- 6. 查询 qy 产品（product='qy'）的红单数据
-- ==========================================
-- 6.1 统计 qy 产品的红单总数（验证 qy 数据是否存在）
SELECT COUNT(*) AS total_count,
       COUNT(CASE WHEN state = '2' THEN 1 END) AS approved_count
FROM pubdb.PUSH_ORDER_CONTENT_MANAGEMENT
WHERE product = 'qy';

-- 6.2 查询 qy 产品最近的红单（如果有数据）
SELECT id,
       user_name,
       title,
       match_name,
       price,
       number_buyer,
       lian_hong,
       competition_results,
       state,
       product,
       create_time
FROM pubdb.PUSH_ORDER_CONTENT_MANAGEMENT
WHERE product = 'qy'
ORDER BY create_time DESC
FETCH FIRST 10 ROWS ONLY;

-- ==========================================
-- 7. 查看推单参数配置（验证配置数据）
-- ==========================================
-- 7.1 查询 qm 产品（product='at'）的推单参数配置
SELECT id,
       type,
       product,
       purchase_bonus,
       click_count_bonus,
       create_time,
       update_time
FROM pubdb.PUSH_ORDER_PARAM_CONFIG
WHERE product = 'at'
ORDER BY type, id;

-- 7.2 查询 qy 产品（product='qy'）的推单参数配置（验证是否已初始化）
SELECT id,
       type,
       product,
       purchase_bonus,
       click_count_bonus,
       create_time,
       update_time
FROM pubdb.PUSH_ORDER_PARAM_CONFIG
WHERE product = 'qy'
ORDER BY type, id;

-- 7.3 查看所有产品的配置（对比 qm 和 qy）
SELECT product,
       type,
       COUNT(*) AS config_count
FROM pubdb.PUSH_ORDER_PARAM_CONFIG
GROUP BY product, type
ORDER BY product, type;

-- ==========================================
-- 8. 查看推单等级称号配置
-- ==========================================
-- 8.1 查询 qm 产品（product='at'）的等级称号配置
SELECT id,
       product,
       level_name,
       title_name,
       min_hit_rate,
       max_hit_rate,
       create_time
FROM pubdb.PUSH_ORDER_LEVEL_TITLE_CONFIG
WHERE product = 'at'
ORDER BY min_hit_rate;

-- 8.2 查询 qy 产品（product='qy'）的等级称号配置（验证是否已初始化）
SELECT id,
       product,
       level_name,
       title_name,
       min_hit_rate,
       max_hit_rate,
       create_time
FROM pubdb.PUSH_ORDER_LEVEL_TITLE_CONFIG
WHERE product = 'qy'
ORDER BY min_hit_rate;

-- ==========================================
-- 9. 查看系统参数（验证定时任务配置）
-- ==========================================
-- 9.1 查询 AI 推单产品配置（PUSHORDER_PRODUCT 参数）
SELECT category,
       code,
       value,
       description,
       update_time
FROM pubdb.SYSTEM_PARAMETER
WHERE category = 'PUSHORDER'
  AND code = 'PUSHORDER_PRODUCT';

-- 9.2 查看所有 PUSHORDER 相关的系统参数
SELECT category,
       code,
       value,
       description
FROM pubdb.SYSTEM_PARAMETER
WHERE category = 'PUSHORDER'
ORDER BY code;

-- ==========================================
-- 10. 查看推单综合日志（验证日志数据）
-- ==========================================
-- 10.1 统计各类型日志数量
SELECT type,
       CASE type
           WHEN '0' THEN '点击'
           WHEN '1' THEN '购买'
           WHEN '2' THEN '关注'
           ELSE '未知'
       END AS type_desc,
       COUNT(*) AS log_count
FROM pubdb.PUSH_ORDER_CONTENT_GENERAL_LOG
GROUP BY type
ORDER BY type;

-- 10.2 查询最近的日志记录（前 20 条）
SELECT id,
       content_management_id,
       type,
       user_name,
       create_time
FROM pubdb.PUSH_ORDER_CONTENT_GENERAL_LOG
ORDER BY create_time DESC
FETCH FIRST 20 ROWS ONLY;

-- ==========================================
-- 11. 数据对比：qm vs qy
-- ==========================================
-- 11.1 对比两个产品的红单数据量
SELECT product,
       COUNT(*) AS total_redbills,
       COUNT(CASE WHEN state = '2' THEN 1 END) AS approved_redbills,
       SUM(number_buyer) AS total_buyers,
       SUM(profit) AS total_profit
FROM pubdb.PUSH_ORDER_CONTENT_MANAGEMENT
WHERE product IN ('at', 'qy')
GROUP BY product
ORDER BY product;

-- 11.2 对比两个产品的配置数据
SELECT product,
       COUNT(*) AS config_count
FROM pubdb.PUSH_ORDER_PARAM_CONFIG
WHERE product IN ('at', 'qy')
GROUP BY product
ORDER BY product;

-- ==========================================
-- 12. 验证数据隔离（确保 qm 和 qy 数据完全分离）
-- ==========================================
-- 12.1 检查是否有 product 字段为空或异常的数据
SELECT COUNT(*) AS null_product_count
FROM pubdb.PUSH_ORDER_CONTENT_MANAGEMENT
WHERE product IS NULL OR product NOT IN ('at', 'qy', 'qm');

-- 12.2 检查 qm 产品是否有 product='qy' 的数据（应该为 0）
SELECT COUNT(*) AS wrong_product_count
FROM pubdb.PUSH_ORDER_CONTENT_MANAGEMENT
WHERE product = 'at'
  AND user_name LIKE '%qy%';  -- 简单检查，实际应该更严格

-- ==========================================
-- 13. 性能检查：查看表的数据量
-- ==========================================
SELECT 'PUSH_ORDER_CONTENT_MANAGEMENT' AS table_name,
       COUNT(*) AS row_count
FROM pubdb.PUSH_ORDER_CONTENT_MANAGEMENT
UNION ALL
SELECT 'PUSH_ORDER_CONTENT_GENERAL_LOG',
       COUNT(*)
FROM pubdb.PUSH_ORDER_CONTENT_GENERAL_LOG
UNION ALL
SELECT 'PUSH_ORDER_PARAM_CONFIG',
       COUNT(*)
FROM pubdb.PUSH_ORDER_PARAM_CONFIG
UNION ALL
SELECT 'PUSH_ORDER_LEVEL_TITLE_CONFIG',
       COUNT(*)
FROM pubdb.PUSH_ORDER_LEVEL_TITLE_CONFIG;

-- ==========================================
-- 使用说明：
-- 1. 按顺序执行上述 SQL，验证数据库连接和数据结构
-- 2. 重点关注 qm（product='at'）和 qy（product='qy'）的数据对比
-- 3. 检查 qy 产品的配置数据是否已初始化
-- 4. 验证数据隔离是否正常
-- ==========================================

