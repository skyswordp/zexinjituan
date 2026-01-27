-- ==========================================
-- qm -> qy 红单复刻：配置初始化和系统参数配置
-- 执行位置：在 Query1.sql 中执行
-- 数据库：pubdb (生产库)
-- 用户：rdpubdb (只读用户，需要写入权限时请联系管理员)
-- ==========================================

-- ==========================================
-- 第一部分：配置初始化
-- ==========================================

-- ==========================================
-- 1.1 推单参数配置初始化
-- ==========================================
-- 操作：复制qm（at）的推单参数配置到qy

-- 步骤1：先查看qm（at）的配置（验证源数据）
SELECT 
    PRODUCT,
    TYPE,
    USER_LEVEL,
    PRICE,
    CREATE_TIME,
    OPERATOR,
    DEL,
    COUNT(*) OVER() AS total_count
FROM pubdb.PUSH_ORDER_PARAM_CONFIG
WHERE PRODUCT = 'at'
  AND DEL = '0'
ORDER BY TYPE, USER_LEVEL;

-- 步骤2：执行复制（需要写入权限）
-- ⚠️ 注意：如果当前用户是只读用户，需要联系管理员执行
INSERT INTO pubdb.PUSH_ORDER_PARAM_CONFIG (
    PRODUCT, TYPE, USER_LEVEL, PRICE, CREATE_TIME, OPERATOR, OPERATOR_TIME, DEL
)
SELECT 
    'qy' AS PRODUCT,  -- 改为qy
    TYPE, 
    USER_LEVEL, 
    PRICE, 
    SYSDATE AS CREATE_TIME, 
    'system' AS OPERATOR, 
    SYSDATE AS OPERATOR_TIME, 
    DEL
FROM pubdb.PUSH_ORDER_PARAM_CONFIG
WHERE PRODUCT = 'at'  -- 从qm（at）复制
  AND DEL = '0';

-- 步骤3：验证qy配置已创建
SELECT 
    PRODUCT,
    TYPE,
    USER_LEVEL,
    PRICE,
    CREATE_TIME,
    OPERATOR,
    DEL,
    COUNT(*) OVER() AS total_count
FROM pubdb.PUSH_ORDER_PARAM_CONFIG
WHERE PRODUCT = 'qy'
ORDER BY TYPE, USER_LEVEL;

-- 步骤4：对比qm和qy的配置数量（应该一致）
SELECT 
    PRODUCT,
    COUNT(*) AS config_count
FROM pubdb.PUSH_ORDER_PARAM_CONFIG
WHERE PRODUCT IN ('at', 'qy')
  AND DEL = '0'
GROUP BY PRODUCT
ORDER BY PRODUCT;

-- ==========================================
-- 1.2 等级称号配置初始化
-- ==========================================
-- 操作：复制qm（at）的等级称号配置到qy

-- 步骤1：先查看qm（at）的配置（验证源数据）
SELECT 
    PRODUCT,
    TYPE,
    LEVEL,
    TITLE,
    SORT,
    CREATE_TIME,
    OPERATOR,
    DEL,
    COUNT(*) OVER() AS total_count
FROM pubdb.PUSH_ORDER_LEVEL_TITLE_CONFIG
WHERE PRODUCT = 'at'
  AND DEL = '0'
ORDER BY TYPE, SORT;

-- 步骤2：执行复制（需要写入权限）
-- ⚠️ 注意：如果当前用户是只读用户，需要联系管理员执行
INSERT INTO pubdb.PUSH_ORDER_LEVEL_TITLE_CONFIG (
    PRODUCT, TYPE, LEVEL, TITLE, SORT, CREATE_TIME, OPERATOR, OPERATOR_TIME, DEL
)
SELECT 
    'qy' AS PRODUCT,  -- 改为qy
    TYPE, 
    LEVEL, 
    TITLE, 
    SORT, 
    SYSDATE AS CREATE_TIME, 
    'system' AS OPERATOR, 
    SYSDATE AS OPERATOR_TIME, 
    DEL
FROM pubdb.PUSH_ORDER_LEVEL_TITLE_CONFIG
WHERE PRODUCT = 'at'  -- 从qm（at）复制
  AND DEL = '0';

-- 步骤3：验证qy配置已创建
SELECT 
    PRODUCT,
    TYPE,
    LEVEL,
    TITLE,
    SORT,
    CREATE_TIME,
    OPERATOR,
    DEL,
    COUNT(*) OVER() AS total_count
FROM pubdb.PUSH_ORDER_LEVEL_TITLE_CONFIG
WHERE PRODUCT = 'qy'
ORDER BY TYPE, SORT;

-- 步骤4：对比qm和qy的配置数量（应该一致）
SELECT 
    PRODUCT,
    COUNT(*) AS config_count
FROM pubdb.PUSH_ORDER_LEVEL_TITLE_CONFIG
WHERE PRODUCT IN ('at', 'qy')
  AND DEL = '0'
GROUP BY PRODUCT
ORDER BY PRODUCT;

-- ==========================================
-- 第二部分：系统参数配置
-- ==========================================

