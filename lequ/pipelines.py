# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 导入python与mysql交互的第三方库
import pymysql

class MyPipeline(object):
    """
    因为两个爬虫需要存入到不同的表中,那么就需要两个pipeline类,
    但是可以发现,两个pipeline有一些方法是相同的,比如连接数据库,创建游标,关闭数据库等,
    那么可以自定义pipeline父类来实现这些操作,让这两个pipeline类继承于自定义的父类,简化代码
    pipeline需要实现3个方法,open_spider用于爬虫启动的时候执行,process_item接收到数据的时候执行,close_spider爬虫停止的时候执行
    """
    def __init__(self):
        # 连接mysql数据库
        self.conn = pymysql.Connect(
            host='localhost', # 数据库ip
            port=3306,      # 数据库端口号
            user='root',    # 数据库用户名
            passwd='root',  # 数据库密码
            db='lequ',      # 要连接的数据库名
            charset='utf8', # 编码
        )
        # 创建数据库游标操作数据库语句
        self.cursor = self.conn.cursor()

    def open_spider(self, spider):

        pass


    def close_spider(self, spider):
        # 爬虫停止的时候关闭数据库
        self.conn.close()
        print('{}爬虫已停止'.format(self.__class__))

class LequPipeline(MyPipeline):
    """用户信息内容爬虫Pipeline类"""

    def process_item(self, item, spider):

        name = item['name']
        create_time = item['create_time']
        active_time = item['active_time']
        last_login = item['last_login']
        last_activity = item['last_activity']
        area = item['area']
        signature = item['signature']
        friend_nums = item['friend_nums']
        reply_times = item['reply_times']
        theme_nums = item['theme_nums']
        identity = item['identity']
        uid = item['uid']
        forum_money = item['forum_money']

        sql = """insert into lequ_user (name, create_time, active_time, last_login, last_activity, area, signature, reply_times, theme_nums, identity, uid, forum_money, friend_nums) 
                           values('{}', '{}', {}, '{}', '{}', '{}', '{}', {}, {}, '{}', {}, {}, {})"""

        self.cursor.execute(sql.format(name, create_time, active_time, last_login, last_activity,
                                            area, signature, reply_times, theme_nums, identity, uid, forum_money, friend_nums))
        self.conn.commit()


class ContentPipeline(MyPipeline):
    """帖子内容爬虫Pipeline类"""
    def process_item(self, item, spider):

        name = item['name']
        content = item['content']
        public_time = item['public_time']
        read_count = item['read_count']
        reply_count = item['reply_count']

        sql = """
                insert into content (name, content, public_time, read_count, reply_count) 
                values('{}', '{}', '{}', {}, {})"""

        self.cursor.execute(sql.format(name, content, public_time, read_count, reply_count))

        self.conn.commit()