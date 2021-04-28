# coding=utf-8
import configparser
import copy
import os
from CH_Request.util.SQLAlchemy.reStructFromSQL import *
from CH_Request.util.SQLAlchemy.tools.py.other_source import *
from CH_Request.util.SQLAlchemy.tools.py.model_new import *
# from SQLAlchemy.tools.py.model import *
from CH_DB.fetchDataBase import *
from rabbitMQ.logger import Logger
from datetime import timedelta, datetime, date
import traceback
from concurrent.futures import ThreadPoolExecutor
import gc
from collections import defaultdict
from CH_Request.util.SQLAlchemy.KeyOfTable import mainfield
from CH_Request.util.SQLAlchemy.jsonEncoderService import JsonSerialize, queryResult2Json
from sqlalchemy import distinct
from sqlalchemy import and_

class DAF:
    def __init__(self, search_key):
        self.logger = Logger(__name__)
        self.cf = self.get_config()
        self.host = '192.168.2.23'
        self.port = '7865'
        self.username = 'ch_data_store'
        self.password = '123456'
        self.databaseService = None
        self.serch_json = search_key
        # self.dbnameList = get_crawl_database_name('crawl')  # 获取多个数据库名
        # self.dslist = self.get_DSList()  # 获取多个数据库连接

    # 读取数据库配置
    def get_config(self):
        cf = configparser.ConfigParser()
        # print(os.path.abspath(os.path.dirname(os.getcwd())) + "/SQLAlchemy/dbname.conf")
        cf.read(os.path.abspath(os.path.dirname(os.getcwd())) + "/SQLAlchemy/dbname.conf")
        return cf

    # 获取多个数据库连接
    def get_DSList(self):
        list = []
        for dbname in self.dbnameList:
            db = DatabaseService(self.host, self.port, self.username, self.password, dbname)
            list.append(db)
        return list

    # # 搜索得到数据
    # def search_company_from_each_database(self, databaseService):
    #     base = None
    #     session = databaseService.session
    #     if self.serch_json['company']:
    #         base = session.query(BaseInfo).filter(
    #             BaseInfo.Enterprise_name == self.serch_json['company']).order_by(BaseInfo.id.desc()).first()
    #         if base is None:
    #             if self.serch_json['scode']:
    #                 base = session.query(BaseInfo).filter(
    #                     BaseInfo.Enterprise_tyshxydm == self.serch_json['scode']).order_by(
    #                     BaseInfo.id.desc()).first()
    #     return base

    def get_data_from_other_source(self):
        if self.serch_json['company']:
            item = {}
            db = DatabaseService(self.host, self.port, self.username, self.password, self.cf.get('DB', 'other_source'))
            item['toExecuteRel'] = db.session.query(ToExecute).filter(
                ToExecute.executed.like("%" + self.serch_json['company'] + "%")).all()
            item['courtNoticeRel'] = db.session.query(CourtNotice).filter(
                CourtNotice.litigant.like("%" + self.serch_json['company'] + "%")).all()
            self.logger.logger.info("%s from other_source %s" % (self.serch_json['company'], str(item)))
            # print(item)
            return item

    # 处理数据进行合并
    def deal_each_data(self):
        company_list = []
        for ds in self.dslist:
            # db = self.get_databaseService(dbname)
            base = self.search_company_from_each_database(ds)
            # print(base)
            self.logger.logger.info('%s get data %s' % (ds.database, base))
            if base is not None:
                company_list.append(base)  ##获取多个数据库数据
                # self.combine(company_list, base)
        final_one = self.combine(company_list)  # 开始整合
        final_one = self.combine_other(final_one)  # 整合其他补充数据(如执行人信息等)
        if final_one:
            final_one.local_update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db = DatabaseService(self.host, self.port, self.username, self.password,'db_store')
            self.IfExistDelete(db, final_one)  # 如已存在,先删除再insert
            db.session.add(final_one)
            db.session.commit()
            db.session.close()
            self.logger.logger.info('combine {} success and insert database!!!'.format(str(self.serch_json)))
            # del final_one
            gc.collect()
        # return final_one

    # def IfExistDelete(self, db, final_one):
    #     kk = db.session.query(BaseInfo).filter(BaseInfo.Enterprise_name == final_one.Enterprise_name).all()
    #     if kk:
    #         for a in kk:
    #             print('exist, delete')
    #             db.session.delete(a)
    #     db.session.commit()
    #
    # def combineListFromBase(self, com_list, base):
    #     flag = False
    #     if len(com_list) == 0:
    #         com_list.append(jump2Object(base))
    #         flag = True
    #     for com in com_list:
    #         for key, value in vars(com).items():
    #             if isinstance(value, list):
    #                 baseRel = creatNewList(getattr(base, key))
    #                 if flag:
    #                     baseRel = None
    #                 new_list = self.conbine_list(creatNewList(value), baseRel)
    #                 setattr(com, key, new_list)
    #             elif getattr(com, key) is None or getattr(com, key) is '':
    #                 t = None
    #                 if getattr(base, key):
    #                     t = getattr(base, key).copy()
    #                 setattr(com, key, t)
    #
    #     return com_list

    def creat_hash_dict(self, newlist):
        d = defaultdict(list)
        if newlist:
            field = mainfield[newlist[0]]
            for data in newlist:
                key = hash(data[field])
                d[key].append(data)
        result = {}
        for k in sorted(d):
            result[k] = d[k]
        return result

    def combine_other(self, final_one):
        if final_one:
            item = self.get_data_from_other_source()
            if item:
                for k, v in item.items():
                    if v:
                        new_list = self.conbine_list(creatNewList(getattr(final_one, k)), creatNewList(v))
                        setattr(final_one, k, new_list)
            # del item
        return final_one

    def deal_list_with_multi(self, com, key, flag, final_one):
        baseRel = creatNewList(getattr(com, key))
        if baseRel:
            print(type(baseRel[0]))
        if flag:
            baseRel = []
            # 传入t_list为空(只有一条数据),数据的列表需要 对自身进行遍历去重
            new_list = self.conbine_list2(t_list=baseRel, new_list=creatNewList(getattr(final_one, key)))
        else:
            new_list = self.conbine_list2(creatNewList(getattr(final_one, key)), baseRel)
        setattr(final_one, key, new_list)  # 合并完,对final_one列表的值重新赋值

    # 多条数据进行合并
    def combine(self, com_list):
        final_one = None  # 最终返回的数据(先定义)
        for com in com_list:
            flag = False  # 列表只有一条数据,默认False
            if final_one is None:
                final_one = jump2Object(com)
                flag = True
            executor = ThreadPoolExecutor(max_workers=5)
            for key in self.get_attribute_name(com):
                if isinstance(getattr(com, key), list):
                    executor.submit(self.deal_list_with_multi, com, key, flag, final_one)
                elif not flag:
                    if not key.endswith('id'):
                        if getattr(final_one, key) is None or getattr(final_one, key) is '':
                            t = None
                            if getattr(com, key):
                                t = copy.copy(getattr(com, key))
                            setattr(final_one, key, t)
            executor.shutdown()
        # del com_list
        # gc.collect()
        self.logger.logger.info(final_one)
        return final_one

    def get_attribute_name(self, base):
        temp = []
        for key in base.__dir__():
            if not key.startswith('_') and key != 'metadata' and key != 'baseInfo':
                temp.append(key)
        temp.reverse()
        return temp

    def conbine_list2(self, t_list, new_list):
        '''
        :param t_list: 已去重合并完成的列表数据
        :param new_list: 需要与t_list中的数据进行对比合并的列表数据
        :return:    最终返回t_list列表
        '''
        if new_list:
            key_list = self.get_attribute_name(new_list[0])
            for rel in new_list:
                flag = True
                if not t_list:  # 如果只有一条数据,数据的列表需要 对自身进行遍历去重
                    t_list = []
                    t_list.append(rel)
                    # 将列表的第一条数据添加到t_list,跳出
                    continue
                for t in t_list:
                    print("t", t)
                    None_index = 0
                    Break = False
                    for key in key_list:
                        # 首先遍历对比非列表数据,若非列表数据相同,则判断为同一条数据,再对列表数据进行合并
                        if not isinstance(getattr(t, key), list) and not key.endswith('id'):
                            temp = self.isDiff2(getattr(t, key), getattr(rel, key))
                            if temp == 0:
                                Break = True
                                break
                            if temp == 1:
                                None_index = temp
                    if Break:
                        continue
                    # 判断两条数据中的不同,是否存在其中一个或两个都为None,满足条件,即为同一条数据,进行合并
                    if None_index == 1:
                        flag = False
                        for key in key_list:
                            if getattr(t, key) is None and getattr(rel, key):
                                setattr(t, key, copy.copy(getattr(rel, key)))
                    else:
                        flag = False
                        for key in key_list:  # 当数据的非列表数据都相同时,再判断是否存在列表数据
                            if isinstance(getattr(t, key), list):
                                new = self.conbine_list(creatNewList(getattr(t, key)),
                                                        creatNewList(getattr(rel, key)))
                                if new:
                                    setattr(t, key, new.copy())
                    gc.collect()
                if flag:
                    t_list.append(rel)
        # del new_list
        gc.collect()
        return t_list

    def conbine_list(self, t_list, new_list):
        '''
        :param t_list: 已去重合并完成的列表数据
        :param new_list: 需要与t_list中的数据进行对比合并的列表数据
        :return:    最终返回t_list列表
        '''
        if new_list:
            key_list = self.get_attribute_name(new_list[0])
            for rel in new_list:
                flag = True
                if not t_list:  # 如果只有一条数据,数据的列表需要 对自身进行遍历去重
                    t_list = []
                    t_list.append(rel)
                    # 将列表的第一条数据添加到t_list,跳出
                    continue
                for t in t_list:
                    print("t", t)
                    diff_index = 0
                    None_index = 0
                    for key in key_list:
                        # 首先遍历对比非列表数据,若非列表数据相同,则判断为同一条数据,再对列表数据进行合并
                        if not isinstance(getattr(t, key), list) and not key.endswith('id'):
                            if self.isDiff(getattr(t, key), getattr(rel, key)):
                                diff_index += 1
                                if self.OneOfDiffIsNone(getattr(t, key), getattr(rel, key)):
                                    None_index += 1
                    if diff_index == 0:
                        flag = False
                        for key in key_list:  # 当数据的非列表数据都相同时,再判断是否存在列表数据
                            if isinstance(getattr(t, key), list):
                                new = self.conbine_list(creatNewList(getattr(t, key)),
                                                        creatNewList(getattr(rel, key)))
                                if new:
                                    setattr(t, key, new.copy())
                    # 判断两条数据中的不同,是否存在其中一个或两个都为None,满足条件,即为同一条数据,进行合并
                    if diff_index != 0 and diff_index == None_index:
                        flag = False
                        for key in key_list:
                            if getattr(t, key) is None and getattr(rel, key):
                                setattr(t, key, copy.copy(getattr(rel, key)))
                    gc.collect()
                if flag:
                    t_list.append(rel)
        # del new_list
        # gc.collect()
        return t_list

    def isDiff2(self, one, two):
        '''

        :param one:
        :param two:
        :return: 0,两边值都不同，且没有一个为None
        :return: 1,两边值都不同，且至少一个为None
        :return: 2,两边值相同
        '''
        one = databaseTool.removePunctuation(copy.copy(one))
        two = databaseTool.removePunctuation(copy.copy(two))

        if one != two:
            if one and two:
                # del one
                # del two
                return 0
        if self.OneOfDiffIsNone(one, two):
            return 1
        # del one
        # del two
        # gc.collect()
        return 2

    def isDiff(self, one, two):
        one = databaseTool.removePunctuation(copy.copy(one))
        two = databaseTool.removePunctuation(copy.copy(two))

        if one != two:
            # del one
            # del two
            # gc.collect()
            return True
        # del one
        # del two
        # gc.collect()
        return False

    def OneOfDiffIsNone(self, one, two):
        if one is None or two is None:
            # del one
            # del two
            # gc.collect()
            return True
        # del one
        # del two
        # gc.collect()
        return False

    # def getInfoFromLocal(self, expireDay, credit_score=None, credit_level=None):
    #     '''
    #
    #     :param companyName: 来自搜索的公司名
    #     :param scode: 来自搜索的社会统一信仰代码
    #     :param expireDay: 数据保质期(7天)
    #     :return:
    #     '''
    #     databaseService = DatabaseService(self.host, self.port, self.username, self.password,
    #                                       self.cf.get('DB', 'dataggregate'))
    #     try:
    #         baseInfo = None
    #         if self.serch_json['scode'] is not None:
    #             baseInfo = databaseService.session.query(BaseInfo).filter(
    #                 BaseInfo.Enterprise_tyshxydm == self.serch_json['scode']).order_by(BaseInfo.id.desc()).first()
    #
    #         if baseInfo is None:
    #             baseInfo = databaseService.session.query(BaseInfo).filter(
    #                 BaseInfo.Enterprise_name == self.serch_json['company']).order_by(BaseInfo.id.desc()).first()
    #
    #         jsonResult = None
    #         if baseInfo is not None:
    #             if credit_score is not None:
    #                 baseInfo.score = credit_score
    #             baseInfo.level = None
    #             if credit_level is not None:
    #                 baseInfo.level = credit_level
    #
    #             today_ele = datetime.now()
    #             expireDay = today_ele - timedelta(days=expireDay)
    #             print('expireDay', expireDay)
    #             if baseInfo.local_update_time > expireDay:
    #                 jsonResult = JsonSerialize(baseInfo)
    #         databaseService.session.commit()
    #         databaseService.session.close()
    #         databaseService.close_engine()
    #         if jsonResult is not None:
    #             self.logger.logger.info(
    #                 "get company[%s, %s] from local database." % (self.serch_json['company'], self.serch_json['scode']))
    #             self.logger.logger.debug(jsonResult)
    #
    #         return jsonResult
    #     except:
    #         self.logger.logger.error(traceback.format_exc())
    #         return None

    def getDataFromDbStore(self, pay_id):
        db_service = DatabaseService(self.host, self.port, self.username, self.password,
                                     'db_store')
        json_result = '{}'
        json_result = json.loads(json_result)
        print(json_result)
        try:
            baseInfo = None
            if self.serch_json['COMPANY_USCC'] is not None:
                baseInfo = db_service.session.query(CBaseInfo.COMPANY_ID.label("id"),
                                                    CBaseInfo.ENTERPRISE_NAME.label("companyName"),
                                                    CBaseInfo.USCC.label("uscc"),
                                                    CBaseInfo.REGISTERED_NO.label("registeredNo"),
                                                    CBaseInfo.ORGANIZATION_CODE.label("organizationCode"),
                                                    CBaseInfo.LEGAL_PERSON.label("legalPerson"),
                                                    CBaseInfo.FOUNDED_DATE.label("foundedDate"),
                                                    CBaseInfo.OPEN_DATE.label("openDate"),
                                                    CBaseInfo.REGISTERED_CAPITAL.label("registeredCapital"),
                                                    CBaseInfo.REGISTRATION_AUTHORITY.label("registrationAuthority"),
                                                    CBaseInfo.BUSINESS_SCOPE.label("businessScope"),
                                                    CBaseInfo.BUSINESS_TERM.label("businessTerm"),
                                                    CBaseInfo.BUSINESS_STATUS.label("businessStatus"),
                                                    CBaseInfo.REGISTERED_ADDRESS.label("registeredAddress"),
                                                    CBaseInfo.CONTACT_PHONE.label("contactPhone"),
                                                    CBaseInfo.TRADE.label("trade"),
                                                    CBaseInfo.POST_CODE.label("postCode"),
                                                    CBaseInfo.STATEDATE.label("updtTime")).filter(and_(CBaseInfo.USCC == self.serch_json['COMPANY_USCC'],CBaseInfo.STATE=='10A')).order_by(CBaseInfo.STATEDATE.desc()).first()
                print(baseInfo[0])
                #print(dict(baseInfo))

            if baseInfo is None:
                baseInfo = db_service.session.query(CBaseInfo.COMPANY_ID.label("id"),
                                                    CBaseInfo.USCC.label("uscc"),
                                                    CBaseInfo.REGISTERED_NO.label("registeredNo"),
                                                    CBaseInfo.ENTERPRISE_NAME.label("companyName"),
                                                    CBaseInfo.ORGANIZATION_CODE.label("organizationCode"),
                                                    CBaseInfo.LEGAL_PERSON.label("legalPerson"),
                                                    CBaseInfo.FOUNDED_DATE.label("foundedDate"),
                                                    CBaseInfo.OPEN_DATE.label("openDate"),
                                                    CBaseInfo.REGISTERED_CAPITAL.label("registeredCapital"),
                                                    CBaseInfo.REGISTRATION_AUTHORITY.label("registrationAuthority"),
                                                    CBaseInfo.BUSINESS_SCOPE.label("businessScope"),
                                                    CBaseInfo.BUSINESS_TERM.label("businessTerm"),
                                                    CBaseInfo.BUSINESS_STATUS.label("businessStatus"),
                                                    CBaseInfo.REGISTERED_ADDRESS.label("registeredAddress"),
                                                    CBaseInfo.CONTACT_PHONE.label("contactPhone"),
                                                    CBaseInfo.TRADE.label("trade"),
                                                    CBaseInfo.POST_CODE.label("postCode"),
                                                    CBaseInfo.STATEDATE.label("updtTime")).distinct().filter(and_(CBaseInfo.ENTERPRISE_NAME == self.serch_json['COMPANY_NAME'], CBaseInfo.STATE=='10A')).order_by(CBaseInfo.STATEDATE.desc()).first()
            branchInfo = db_service.session.query(CBranch.ID.label("id"),
                                                  CBranch.COMPANY_ID.label("companyId"),
                                                  CBranch.COMPANY_NAME.label("companyName"),
                                                  CBaseInfo.LEGAL_PERSON.label("legalPerson"),
                                                  CBaseInfo.BUSINESS_STATUS.label("state"),
                                                  CBaseInfo.FOUNDED_DATE.label("registerDate"),
                                                  CBaseInfo.REGISTERED_CAPITAL.label("registerCapital"),
                                                  CBranch.STATEDATE.label("updtTime")).distinct().join(CBaseInfo, CBranch.BRANCH_COMPANY_ID==CBaseInfo.COMPANY_ID).filter(CBranch.COMPANY_ID == baseInfo[0]).all()
            abnormalInfo = db_service.session.query(CAbnormal.ID.label("id"),
                                                    CAbnormal.COMPANY_ID.label("companyId"),
                                                    CAbnormal.INCLUDED_DATE.label("putDate"),
                                                    CAbnormal.PUT_OFFICE.label("decisionOffice"),
                                                    CAbnormal.PUT_REASON.label("putReason"),
                                                    CAbnormal.REMOVED_REASON.label("outReason"),
                                                    CAbnormal.REMOVED_DATE.label("outDate"),
                                                    CAbnormal.STATEDATE.label("updtTime")).distinct().filter(and_(CAbnormal.COMPANY_ID == baseInfo[0]
                                                                                                 ,CAbnormal.TYPE == "10BE")).all()
            illegalInfo = db_service.session.query(CAbnormal.ID.label("id"),
                                                    CAbnormal.COMPANY_ID.label("companyId"),
                                                    CAbnormal.INCLUDED_DATE.label("includedDate"),
                                                    CAbnormal.PUT_OFFICE.label("type"),
                                                    CAbnormal.PUT_REASON.label("putReason"),
                                                    CAbnormal.REMOVED_REASON.label("removedReason"),
                                                    CAbnormal.REMOVED_DATE.label("removedDate"),
                                                    CAbnormal.REMOVED_OFFICE.label("removedOffice"),
                                                    CAbnormal.STATEDATE.label("updtTime")).distinct().filter(and_(CAbnormal.COMPANY_ID == baseInfo[0],
                                                                                                 CAbnormal.TYPE == "10SI")).all()
            bidInfo = db_service.session.query(CBidInfo.ID.label("id"),
                                               CBidInfo.COMPANY_ID.label("companyId"),
                                               CBidInfo.DESCRIPTION.label("putDate"),
                                               CBidInfo.PUBLIC_DATE.label("decisionOffice"),
                                               CBidInfo.CHECK_TYPE.label("putReason"),
                                               CBidInfo.STATEDATE.label("outReason"),
                                               CBidInfo.PURCHASING_AGENT.label("outDate")).distinct().filter(and_(CBidInfo.COMPANY_ID == baseInfo[0],
                                                                                                CBidInfo.TAB_TYPE == "10Z")).all()
            checkInfo = db_service.session.query(CBidInfo.ID.label("id"),
                                                 CBidInfo.COMPANY_ID.label("companyId"),
                                                 CBidInfo.TITLE.label("itemTitle"),
                                                 CBidInfo.CHECK_TYPE.label("checkType"),
                                                 CBidInfo.PUBLIC_DATE.label("checkDate"),
                                                 CBidInfo.DESCRIPTION.label("checkResult"),
                                                 CBidInfo.STATEDATE.label("updtTime"),
                                                 CBidInfo.PURCHASING_AGENT.label("office")).distinct().filter(and_(CBidInfo.COMPANY_ID == baseInfo[0],
                                                                                                 CBidInfo.TAB_TYPE == "10C")).all()
            changeInfo = db_service.session.query(CChangeInfo.ID.label("id"),
                                                  CChangeInfo.COMPANY_ID.label("companyId"),
                                                  CChangeInfo.CHANGE_ITEM.label("changeItem"),
                                                  CChangeInfo.BEFORE_CHANGE.label("beforeChange"),
                                                  CChangeInfo.AFTER_CHANGE.label("afterChange"),
                                                  CChangeInfo.CHANGE_TIME.label("changeTime"),
                                                  CChangeInfo.STATEDATE.label("updtTime")).distinct().filter(CChangeInfo.COMPANY_ID == baseInfo[0]).all()

            mortgageInfo = db_service.session.query(CCompanyMortgage.ID.label("id"),
                                                    CCompanyMortgage.COMPANY_ID.label("companyId"),
                                                    CCompanyMortgage.REGISTER_DATE.label("registerDate"),
                                                    CCompanyMortgage.REGISTER_NUMBER.label("registerNumber"),
                                                    CCompanyMortgage.REGISTER_OFFICE.label("registerOffice"),
                                                    CCompanyMortgage.WARRANT_TYPE.label("guaranteedType"),
                                                    CCompanyMortgage.GUARANTEED_AMOUNT.label("guaranteedAmount"),
                                                    CCompanyMortgage.MORT_STATUS.label("state"),
                                                    CCompanyMortgage.STATEDATE.label("updtTime")).distinct().filter(and_(CCompanyMortgage.COMPANY_ID == baseInfo[0],
                                                                                                        CCompanyMortgage.QUALITY_TYPE == "10CM")).all()
            equityPleInfo = db_service.session.query(CCompanyMortgage.ID.label("id"),
                                                     CCompanyMortgage.COMPANY_ID.label("companyId"),
                                                     CCompanyMortgage.REGISTER_DATE.label("registerDate"),
                                                     CCompanyMortgage.REGISTER_NUMBER.label("registerNumber"),
                                                     CCompanyMortgage.MORTGAGE_NAME.label("pledgor"),
                                                     CCompanyMortgage.PEOPLE_NAME.label("pledgee"),
                                                     CCompanyMortgage.MORT_STATUS.label("state"),
                                                     CCompanyMortgage.GUARANTEED_AMOUNT.label("equityAmount"),
                                                     CCompanyMortgage.STATEDATE.label("updtTime")).distinct().filter(and_(CCompanyMortgage.COMPANY_ID == baseInfo[0]
                                                                                                         ,CCompanyMortgage.QUALITY_TYPE == "10PE")).all()

            copySoftInfo = db_service.session.query(CCopyrightSoftware.ID.label("id"),
                                                    CCopyrightSoftware.COMPANY_ID.label("companyId"),
                                                    CCopyrightSoftware.COPYRIGHT_NAME.label("softwareName"),
                                                    CCopyrightSoftware.REGISTER_NUMBER.label("registerNumber"),
                                                    CCopyrightSoftware.VERSION_NUMBER.label("versionNumber"),
                                                    CCopyrightSoftware.CLASSIFICATION_NUMBER.label("classificationNumber"),
                                                    CCopyrightSoftware.REGISTER_DATE.label("registerDate"),
                                                    CCopyrightSoftware.SOFTWARE_ABBREVIATION.label("softwareAbbreviation"),
                                                    CCopyrightSoftware.COPYRIGHT_AUTHOR.label("copyright"),
                                                    CCopyrightSoftware.WORKS_FINISH_DATE.label("firstPublicDate"),
                                                    CCopyrightSoftware.STATEDATE.label("updtTime")).distinct().filter(and_(CCopyrightSoftware.COMPANY_ID == baseInfo[0]
                                                                                                          ,CCopyrightSoftware.COPYRIGHT_TYPE == "10SC")).all()

            copyWorkInfo = db_service.session.query(CCopyrightSoftware.ID.label("id"),
                                                    CCopyrightSoftware.COMPANY_ID.label("companyId"),
                                                    CCopyrightSoftware.COPYRIGHT_NAME.label("worksName"),
                                                    CCopyrightSoftware.REGISTER_NUMBER.label("registerNumber"),
                                                    CCopyrightSoftware.WORKS_TYPE.label("versionNumber"),
                                                    CCopyrightSoftware.REGISTER_DATE.label("registerDate"),
                                                    CCopyrightSoftware.WORKS_FINISH_DATE.label("worksFinishDate"),
                                                    CCopyrightSoftware.FIRST_PUBLIC_DATE.label("firstPublicDate"),
                                                    CCopyrightSoftware.STATEDATE.label("updtTime")).distinct().filter(and_(CCopyrightSoftware.COMPANY_ID == baseInfo[0],
                                                                                                          CCopyrightSoftware.COPYRIGHT_TYPE == "10WC")).all()

            courtAutoInfo = db_service.session.query(CCourtAuto.ID.label("id"),
                                                     CCourtAuto.COMPANY_ID.label("companyId"),
                                                     CCourtAuto.PUBLIC_DATE.label("announcementDate"),
                                                     CCourtAuto.CASE_REASON.label("caseReason"),
                                                     CCourtAuto.APPELLANT.label("appellant"),
                                                     CCourtAuto.DEFENDANT.label("defendant"),
                                                     CCourtAuto.CASE_NUMBER.label("caseNumber"),
                                                     CCourtAuto.COURT.label("court"),
                                                     CCourtAuto.STATEDATE.label("updtTime")).distinct().filter(and_(CCourtAuto.COMPANY_ID == baseInfo[0],
                                                                                                   CCourtAuto.PUBLIC_TYPE == "10CA")).all()

            courtNotiInfo = db_service.session.query(CCourtAuto.ID.label("id"),
                                                     CCourtAuto.COMPANY_ID.label("companyId"),
                                                     CCourtAuto.PUBLIC_DATE.label("pubilcDate"),
                                                     CCourtAuto.ANNOUNCE_TYPE.label("publicType"),
                                                     CCourtAuto.PUBLIC_CONTEXT.label("publicContext"),
                                                     CCourtAuto.APPELLANT.label("appellant"),
                                                     CCourtAuto.DEFENDANT.label("defendant"),
                                                     CCourtAuto.COURT.label("court"),
                                                     CCourtAuto.STATEDATE.label("updtTime")).distinct().filter(and_(CCourtAuto.COMPANY_ID == baseInfo[0],
                                                                                                   CCourtAuto.PUBLIC_TYPE == "10CN")).all()
            judsaleInfo = db_service.session.query(CCourtAuto.ID.label("id"),
                                                   CCourtAuto.COMPANY_ID.label("companyId"),
                                                   CCourtAuto.LITIGANT.label("auctionNotice"),
                                                   CCourtAuto.PUBLIC_DATE.label("noticeDate"),
                                                   CCourtAuto.COURT.label("implementCourt"),
                                                   CCourtAuto.ANNOUNCE_TYPE.label("auctionTarget"),
                                                   CCourtAuto.STATEDATE.label("updtTime")).distinct().filter(and_(CCourtAuto.COMPANY_ID == baseInfo[0],
                                                                                                 CCourtAuto.PUBLIC_TYPE == "10JA")).all()

            dishonestInfo = db_service.session.query(CDishonestInfo.ID.label("id"),
                                                     CDishonestInfo.COMPANY_ID.label("companyId"),
                                                     CDishonestInfo.SET_DATE.label("setDate"),
                                                     CDishonestInfo.CASE_NUMBER.label("caseNumber"),
                                                     CDishonestInfo.PERFORM_NUMBER.label("performNumber"),
                                                     CDishonestInfo.IMPLEMENT_COURT.label("implementCourt"),
                                                     CDishonestInfo.PERFORM_STATE.label("performState"),
                                                     CDishonestInfo.STATEDATE.label("updtTime")).distinct().filter(and_(CDishonestInfo.COMPANY_ID == baseInfo[0],
                                                                                                       CDishonestInfo.DISHONEST_TYPE == "10DI")).all()

            executedInfo = db_service.session.query(CDishonestInfo.ID.label("id"),
                                                    CDishonestInfo.COMPANY_ID.label("companyId"),
                                                    CDishonestInfo.SET_DATE.label("setDate"),
                                                    CDishonestInfo.CASE_NUMBER.label("caseNumber"),
                                                    CDishonestInfo.IMPLEMENT_TARGET.label("implementTarget"),
                                                    CDishonestInfo.IMPLEMENT_COURT.label("implementCourt"),
                                                    CDishonestInfo.STATEDATE.label("updtTime")).distinct().filter(and_(CDishonestInfo.COMPANY_ID == baseInfo[0],
                                                                                                      CDishonestInfo.DISHONEST_TYPE == "10EP")).all()

            websiteInfo = db_service.session.query(CWebsiteInfo.ID.label("id"),
                                                   CWebsiteInfo.COMPANY_ID.label("companyId"),
                                                   CWebsiteInfo.WEB_HOME.label("webHome"),
                                                   CWebsiteInfo.WEB_NAME.label("webName"),
                                                   CWebsiteInfo.CASE_NUMBER.label("caseNumber"),
                                                   CWebsiteInfo.AUDIT_DATE.label("auditDate"),
                                                   CWebsiteInfo.DOMAIN_NAME.label("domainName"),
                                                   CWebsiteInfo.COMPANY_TYPE.label("companyType"),
                                                   CWebsiteInfo.STATEDATE.label("updtTime")).distinct().filter(CWebsiteInfo.COMPANY_ID == baseInfo[0]).all()

            yearReportInfo = db_service.session.query(CYearReport.ID.label("id"),
                                                      CYearReport.COMPANY_ID.label("companyId"),
                                                      CYearReport.YEAR.label("year"),
                                                      CYearReport.CAPITAL_TOTAL.label("capitalTotal"),
                                                      CYearReport.MAIN_TOTAL.label("mainTotal"),
                                                      CYearReport.OWNER_TOTAL.label("ownerTotal"),
                                                      CYearReport.NET_PROFIT.label("netProfit"),
                                                      CYearReport.BUSINESS_TOTAL.label("businessTotal"),
                                                      CYearReport.TAX_TOTAL.label("taxTotal"),
                                                      CYearReport.PROFIT_TOTAL.label("profitTotal"),
                                                      CYearReport.LIABILITIES_TOTAL.label("liabilitiesTotal"),
                                                      CYearReport.STATEDATE.label("updtTime")).distinct().filter(CYearReport.COMPANY_ID == baseInfo[0]).all()

            tmInfo = db_service.session.query(CTmInfo.ID.label("id"),
                                              CTmInfo.COMPANY_ID.label("companyId"),
                                              CTmInfo.TRADEMARK_PIC.label("trademarkPic"),
                                              CTmInfo.TRADEMARK_NAME.label("trademarkName"),
                                              CTmInfo.REGISTER_NUMBER.label("registerNumber"),
                                              CTmInfo.SERVICE_LIST.label("serviceList"),
                                              CTmInfo.TRADEMARK_STATE.label("state"),
                                              CTmInfo.APPLY_DATE.label("applyDate"),
                                              CTmInfo.TRADEMARK_TYPE.label("trademarkType"),
                                              CTmInfo.STATEDATE.label("updtTime")).distinct().filter(CTmInfo.COMPANY_ID == baseInfo[0]).all()

            shareholderInfo = db_service.session.query(CShareholder.ID.label("id"),
                                                       CShareholder.COMPANY_ID.label("companyId"),
                                                       CShareholder.SHAREHOLDER.label("shareholder"),
                                                       CShareholder.SUBSCRIBED_CAPITAL.label("subscribedCapital"),
                                                       CShareholder.SUBSCRIBED_DATE.label("subscribedDate"),
                                                       CShareholder.SUBSCRIBED_PROPORTION.label("subscribedProportion"),
                                                       CShareholder.CURRENCY.label("currency"),
                                                       CShareholder.NATIONALITY.label("nationality"),
                                                       CShareholder.STATEDATE.label("updtTime")).distinct().filter(
                CShareholder.COMPANY_ID == baseInfo[0]).all()

            punishmentInfo = db_service.session.query(CPunishment.ID.label("id"),
                                                      CPunishment.COMPANY_ID.label("companyId"),
                                                      CPunishment.DECISION_NUMBER.label("decisionNumber"),
                                                      CPunishment.PUNISH_TYPE.label("punishType"),
                                                      CPunishment.PUNISH_TEXT.label("punishText"),
                                                      CPunishment.DECISION_DATE.label("decisionDate"),
                                                      CPunishment.DECISION_OFFICE.label("decisionOffice"),
                                                      CPunishment.STATEDATE.label("updtTime")).distinct().filter(CPunishment.COMPANY_ID == baseInfo[0]).all()

            productInfo = db_service.session.query(CProduct.ID.label("id"),
                                                   CProduct.COMPANY_ID.label("companyId"),
                                                   CProduct.PRODUCT_NAME.label("name"),
                                                   CProduct.CLASSES.label("classes"),
                                                   CProduct.BRIEF.label("brief"),
                                                   CProduct.ICON.label("icon"),
                                                   CProduct.PRODUCT_TYPE.label("productType"),
                                                   CProduct.STATEDATE.label("updtTime")).distinct().filter(CProduct.COMPANY_ID == baseInfo[0]).all()

            patentInfo = db_service.session.query(CPatent.ID.label("id"),
                                                  CPatent.COMPANY_ID.label("companyId"),
                                                  CPatent.APPLY_NUMBER.label("applyNumber"),
                                                  ("["+CPatent.APPLY_NUMBER+"]"+CPatent.SUMMARY).label("summary"),
                                                  CPatent.INVENTOR.label("inventor"),
                                                  CPatent.INVENTION.label("invention"),
                                                  CPatent.APPLY_PERSON.label("applyPerson"),
                                                  CPatent.APPLY_DATE.label("applyDate"),
                                                  CPatent.APPLY_PUBLIC_DATE.label("applyPublicDate"),
                                                  CPatent.AGENCY.label("agency"),
                                                  CPatent.AGENT.label("agent"),
                                                  CPatent.ADDRESS.label("address"),
                                                  CPatent.STATEDATE.label("updtTime")).distinct().filter(CPatent.COMPANY_ID == baseInfo[0]).order_by(CPatent.APPLY_NUMBER).all()

            owingInfo = db_service.session.query(COwingTax.ID.label("id"),
                                                 COwingTax.COMPANY_ID.label("companyId"),
                                                 COwingTax.PUBLIC_DATE.label("publicDate"),
                                                 COwingTax.TAXPAYER_NUMBER.label("taxpayerNumber"),
                                                 COwingTax.TAX_TYPE.label("taxType"),
                                                 COwingTax.TAX_OWED.label("taxArrears"),
                                                 COwingTax.CURRENT_TAX_OWED.label("over"),
                                                 COwingTax.OFFICE.label("office"),
                                                 COwingTax.STATEDATE.label("updtTime")).distinct().filter(and_(COwingTax.COMPANY_ID == baseInfo[0],
                                                                                              COwingTax.TAX_RATING == "10TO")).all()

            taxcredInfo = db_service.session.query(COwingTax.ID.label("id"),
                                                   COwingTax.COMPANY_ID.label("companyId"),
                                                   COwingTax.YEARS.label("year"),
                                                   COwingTax.GRADE.label("taxLevel"),
                                                   COwingTax.TAX_TYPE.label("type"),
                                                   COwingTax.TAXPAYER_NUMBER.label("taxpayerNumber"),
                                                   COwingTax.OFFICE.label("office"),
                                                   COwingTax.STATEDATE.label("updtTime")).distinct().filter(and_(COwingTax.COMPANY_ID == baseInfo[0],
                                                                                                COwingTax.TAX_RATING == "10TR")).all()
            memberInfo = db_service.session.query(CMembers.ID.label("id"),
                                                  CMembers.COMPANY_ID.label("companyId"),
                                                  PBasicInfo.REAL_NAME.label("name"),
                                                  CMembers.POSITION.label("position"),
                                                  CMembers.STATEDATE.label("updtTime")).distinct().join(PBasicInfo, PBasicInfo.PERSON_ID==CMembers.PERSON_ID).filter(CMembers.COMPANY_ID == baseInfo[0]).all()

            licenceInfo = db_service.session.query(CLicenceInfo.ID.label("id"),
                                                   CLicenceInfo.COMPANY_ID.label("companyId"),
                                                   CLicenceInfo.AUTHENTICATION_NAME.label("administrativeLicensingName"),
                                                   CLicenceInfo.AUTHENTICATION_TEXT.label("administrativeLicensingContext"),
                                                   CLicenceInfo.AUTHENTICATION_NUMBER.label("administrativeLicensingNumber"),
                                                   CLicenceInfo.AUTHENTICATION_OFFICE.label("administrativeLicensingOffice"),
                                                   CLicenceInfo.AUTHENTICATION_EXPIRY.label("administrativeLicensingEnd"),
                                                   CLicenceInfo.AUTHENTICATION_DATE.label("administrativeLicensingExpiry"),
                                                   CLicenceInfo.STATEDATE.label("updtTime")).distinct().filter(and_(CLicenceInfo.COMPANY_ID == baseInfo[0],
                                                                                                   CLicenceInfo.AUTHENTICATION_TYPE == "10AL")).all()

            qualifyInfo = db_service.session.query(CLicenceInfo.ID.label("id"),
                                                   CLicenceInfo.COMPANY_ID.label("companyId"),
                                                   CLicenceInfo.CERTIFICATE_TYPE.label("certificateType"),
                                                   CLicenceInfo.AUTHENTICATION_NUMBER.label("certificate_number"),
                                                   CLicenceInfo.AUTHENTICATION_EXPIRY.label("expiredDate"),
                                                   CLicenceInfo.AUTHENTICATION_DATE.label("issueDate"),
                                                   CLicenceInfo.STATEDATE.label("updtTime")).distinct().filter(and_(CLicenceInfo.COMPANY_ID == baseInfo[0],
                                                                                                   CLicenceInfo.AUTHENTICATION_TYPE == "10CF")).all()
            lawsuitInfo = db_service.session.query(CLawsuitBasic.ID.label("id"),
                                                   CLawsuitBasic.COMPANY_ID.label("companyId"),
                                                   CLawsuitBasic.SENTENCE_DATE.label("sentenceDate"),
                                                   CLawsuitBasic.PLAINTIFF.label("plaintiff"),
                                                   CLawsuitBasic.DEFENDANT.label("defendant"),
                                                   CLawsuitBasic.CASE_TYPE.label("caseType"),
                                                   CLawsuitBasic.CASE_NUMBER.label("caseNumber"),
                                                   CLawsuitBasic.CASE_DETAIL.label("sentenceContext"),
                                                   CLawsuitBasic.RESULT.label("sentenceResult"),
                                                   CLawsuitBasic.STATEDATE.label("updtTime")).distinct().filter(CLawsuitBasic.COMPANY_ID == baseInfo[0]).all()

            investInfo = db_service.session.query(CInvest.ID.label("id"),
                                                  CInvest.COMPANY_ID.label("companyId"),
                                                  CInvest.INVEST_COMPANY.label("investCompany"),
                                                  CInvest.LEGAL_PERSON.label("overLegalEpresentative"),
                                                  CInvest.FOUNDED_DATE.label("buildDate"),
                                                  CInvest.REGISTERED_CAPITAL.label("registerCapital"),
                                                  CInvest.BUSINESS_STATUS.label("manageState"),
                                                  CInvest.INVEST_NUMBER.label("investNumber"),
                                                  CInvest.INVEST_PROPORTION.label("investProportion"),
                                                  CInvest.STATEDATE.label("updtTime")).distinct().filter(CInvest.COMPANY_ID == baseInfo[0]).all()

            imExportInfo = db_service.session.query(CImExportBase.ID.label("id"),
                                                    CImExportBase.COMPANY_ID.label("companyId"),
                                                    CImExportBase.REGISTERED_DATE.label("registeredDate"),
                                                    CImExportBase.CUSTOMS_REGISTERED_NUMBER.label("customsRegisteredNumber"),
                                                    CImExportBase.REGISTERED_CUSTOMS.label("registeredCustoms"),
                                                    CImExportBase.ADMIN_AREA.label("adminArea"),
                                                    CImExportBase.ECONOMY_AREA.label("economyArea"),
                                                    CImExportBase.MANAGE_TYPE.label("manageType"),
                                                    CImExportBase.SPECIAL_AREA.label("specialArea"),
                                                    CImExportBase.INDUSTRY_TYPE.label("industryType"),
                                                    CImExportBase.EFFECTIVE_DATE.label("effectiveDate"),
                                                    CImExportBase.CUSTOMS_LOGOUT.label("customsLogout"),
                                                    CImExportBase.YEAR_RESULT.label("yearResult"),
                                                    CImExportBase.BUSINESS_TYPE.label("businessType"),
                                                    CImExportBase.CREDIT_LEVEL.label("authDate"),
                                                    CImExportBase.AUTH_DATE.label("authNumber"),
                                                    CImExportBase.AUTH_NUMBER.label("creditLevel"),
                                                    CImExportBase.STATEDATE.label("updtTime")).distinct().filter(CImExportBase.COMPANY_ID == baseInfo[0]).all()
            onlineShopInfo = db_service.session.query(CYearReport.ID.label("id"),
                                                      CYearReport.COMPANY_ID.label("companyId"),
                                                      CYearReport.YEAR.label("year"),
                                                      CYearReport.WEB_NAME.label("shopName"),
                                                      CYearReport.STATEDATE.label("updtTime")).distinct().filter(
                CYearReport.COMPANY_ID == baseInfo[0]).all()
            #
            base_info = queryResult2Json(baseInfo)
            branch_info = queryResult2Json(branchInfo)
            abnormal_info = queryResult2Json(abnormalInfo)
            illegal_info = queryResult2Json(illegalInfo)
            bid_info = queryResult2Json(bidInfo)
            check_info = queryResult2Json(checkInfo)
            change_info = queryResult2Json(changeInfo)
            mortgage_info = queryResult2Json(mortgageInfo)
            equity_ple_info = queryResult2Json(equityPleInfo)
            copy_soft_info = queryResult2Json(copySoftInfo)
            copy_work_info = queryResult2Json(copyWorkInfo)
            court_auto_info = queryResult2Json(courtAutoInfo)

            court_noti_info = queryResult2Json(courtNotiInfo)
            dishonest_info = queryResult2Json(dishonestInfo)
            executed_info = queryResult2Json(executedInfo)
            website_info = queryResult2Json(websiteInfo)
            year_report_info = queryResult2Json(yearReportInfo)
            tm_info = queryResult2Json(tmInfo)
            shareholder_info = queryResult2Json(shareholderInfo)
            punishment_info = queryResult2Json(punishmentInfo)
            product_info = queryResult2Json(productInfo)
            patent_info =queryResult2Json(patentInfo)
            owing_info = queryResult2Json(owingInfo)
            taxcred_info =queryResult2Json(taxcredInfo)
            member_info = queryResult2Json(memberInfo)
            licence_info = queryResult2Json(licenceInfo)
            lawsuit_info = queryResult2Json(lawsuitInfo)
            qualify_info = queryResult2Json(qualifyInfo)
            invest_info = queryResult2Json(investInfo)
            imexport_info = queryResult2Json(imExportInfo)
            judsale_info = queryResult2Json(judsaleInfo)
            online_shop_info = queryResult2Json(onlineShopInfo)

            json_result["COMPANY_BASIC_INFO"] = json.loads(base_info)
            json_result["COMPANY_BRANCH_INFO"] = json.loads(branch_info)
            json_result["COMPANY_MANAGE_ABNORMAL_INFO"] = json.loads(abnormal_info)
            json_result["COMPANY_ILLEGAL_INFO"] = json.loads(illegal_info)
            json_result["COMPANY_BID_INFO"] = json.loads(bid_info)
            json_result["COMPANY_CHECK_INFO"] = json.loads(check_info)
            json_result["COMPANY_CHANGE_MESSAGE_INFO"] = json.loads(change_info)
            json_result["COMPANY_CHATTEL_MORTGAGE_INFO"] = json.loads(mortgage_info)
            json_result["COMPANY_EQUITY_INFO"] = json.loads(equity_ple_info)
            json_result["COMPANY_SOFTWARE_COPYRIGHT_INFO"] = json.loads(copy_soft_info)
            json_result["COMPANY_WORKS_COPYRIGHT_INFO"] = json.loads(copy_work_info)
            json_result["COMPANY_COURT_ANNOUNCEMENT_INFO"] = json.loads(court_auto_info)
            json_result["COMPANY_COURT_PUBLIC_INFO"] = json.loads(court_noti_info)
            json_result["COMPANY_POOR_CREDIT_PERSON_INFO"] = json.loads(dishonest_info)
            json_result["COMPANY_EXECUTED_PERSON_INFO"] = json.loads(executed_info)
            json_result["COMPANY_DOMAIN_NAME_INFO"] = json.loads(website_info)
            json_result["COMPANY_YEAR_REPORT_INFO"] = json.loads(year_report_info)
            json_result["COMPANY_TRADEMARK_INFO"] = json.loads(tm_info)
            json_result["COMPANY_SHAREHOLDER_INFO"] = json.loads(shareholder_info)
            json_result["COMPANY_OFFICE_PUNISH_INFO"] = json.loads(punishment_info)
            json_result["COMPANY_GOODS_INFO"] = json.loads(product_info)
            json_result["COMPANY_PATENT_INFO"] = json.loads(patent_info)
            json_result["COMPANY_TAX_ARREARS_INFO"] = json.loads(owing_info)
            json_result["COMPANY_TAX_GRADE_INFO"] = json.loads(taxcred_info)
            json_result["COMPANY_MAIN_PERSONNEL_INFO"] = json.loads(member_info)
            json_result["COMPANY_ADMINISTRATIVE_LICENSING_INFO"] = json.loads(licence_info)
            json_result["COMPANY_LEGAL_PROCEEDINGS_INFO"] = json.loads(lawsuit_info)
            json_result["COMPANY_QUALIFICATIONS_CERTIFICATE_INFO"] = json.loads(qualify_info)
            json_result["COMPANY_OUT_INVEST_INFO"] = json.loads(invest_info)
            json_result["COMPANY_IMPORT_EXPORT_INFO"] = json.loads(imexport_info)
            json_result["COMPANY_AUCTION_MESSAGE_INFO"] = json.loads(judsale_info)
            json_result["O_PAY_INFO_ID"] = pay_id
            json_result["COMPANY_MAIN_INFO"] = []
            json_result["COMPANY_EXTRA_INFO"] = []
            json_result["COMPANY_BAD_INFO"] = []
            json_result["COMPANY_ONLINE_SHOP_INFO"] = json.loads(online_shop_info)
            json_result["COMPANY_QUALIFICATIONS_INFO"] = []
            json_result["COMPANY_AUTHENTICATION_INFO"] = []
            json_result["COMPANY_BOND_INFO"] = []
            json_result["COMPANY_GOOD_INFO"] = []
            json_result["COMPANY_COURT_SENTENCE_INFO"] = []
            json_result["COMPANY_CONTACT_INFO"] = []
            json_result["COMPANY_ENVIRONMENT_PUNISH_INFO"] = []
            json_result["COMPANY_PURCHASE_LAND_INFO"] = []
            json_result["COMPANY_PUBLIC_RECORD_INFO"] = []

            json_result = json.dumps(json_result, ensure_ascii=False)
            db_service.session.commit()
            db_service.session.close()
            db_service.close_engine()
            print(json_result)
            return json_result
        except:
            self.logger.logger.error(traceback.format_exc())
            return None





if __name__ == '__main__':
    # key = {'company': '福建华威商贸物流有限公司', 'scode': None}
    key = {"COMPANY_USCC": "9135020073786628XK", "COMPANY_NAME": "四三九九网络股份有限公司"}
    # key = {'company': '福建龙泰时代建设工程有限公司', 'scode': None}
    g = DAF(key)
    kk = g.getDataFromDbStore('fc840651435e11eba36690b11c3cc21d')

    # key = {'company': '福建省理想建筑工程有限公司', 'scode': None}
    # g = DAF(key)
    print(kk)

    # g.deal_each_data()
    # key = {'company': '福建三石建设工程有限公司', 'scode': None}
    # g = DAF(key)
    # g.deal_each_data()
    # print(os.path.abspath(os.path.dirname(os.getcwd())) + "/SQLAlchemy/dbname.conf")
