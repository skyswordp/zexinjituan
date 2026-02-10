-- ============================================
-- F_USER 表：验证 adults123 用户是否存在
-- Oracle 数据库
-- ============================================

-- 1. 先查看 F_USER 表结构（确认正确的列名）
SELECT COLUMN_NAME, DATA_TYPE
FROM ALL_TAB_COLUMNS
WHERE TABLE_NAME = 'F_USER' 
AND OWNER = 'PUBDB';

-- 2. 查看表里现有数据样例（确认字段格式）
SELECT * FROM PUBDB.F_USER WHERE ROWNUM <= 5;

-- 3. 查看 userId=426908 的用户（对比参考）
SELECT * FROM PUBDB.F_USER WHERE ID = 426908;

-- ============================================
-- 确认列名后，用以下模板查询/插入 adults123
-- （请根据第1步查出的实际列名修改）
-- ============================================

-- 查询 adults123（假设列名是 USER_NAME，请按实际修改）
SELECT * FROM PUBDB.F_USER WHERE USER_NAME = 'adults123';

-- 插入 adults123（Oracle 语法，请按实际表结构修改）
INSERT INTO PUBDB.F_USER (USER_NAME, NICK_NAME, HEAD_URL, CREATE_TIME)
VALUES ('adults123', 'adults123', NULL, SYSDATE);
COMMIT;


-- 重点看这两条
SELECT id, user_name, nick_name, status FROM f_user WHERE id IN (1817302, 487208);
SELECT * FROM f_user_follow WHERE user_id = 1817302 AND be_user_id = 487208;