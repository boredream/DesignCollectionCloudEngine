# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3


class SqlitePipeline(object):
    def __init__(self):
        self.sql = ''
        self.conn = sqlite3.connect('data.db')

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        if self.sql == '':
            # 初始化table
            self.sql = 'CREATE TABLE DATA (ID INTEGER PRIMARY KEY, '
            for (key, value) in dict(item).items():
                # if isinstance(type(value), types.IntType):
                #     self.sql += (key + ' INTEGER, ')
                # elif isinstance(type(value), types.BooleanType):
                #     # boolean 用 int 型
                #     self.sql += (key + ' INTEGER, ')
                # else:
                #     self.sql += (key + ' TEXT,')

                self.sql += (key + ' TEXT,')

                print type(value)
            self.sql += ');'
            self.sql = self.sql.replace(',);', ');')

            print '------------- create Table = ' + self.sql

            self.conn.execute(self.sql)
            self.conn.commit()

        keys = ''
        values = ''
        for (key, value) in dict(item).items():
            keys += (', ' + key)
            # 存入数据库时，两个单引号代表一个单引号
            values += (', \'' + value.replace('\'', '\'\'') + '\'')

        insertSql = 'INSERT INTO DATA (' + keys[2:] + ') VALUES (' + values[2:] + ')'

        print 'insert sql = ' + insertSql

        self.conn.execute(insertSql)
        self.conn.commit()

        return item
