# -*- coding: utf-8 -*-
# @Time : 2021/4/24 20:02
# @Author :  Meow_J

"""
专从列表中遍历取出数据
"""
import hashlib
from datetime import datetime
from CH_DB.dataBaseOperation import DBOperation

DB = DBOperation()

IMP_STATE = '10A'
CHANGE_STATE = '10A'

def getrandominspection(dataList,cid,batchId):
    """
    抽查检查
    :param dataList:
    :return:
    """
    for i in dataList:
        inspectionAuthority = i.get("inspectionAuthority")#检查机构
        inspectionResult = i.get("inspectionResult")#结果
        inspectionType = i.get("inspectionType")#类型
        inspectionDate = i.get("inspectionDate")#日期

def getfoodquality(dataList,cid,batchId):
    """
    食品抽查检查
    :param dataList:
    :return:
    """
    for i in dataList:
        # 还有部分内容未提取
        productName = i.get("productName")#抽查产品
        notificationDate = i.get("notificationDate")#通报时间
        notificationNum = i.get("notificationNum")#通报文号
        result = i.get("result")#抽查结果

def getchattelmortgage(dataList,cid,batchId):
    """
    动产抵押 (数据较少，如需详情根据detailUrl取)
    :param dataList:
    :return:
    """
    nowDate = datetime.now()
    for i in dataList:
        detailUrl = i.get("detailUrl")#详情Url
        issueDate = i.get("issueDate") #登记日期
        guaranteeClaimAmount = i.get("guaranteeClaimAmount") #被担保债权数额
        issueAuthority = i.get("issueAuthority") #登记机关
        guaranteeClaimStatusCode = i.get("guaranteeClaimStatusCode") #状态
        MD5VALUE = hashlib.md5((issueAuthority + guaranteeClaimStatusCode).encode(encoding='utf-8')).hexdigest()
        CHANGE_STATE_DT = nowDate
        dataReady = [
            cid,issueDate,guaranteeClaimAmount,guaranteeClaimStatusCode,
            MD5VALUE,batchId,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT
        ]
        DB.insertChattelmortgage(args=dataReady)

def getstockFreeze(dataList,cid,batchId):
    """
    股权冻结
    :param dataList:
    :return:
    """
    for i in dataList:
        beExecutedPerson = i.get("beExecutedPerson")#被执行人
        equalityAmount = i.get("equalityAmount")#股权数额
        notificationNumber = i.get("notificationNumber")#执行通知文书号
        type = i.get("type")#类型
        status = i.get("status")#状态

def getenvpunishment(dataList,cid,batchId):
    """
    环境处罚
    :param dataList:
    :return:
    """
    for i in dataList:
        documentNo = i.get("documentNo")#决定文书号
        illegalType = i.get("illegalType")#违法类型
        punishmentType = i.get("punishmentType")#处罚类别
        punishmentDept = i.get("punishmentDept")#处罚单位
        punishmentDate = i.get("punishmentDate")#处罚日期
        punishmentBasis = i.get("punishmentBasis")#处罚依据
        punishmentResult = i.get("punishmentResult")#处罚结果

def getterminationcase(dataList,cid,batchId):
    """
    终本案件
    :param dataList:
    :return:
    """
    for i in dataList:
        filingDate = i.get("filingDate")#立案日期
        caseNoTerminal = i.get("caseNoTerminal")#案号
        amount = i.get("amount")#执行标的
        court = i.get("court")#执行法院
        terminateDate = i.get("terminateDate")#终本日期
        detailUrl = i.get("detailUrl")#Url

def gettaxviolation(dataList,cid,batchId):
    """
    税务违法
    :param dataList:
    :return:
    """
    for i in dataList:
        name = i.get("name")#纳税人名称
        regCode = i.get("regCode")#注册号
        penaltyType = i.get("penaltyType")#案件性质
        reportDate = i.get("reportDate")#案件上报日期
        detailUrl = i.get("detailUrl")#Url

def getuntax(dataList,cid,batchId):
    """
    税务非正常
    :param dataList:
    :return:
    """
    nowDate = datetime.now()
    for i in dataList:
        taxNum = i.get("taxNum")#纳税人识别号
        name = i.get("name")#公司名
        area = i.get("area")#地址
        overdueAmount = i.get("overdueAmount")#欠税金额
        judgeDate = i.get("judgeDate")#认定日期
        overdueType = i.get("overdueType")#欠税税务种类
        state = i.get("state")#纳税人状态
        MD5VALUE = hashlib.md5((taxNum + overdueAmount).encode(encoding='utf-8')).hexdigest()
        CHANGE_STATE_DT = nowDate
        dataReady = [
            cid,taxNum,overdueAmount,overdueType,judgeDate,
            MD5VALUE,batchId,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT
        ]
        DB.insertUntax(dataReady)

