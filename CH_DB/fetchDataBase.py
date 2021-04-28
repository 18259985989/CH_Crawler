# -*- coding: utf-8 -*-
# coding=utf-8
import pymysql
import json

from CH_DB.get_database import databaseTool
from CH_Request.util.SQLAlchemy.tools.py.mytest import BusinessDirectory
from CH_Request.util.SQLAlchemy.databaseService import DatabaseService
from sqlalchemy.sql.expression import func
import datetime
from sqlalchemy.orm import aliased
from rabbitMQ.logger import Logger
import traceback
import time

def get_serchKeyTessst():
    today = datetime.datetime.now()
    re_date = (today + datetime.timedelta(days=-30)).strftime('%Y-%m-%d')
    db = DatabaseService('192.168.10.68', '3306', 'root', '123456', 'mytest')
    # result = db.session.query(BusinessDirectory.company, BusinessDirectory.scode, BusinessDirectory.data_acquisition_time).filter(
    #     BusinessDirectory.data_acquisition_time < re_date).order_by(func.random()).limit(10).all()
    insider = aliased(BusinessDirectory)
    outer = aliased(BusinessDirectory)
    # result = db.session.query(outer).join((
    #     (func.min(insider.id) + func.round(func.random() * (func.max(insider.id) - 2 - func.min(insider.id)))).label('iid')).filter(insider.data_acquisition_time < re_date),outer.id>=insider.id)
    #
    # (
    #     (func.min(insider.id) + func.round(func.random() * (func.max(insider.id) - 2 - func.min(insider.id)))).label('iid'))

    result = db.session.query(outer, (func.min(insider.id) + func.round(
        func.random() * (func.max(insider.id) - 2 - func.min(insider.id)))).label('iid'))
    res = db.session.query(outer).join(result, insider.id >= outer.id)

    # .filter(
    #     BusinessDirectory.data_acquisition_time < re_date).join(BusinessDirectory,=BusinessDirectory.id).limit(10).all()
    print(result)
    print(res)
    return result


# def get_crawl_database_name(partOfName):
#     item = ['tyc', 'gsxt']
#     try:
#         conn = pymysql.connect("192.168.2.23", "root",
#                                "123456", "mytest", charset='utf8')
#         cursor = conn.cursor()
#         sql = 'show databases'
#         cursor.execute(sql)
#         res = cursor.fetchall()
#         for re in res:
#             for r in re:
#                 if partOfName in r:
#                     item.append(r)
#     except:
#         print(traceback.format_exc())
#         Logger(__name__).logger.error(traceback.format_exc())
#     return item


def ifExist(company, fromtime):
    conn = pymysql.connect(host='192.168.2.23', user='ch_data_source', passwd='123456', db='db_source',port=7865)
    cursor = conn.cursor()
    # sql = 'select company from business_directory b where b.company=%s and ((to_days(now()) - to_days(b.' + fromtime + '))>30 or b.' + fromtime + ' is null) order by id desc'
    # sql = 'select company from business_directory b where b.id=%s and (b.' + fromtime + ' is null) order by id desc'
    sql = 'select Enterprise_name from base_info where Enterprise_name="{}" '.format(company)
    cursor.execute(sql,)
    res = cursor.fetchone()
    # print(res)
    if res:
        return True
    return True


def updateCrawlTime(id, fromtime):
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db = DatabaseService('192.168.2.23', '3306', 'root', '123456', 'mytest')
    try:
        data = db.session.query(BusinessDirectory).filter(BusinessDirectory.id == id).all()
        if isinstance(data, list):
            for a in data:
                setattr(a, fromtime, dt)
        db.session.commit()
        print('%s update %s success' % (id, fromtime))
        Logger(__name__).logger.info('%s update %s success' % (id, fromtime))
    except:
        Logger(__name__).logger.error(traceback.format_exc())
        db.session.rollback()
    db.session.close()


def get_serchKey():
    try:
        conn = pymysql.connect("192.168.10.68", "root",
                               "123456", "mytest", charset='utf8')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # sql = '''select q1.company, q1.scode
        #     from business_directory q1
        #     inner join
        #     (select(min(q2.id) + round(rand() * (max(q2.id) - 2 - min(q2.id)))) as id
        #     from business_directory q2
        #     where (TO_DAYS(NOW()) -TO_DAYS(q2.data_acquisition_time) > 30 or q2.data_acquisition_time is null)) as t
        #     on q1.id >= t.id limit 10;'''
        sql = '''select q1.id,company,scode
            from business_directory q1
            inner join
            (select(min(q2.id) + round(rand() * (max(q2.id) - 2 - min(q2.id)))) as id
            from business_directory q2
            where q2.tyc_time is null  or q2.bzxr_time is null or q2.fygg_time is null) as t
            on q1.id >= t.id limit 10'''

        print(sql)
        cursor.execute(sql)
        rs = cursor.fetchall()
        print('fecth done')
        return rs
    except:

        Logger(__name__).logger.info(traceback.format_exc())
    conn.close()


