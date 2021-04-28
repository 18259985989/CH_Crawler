# -*- coding: utf-8 -*-
# @Time : 2021/4/17 10:23
# @Author :  Meow_J

import hashlib
from datetime import datetime
from CH_DB.dataBaseOperation import DBOperation

DB = DBOperation()


IMP_STATE = '10A'
CHANGE_STATE = '10A'

"""
爱企查中基本数据清洗并入库
"""

def getBaseData(Json,batchId):
    """
    从Json中获取BaseInfo
    :param Json:请求得到数据源
    :return:
    """
    data = Json.get("data")
    basicData = data.get("basicData") #基本信息字典
    entName = basicData.get("entName") #公司名
    unifiedCode = basicData.get("unifiedCode") #统一社会信用代码
    openStatus = basicData.get("openStatus") #经营状态
    entType = basicData.get("entType") #企业类型
    regNo = basicData.get("licenseNumber") #工商注册号
    orgNo = basicData.get("orgNo") #组织机构代码
    # taxNo = basicData.get("taxNo") #税号
    scope = basicData.get("scope") #经营范围
    regAddr = basicData.get("regAddr") #公司地址
    legalPerson = basicData.get("legalPerson") #法人代表
    startDate = datetime.strptime(basicData.get("startDate"),"%Y-%m-%d") #成立时间
    annualDate = datetime.strptime(basicData.get("annualDate"),"%Y-%m-%d") #核准日期
    regCapital = basicData.get("regCapital") #注册资本
    industry = basicData.get("industry") #所属行业
    telephone = basicData.get("telephone") #公司电话
    # district = basicData.get("district") #行政区划
    authority = basicData.get("authority") #登记机关
    describe = basicData.get("describe") #企业简介
    email = basicData.get("email") #企业邮箱
    nowDate = datetime.now()
    CHANGE_STATE_DT = nowDate
    source_update_time = nowDate  # 更新时间
    local_update_time = nowDate
    MD5VALUE = hashlib.md5((entName + orgNo).encode(encoding='utf-8')).hexdigest()
    BATCH_ID = batchId
    opFrom = ""
    opTo = ""
    openTime = basicData.get("openTime").split("至")  # 营业期限
    if len(openTime) ==1:
        opFrom = datetime.strptime("9999-12-31","%Y-%m-%d")
        opTo = datetime.strptime("9999-12-31","%Y-%m-%d")
    elif len(openTime) == 2:
        try:
            opFrom = datetime.strptime(openTime[0].strip(),"%Y-%m-%d")
        except:
            opFrom = datetime.strptime("9999-12-31","%Y-%m-%d")
        try:
            opTo = datetime.strptime(openTime[1].strip(),"%Y-%m-%d")
        except:
            opTo = datetime.strptime("9999-12-31","%Y-%m-%d")
    dataReady = [entName,unifiedCode,openStatus,entType,regNo,orgNo,scope,regAddr,legalPerson,startDate,annualDate,
                 regCapital,industry,telephone,authority,describe,source_update_time,local_update_time,
                 IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT,BATCH_ID,MD5VALUE,email,opFrom,opTo]
    DB.insertBaseInfo(dataReady)

def ChangeRecord(Json,batchId,cid):
    """
    变更信息
    :param Json:
    :return:
    """
    nowDate =datetime.now()
    try:
        data = Json.get("data")
    except:
        data = datetime.strptime("9999-12-31", "%Y-%m-%d")
    changeRecordData = data.get("changeRecordData")
    totalNum = changeRecordData.get("totalNum") #可根据数量进行判断是否大于10
    dataList = changeRecordData.get("list") #数据列表
    for i in dataList:
        date = datetime.strptime(i.get("date"),"%Y-%m-%d") #日期 date类型
        fieldName = i.get("fieldName") #变更项
        oldValue = i.get("oldValue") #旧值
        newValue = i.get("newValue") #新值
        CHANGE_STATE_DT = nowDate,
        MD5VALUE = hashlib.md5((fieldName + oldValue).encode(encoding='utf-8')).hexdigest()
        dataReady = [cid,fieldName,oldValue,newValue,date,MD5VALUE,batchId,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT]
        DB.insertChangeInfo(args=dataReady)