def getrestrictedConsumer(dataList,cid,batchId):
    """
    限制高消费 (被执行人一种 类型10XZ)
    :param dataList:
    :return:
    """
    nowDate = datetime.now()
    for i in dataList:
        releaseDate = i.get("releaseDate")#发布日期
        personName = i.get("personName")#被限制人姓名
        companyName = i.get("companyName")#关联公司名
        execComapnyName = i.get("execComapnyName")#申请执行人
        court = i.get("court")#执行法院
        doc_type = "10XZ"
        MD5VALUE = hashlib.md5((releaseDate + personName).encode(encoding='utf-8')).hexdigest()
        CHANGE_STATE_DT = nowDate
        dataReady = [
            cid,releaseDate,personName,court,doc_type,
            MD5VALUE,batchId,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT
        ]
        DB.insertRestrictedConsumer(args=dataReady)

def getabnormal(dataList,cid,batchId):
    """
    经营异常
    :param dataList:
    :return:
    """
    nowDate = datetime.now()
    for i in dataList:
        enterDate = i.get("enterDate")#列入日期
        enterReason = i.get("enterReason")#列入原因
        leaveDate = i.get("leaveDate")#移除日期
        leaveReason = i.get("leaveReason")#移除原因
        authority = i.get("authority")#列入决定机关
        leaveAuthority = i.get("leaveAuthority")#移出决定机关
        MD5VALUE = hashlib.md5((enterDate + enterReason).encode(encoding='utf-8')).hexdigest()
        CHANGE_STATE_DT = nowDate
        dataReady = [
            cid,enterDate,enterReason,leaveDate,leaveReason,authority,leaveAuthority,
            MD5VALUE,batchId,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT
        ]
        DB.insertAbnormal(args=dataReady)

def getdiscredit(dataList,cid,batchId):
    """
    失信被执行人
    :param dataList:
    :return:
    """
    nowDate = datetime.now()
    for i in dataList:
        publishDate = i.get("publishDate")#发布日期
        verdictDate = i.get("verdictDate")#立案日期
        verdictCaseNumber = i.get("verdictCaseNumber")#案号
        implementCourtName = i.get("implementCourtName")#执行法院
        performStatus = i.get("performStatus")#履行情况
        implementCaseNumber = i.get("implementCaseNumber")#执行依据文号
        MD5VALUE = hashlib.md5((verdictCaseNumber + performStatus).encode(encoding='utf-8')).hexdigest()
        CHANGE_STATE_DT = nowDate
        dataReady = [
            cid, publishDate, verdictDate, verdictCaseNumber, implementCourtName, performStatus, implementCaseNumber,
            MD5VALUE,batchId,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT
        ]
        DB.insertDiscredit(args=dataReady)

def getillegal(dataList,cid,batchId):
    """
    严重违法
    :param dataList:
    :return:
    """
    nowDate = datetime.now()
    for i in dataList:
        enterDate = i.get("enterDate")#列入日期
        enterReason = i.get("enterReason")#列入原因
        authority = i.get("authority")#决定机关
        leaveDate = i.get("leaveDate")#移出日期
        leaveReason = i.get("leaveReason")#移出原因
        leaveAuthority = i.get("leaveAuthority")#移出机关
        MD5VALUE = hashlib.md5((enterDate + authority).encode(encoding='utf-8')).hexdigest()
        CHANGE_STATE_DT = nowDate
        dataReady = [
            cid,enterDate,enterReason,authority,leaveDate,leaveReason,leaveAuthority,
            MD5VALUE,batchId,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT
        ]
        DB.insertIllegal(args=dataReady)

def getlawWenshu(dataList,cid,batchId):
    """
    获取裁判文书中的信息
    :param dataList:
    :return:
    """
    nowDate = datetime.now()
    for i in dataList:
        type = i.get("type")  # 案由
        verdictDate = i.get("verdictDate")  # 日期
        caseNo = i.get("caseNo")  # 案号
        role = i.get("role")  # 角色
        wenshuName = i.get("wenshuName")  # 文书名称
        wenshuId = i.get("wenshuId")  # 文书ID
        detailUrl = i.get("detailUrl")  # 文书详情URL
        MD5VALUE = hashlib.md5((caseNo + wenshuName).encode(encoding='utf-8')).hexdigest()
        CHANGE_STATE_DT = nowDate
        dataReady = [cid,type,verdictDate,caseNo,wenshuName,MD5VALUE,batchId,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT]
        DB.insertLawWenshu(dataReady)

