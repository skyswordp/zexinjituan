-- ==========================================
-- qm -> qy 定时任务数据验证 SQL
-- 结合代码逻辑验证 qy 产品数据是否已生成
-- ==========================================

-- ==========================================
-- 第一部分：系统参数验证（定时任务配置）
-- ==========================================

-- 1.1 验证系统参数是否包含 qy
-- 代码位置：AIPushOrderServiceImpl.java 第74-87行
-- 方法：getSystemPushOrderProduct()
-- 说明：定时任务会读取这个参数，获取需要生成推单的产品列表
SELECT 
    CATEGORY,
    CODE,
    VALUE,
    CASE 
        WHEN VALUE LIKE '%qy%' THEN '✅ qy已配置，定时任务会为qy生成推单'
        ELSE '❌ qy未配置，定时任务不会为qy生成推单'
    END AS status,
    DESCRIPTION,
    UPDATE_TIME
FROM pubdb.S_SYSTEM_PARAMETER
WHERE CATEGORY = 'PUSHORDER'
  AND CODE = 'PUSHORDER_PRODUCT';

-- 1.2 解析产品列表（验证格式）
-- 代码逻辑：value.split("\\,") - 按逗号分割
SELECT 
    VALUE,
    REGEXP_COUNT(VALUE, ',') + 1 AS product_count,
    CASE 
        WHEN VALUE LIKE '%qy%' THEN '✅ 包含qy'
        ELSE '❌ 不包含qy'
    END AS qy_status
FROM pubdb.S_SYSTEM_PARAMETER
WHERE CATEGORY = 'PUSHORDER'
  AND CODE = 'PUSHORDER_PRODUCT';

-- ==========================================
-- 第二部分：AI推单数据验证（核心表）
-- ==========================================

-- 2.1 验证 qy 产品的推单数据是否存在
-- 代码位置：AIPushOrderServiceImpl.java 第1364行
-- 方法：masterPushOrderContentManagementService.insert(pushOrder)
-- 说明：定时任务生成的推单会插入到 PUSH_ORDER_CONTENT_MANAGEMENT 表
SELECT 
    PRODUCT,
    COUNT(*) AS total_count,
    COUNT(CASE WHEN STATE = '0' THEN 1 END) AS draft_count,      -- 0=编辑
    COUNT(CASE WHEN STATE = '1' THEN 1 END) AS pending_count,    -- 1=待审核
    COUNT(CASE WHEN STATE = '2' THEN 1 END) AS approved_count,    -- 2=审核通过
    COUNT(CASE WHEN STATE = '3' THEN 1 END) AS rejected_count,   -- 3=审核驳回
    COUNT(CASE WHEN OPERATION_PORT = '2' THEN 1 END) AS ai_generated_count,  -- 2=AI生成
    MIN(CREATE_TIME) AS first_create_time,
    MAX(CREATE_TIME) AS last_create_time
FROM pubdb.PUSH_ORDER_CONTENT_MANAGEMENT
WHERE PRODUCT IN ('at', 'qy')
GROUP BY PRODUCT
ORDER BY PRODUCT;

-- 2.2 查看 qy 产品最近生成的推单（验证定时任务是否执行）
-- 代码逻辑：定时任务每天21:00执行，生成未来第2天的推单
SELECT 
    ID,
    USER_NAME,
    TITLE,
    MATCH_NAME,
    PRODUCT,
    STATE,
    OPERATION_PORT,
    CASE OPERATION_PORT
        WHEN '0' THEN '后台'
        WHEN '1' THEN '前端'
        WHEN '2' THEN 'AI生成 ⭐'
        WHEN '3' THEN '安卓'
        WHEN '4' THEN '苹果'
        ELSE '未知'
    END AS operation_desc,
    CREATE_TIME,
    MATCH_START_TIME
FROM pubdb.PUSH_ORDER_CONTENT_MANAGEMENT
WHERE PRODUCT = 'qy'
ORDER BY CREATE_TIME DESC
FETCH FIRST 20 ROWS ONLY;