def update_data_acquisition_time(key, utime):
    # print('update_data_acquisition_time: ', key)
    # print(type(key))
    kk = json.loads(key)

    conn = pymysql.connect("192.168.10.68", "root", "123456", "mytest", charset='utf8')
    cursor = conn.cursor()
    if kk['scode']:
        sql = "UPDATE business_directory  SET data_acquisition_time='" + \
              utime + "' WHERE scode='" + kk['scode'] + "'"
    else:
        sql = "UPDATE business_directory  SET data_acquisition_time='" + \
              utime + "' WHERE company='" + kk['company'] + "'"
    print(sql)
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        Logger(__name__).logger.error(traceback.format_exc())
        conn.rollback()
    conn.close()
    return True


def is_in_database(message):
    message = databaseTool.unify_character_from_item(message)
    conn = pymysql.connect("192.168.10.68", "root",
                           "123456", "dataggregate", charset='utf8')
    cursor = conn.cursor()
    # company=message['company'].
    cursor.execute(
        "select * from  base_info where Enterprise_name='" + message['company'] + "' order by id desc limit 1")
    com_name = cursor.fetchall()
    scode = None
    if message['scode']:
        cursor.execute(
            "select * from  base_info where Enterprise_tyshxydm='" + message['scode'] + "' order by id desc limit 1")
        scode = cursor.fetchall()

    flag = False
    if com_name or scode:
        flag = True
    return flag


def get_fygg_court(com_name):
    db = pymysql.connect("192.168.10.68", "root", "123456",
                         "other_source", charset="utf8")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "select `litigant`, `announce_type`, `publish_date`, `publish_page`, `appellant`, `court`, `content`, `province`, `announce_num` from court_notice  where litigant like '%" + com_name + "%'"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    cursor.close()
    db.close()
    return databaseTool.unify_character_from_list(result)


def get_bdu_zhixing(com_name):
    com_name = databaseTool.unify_character(com_name)
    db = pymysql.connect("192.168.10.68", "root", "123456",
                         "other_source", charset="utf8")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "select `executed`, `org_code`, `exec_money`, `exec_court`, `case_create_date`, `publish_date`, `case_number`, `sex`, `province`, `gist_num`, `gist_unit`, `duty`, `performance`, `disrupttype_name`, `end_date`, `unexectued`, `legal_person` from baidu_to_execute where executed=%s"
    cursor.execute(sql, (com_name,))
    result = cursor.fetchall()
    print(result)
    cursor.close()
    db.close()
    return databaseTool.unify_character_from_list(result)


def IfInAggDataBase(message):
    message = databaseTool.unify_character_from_item(message)
    conn = pymysql.connect("192.168.10.68", "root",
                           "123456", "dataggregate", charset="utf8")
    cursor = conn.cursor()
    # company=message['company'].
    print(message)
    sql = "select * from  base_info b where Enterprise_name='" + message[
        'company'] + "' and (to_days(now()) - to_days(b.local_update_time))<30 order by id desc limit 1"
    print(sql)
    cursor.execute(sql)
    com_name = cursor.fetchall()
    scode = None
    if message['scode']:
        sql = "select * from  base_info b where Enterprise_tyshxydm='" + message[
            'scode'] + "' and (to_days(now()) - to_days(b.local_update_time))<30 order by id desc limit 1"
        print(sql)
        cursor.execute(sql)
        scode = cursor.fetchall()
    flag = False
    if com_name or scode:
        flag = True
    return flag


def base_data_from_aggregation(search_json):
    search = databaseTool.unify_character_from_item(search_json)
    db = pymysql.connect("192.168.10.68", "root", "123456",
                         "dataggregate", charset="utf8")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "select * from base_info where Enterprise_name=%s order by id desc limit 1"
    cursor.execute(sql, (search['company'],))
    result = cursor.fetchone()
    print('base_data : ', result)
    cursor.close()
    db.close()
    return result


def ifExistDelete(com_name):
    com_name = databaseTool.unify_character(com_name)
    db = pymysql.connect("192.168.10.68", "root", "123456",
                         "dataggregate", charset="utf8")
    cursor = db.cursor()
    sql = 'select id from base_info where Enterprise_name=%s'
    cursor.execute(sql, (com_name,))
    ids = cursor.fetchall()
    print("ids: : : ", ids)
    if ids:
        print("该企业数据已存在:", ids)
        for id in ids:
            # 删除主表
            sql_main = "delete from base_info where id=%s"
            cursor.execute(sql_main, (id,))
            db.commit()
            tables = ['shareholder', 'change_info', 'branch', 'equity_pledge', 'members', 'invest',
                      'licence_info', 'punishment', 'tm_info', 'abnormal', 'illegal_info', 'judicial_assistance',
                      'check_info', 'qualification', 'bid_info', 'product', 'patent', 'copyright_software',
                      'equity_change', 'pledgereg', 'court_auto', 'court_notice', 'dishonest_info', 'to_execute',
                      'judicial_sale', 'taxcred', 'copyright_work', 'website_info']
            for table in tables:
                sql = "delete from " + table + " where c_id =%s"
                cursor.execute(sql, (id,))
                db.commit()
            select_regN = 'select reg_number from company_mortgage where c_id=%s'
            cursor.execute(select_regN, (id,))
            regNs = cursor.fetchall()
            del_mor = 'delete from company_mortgage where c_id=%s'
            db.commit()
            cursor.execute(del_mor, (id,))
            mor_tables = ['company_mortgage_pledgee',
                          'company_mortgage_change', 'company_mortgage_collateral']
            for reg in regNs:
                for table in mor_tables:
                    sql = "delete from " + table + " where reg_number=%s"
                    cursor.execute(sql, (reg,))
                    db.commit()
    cursor.close()
    db.commit()
    db.close()