def getpenalties(dataList,cid,batchId):
    """
    行政处罚
    :param dataList:
    :return:
    """
    nowDate = datetime.now()
    for i in dataList:
        penaltiesNumber = i.get("penaltiesNumber")  # 决定文书号
        # penaltiesName = i.get("penaltiesName")  # 决定文书名称
        # penaltiesReason = i.get("penaltiesReason")  # 事由
        penaltiesType = i.get("penaltiesType")  # 处罚类型
        penalties = i.get("penalties")  # 处罚单位
        penaltiesDate = i.get("penaltiesDate")  # 处罚日期
        detailUrl = i.get("detailUrl")  # 具体情况Url
        MD5VALUE = hashlib.md5((penaltiesNumber + penaltiesType).encode(encoding='utf-8')).hexdigest()
        CHANGE_STATE_DT = nowDate
        dataReady = [cid,penaltiesNumber,penaltiesType,penalties,penaltiesDate,MD5VALUE,batchId,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT]
        DB.insertPenalties(args=dataReady)

def getopennotice(dataList,cid,batchId):
    """
    开庭公告
    :param dataList:
    :return:
    """
    nowDate = datetime.now()
    for i in dataList:
        hearingDate = i.get("hearingDate") #开庭日期
        caseNo = i.get("caseNo") #案号
        caseReason = i.get("caseReason") #案由
        content = i.get("content") #内容
        region = i.get("region") #地区
        court = i.get("court") #法院
        tribunal = i.get("tribunal") #法庭
        department = i.get("department") #承办部门
        plaintiff = ""
        defendant = ""
        MD5VALUE = hashlib.md5((caseNo + hearingDate).encode(encoding='utf-8')).hexdigest()
        CHANGE_STATE_DT = nowDate
        plaintifflist = i.get("plaintifflist") #原告
        for k in plaintifflist:
            if k != "-":
                plaintiff = plaintiff + k + " ; "
        defendantlist = i.get("defendantlist") #被告
        for j in defendantlist:
            if j != "-":
                defendant = defendant + j + " ; "
        dataReady = [cid,hearingDate,caseNo,caseReason,court,tribunal,plaintifflist,defendant,MD5VALUE,batchId,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT]
        DB.insertOpennotice(args=dataReady)

def getjudicialauction(dataList,cid,batchId):
    """
    司法拍卖(数据库中没有合适表)
    :param dataList:
    :return:
    """
    for i in dataList:
        date = i.get("date") #拍卖日期  （String类型  例：2020年12月11日10时至2020年12月12日10时止）
        name = i.get("name") #拍卖名称
        description = i.get("description") #拍卖内容描述
        startPrice = i.get("startPrice") #起拍价
        estPrice = i.get("estPrice") #评估价
        court = i.get("court") #法院
        detailUrl = i.get("detailUrl") #详情Url
        result = i.get("result") #成交结果
        dataReady = []
        DB.insertJudicialauction(args=dataReady)

def getCourtNoticeData(dataList,cid,batchId):
    """
    法院公告
    :param dataList:
    :return:
    """
    nowDate = datetime.now()
    for i in dataList:
        date = i.get("date") #公告日期
        type = i.get("type") #公告类型
        cause = i.get("cause") #案由
        court = i.get("court") #受理法院
        detailUrl = i.get("detailUrl") #详情Url
        MD5VALUE = hashlib.md5((cause + court).encode(encoding='utf-8')).hexdigest()
        CHANGE_STATE_DT = nowDate,
        people = ""
        peopleList = i.get("people")
        for k in peopleList:
            if k.get("name") != '-':
                people = people+k.get("name")+" ; "
        dataReady = [cid,date,type,court,people,MD5VALUE,batchId,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT]
        DB.insertCourtNotice(args=dataReady)

def getfilinginfo(dataList,cid,batchId):
    """
    立案信息
    :param dataList:
    :return:
    """
    nowDate = datetime.now()
    for i in dataList:
        date = i.get("date") #立案时间
        caseNumber = i.get("caseNumber") #案号
        court = i.get("court") #受理法院
        plaintiff = ""
        defendant = ""
        plaintiffList = i.get("plaintiff")
        for k in plaintiffList:
            plaintiff = plaintiff + k.get("name") +" ; "
        defendantList = i.get("defendant")
        for j in defendantList:
            defendant = defendant + j.get("name") + " ; "
        MD5VALUE = hashlib.md5((caseNumber + date).encode(encoding='utf-8')).hexdigest()
        CHANGE_STATE_DT = nowDate
        dataReady = [
            cid,date,caseNumber,court,plaintiff,defendant,
            MD5VALUE,batchId,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT
        ]
        DB.insertFilinginfo(args=dataReady)

