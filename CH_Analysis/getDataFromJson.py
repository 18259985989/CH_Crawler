# -*- coding: utf-8 -*-
# @Time : 2021/4/24 20:02
# @Author :  Meow_J

"""
专从列表中遍历取出数据
"""

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
        for i in plaintifflist:
            if i != "-":
                plaintiff = plaintiff + i + ";"
        defendantlist = i.get("defendantlist") #被告
        for k in defendantlist:
            if k != "-":
                defendant = defendant + i + ";"

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