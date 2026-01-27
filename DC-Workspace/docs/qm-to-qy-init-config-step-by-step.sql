-- ==========================================
-- qm -> qy 红单复刻：初始化配置（一步一步执行）
-- 执行位置：Oracle数据库客户端（DBeaver / SQLTools / Navicat）
-- 数据库：pubdb
-- 执行顺序：必须按顺序执行，不能跳过
-- ==========================================

-- ==========================================
-- 执行前检查：先查看qm（at）的源数据
-- ==========================================

-- 检查1：推单参数配置（at产品有多少条）
SELECT 
    '推单参数配置' AS config_name,
    PRODUCT,
    COUNT(*) AS count
FROM pubdb.PUSH_ORDER_PARAM_CONFIG
WHERE PRODUCT = 'at' AND DEL = '0'
GROUP BY PRODUCT;

-- 检查2：等级称号配置（at产品有多少条）
SELECT 
    '等级称号配置' AS config_name,
    PRODUCT,
    COUNT(*) AS count
FROM pubdb.PUSH_ORDER_LEVEL_TITLE_CONFIG
WHERE PRODUCT = 'at' AND DEL = '0'
GROUP BY PRODUCT;

-- 检查3：AI推单用户配置（at产品有多少个启用的用户）
SELECT 
    'AI推单用户配置' AS config_name,
    PRODUCT,
    COUNT(*) AS count
FROM pubdb.PUSH_ORDER_AI_USER
WHERE PRODUCT = 'at' AND STATUS = 0
GROUP BY PRODUCT;

-- 检查4：AI用户文案配置（at产品有多少条文案）
SELECT 
    'AI用户文案配置' AS config_name,
    u.PRODUCT,
    COUNT(*) AS count
FROM pubdb.PUSH_ORDER_AI_USER_COPYWRITE cw
INNER JOIN pubdb.PUSH_ORDER_AI_USER u ON cw.POAUID = u.ID
WHERE u.PRODUCT = 'at'
GROUP BY u.PRODUCT;

-- 检查5：系统参数（当前值是什么）
SELECT 
    '系统参数' AS config_name,
    CATEGORY,
    CODE,
    VALUE,
    UPDATE_TIME
FROM pubdb.S_SYSTEM_PARAMETER
WHERE CATEGORY = 'PUSHORDER' AND CODE = 'PUSHORDER_PRODUCT';

-- ==========================================
-- 步骤1：推单参数配置初始化
-- ==========================================
-- 说明：复制qm（at）的推单参数配置到qy
-- 用途：定时任务需要这个配置来给推单定价

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

-- 验证步骤1：检查qy的推单参数配置是否创建成功
SELECT 
    '步骤1验证：推单参数配置' AS step,
    PRODUCT,
    COUNT(*) AS count,
    CASE 
        WHEN COUNT(*) > 0 THEN '✅ 成功'
        ELSE '❌ 失败'
    END AS status
FROM pubdb.PUSH_ORDER_PARAM_CONFIG
WHERE PRODUCT = 'qy'
GROUP BY PRODUCT;

-- ==========================================
-- 步骤2：等级称号配置初始化
-- ==========================================
-- 说明：复制qm（at）的等级称号配置到qy
-- 用途：前端展示用户等级称号（足球大师/篮球大师）

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

-- 验证步骤2：检查qy的等级称号配置是否创建成功
SELECT 
    '步骤2验证：等级称号配置' AS step,
    PRODUCT,
    COUNT(*) AS count,
    CASE 
        WHEN COUNT(*) > 0 THEN '✅ 成功'
        ELSE '❌ 失败'
    END AS status
FROM pubdb.PUSH_ORDER_LEVEL_TITLE_CONFIG
WHERE PRODUCT = 'qy'
GROUP BY PRODUCT;

-- ==========================================
-- 步骤3：AI推单用户配置初始化（关键！）
-- ==========================================
-- 说明：复制qm（at）的AI推单用户配置到qy
-- 用途：定时任务需要知道为哪些用户生成推单
-- ⚠️ 注意：这是关键步骤，没有这个配置，定时任务会跳过qy产品

