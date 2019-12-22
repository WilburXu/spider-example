# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymysql

class NewsPipeline(object):
    def __init__(self, mysql_host, mysql_port, mysql_user, mysql_pass, mysql_db, mysql_charset):
        self.mysql_host = mysql_host
        self.mysql_port = mysql_port
        self.mysql_user = mysql_user
        self.mysql_pass = mysql_pass
        self.mysql_db = mysql_db
        self.mysql_charset = mysql_charset

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST'),
            mysql_port=crawler.settings.get('MYSQL_PORT'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_pass=crawler.settings.get('MYSQL_PASS'),
            mysql_db=crawler.settings.get('MYSQL_DB'),
            mysql_charset=crawler.settings.get('MYSQL_CHARSET'),
        )

    def process_item(self, item, spider):
        # insert
        insertSQL = "INSERT INTO wx_crawl (title, publish_time, excerpt, author, source_url, content, cover_url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        try:
            data = self._cursor_.execute(insertSQL, (
                item['title'], item['publish_time'], item['excerpt'], item['author'], item['source_url'],
                item['content'], item['cover_url']))
            self._connect_.commit()
            logging.info("【insert success: %s】" % item['title'])
            logging.info("############################   end  #################################" % data)
        except Exception as e:
            logging.info(e)
            self._connect_.rollback()

    def get_post_info(self, title, author):
        crawlInfoSQL = "select id from wx_crawl where author = %s and title = %s"
        self._cursor_.execute(crawlInfoSQL, (author, title))
        crawlInfo = self._cursor_.fetchone()
        logging.info(crawlInfo)
        return crawlInfo

    def open_spider(self, spider):
        print("当爬虫执行开始的时候回调:open_spider")
        self._connect_ = pymysql.connect(host=self.mysql_host, port=self.mysql_port, user=self.mysql_user,
                                         passwd=self.mysql_pass, db=self.mysql_db, charset=self.mysql_charset,
                                         cursorclass=pymysql.cursors.DictCursor)
        self._cursor_ = self._connect_.cursor()

        spider.mysqlObj = self

    def close_spider(self, spider):
        self._cursor_.close()
        self._connect_.close()
