-- 清理测试数据

-- 清理用户卡券表
DELETE FROM user_coupons WHERE user_id IN (SELECT id FROM users WHERE username LIKE 'test_%');

-- 清理卡券表
DELETE FROM coupons WHERE name LIKE '测试%' OR name LIKE 'test%';

-- 清理活动参与记录
DELETE FROM activity_participants WHERE activity_id IN (SELECT id FROM activities WHERE title LIKE '测试%');

-- 清理活动表
DELETE FROM activities WHERE title LIKE '测试%';

-- 清理测试用户
DELETE FROM users WHERE username LIKE 'test_%';

-- 重置自增ID（可选）
-- ALTER TABLE coupons AUTO_INCREMENT = 1;
-- ALTER TABLE user_coupons AUTO_INCREMENT = 1;
-- ALTER TABLE activities AUTO_INCREMENT = 1;
-- ALTER TABLE activity_participants AUTO_INCREMENT = 1;
-- ALTER TABLE users AUTO_INCREMENT = 1;