INSERT INTO pubdb.PUSH_ORDER_AI_USER (
    ID, USER_NAME, PRODUCT, PUSH_QUANTITY, STATUS, CREATE_TIME, CREATE_BY,
    MATCH_TYPE, HANDICAP_ITEM, LEAGUE_ID, USER_TYPE, SKIP_APPROVE, PUSH_SERIES_QUANTITY
)
SELECT 
    SEQ_PUSH_ORDER_AI_USER.NEXTVAL,  -- 使用序列生成新ID
    USER_NAME,
    'qy' AS PRODUCT,  -- 改为qy
    PUSH_QUANTITY,
    STATUS,
    SYSDATE AS CREATE_TIME,
    'system' AS CREATE_BY,
    MATCH_TYPE,
    HANDICAP_ITEM,
    LEAGUE_ID,
    USER_TYPE,
    SKIP_APPROVE,
    PUSH_SERIES_QUANTITY
FROM pubdb.PUSH_ORDER_AI_USER
WHERE PRODUCT = 'at'  -- 从qm（at）复制
  AND STATUS = 0;  -- 只复制启用的用户

-- 验证步骤3：检查qy的AI推单用户配置是否创建成功
SELECT 
    '步骤3验证：AI推单用户配置' AS step,
    PRODUCT,
    COUNT(*) AS count,
    CASE 
        WHEN COUNT(*) > 0 THEN '✅ 成功'
        ELSE '❌ 失败'
    END AS status
FROM pubdb.PUSH_ORDER_AI_USER
WHERE PRODUCT = 'qy' AND STATUS = 0
GROUP BY PRODUCT;

-- ==========================================
-- 步骤4：AI用户文案配置初始化（关键！）
-- ==========================================
-- 说明：复制qm（at）的AI用户文案配置到qy
-- 用途：AI生成推单时需要文案模板，没有文案无法生成推单内容
-- ⚠️ 注意：必须先执行步骤3（AI用户配置），因为需要关联新插入的qy用户ID

INSERT INTO pubdb.PUSH_ORDER_AI_USER_COPYWRITE (
    CWID, POAUID, MATCH_TYPE, HANDICAP, AI_TYPE, COPYWRITE, HANDICAP_TYPE
)
SELECT 
    SEQ_PUSH_ORDER_AI_USER_COPYWRITE.NEXTVAL,  -- 使用序列生成新ID
    qy_user.ID AS POAUID,  -- 使用qy用户的新ID（关键！）
    at_copywrite.MATCH_TYPE,
    at_copywrite.HANDICAP,
    at_copywrite.AI_TYPE,
    at_copywrite.COPYWRITE,
    at_copywrite.HANDICAP_TYPE
FROM pubdb.PUSH_ORDER_AI_USER_COPYWRITE at_copywrite
INNER JOIN pubdb.PUSH_ORDER_AI_USER at_user 
    ON at_copywrite.POAUID = at_user.ID
INNER JOIN pubdb.PUSH_ORDER_AI_USER qy_user 
    ON at_user.USER_NAME = qy_user.USER_NAME  -- 通过用户名关联
    AND qy_user.PRODUCT = 'qy'  -- 确保是qy用户
WHERE at_user.PRODUCT = 'at';  -- 从qm（at）复制

-- 验证步骤4：检查qy的AI用户文案配置是否创建成功
SELECT 
    '步骤4验证：AI用户文案配置' AS step,
    u.PRODUCT,
    COUNT(*) AS count,
    CASE 
        WHEN COUNT(*) > 0 THEN '✅ 成功'
        ELSE '❌ 失败'
    END AS status
FROM pubdb.PUSH_ORDER_AI_USER_COPYWRITE cw
INNER JOIN pubdb.PUSH_ORDER_AI_USER u ON cw.POAUID = u.ID
WHERE u.PRODUCT = 'qy'
GROUP BY u.PRODUCT;

