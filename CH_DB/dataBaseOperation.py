# -*- coding: utf-8 -*-
# @Time : 2021/4/25 14:19
# @Author :  Meow_J

"""
数据库相关操作
"""

import pymysql
from requests.exceptions import RequestException


class DBOperation(object):

    def __init__(self):
        self.host = '192.168.2.23'
        self.port = 7865
        self.userName = 'ch_data_source'
        self.passWord = '123456'
        self.charset = 'utf-8'
        self.database = 'db_source'

    def selectComId(self,comName):
        """
        获取公司基本信息主体Id
        :return:
        """
        db = pymysql.connect(host=self.host, port=self.port, user=self.userName, passwd=self.passWord, db=self.database)
        sql = "select id from base_info where Enterprise_name = '{}'".format(comName)
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            cid = cursor.fetchone()[0]
            db.commit()
            cursor.close()
            db.close()
            return cid
        except RequestException as err:
            print(err)

    def insertBaseInfo(self,args):
        db = pymysql.connect(host=self.host, port=self.port, user=self.userName, passwd=self.passWord, db=self.database)
        sql = "insert into base_info(Enterprise_name,jyzt,gslx,Enterprise_gszch,Enterprise_zzjgdm,f_body,registered_address" \
              "Legalrepresentative,rtime,approval_date,zczb,industry,Contact_number,djjg,z_body,email,op_from,op_to)"

    def insertLawWenshu(self,args):
        db = pymysql.connect(host=self.host,port=self.port, user=self.userName, passwd=self.passWord, db=self.database)
        sql = "insert into lawsuit_basic(c_id, licence_number, licence_name, licence_anth, from_date, to_date, licence_content, legal_person, audit_type) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"


if __name__ == '__main__':
    a = DBOperation()
    a.selectComId(comName="福建八闽置业有限公司")