def getexecutedPerson(dataList,cid,batchId):
    """
    被执行人
    :param dataList:
    :return:
    """
    for i in dataList:
        date = i.get("date")  #立案时间
        executeNumber = i.get("executeNumber")  #案号
        subjectMatter = i.get("subjectMatter")  #执行标的
        executeName = i.get("executeName")  #被执行人
        court = i.get("court")  #执行法院
        detailUrl = i.get("detailUrl")  #详情Url

def getequitypledge(dataList,cid,batchId):
    """
    股权出质
    :param dataList:
    :return:
    """
    nowDate = datetime.now()
    for i in dataList:
        issueDate = i.get("issueDate") #登记日期
        licenseNumber = i.get("licenseNumber") #登记编号
        equalityPledgor = i.get("equalityPledgor") #出质人
        equalityPawnee = i.get("equalityPawnee") #质权人
        equalityPledgeStatusCode = i.get("equalityPledgeStatusCode") #状态
        detailUrl = i.get("detailUrl")  #详情Url
        MD5VALUE = hashlib.md5((licenseNumber + equalityPledgor).encode(encoding='utf-8')).hexdigest()
        CHANGE_STATE_DT = nowDate
        dataReady = [
            cid,issueDate,licenseNumber,equalityPledgor,equalityPawnee,equalityPledgeStatusCode,
            MD5VALUE,batchId,IMP_STATE,CHANGE_STATE,CHANGE_STATE_DT
        ]
        DB.insertEquitypledge(args=dataReady)

def getcopyright(dataList,cid,batchId):
    """
    软件著作权
    :param dataList:
    :return:
    """
    for i in dataList:
        softwareName = i.get("softwareName") #软件名称
        shortName = i.get("shortName") #软件简介
        batchNum = i.get("batchNum") #版本号
        softwareType = i.get("softwareType") #软件著作分类
        typeCode = i.get("typeCode") #行业分类
        regDate = i.get("regDate") #登记日期
        detailUrl = i.get("detailUrl") #详情Url
        regNo = i.get("detail").get("regNo") #注册号（i.get("detail")为一个字典）

def geticpinfo(dataList,cid,batchId):
    """
    网站备案
    :param dataList:
    :return:
    """
    for i in dataList:
        siteName = i.get("siteName") #网站名称
        icpNo = i.get("icpNo") #备案号
        homeSite = "" #网址
        domain = "" #域名
        homeSiteList = i.get("homeSite")
        if len(homeSiteList) != 0:
            for k in homeSiteList:
                if k != "" and k!="-":
                    homeSite = homeSite + k + " ; "
        domainList = i.get("domain")
        if len(domainList) != 0:
            for j in domainList:
                if j != "" and j!="-":
                    domain = domain + j + " ; "

def getpatent(dataList,cid,batchId):
    """
    专利信息
    :param dataList:
    :return:
    """
    for i in dataList:
        patentName = i.get("patentName")#专利名称
        publicationNumber = i.get("publicationNumber")#公布号
        patentType = i.get("patentType")#专利类型
        publicationDate = i.get("publicationDate")#公布日期
        detailUrl = i.get("detailUrl")#详情Url

def getmark(dataList,cid,batchId):
    """
    商标信息
    :param dataList:
    :return:
    """
    for i in dataList:
        markLogo = i.get("markLogo")#商标Logo Url链接
        markName = i.get("markName")#商标名称
        markRegNo = i.get("markRegNo")#注册号
        applyDate = i.get("applyDate")#申请时间
        markType = i.get("markType")#国际分类
        detailUrl = i.get("detailUrl")#详情Url

def getworkright(dataList,cid,batchId):
    """
    作品著作权
    :param dataList:
    :return:
    """
    for i in dataList:
        registrationNo = i.get("registrationNo")#登记号
        type = i.get("type")#作品类别
        name = i.get("name")#作品名称
        completionDate = i.get("completionDate")#创作完成日期
        registrationDate = i.get("registrationDate")#登记日期
        publicationDate = i.get("publicationDate")#首次发表日期

