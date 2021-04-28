# coding=utf-8
# Author: Shawn
# @Time:2019/12/31 11:50
from CH_Request.util.SQLAlchemy.tools.py.model import *

'''
根据表的某个值算出hash值，进行排序
此字段需最能区分各条数据的不同
'''
mainfield = {
    Abnormal: 'put_reason',
    BidInfo: 'title',
    Branch: 'branch_name',
    ChangeInfo: 'before_change',
    CheckInfo: 'check_date',
    CompanyMortgage: 'reg_number',
    CompanyMortgageChange: 'change_content',
    CompanyMortgageCollateral: 'collateral',
    CompanyMortgagePledgee: 'people_name',
    CopyrightSoftware: 'software_name',
    CopyrightWork: 'reg_number',
    CourtAuto: 'case_number',
    CourtNotice: 'publish_date',
    DishonestInfo: 'gist_num',
    EquityChange: 'shareholder',
    EquityPledge: 'reg_number',
    IllegalInfo: 'put_date',
    ImExportBase: 'crcode',
    ImExportCredit: 'credit_rating',
    ImExportPunish: 'decision_number',
    Invest: 'credit_code',
    JudicialAssistance: 'execute_notice',
    JudicialSale: 'title',
    LawsuitBasic: 'caseno',
    LicenceInfo: 'licence_number',
    Members: 'person_name',
    OwingTax: 'own_tax_balance',
    Patent: 'pub_number',
    Pledgereg: 'reg_number',
    Product: 'app_name',
    Punishment: 'penish_dec_num',
    Qualification: 'cert_number',
    Shareholder: 'shareholder',
    Taxcred: 'years',
    TmInfo: 'reg_number',
    ToExecute: 'case_number',
    YearReport: 'report_year',
    YearReportAssert: 'report_year',
    YearReportSocialSecurity: 'report_year',
    YearReportStore: 'report_year'
}

p = {}
for k, v in p.items():
    print(v)
