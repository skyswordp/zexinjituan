-- 验证 saveFollow 接口相关数据

-- 1. 验证用户是否存在
SELECT id, user_name, nick_name, status
FROM f_user
WHERE id IN (1817302, 487208);

-- 2. 查询是否已经存在关注记录
SELECT *
FROM f_user_follow
WHERE user_id = 1817302 AND be_user_id = 487208;

-- 3. 查看用户1817302的所有关注记录
SELECT *
FROM f_user_follow
WHERE user_id = 1817302
ORDER BY create_time DESC
LIMIT 10;

-- 4. 查看用户487208被谁关注了
SELECT *
FROM f_user_follow
WHERE be_user_id = 487208
ORDER BY create_time DESC
LIMIT 10;

-- 5. 如果需要清除测试数据（慎用！）
-- DELETE FROM f_user_follow WHERE user_id = 1817302 AND be_user_id = 487208;

-- 6. 插入测试关注记录（如果需要手动插入）
-- INSERT INTO f_user_follow (user_id, be_user_id, create_time)
-- VALUES (1817302, 487208, NOW());