-- ==========================================
-- 步骤5：系统参数配置
-- ==========================================
-- 说明：更新系统参数，添加qy到产品列表
-- 用途：告诉定时任务要为qy产品生成推单
-- ⚠️ 注意：如果VALUE已经包含qy，这个UPDATE不会执行（因为有NOT LIKE '%qy%'条件）

-- 先查看当前值
SELECT 
    '步骤5执行前：系统参数当前值' AS step,
    CATEGORY,
    CODE,
    VALUE,
    UPDATE_TIME
FROM pubdb.S_SYSTEM_PARAMETER
WHERE CATEGORY = 'PUSHORDER' AND CODE = 'PUSHORDER_PRODUCT';

-- 更新系统参数（添加qy）
UPDATE pubdb.S_SYSTEM_PARAMETER 
SET VALUE = VALUE || ',qy',  -- 在现有值后面追加,qy
    UPDATE_TIME = SYSDATE
WHERE CATEGORY = 'PUSHORDER'
  AND CODE = 'PUSHORDER_PRODUCT'
  AND VALUE NOT LIKE '%qy%';  -- 避免重复添加

-- 验证步骤5：检查系统参数是否更新成功
SELECT 
    '步骤5验证：系统参数配置' AS step,
    CATEGORY,
    CODE,
    VALUE,
    CASE 
        WHEN VALUE LIKE '%qy%' THEN '✅ qy已添加'
        ELSE '❌ qy未添加'
    END AS status,
    UPDATE_TIME
FROM pubdb.S_SYSTEM_PARAMETER
WHERE CATEGORY = 'PUSHORDER' AND CODE = 'PUSHORDER_PRODUCT';

-- ==========================================
-- 最终验证：所有配置完整性检查
-- ==========================================

-- 综合验证：对比qm（at）和qy的配置数量
SELECT 
    '最终验证：配置完整性对比' AS verification,
    '推单参数配置' AS config_type,
    PRODUCT,
    COUNT(*) AS count
FROM pubdb.PUSH_ORDER_PARAM_CONFIG
WHERE PRODUCT IN ('at', 'qy') AND DEL = '0'
GROUP BY PRODUCT
UNION ALL
SELECT 
    '最终验证：配置完整性对比' AS verification,
    '等级称号配置' AS config_type,
    PRODUCT,
    COUNT(*) AS count
FROM pubdb.PUSH_ORDER_LEVEL_TITLE_CONFIG
WHERE PRODUCT IN ('at', 'qy') AND DEL = '0'
GROUP BY PRODUCT
UNION ALL
SELECT 
    '最终验证：配置完整性对比' AS verification,
    'AI推单用户配置' AS config_type,
    PRODUCT,
    COUNT(*) AS count
FROM pubdb.PUSH_ORDER_AI_USER
WHERE PRODUCT IN ('at', 'qy') AND STATUS = 0
GROUP BY PRODUCT
UNION ALL
SELECT 
    '最终验证：配置完整性对比' AS verification,
    'AI用户文案配置' AS config_type,
    u.PRODUCT,
    COUNT(*) AS count
FROM pubdb.PUSH_ORDER_AI_USER_COPYWRITE cw
INNER JOIN pubdb.PUSH_ORDER_AI_USER u ON cw.POAUID = u.ID
WHERE u.PRODUCT IN ('at', 'qy')
GROUP BY u.PRODUCT
ORDER BY config_type, PRODUCT;

-- ==========================================
-- 执行说明：
-- ==========================================
-- 1. 执行前检查：先运行"执行前检查"部分的SQL，确认源数据存在
-- 2. 按顺序执行：步骤1 → 步骤2 → 步骤3 → 步骤4 → 步骤5
-- 3. 每步验证：每个步骤执行后，运行对应的验证SQL，确认成功
-- 4. 最终验证：所有步骤完成后，运行"最终验证"SQL，确认配置完整性
-- 5. 权限要求：如果当前用户是只读用户，需要联系管理员执行INSERT/UPDATE操作
-- 6. 执行时间：预计10-15分钟
-- ==========================================