def getbrandProject(dataList,cid,batchId):
    """
    企业品牌项目
    :param dataList:
    :return:
    """
    for i in dataList:
        name = i.get("name")#项目名称
        logo = i.get("logo")#商标url
        round = i.get("round")#融资轮次
        startYear = i.get("startYear")#开始时间
        district = i.get("district")#所属地
        regCapital = i.get("regCapital")#资本
        brief = i.get("brief")#项目简介
        detailUrl = i.get("detailUrl")#详情Url

def getinvestorlist(dataList,cid,batchId):
    """
    投资机构
    :param dataList:
    :return:
    """
    for i in dataList:
        investorName = i.get("investorName")#投资机构
        startYear = i.get("startYear")#成立年份
        land = i.get("land")#所属地
        brief = i.get("brief")#简介

def getprojectSimilarsInfo(dataList,cid,batchId):
    """
    竞品信息
    :param dataList:
    :return:
    """
    for i in dataList:
        projectName = i.get("projectName") #竞品名称
        projectLogo = i.get("projectLogo") #logoUrl
        projectLatestRound = i.get("projectLatestRound") #最新融资轮次
        projectStartDate = i.get("projectStartDate") #竞品成立时间
        projectAddress = i.get("projectAddress") #所属地
        projectBrief = i.get("projectBrief") #项目简介
        similarPrincipalName = i.get("similarPrincipalName") #所属企业

def getCompPersonList(dataList,cid,batchId):
    """
    核心成员
    :param dataList:
    :return:
    """
    for i in dataList:
        personName = i.get("personName") #名称
        positionTitle = i.get("positionTitle") #职位
        personIncumbency = i.get("personIncumbency") #在职状态
        personBrief = i.get("personBrief") #人员简介

def projectFinance(dataList,cid,batchId):
    """
    融资信息
    :param dataList:
    :return:
    """
    for i in dataList:
        financeDate = i.get("financeDate")#发布日期
        financeRound = i.get("financeRound")#融资轮次
        financeAmount = i.get("financeAmount")#融资金额
        financeInvestor = ""#投资方
        financeInvestorList = i.get("financeInvestor")
        if len(financeInvestorList) != 0:
            for k in financeInvestorList:
                financeInvestor = financeInvestor + k +" ; "

def getlicense(dataList,cid,batchId):
    """
    行政许可
    :param dataList:
    :return:
    """
    for i in dataList:
        licenseNumber = i.get("licenseNumber") #许可号
        licenseName = i.get("licenseName") #许可名称
        licenseContent = i.get("licenseContent") #许可内容
        validityFrom = i.get("validityFrom") #有效期自
        validityTo = i.get("validityTo") #有效期至
        issueAuthority = i.get("issueAuthority") #许可机关

def getimportexport(dataList,cid,batchId):
    """
    进出口信用
    :param dataList:
    :return:
    """
    for i in dataList:
        regDate = i.get("regDate") #注册日期
        customsNum = i.get("customsNum") #海关编码
        businessCategory = i.get("businessCategory") #经营类别
        customsReg = i.get("customsReg") #注册海关
        detailUrl = i.get("detailUrl") #详情Url

def getquality(dataList,cid,batchId):
    """
    质量监督检查
    :param dataList:
    :return:
    """
    for i in dataList:
        productName = i.get("productName")#抽查产品
        samlingBatch = i.get("samlingBatch")#质量监督抽查批次
        samplingResult = i.get("detail").get("samplingResult")#结果
        agency = i.get("detail").get("agency")#检查机构
        productDate = i.get("detail").get("productDate")#生产日期/批号
        manufacturer = i.get("detail").get("manufacturer")#生产企业

def getdoublecheckup(dataList,cid,batchId):
    """
    双随机检查
    :param dataList:
    :return:
    """
    for i in dataList:
        raninsPlanId = i.get("raninsPlanId") #计划编号
        raninsPlaneName = i.get("raninsPlaneName") #计划名称
        raninsTypeName = i.get("raninsTypeName") #检查类型
        insauth = i.get("insauth") #检察机关
        insDate = i.get("insDate") #检查日期
        detailUrl = i.get("detailUrl") #详情Url

def gettenderbidding(dataList,cid,batchId):
    """
    招投标
    :param dataList:
    :return:
    """
    for i in dataList:
        title = i.get("title")#标题
        publishDate = i.get("publishDate")#发布日期
        district = i.get("district")#地域
        detailUrl = i.get("detailUrl")#详情Url
        tender = ""#招标公司
        winner = ""#中标公司
        tenderList = i.get("tender")
        for k in tenderList:
            if isinstance(k,dict):
                tender = tender + k.get("name") + " ; "
        winnerList = i.get("winnerList")
        for j in winnerList:
            if isinstance(j,dict):
                winner = winner + j.get("name") + " ; "