-- 2.3 对比 qm（at）和 qy 的数据量（验证数据是否正常生成）
SELECT 
    PRODUCT,
    COUNT(*) AS total_redbills,
    COUNT(CASE WHEN OPERATION_PORT = '2' THEN 1 END) AS ai_generated,
    COUNT(CASE WHEN STATE = '2' THEN 1 END) AS approved,
    COUNT(CASE WHEN TRUNC(CREATE_TIME) = TRUNC(SYSDATE) THEN 1 END) AS today_generated,
    COUNT(CASE WHEN TRUNC(CREATE_TIME) = TRUNC(SYSDATE - 1) THEN 1 END) AS yesterday_generated
FROM pubdb.PUSH_ORDER_CONTENT_MANAGEMENT
WHERE PRODUCT IN ('at', 'qy')
GROUP BY PRODUCT
ORDER BY PRODUCT;

-- ==========================================
-- 第三部分：AI用户验证（定时任务使用的用户）
-- ==========================================

-- 3.1 验证 qy 产品是否有AI推单用户
-- 代码位置：AIPushOrderServiceImpl.java 第834-850行
-- 说明：定时任务会查询每个产品的AI用户，为这些用户生成推单
SELECT 
    PRODUCT,
    COUNT(*) AS ai_user_count,
    LISTAGG(USER_NAME, ', ') WITHIN GROUP (ORDER BY USER_NAME) AS user_list
FROM pubdb.F_USER
WHERE PRODUCT IN ('at', 'qy')
  AND USER_NAME LIKE 'ai%'  -- AI用户通常以ai开头
GROUP BY PRODUCT
ORDER BY PRODUCT;

-- 3.2 查看 qy 产品的AI用户详情
SELECT 
    USER_NAME,
    PRODUCT,
    USER_LEVEL,
    CREATE_TIME
FROM pubdb.F_USER
WHERE PRODUCT = 'qy'
  AND USER_NAME LIKE 'ai%'
ORDER BY USER_NAME;

-- ==========================================
-- 第四部分：定时任务执行时间验证
-- ==========================================

-- 4.1 查看最近7天 qy 产品的推单生成情况
-- 定时任务：每天21:00执行
SELECT 
    TRUNC(CREATE_TIME) AS create_date,
    PRODUCT,
    COUNT(*) AS generated_count,
    COUNT(CASE WHEN OPERATION_PORT = '2' THEN 1 END) AS ai_generated_count
FROM pubdb.PUSH_ORDER_CONTENT_MANAGEMENT
WHERE PRODUCT = 'qy'
  AND CREATE_TIME >= SYSDATE - 7
GROUP BY TRUNC(CREATE_TIME), PRODUCT
ORDER BY create_date DESC;

-- 4.2 对比 qm 和 qy 最近7天的生成情况
SELECT 
    TRUNC(CREATE_TIME) AS create_date,
    PRODUCT,
    COUNT(*) AS generated_count
FROM pubdb.PUSH_ORDER_CONTENT_MANAGEMENT
WHERE PRODUCT IN ('at', 'qy')
  AND CREATE_TIME >= SYSDATE - 7
  AND OPERATION_PORT = '2'  -- 只统计AI生成的
GROUP BY TRUNC(CREATE_TIME), PRODUCT
ORDER BY create_date DESC, PRODUCT;

-- ==========================================
-- 第五部分：推单综合日志验证
-- ==========================================

-- 5.1 查看 qy 产品的推单日志（点击、购买、关注）
SELECT 
    gl.TYPE,
    CASE gl.TYPE
        WHEN '0' THEN '点击'
        WHEN '1' THEN '购买'
        WHEN '2' THEN '关注'
        ELSE '未知'
    END AS type_desc,
    COUNT(*) AS log_count
FROM pubdb.PUSH_ORDER_CONTENT_GENERAL_LOG gl
INNER JOIN pubdb.PUSH_ORDER_CONTENT_MANAGEMENT cm 
    ON gl.CONTENT_MANAGEMENT_ID = cm.ID
