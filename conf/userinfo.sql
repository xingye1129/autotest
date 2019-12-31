
SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS `userinfo`;
CREATE TABLE `userinfo` (
  `id` int(8) unsigned NOT NULL AUTO_INCREMENT COMMENT 'userid',
  `nickname` varchar(36) DEFAULT NULL COMMENT '昵称',
  `describe` varchar(128) DEFAULT NULL COMMENT '个人介绍',
  `username` varchar(16) NOT NULL,
  `pwd` varchar(16) NOT NULL COMMENT '密码',
  PRIMARY KEY (`id`,`username`),
  UNIQUE KEY `username` (`username`) USING BTREE,
  UNIQUE KEY `password` (`username`,`pwd`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;


INSERT INTO `userinfo` VALUES ('1', 'Will_Testing', '擅长Python、Java自动化开发；是特斯汀学院最可爱的老师', 'Will', '123456');
INSERT INTO `userinfo` VALUES ('5', '星野', '测试账号', 'xingye', '123456');
INSERT INTO `userinfo` VALUES ('7', 'test', 'test', 'test', 'test');
INSERT INTO `userinfo` VALUES ('8', 'test2', 'test2', 'test2', 'test2');
INSERT INTO `userinfo` VALUES ('9', '测试账号', '这是测试账号', 'zhang', '123456');
