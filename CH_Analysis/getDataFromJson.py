# -*- coding: utf-8 -*-
# @Time : 2021/4/24 20:02
# @Author :  Meow_J

"""
专从列表中遍历取出数据
"""

from CH_DB.dataBaseOperation import DBOperation

DB = DBOperation()

def getlawWenshu(dataList):
    """
    获取裁判文书中的信息
    :param Json:
    :return:
    """
    for i in dataList:
        type = i.get("type")  # 案由
        verdictDate = i.get("verdictDate")  # 日期
        caseNo = i.get("caseNo")  # 案号
        role = i.get("role")  # 角色
        wenshuName = i.get("wenshuName")  # 文书名称
        wenshuId = i.get("wenshuId")  # 文书ID
        detailUrl = i.get("detailUrl")  # 文书详情URL
        dataReady = []
        DB.insertLawWenshu(dataReady)

def getpenalties(dataList):
    """
    行政处罚
    :param dataList:
    :return:
    """
    for i in dataList:
        penaltiesNumber = i.get("penaltiesNumber")  # 决定文书号
        penaltiesName = i.get("penaltiesName")  # 决定文书名称
        penaltiesReason = i.get("penaltiesReason")  # 事由
        penaltiesType = i.get("penaltiesType")  # 处罚类型
        penalties = i.get("penalties")  # 处罚单位
        penaltiesDate = i.get("penaltiesDate")  # 处罚日期
        detailUrl = i.get("detailUrl")  # 具体情况Url

def getopennotice(dataList):
    """
    开庭公告
    :param dataList:
    :return:
    """
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
        plaintifflist = i.get("plaintifflist") #原告
        for k in plaintifflist:
            if k != "-":
                plaintiff = plaintiff + k + " ; "
        defendantlist = i.get("defendantlist") #被告
        for j in defendantlist:
            if j != "-":
                defendant = defendant + j + " ; "

def getjudicialauction(dataList):
    """
    司法拍卖
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

def getCourtNoticeData(dataList):
    """
    法院公告
    :param dataList:
    :return:
    """
    for i in dataList:
        date = i.get("date") #公告日期
        type = i.get("type") #公告类型
        cause = i.get("cause") #案由
        court = i.get("court") #受理法院
        detailUrl = i.get("detailUrl") #详情Url
        people = ""
        peopleList = i.get("people")
        for k in peopleList:
            if k.get("name") != '-':
                people = people+k.get("name")+" ; "

def getfilinginfo(dataList):
    """
    立案信息
    :param dataList:
    :return:
    """
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

def getexecutedPerson(dataList):
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

def getequitypledge(dataList):
    """
    股权出质
    :param dataList:
    :return:
    """
    for i in dataList:
        issueDate = i.get("issueDate") #登记日期
        licenseNumber = i.get("licenseNumber") #登记编号
        equalityPledgor = i.get("equalityPledgor") #出质人
        equalityPawnee = i.get("equalityPawnee") #质权人
        equalityPledgeStatusCode = i.get("equalityPledgeStatusCode") #状态
        detailUrl = i.get("detailUrl")  #详情Url

def getcopyright(dataList):
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

def geticpinfo(dataList):
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

def getpatent(dataList):
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

def getmark(dataList):
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

def getworkright(dataList):
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

def getbrandProject(dataList):
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

def getinvestorlist(dataList):
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

def getprojectSimilarsInfo(dataList):
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

def getCompPersonList(dataList):
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

def projectFinance(dataList):
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

def getlicense(dataList):
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

def getimportexport(dataList):
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

def getquality(dataList):
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

def getdoublecheckup(dataList):
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

def gettenderbidding(dataList):
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

