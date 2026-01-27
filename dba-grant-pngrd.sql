-- ========================================
-- 给 DBA 的 SQL 脚本
-- 目的：让 pngrd 用户能够访问 PNGDEV schema 下的所有表
-- ========================================

-- 连接信息：190.92.232.31:1531:pngp
-- 需要用 DBA 权限用户（system/sys）执行

-- 方案1：创建公共同义词（推荐，所有用户都能用）
CREATE PUBLIC SYNONYM BACKEND_ADMIN FOR PNGDEV.BACKEND_ADMIN;
CREATE PUBLIC SYNONYM BACKEND_ADMIN_ROLE FOR PNGDEV.BACKEND_ADMIN_ROLE;

-- 方案2：授权 + 让 pngrd 自己创建同义词
GRANT CREATE SYNONYM TO pngrd;
GRANT SELECT ON PNGDEV.BACKEND_ADMIN TO pngrd;
GRANT SELECT ON PNGDEV.BACKEND_ADMIN_ROLE TO pngrd;

-- 如果需要访问所有 PNGDEV 的表，可以批量授权
BEGIN
  FOR t IN (SELECT table_name FROM all_tables WHERE owner = 'PNGDEV') LOOP
    EXECUTE IMMEDIATE 'GRANT SELECT ON PNGDEV.' || t.table_name || ' TO pngrd';
  END LOOP;
END;
/

COMMIT;

-- 验证
SELECT * FROM DBA_TAB_PRIVS WHERE GRANTEE = 'PNGRD';
