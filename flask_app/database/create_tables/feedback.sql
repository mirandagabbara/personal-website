CREATE TABLE IF NOT EXISTS `feedback` (
`comment_id`         int(11)       NOT NULL AUTO_INCREMENT	COMMENT 'The comment id',
`name`               varchar(100)  NOT NULL					COMMENT 'Name of commenter',
`email`              varchar(100)  NOT NULL				COMMENT 'Email of commenter',
`comment`            varchar(200)  NOT NULL				COMMENT 'Comment from commenter',

PRIMARY KEY (`comment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="My skills";