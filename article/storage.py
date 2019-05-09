# coding=utf-8

import pymysql
import configparser
import os


class Storage:
    def __init__(self):
        self.instance = None
        self.conn = None
        conf = configparser.ConfigParser()
        conf.read('.env')
        host = conf.get('db', 'db_host')
        user = conf.get('db', 'db_user')
        name = conf.get('db', 'db_name')
        port = conf.get('db', 'db_port')
        pwd = conf.get('db', 'db_password')
        if not self.instance:
            conn = pymysql.connect(host=host, user=user, passwd=pwd, port=int(port), db=name, charset='utf8')
            self.conn = conn
            curl = conn.cursor(cursor=pymysql.cursors.DictCursor)
            self.instance = curl
        flag = conf.get('db', 'db_flag')
        if not flag:
            self.create_table()
            conf.set('db', 'db_flag', '1')
            # 将值写入到文件中
            conf.write(open(os.path.join('..', '.env'), 'w'))

    def create_table(self):
        # 创建课程列表
        self.instance.execute("""
        CREATE TABLE `course` (
            `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
            `column_id` int(11) unsigned NOT NULL DEFAULT 0 COMMENT '课程ID',
            `column_type` varchar(255) NOT NULL DEFAULT '' COMMENT '课程类型',
            `column_title` varchar(255) NOT NULL DEFAULT '' COMMENT '课程标题',
            `column_subtitle` varchar(255) NOT NULL DEFAULT '' COMMENT '课程子标题',
            `author_name` varchar(255) NOT NULL DEFAULT '' COMMENT '作者姓名',
            `author_intro` varchar(255) NOT NULL DEFAULT '' COMMENT '作者简介',
            `had_sub` tinyint(1) NOT NULL DEFAULT 1 COMMENT '是否订阅 1：订阅 0：未订阅',
            `update_frequency` varchar(255) NOT NULL DEFAULT '' COMMENT '更新频率',
            `author_header` varchar(255) NOT NULL DEFAULT '' COMMENT '作者头像',
            `column_unit` varchar(255) NOT NULL DEFAULT '' COMMENT '课程节数',
            `column_cover` varchar(255) NOT NULL DEFAULT '' COMMENT '课程封面',
            `column_begin_time` int(11) NOT NULL DEFAULT 0 COMMENT '课程开始时间',
            `column_intro` TEXT COMMENT '课程简介',
            `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`)
        )ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
        """)
        # 创建课节表
        self.instance.execute("""
        CREATE TABLE `chapter` (
            `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
            `article_content` TEXT COMMENT '课程内容',
            `column_id` int(11) unsigned NOT NULL DEFAULT 0 COMMENT '课程ID',
            `article_id` int(11) NOT NULL DEFAULT 0 COMMENT '课节ID',
            `article_title` varchar(255) NOT NULL DEFAULT '' COMMENT '课节标题',
            `article_subtitle` varchar(255) NOT NULL DEFAULT '' COMMENT '课节子标题',
            `article_ctime` varchar(255) NOT NULL DEFAULT '' COMMENT '课节创建时间',
            `article_cover` varchar(255) NOT NULL DEFAULT '' COMMENT '课节封面',
            `video_cover` varchar(255) NOT NULL DEFAULT '' COMMENT '视频封面',
            `video_media` varchar(255) NOT NULL DEFAULT '' COMMENT '更新频率',
            `article_summary` varchar(255) NOT NULL DEFAULT '' COMMENT '课节概览',
            `audio_download_url` varchar(255) NOT NULL DEFAULT '' COMMENT '音频下载地址',
            `audio_url` varchar(255) NOT NULL DEFAULT '' COMMENT '音频播放地址',
            `audio_time` varchar(255) NOT NULL DEFAULT '' COMMENT '音频时长',
            `author_name` varchar(255) NOT NULL DEFAULT '' COMMENT '作者姓名',
            `article_poster_wxlite` varchar(255) NOT NULL DEFAULT '' COMMENT '',
            `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`)
        )ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
        """)

    def save_course_info(self, kwargs):
        try:
            sql = """
                    INSERT INTO course VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
            # 批量插入
            self.instance.executemany(sql, kwargs)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def get_last_info(self, table):
        try:
            sql = 'select * from ' + table + ' where 1=1 order by id desc '
            return self.instance.execute(sql)
        except Exception as e:
            print(e)
            self.conn.rollback()

    def save_chapter_info(self, kwargs):
        try:
            sql = """
            INSERT INTO chapter VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # 批量插入
            self.instance.executemany(sql, kwargs)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()