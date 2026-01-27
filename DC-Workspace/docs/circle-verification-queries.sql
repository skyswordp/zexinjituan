-- ==========================================
-- 朋友圈数据验证SQL（qy产品）
-- ==========================================
-- 说明：去掉schema前缀，直接使用表名（代码中使用的是F_CIRCLE，不是pubdb.F_CIRCLE）

-- 1. 查看 qy 产品的朋友圈数据（包括待审核的）
SELECT 
    c.id,
    c.user_id,
    u.user_name,
    u.nick_name,
    c.content,
    c.product,
    c.status,  -- 0=通过, 1=未通过, 2=待审核
    c.deleted,
    c.create_time,
    c.comment_count,
    c.praise_count
FROM F_CIRCLE c
LEFT JOIN F_USER u ON u.id = c.user_id
WHERE c.product = 'qy'
ORDER BY c.create_time DESC;

-- 2. 统计各状态的数量
SELECT 
    c.status,
    COUNT(*) as count,
    CASE 
        WHEN c.status = 0 THEN '审核通过'
        WHEN c.status = 1 THEN '审核未通过'
        WHEN c.status = 2 THEN '待审核'
        ELSE '其他'
    END as status_desc
FROM F_CIRCLE c
WHERE c.product = 'qy' AND c.deleted = 0
GROUP BY c.status;

-- 3. 查看可以显示在列表中的数据（status=0, deleted=0）
SELECT COUNT(*) as visible_count
FROM F_CIRCLE c
WHERE c.product = 'qy' 
  AND c.status = 0 
  AND c.deleted = 0;

-- 4. 查看 qy 产品的朋友圈详细信息（包含图片、视频等）
SELECT 
    c.id,
    c.user_id,
    u.user_name,
    u.nick_name,
    u.head_url,
    c.content,
    c.product,
    c.status,
    c.deleted,
    c.create_time,
    c.comment_count,
    c.praise_count,
    c.read_count,
    c.circle_sort,
    c.hot,
    c.bright
FROM F_CIRCLE c
LEFT JOIN F_USER u ON u.id = c.user_id
WHERE c.product = 'qy' 
  AND c.deleted = 0
  AND c.status = 0
ORDER BY c.circle_sort DESC, c.create_time DESC;

-- 5. 如果需要手动审核通过（将status=2改为0），可以使用：
-- UPDATE F_CIRCLE 
-- SET status = 0 
-- WHERE product = 'qy' 
--   AND status = 2 
--   AND deleted = 0;
-- （注意：生产环境谨慎操作）