WHERE cm.PRODUCT = 'qy'
GROUP BY gl.TYPE
ORDER BY gl.TYPE;

-- 5.2 对比 qm 和 qy 的日志数据量
SELECT 
    cm.PRODUCT,
    COUNT(*) AS total_logs,
    COUNT(CASE WHEN gl.TYPE = '0' THEN 1 END) AS click_logs,
    COUNT(CASE WHEN gl.TYPE = '1' THEN 1 END) AS purchase_logs,
    COUNT(CASE WHEN gl.TYPE = '2' THEN 1 END) AS follow_logs
FROM pubdb.PUSH_ORDER_CONTENT_GENERAL_LOG gl
INNER JOIN pubdb.PUSH_ORDER_CONTENT_MANAGEMENT cm 
    ON gl.CONTENT_MANAGEMENT_ID = cm.ID
WHERE cm.PRODUCT IN ('at', 'qy')
GROUP BY cm.PRODUCT
ORDER BY cm.PRODUCT;

-- ==========================================
-- 第六部分：综合验证报告
-- ==========================================

-- 6.1 生成完整的验证报告
SELECT 
    '系统参数配置' AS check_item,
    CASE 
        WHEN EXISTS (
            SELECT 1 FROM pubdb.S_SYSTEM_PARAMETER 
            WHERE CATEGORY = 'PUSHORDER' 
              AND CODE = 'PUSHORDER_PRODUCT' 
              AND VALUE LIKE '%qy%'
        ) THEN '✅ 已配置'
        ELSE '❌ 未配置'
    END AS qy_status,
    NULL AS data_count
FROM dual
UNION ALL
SELECT 
    '推单数据总量',
    CASE 
        WHEN COUNT(*) > 0 THEN '✅ 有数据'
        ELSE '❌ 无数据'
    END,
    TO_CHAR(COUNT(*))
FROM pubdb.PUSH_ORDER_CONTENT_MANAGEMENT
WHERE PRODUCT = 'qy'
UNION ALL
SELECT 
    'AI生成推单',
    CASE 
        WHEN COUNT(*) > 0 THEN '✅ 有AI推单'
        ELSE '❌ 无AI推单'
    END,
    TO_CHAR(COUNT(*))
FROM pubdb.PUSH_ORDER_CONTENT_MANAGEMENT
WHERE PRODUCT = 'qy'
  AND OPERATION_PORT = '2'
UNION ALL
SELECT 
    'AI用户数量',
    CASE 
        WHEN COUNT(*) > 0 THEN '✅ 有AI用户'
        ELSE '❌ 无AI用户'
    END,
    TO_CHAR(COUNT(*))
FROM pubdb.F_USER
WHERE PRODUCT = 'qy'
  AND USER_NAME LIKE 'ai%'
UNION ALL
SELECT 
    '最近7天生成量',
    CASE 
        WHEN COUNT(*) > 0 THEN '✅ 有生成'
        ELSE '❌ 无生成'
    END,
    TO_CHAR(COUNT(*))
FROM pubdb.PUSH_ORDER_CONTENT_MANAGEMENT
WHERE PRODUCT = 'qy'
  AND CREATE_TIME >= SYSDATE - 7
  AND OPERATION_PORT = '2';

-- ==========================================
-- 使用说明：
-- 1. 按顺序执行上述SQL，验证qy产品的数据情况
-- 2. 重点关注：
--    - 系统参数是否包含qy（定时任务配置）
--    - PUSH_ORDER_CONTENT_MANAGEMENT表中是否有qy数据
--    - 数据是否由AI定时任务生成（OPERATION_PORT='2'）
--    - 最近是否有新数据生成（验证定时任务是否正常执行）
-- 3. 如果数据为0，说明：
--    - 系统参数未配置qy（需要执行配置初始化）
--    - 或定时任务还未执行（等待21:00执行）
--    - 或定时任务执行失败（需要查看日志）
-- ==========================================

