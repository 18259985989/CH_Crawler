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

    def insertData(self,sql,dataList):
        db = pymysql.connect(host=self.host, port=self.port, user=self.userName, passwd=self.passWord, db=self.database)
        try:
            cursor = db.cursor()
            cursor.execute(sql, dataList)
            db.commit()
            db.close()
        except RequestException as err:
            print(err)

    def makePlaceholder(self,data):
        placeholder = ""
        length = len(data)
        for i in range(0,length):
            if i == length - 1:
                placeholder = placeholder + "%s"
            else:
                placeholder = placeholder + "%s" + ","
        return placeholder

    def insertBaseInfo(self,args):
        sql = "insert into base_info(Enterprise_name,Enterprise_tyshxydm,jyzt,gslx,Enterprise_gszch,Enterprise_zzjgdm,f_body,registered_address," \
              "Legalrepresentative,rtime,approval_date,zczb,industry,Contact_number,djjg,z_body,source_update_time,local_update_time," \
              "IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT,BATCH_ID,MD5VALUE,email,op_from,op_to) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
              "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.insertData(sql=sql,dataList=args)

    def insertChangeInfo(self,args):
        sql = "insert into change_info(c_id,change_item,before_change,after_change,change_date," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) VALUES (%s,%s,%s,%s,%s," \
              "%s,%s,%s,%s,%s)"
        self.insertData(sql=sql, dataList=args)

    def insertShareholders(self,args):
        sql = "insert into shareholder(c_id,shareholder,con_capital,share_ratio,con_paid_in_capital," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) VALUES (%s,%s,%s,%s,%s," \
              "%s,%s,%s,%s,%s)"
        self.insertData(sql=sql, dataList=args)

    def insertDirectors(self,args):
        sql = "insert into members(c_id,person_name,position," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) VALUES (%s,%s,%s,%s,%s," \
              "%s,%s,%s)"
        self.insertData(sql=sql, dataList=args)

    def insertBranch(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into branch(c_id,branch_name,legal_person,estiblish_date,business_state," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) VALUES ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)


    def insertCourtNotice(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into court_notice(c_id,publish_date,announce_type,court,litigant,MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) " \
              "values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertJudicialauction(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into judicial_sale(c_id,,MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) " \
              "values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertOpennotice(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into court_auto(c_id,start_date,case_number,case_reason,court,courtroom,plaintiff,defendant," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertLawWenshu(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into lawsuit_basic(c_id,casereason,decision_time,caseno,title," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertPenalties(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into punishment(c_id,penish_dec_num,punish_type,punish_auth,decision_date," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertDiscredit(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into dishonest_info(c_id,publish_date,reg_date,case_code,court,performance,gist_num," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertChattelmortgage(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into company_mortgage(c_id,reg_date,guaranteed_amount,status," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertAbnormal(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into abnormal(c_id,put_date,put_reason,remove_date,remove_reason,put_department,remove_department," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertFilinginfo(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into lian(c_id,registdate,caseno,court,prosecutor,appellee," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertEquitypledge(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into equity_pledge(c_id,reg_date,reg_number,pledgor,pledgee,state," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertIllegal(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into illegal_info(c_id,put_date,put_reason,put_department,remove_date,remove_reason,remove_department," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertRestrictedConsumer(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into to_execute(c_id,publish_date,executed,exec_court,doc_type," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertUntax(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into owing_tax(c_id,tax_id_number,own_tax_balance,tax_category,publish_date," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertTaxviolation(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into taxviolation(c_id,taxpayername,taxpayernumber,casenature,publishtime," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertStockFreeze(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into stockfreeze(c_id,executedby,equityamount,executionnoticenum,statuestype,status," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertEnvpunishment(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into env_punishment(c_id,CaseNo,IllegalType,PunishGov,PunishDate,PunishBasis,PunishmentResult," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertTerminationcase(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into to_execute(c_id,case_create_date,case_number,exec_money,exec_court,end_date,doc_type," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertExecutedPerson(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into to_execute(c_id,case_create_date,executed,exec_money,exec_court,case_number,doc_type," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertLicense(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into licence_info(c_id,licence_number,licence_name,licence_content,from_date,to_date,licence_anth," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertImportexport(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into im_export_base(c_id,record_date,crcode,management_category,customs_registered_address," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertQuality(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into check_info(c_id,productName,samlingBatch,check_result,check_authority,check_type," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertDoublecheckup(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into check_info(c_id,raninsPlanId,raninsPlaneName,check_authority,check_date,check_type," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertRandominspection(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into check_info(c_id,check_authority,check_result,check_type,check_date," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertFoodquality(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into check_info(c_id,productName,check_date,check_result,check_type," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertTenderbidding(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into bid_info(c_id,title,publish_date,purchaser," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertCopyright(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into copyright_software(c_id,software_name,simple_name,version,work_type,reg_date,reg_number," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertIcpinfo(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into website_info(c_id,web_name,liscense,web_site,ym," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertWorkright(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into copyright_work(c_id,reg_number,work_type,work_name,finish_date,reg_date,publish_date," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertMark(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into tm_info(c_id,pic_url,tm_name,reg_number,apply_date,tm_type," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)

    def insertPatent(self,args):
        placeholder = self.makePlaceholder(data=args)
        sql = "insert into patent(c_id,patent_name,pub_number,app_publish_date," \
              "MD5VALUE,BATCH_ID,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT) values ({})".format(placeholder)
        self.insertData(sql=sql, dataList=args)
