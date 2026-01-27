-- ========== 查询生产库 PNGDEV 用户的所有表 ==========
SELECT table_name FROM all_tables WHERE owner='PNGDEV' ORDER BY table_name;

-- ========== 管理员相关操作（生产库 PNGDEV.BACKEND_ADMIN）==========

-- 1. 查询现有管理员账号
SELECT USERNAME, PASSWORD, STATUS, ROLEID, CREATEDATE, LASTLOGINDATE 
FROM pngdev.BACKEND_ADMIN 
WHERE STATUS='active';

-- 2. 查询角色列表
SELECT IDN, ROLENAME, PRODUCT, MAINACCESS 
FROM pngdev.BACKEND_ADMIN_ROLE 
WHERE STATUS='active';

-- 3. 查询最大管理员IDN
SELECT MAX(IDN) FROM pngdev.BACKEND_ADMIN;

-- 4. 创建新管理员（密码：admin123 -> MD5: 0192023a7bbd73250516f069df18b500）
-- 注意：先执行上面的查询，用最大IDN+1，假设最大IDN是100
INSERT INTO pngdev.BACKEND_ADMIN (IDN, USERNAME, PASSWORD, STATUS, ROLEID, PRODUCT, CREATEDATE) 
VALUES (101, 'testadmin', '0192023a7bbd73250516f069df18b500', 'active', 1, 'ALL', SYSDATE);

-- 5. 重置现有管理员密码（假设用户名是admin，新密码：admin123）
UPDATE pngdev.BACKEND_ADMIN 
SET PASSWORD = '0192023a7bbd73250516f069df18b500' 
WHERE USERNAME = 'admin' AND STATUS = 'active';

-- 6. 提交事务
COMMIT;

-- 常用密码的MD5值：
-- admin123: 0192023a7bbd73250516f069df18b500
-- 123456:   e10adc3949ba59abbe56e057f20f883e
-- password: 5f4dcc3b5aa765d61d8327deb882cf99

-- ========== 查询表数量 ==========
-- 查询当前用户下有多少张表
SELECT COUNT(*) AS table_count FROM user_tables;

-- 查询所有表名（按名称排序）
SELECT table_name FROM user_tables ORDER BY table_name;

-- 或者查询 pngdev 用户下的所有表（需要权限）
SELECT COUNT(*) AS table_count FROM all_tables WHERE owner='PNGDEV';
SELECT table_name FROM all_tables WHERE owner='PNGDEV' ORDER BY table_name;

-- ========== 管理员账号查询 ==========
SELECT USERNAME, PASSWORD, STATUS, ROLEID, CREATEDATE, LASTLOGINDATE 
FROM pngdev.BACKEND_ADMIN 
WHERE STATUS='active';


-- 先查询角色ID
SELECT IDN, ROLENAME FROM pngdev.BACKEND_ADMIN_ROLE WHERE STATUS='active';

-- 然后插入（假设角色ID是1）- PRODUCT 是保留字需加双引号
INSERT INTO pngdev.BACKEND_ADMIN (USERNAME, PASSWORD, STATUS, ROLEID, "PRODUCT", CREATEDATE) 
VALUES ('testadmin', '0192023a7bbd73250516f069df18b500', 'active', 1, 'ALL', SYSDATE);


INSERT INTO pngdev.BACKEND_ADMIN (IDN, USERNAME, PASSWORD, STATUS, ROLEID, "PRODUCT", CREATEDATE) 
VALUES (
  BACKEND_ADMIN_SEQ.NEXTVAL,  -- 自增ID（如果有序列的话）
  'admin',                     -- 用户名
  '123456',             -- 密码（可能需要加密）
  'active',                    -- 状态
  1,                           -- 角色ID（需要先查 BACKEND_ADMIN_ROLE 表）
  'ALL',                       -- 产品权限
  SYSDATE                      -- 创建时间
);


-- 先查询角色ID
SELECT IDN, ROLENAME FROM pngdev.BACKEND_ADMIN_ROLE WHERE STATUS='active';

-- 然后插入（假设角色ID是1）- PRODUCT 是保留字需加双引号
INSERT INTO pngdev.BACKEND_ADMIN (USERNAME, PASSWORD, STATUS, ROLEID, "PRODUCT", CREATEDATE) 
VALUES ('testadmin2', '0192023a7bbd73250516f069df18b500', 'active', 1, 'ALL', SYSDATE);



-- 错误的写法
SELECT * FROM USER_TABLES WHERE pngdev.TABLE_NAME = 'BACKEND_ADMIN';

-- 正确的写法1: 查询当前用户的表
SELECT * FROM USER_TABLES WHERE TABLE_NAME = 'BACKEND_ADMIN';

-- 正确的写法2: 查询指定用户(PNGDEV)的表
SELECT * FROM ALL_TABLES WHERE OWNER = 'PNGDEV' AND TABLE_NAME = 'BACKEND_ADMIN';


CREATE SYNONYM BACKEND_ADMIN FOR PNGDEV.BACKEND_ADMIN;