def is_chinese(string):
    for chart in string:
        if '\u4e00' <= chart <= '\u9fa5':
            return True
    return False


def dele(db, cursor, id):
    tables = ['shareholder', 'change_info', 'branch', 'equity_pledge', 'members', 'invest',
              'licence_info', 'punishment', 'tm_info', 'abnormal', 'illegal_info', 'judicial_assistance',
              'check_info', 'qualification', 'bid_info', 'product', 'patent', 'copyright_software',
              'equity_change', 'pledgereg', 'court_auto', 'court_notice', 'dishonest_info', 'to_execute',
              'judicial_sale', 'taxcred', 'copyright_work', 'website_info', 'company_mortgage']
    for table in tables:
        sql = "delete from " + table + " where c_id =%s"
        cursor.execute(sql, (id,))
        print('delete %s %s' % (id, table))
        db.commit()


def get_uscc_from_o_pay_info(search_json):
    search = databaseTool.unify_character_from_item(search_json)
    db = pymysql.connect("192.168.2.23", "ch_data_oper", "123456",
                         "db_store", port=7865, charset="utf8")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "select ID, COMPANY_ID, COMPANY_USCC,COMPANY_NAME from o_pay_info where ID=%s"
    cursor.execute(sql, (search['o_pay_info_id'],))
    result = cursor.fetchone()
    print('base_data : ', result)
    cursor.close()
    db.close()
    return result

def get_uscc_from_basic_info(search_json):
    search = databaseTool.unify_character_from_item(search_json)
    db = pymysql.connect("192.168.2.23", "ch_data_oper", "123456",
                         "db_store", port=7865, charset="utf8")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "select COMPANY_ID, USCC AS COMPANY_USCC, ENTERPRISE_NAME AS COMPANY_NAME from c_basic_info where COMPANY_ID=%s"
    cursor.execute(sql, (search['c_basic_info_company_id'],))
    result = cursor.fetchone()
    print('base_data : ', result)
    cursor.close()
    db.close()
    return result


def insert_credit_report_info(report_id, order_info, company_info):
    o_id = order_info["ID"]
    c_id = order_info["COMPANY_ID"]
    db = pymysql.connect("192.168.2.23", "ch_data_oper", "123456",
                         "db_store", port=7865, charset="utf8")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    try:
        sql = "insert into credit_report_info(CREDIT_REPORT_INFO_ID, " \
              "ORDER_ID, COMPANY_ID, COMPANY_JSON_INFO, STATE, STATEDATE) " \
              "values (%s, %s, %s, %s, %s, %s)"

        sql_result = cursor.execute(sql, [report_id, o_id, c_id, str(company_info), "10A",
                                          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())])
    except Exception as e:
        print(e)
    db.commit()
    cursor.close()
    db.close()
    return sql_result


def update_credit_report_info(order_info):
    o_id = order_info["ID"]
    db = pymysql.connect("192.168.2.23", "ch_data_oper", "123456",
                         "db_store", port=7865, charset="utf8")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    try:
        sql = "UPDATE credit_report_info SET STATE = '10X' WHERE ORDER_ID = %s"

        cursor.execute(sql, o_id)
    except Exception as e:
        print(e)
    db.commit()
    cursor.close()
    db.close()

def update_order_status(o_pay_info_id):
    db = pymysql.connect("192.168.2.23", "ch_data_oper", "123456",
                         "db_store", port=7865, charset="utf8")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    try:
        sql = "UPDATE o_pay_info SET STATE = '10A' WHERE ID = %s"

        cursor.execute(sql, o_pay_info_id)
    except Exception as e:
        print(e)
    db.commit()
    cursor.close()
    db.close()

def callpro():
    db = pymysql.connect("192.168.2.23", "root", "123456",
                         "db_store", port=7865, charset="utf8")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.callproc("ProAllTablesNew")
    db.commit()
    cursor.close()
    db.close()


# if __name__ == '__main__':
    # tt = get_crawl_database_name('crawl')
    # print(tt)
    # if len(tt) == 0:
    #     print('no')