-- ==========================================
-- 2.1 查询当前系统参数配置
-- ==========================================
-- 查看 PUSHORDER_PRODUCT 参数的当前值
SELECT 
    PARAMETER_NAME,
    PARAMETER_VALUE,
    DESCRIPTION,
    UPDATE_TIME
FROM pubdb.SYSTEM_PARAMETER
WHERE PARAMETER_NAME = 'PUSHORDER_PRODUCT';

-- 或者使用 CODE 字段（根据实际表结构选择）
SELECT 
    CATEGORY,
    CODE,
    VALUE,
    DESCRIPTION,
    UPDATE_TIME
FROM pubdb.SYSTEM_PARAMETER
WHERE CATEGORY = 'PUSHORDER'
  AND CODE = 'PUSHORDER_PRODUCT';

-- ==========================================
-- 2.2 更新系统参数（添加qy到产品列表）
-- ==========================================
-- ⚠️ 注意：如果当前用户是只读用户，需要联系管理员执行

-- 方式1：如果使用 PARAMETER_NAME 字段
UPDATE pubdb.SYSTEM_PARAMETER 
SET PARAMETER_VALUE = PARAMETER_VALUE || ',qy',
    UPDATE_TIME = SYSDATE
WHERE PARAMETER_NAME = 'PUSHORDER_PRODUCT'
  AND PARAMETER_VALUE NOT LIKE '%qy%';  -- 避免重复添加

-- 方式2：如果使用 CODE 字段（根据实际表结构选择）
UPDATE pubdb.SYSTEM_PARAMETER 
SET VALUE = VALUE || ',qy',
    UPDATE_TIME = SYSDATE
WHERE CATEGORY = 'PUSHORDER'
  AND CODE = 'PUSHORDER_PRODUCT'
  AND VALUE NOT LIKE '%qy%';  -- 避免重复添加

-- ==========================================
-- 2.3 验证系统参数已更新
-- ==========================================
-- 验证qy已添加到参数值中
SELECT 
    PARAMETER_NAME,
    PARAMETER_VALUE,
    CASE 
        WHEN PARAMETER_VALUE LIKE '%qy%' THEN '✅ qy已添加'
        ELSE '❌ qy未添加'
    END AS status,
    UPDATE_TIME
FROM pubdb.SYSTEM_PARAMETER
WHERE PARAMETER_NAME = 'PUSHORDER_PRODUCT';

-- 或者使用 CODE 字段
SELECT 
    CATEGORY,
    CODE,
    VALUE,
    CASE 
        WHEN VALUE LIKE '%qy%' THEN '✅ qy已添加'
        ELSE '❌ qy未添加'
    END AS status,
    UPDATE_TIME
FROM pubdb.SYSTEM_PARAMETER
WHERE CATEGORY = 'PUSHORDER'
  AND CODE = 'PUSHORDER_PRODUCT';

-- ==========================================
-- 第三部分：综合验证
-- ==========================================

-- 3.1 验证所有配置是否完整
SELECT 
    '推单参数配置' AS config_type,
    PRODUCT,
    COUNT(*) AS count,
    CASE 
        WHEN PRODUCT = 'at' THEN 'qm产品（源）'
        WHEN PRODUCT = 'qy' THEN 'qy产品（目标）'
        ELSE '其他'
    END AS description
FROM pubdb.PUSH_ORDER_PARAM_CONFIG
WHERE PRODUCT IN ('at', 'qy')
  AND DEL = '0'
GROUP BY PRODUCT
UNION ALL
SELECT 
    '等级称号配置' AS config_type,
    PRODUCT,
    COUNT(*) AS count,
    CASE 
        WHEN PRODUCT = 'at' THEN 'qm产品（源）'
        WHEN PRODUCT = 'qy' THEN 'qy产品（目标）'
        ELSE '其他'
    END AS description
FROM pubdb.PUSH_ORDER_LEVEL_TITLE_CONFIG
WHERE PRODUCT IN ('at', 'qy')
  AND DEL = '0'
GROUP BY PRODUCT
ORDER BY config_type, PRODUCT;

-- 3.2 验证系统参数格式（确认逗号分隔格式正确）
SELECT 
    '系统参数' AS config_type,
    PARAMETER_VALUE AS value,
    LENGTH(PARAMETER_VALUE) - LENGTH(REPLACE(PARAMETER_VALUE, ',', '')) + 1 AS product_count,
    CASE 
        WHEN PARAMETER_VALUE LIKE '%qy%' THEN '✅ 包含qy'
        ELSE '❌ 不包含qy'
    END AS qy_status
FROM pubdb.SYSTEM_PARAMETER
WHERE PARAMETER_NAME = 'PUSHORDER_PRODUCT';

-- ==========================================
-- 执行说明：
-- 1. 先执行查询SQL，确认源数据（qm/at）存在
-- 2. 执行INSERT/UPDATE SQL（需要写入权限）
-- 3. 执行验证SQL，确认配置已创建/更新
-- 4. 如果当前用户是只读用户，需要联系管理员执行写入操作
-- ==========================================