def Shareholders(Json,batchId,cid):
    """
    股东信息
    :param Json:
    :return:
    """
    data = Json.get("data")
    nowDate = datetime.now()
    shareholdersData = data.get("shareholdersData")
    totalNum = shareholdersData.get("totalNum") #可根据数量进行判断是否大于10
    dataList = shareholdersData.get("list") #数据列表
    for i in dataList:
        name = i.get("name") #姓名
        subMoney = i.get("subMoney") #出资额
        subRate = i.get("subRate") #占股比例
        paidinMoney = i.get("paidinMoney") #实际出资额
        MD5VALUE = hashlib.md5((name + subRate).encode(encoding='utf-8')).hexdigest()
        CHANGE_STATE_DT = nowDate,
        dataReady = [cid,name,subMoney,subRate,paidinMoney,MD5VALUE,batchId,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT]
        DB.insertShareholders(dataReady)

def Directors(Json,batchId,cid):
    """
    主要人员
    :param Json:
    :return:
    """
    data = Json.get("data")
    directorsData = data.get("directorsData")
    nowDate = datetime.now()
    totalNum = directorsData.get("totalNum")  # 可根据数量进行判断是否大于10
    dataList = directorsData.get("list")  # 数据列表
    for i in dataList:
        name = i.get("name")  # 姓名
        gender = i.get("gender")  # 性别
        title = i.get("title")  # 职位
        compNum = i.get("compNum")  # 关联公司数
        MD5VALUE = hashlib.md5((name + title).encode(encoding='utf-8')).hexdigest()
        CHANGE_STATE_DT = nowDate,
        dataReady = [cid,name,title,MD5VALUE,batchId,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT]
        DB.insertDirectors(args=dataReady)

def Branch(Json,batchId,cid):
    """
    分支机构信息
    :param Json:
    :return:
    """
    data = Json.get("data")
    branchsData = data.get("branchsData")
    nowDate = datetime.now()
    totalNum = branchsData.get("totalNum") #可根据数量进行判断是否大于10
    dataList = branchsData.get("list") #数据列表
    print("分支机构信息：{}".format(dataList))
    for i in dataList:
        entName = i.get("entName") #公司名
        legalPerson = i.get("legalPerson") #法人代表
        personId = i.get("personId") #人员在网站内Id 作用未知
        pid = i.get("pid") #该公司在网站内的Pid
        startDate = i.get("startDate") #成立时间
        openStatus = i.get("openStatus") #状态
        regCapital = i.get("regCapital") #注册资本
        MD5VALUE = hashlib.md5((entName + regCapital).encode(encoding='utf-8')).hexdigest()
        CHANGE_STATE_DT = nowDate,
        dataReady = [
            cid,entName,legalPerson,startDate,openStatus,MD5VALUE,batchId,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT
        ]
        DB.insertBranch(args=dataReady)


def Invest(Json,batchId,cid):
    """
    对外投资信息
    :param Json:
    :return:
    """
    data = Json.get("data")
    nowDate = datetime.now()
    investRecordData = data.get("investRecordData")
    totalNum = investRecordData.get("totalNum")  # 可根据数量进行判断是否大于10
    dataList = investRecordData.get("list")  # 数据列表
    for i in dataList:
        entName = i.get("entName")#被投资企业
        legalPerson = i.get("legalPerson")#法人
        try:
            startDate = datetime.strptime(i.get("startDate"), "%Y-%m-%d")#成立时间
        except:
            startDate = datetime.strptime("9999-12-31", "%Y-%m-%d")
        regCapital = i.get("regCapital")#认缴金额
        regRate = i.get("regRate")#投资占比
        openStatus = i.get("openStatus")#状态
        MD5VALUE = hashlib.md5((entName + regCapital).encode(encoding='utf-8')).hexdigest()
        CHANGE_STATE_DT = nowDate,
        dataReady = [cid,entName,legalPerson,startDate,regCapital,regRate,openStatus,MD5VALUE,batchId,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT]
        DB.insertInvest(dataReady)




def Hold(Json):
    """
    控股企业
    :param Json:
    :return:
    """
    data = Json.get("data")
    holdsData = data.get("holdsData")
    totalNum = holdsData.get("totalNum")  # 可根据数量进行判断是否大于10
    dataList = holdsData.get("list")  # 数据列表
    for i in dataList:
        pass

