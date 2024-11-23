CREATE TABLE IF NOT EXISTS `experiences` (
`experience_id`      int(11)       NOT NULL AUTO_INCREMENT	COMMENT 'The experience id',
`position_id`        int(11)       NOT NULL 				COMMENT 'FK:The position id',
`name`               varchar(100)  NOT NULL					COMMENT 'Name of experience',
`description`        varchar(500)  NOT NULL                 COMMENT 'A brief description of the experience',
`hyperlink`          varchar(500)  NOT NULL                 COMMENT 'Hyperlink association with this experience',
`start_date`         date          NOT NULL                 COMMENT 'My start date for this experience',
`end_date`           date          DEFAULT NULL             COMMENT 'The end date for this experiences',
PRIMARY KEY (`experience_id`),
FOREIGN KEY (position_id) REFERENCES positions(position_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="My professional and educational experiences";