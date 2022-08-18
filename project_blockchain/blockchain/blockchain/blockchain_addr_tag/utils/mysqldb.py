#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : linjie
import pymysql
import logging
mysql_conf = {
    'host': '172.16.2.123',
    'user': 'test',
    'password': '123456',
    'port': 3306,
    'database': 'bitcoin_data',
    'charset': 'utf8'
}


'''mysql工具类'''
class MySQL_util:
    def __init__(self, conf):
        logging.basicConfig(level=logging.DEBUG,
                            format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s'
                            ,datefmt='%Y-%m-%d %H:%M:%S') # datefmt='%Y-%m-%d %H:%M:%S'
        self.conn = pymysql.connect(**conf)
        self.cursor = self.conn.cursor()

    #获取游标
    def get_cousor(self):
        return self.cursor

    #提交事务
    def commit(self):
        self.conn.commit()

    #回滚事务
    def rollback(self):
        self.conn.rollback()

    #关闭游标
    def close_cousor(self):
        self.cursor.close()
    #关闭连接
    def close_conn(self):
        self.conn.close()

    '''
        操作
    '''

    def insert(self, sql,val):
        """
                单条数据插入
                :param sql:sql
                :return:
        """
        cur = self.get_cousor()
        try:
            # logging.info('插入数据中')
            cur.execute(sql,val)
            self.commit()
        except Exception as e:
            # logging.error('插入失败：{}'.format(e))
            self.rollback()
            return 0
        else:
            # logging.info('插入数据成功')
            # pass
            return 1

    def insertOperation(self,sql):
        '''
        单条数据插入
        :param sql:sql
        :return:
        '''
        cur = self.get_cousor()
        try:
            # logging.info('插入数据中')
            cur.execute(sql)
            self.commit()
        except Exception as e:
            # logging.error('插入失败：{}'.format(e))
            self.rollback()
            return 0
        else:
            # logging.info('插入数据成功')
            # pass
            return 1
    def insertOperation_many(self,sql,data):
        '''
        多条数据插入
        :param sql:sql
        :return:
        '''
        cur = self.get_cousor()
        try:
            cur.executemany(sql,data)
            self.commit()
        except Exception as e:
            # logging.error('插入失败：{}'.format(e))
            self.rollback()
        else:
            # logging.info('插入数据成功')
            pass
    #查询
    def queryOperation(self, sql):
        # 获取数据库游标
        cur = self.get_cousor()
        dataList = []
        # print("sdasds")
        # 执行查询
        try:
            cur.execute(sql)
            # 查询结果条数
            # row = cur.rowcount
            # 查询结果集
            dataList = cur.fetchall()
        except Exception as e:
            print(e)

        # 返回查询结果集
        return dataList

    # 更新操作
    def updateOperation(self, sql):
        cur = self.get_cousor()
        result = ""
        try:
            result = cur.execute(sql)
            self.commit()
        except Exception as e:
            print(e)
            self.rollback()
        return result

        # 删除操作
    def deleteOperation(self, sql):
        # 获取数据库游标
        cur = self.get_cousor()
        try:
            # 执行删除
            cur.execute(sql)
            # 提交
            self.commit()

        except Exception as e:
            print(e)
            # 回滚
            self.rollback()
