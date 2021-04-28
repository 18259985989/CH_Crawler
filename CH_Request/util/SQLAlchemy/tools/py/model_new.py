# 导入: 
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Float, Boolean, DECIMAL, Enum, Date, \
    DateTime, Time, Text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类: 
Base1 = declarative_base()

# 定义对象:
class PBasicInfo(Base1):
    # 表的名字:
    __tablename__ = 'P_BASIC_INFO'
    # 表的结构:
    PERSON_ID = Column(String(32), nullable=False, primary_key=True)
    REAL_NAME = Column(String(128))
    GENDER = Column(Integer)
    BIRTHDAY = Column(Date)
    PROFESSIONAL_NAME = Column(String(32))
    CERTIFICATES_NUMBER = Column(String(32))
    CRETIFICATES_TYPE = Column(String(15))
    TEL_PHONE = Column(String(32))
    EMAIL = Column(String(32))
    COMPANY_NAME = Column(String(128))
    USER_PASSWORD=Column(String(128))
    PRESONNEL_SOURCE=Column(String(15))
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)


    def __repr__(self):
        return ""



# 定义对象: 
class CAbnormal(Base1):
    # 表的名字:
    __tablename__ = 'C_ILLEGAL_INFO'
    # 表的结构:
    ID = Column(String(32), nullable=False, primary_key=True)
    COMPANY_ID = Column(String(32), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
    PUT_REASON = Column(String(512))
    INCLUDED_DATE = Column(Date)
    PUT_OFFICE = Column(String(255))
    REMOVED_REASON = Column(String(512))
    REMOVED_DATE = Column(Date)
    REMOVED_OFFICE = Column(String(255))
    TYPE = Column(String(15))
    OLD_TAB_ID = Column(String(32))
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)

    baseInfo = relationship("BaseInfo", backref=backref('abnormalRel', order_by=COMPANY_ID, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, companyId: {1}, putDate: {2}, decisionOffice: {3}, putReason: {4}, outReason: {5}, outDate: {6}, updtTime: {7}".format(
            self.ID, self.COMPANY_ID, self.INCLUDED_DATE, self.PUT_OFFICE, self.PUT_REASON, self.REMOVED_REASON,
            self.REMOVED_DATE, self.STATEDATE)


# 定义对象:
class CBaseInfo(Base1):
    # 表的名字:
    __tablename__ = 'C_BASIC_INFO'
    # 表的结构:
    COMPANY_ID = Column(String(50), nullable=False, primary_key=True)
    ENTERPRISE_NAME = Column(String(128), nullable=False)
    USCC = Column(String(32))
    REGISTERED_NO = Column(String(32))
    ORGANIZATION_CODE = Column(String(32))
    LEGAL_PERSON = Column(String(128))
    FOUNDED_DATE = Column(Date)
    OPEN_DATE = Column(Date)
    COMPANY_TYPE = Column(String(50))
    REGISTERED_CAPITAL = Column(String(32))
    PAID_IN_CAPITAL = Column(String(128))
    REGISTRATION_AUTHORITY = Column(String(128))
    BUSINESS_SCOPE = Column(LONGTEXT)
    BUSINESS_TERM = Column(Date)
    BUSINESS_STATUS = Column(String(32))
    REGISTERED_ADDRESS = Column(String(512))
    CONTACT_PHONE = Column(String(64))
    TRADE = Column(String(32))
    POST_CODE = Column(String(32))
    SOCIAL_STAFF_NUM = Column(String(32))
    YGRS = Column(String(32))
    EMAIL = Column(String(128))
    Z_BODY = Column(LONGTEXT)
    CREDIT_RATING = Column(Integer)
    CREDIT_RATING_TIME = Column(DateTime)
    CREDIT_SCORE = Column(Integer)
    CREDIT_SCORE_DESCRIBE = Column(String(512))
    COMPANY_KIND = Column(String(15))
    OLD_TAB_ID = Column(String(32))
    OSS_KEY = Column(String(50))
    SOURCE_UPDATE_DATE = Column(DateTime)
    UPDT_TIME = Column(DateTime)
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)

    def __repr__(self):
        return "id: {0}, uscc: {1}, registeredNo: {2}, organizationCode: {3}, legalPerson: {4}, " \
               "foundedDate: {5}, openDate: {6}, registeredCapital: {7}, registrationAuthority: {8}, businessScope: {9}, businessTerm: {10}, " \
               "businessStatus: {11}, registeredAddress: {12}, contactPhone: {13}, trade: {14}, postCode: {15}, updtTime: {16}".format(
            self.COMPANY_ID, self.USCC, self.REGISTERED_NO,self.ORGANIZATION_CODE, self.LEGAL_PERSON, self.FOUNDED_DATE,
            self.OPEN_DATE, self.REGISTERED_CAPITAL, self.REGISTRATION_AUTHORITY, self.BUSINESS_SCOPE, self.BUSINESS_TERM,
            self.BUSINESS_STATUS, self.REGISTERED_ADDRESS,self.CONTACT_PHONE, self.TRADE, self.POST_CODE, self.STATEDATE
            )


# 定义对象:
class CBidInfo(Base1):
    # 表的名字:
    __tablename__ = 'C_BID_INFO'
    # 表的结构:
    ID = Column(String(50), nullable=False, primary_key=True)
    COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
    TITLE = Column(Text)
    PUBLIC_DATE = Column(Date)
    PURCHASING_AGENT = Column(String(64))
    DESCRIPTION = Column(LONGTEXT)
    CHECK_TYPE = Column(String(64))
    TAB_TYPE = Column(String(15))
    UPDT_TIME = Column(DateTime)
    OLD_TAB_ID = Column(String(32))
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)


    baseInfo = relationship("BaseInfo", backref=backref('bidInfoRel', order_by=COMPANY_ID, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, companyId: {1}, description: {2}, publicDate: {3}, itemType: {4}, updtTime: {5}, purchasingAgent: {6}".format(
            self.ID, self.COMPANY_ID, self.DESCRIPTION, self.PUBLIC_DATE, self.CHECK_TYPE, self.STATEDATE, self.PURCHASING_AGENT)



# 定义对象:
class CBranch(Base1):
    # 表的名字:
    __tablename__ = 'C_BRANCH_INFO'
    # 表的结构:
    ID = Column(String(50), nullable=False, primary_key=True)
    COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
    BRANCH_COMPANY_ID = Column(String(50))
    COMPANY_NAME = Column(String(255))
    OLD_TAB_ID = Column(String(32))
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)


    baseInfo = relationship("BaseInfo", backref=backref('branchRel', order_by=COMPANY_ID, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, companyId: {1}, companyName: {2}, creditCode: {3}".format(
            self.ID, self.COMPANY_ID, self.BRANCH_COMPANY_ID, self.COMPANY_NAME)


# 定义对象:
class CChangeInfo(Base1):
    # 表的名字:
    __tablename__ = 'C_CHANGE_MESSAGE_INFO'
    # 表的结构:
    ID = Column(String(50), nullable=False, primary_key=True)
    COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
    CHANGE_ITEM = Column(Text)
    BEFORE_CHANGE = Column(Text)
    AFTER_CHANGE = Column(Text)
    CHANGE_TIME = Column(Date)
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)
    OLD_TAB_ID = Column(String(32))

    baseInfo = relationship("BaseInfo", backref=backref('changeInfoRel', order_by=COMPANY_ID, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, companyId: {1}, changeItem: {2}, beforeChange: {3}, afterChange: {4}, changeTime: {5}, updtTime: {6}".format(
            self.ID, self.COMPANY_ID, self.CHANGE_ITEM, self.BEFORE_CHANGE, self.AFTER_CHANGE, self.CHANGE_TIME, self.STATEDATE)


# 定义对象:

# class CheckInfo(Base):
#     # 表的名字:
#     __tablename__ = 'C_BID_INFO'
#     # 表的结构:
#     ID = Column(String(50), nullable=False, primary_key=True)
#     COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
#     TITLE = Column(Text)
#     PUBLIC_DATE = Column(Date)
#     PURCHASING_AGENT = Column(String(64))
#     DESCRIPTION = Column(LONGTEXT)
#     CHECK_TYPE = Column(String(64))
#     UPDT_TIME = Column(DateTime)
#     OLD_TAB_ID = Column(String(32))
#     STATE = Column(String(15))
#     STATEDATE = Column(DateTime)
#
#     baseInfo = relationship("BaseInfo", backref=backref('checkInfoRel', order_by=id, cascade="all, delete-orphan"))
#
#     def __repr__(self):
#         return "id: {0}, companyId: {1}, itemTitle: {2}, checkType: {3}, checkDate: {4}, checkResult: {5}, updtTime: {6}, office: {7}".format(
#             self.ID, self.COMPANY_ID, self.TITLE, self.CHECK_TYPE, self.PUBLIC_DATE, self.DESCRIPTION, self.STATEDATE, self.PURCHASING_AGENT)
#

# 定义对象:
class CCompanyMortgage(Base1):
    # 表的名字:
    __tablename__ = 'C_CHATTEL_MORTGAGE_INFO'
    # 表的结构:
    ID = Column(String(50), nullable=False, primary_key=True)
    COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
    MORTGAGE_NAME = Column(String(128))
    IDENTIFY_NUMBER = Column(String(64))
    REGISTER_NUMBER = Column(String(64))
    REGISTER_DATE = Column(Date)
    REGISTER_OFFICE = Column(String(64))
    GUARANTEED_AMOUNT = Column(String(64))
    PUBLIC_DATA = Column(Date)
    CURRENCY = Column(String(32))
    CANCEL_DATA = Column(Date)
    CANCEL_REASON = Column(String(85))
    WARRANT_TYPE = Column(String(32))
    TERM = Column(String(255))
    SCOPE = Column(String(255))
    MORT_STATUS = Column(String(32))
    NOTE = Column(Text)
    CANCEL_AUTHORITY = Column(String(255))
    PEOPLE_NAME = Column(String(128))
    PLEDGEE_IDENTIFY_NUMBER = Column(String(32))
    QUALITY_TYPE = Column(String(15))
    OLD_TAB_ID = Column(String(32))
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)

    baseInfo = relationship("BaseInfo",
                            backref=backref('companyMortgageRel', order_by=COMPANY_ID, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, companyId: {1}, registerDate: {2}, registerNumber: {3}, registerOffice: {4}, guaranteedType: {5}, guaranteedAmount: {6}, state: {7}, updtTime: {8}".format(
            self.ID, self.COMPANY_ID, self.REGISTER_DATE, self.REGISTER_NUMBER, self.PLEDGEE_IDENTIFY_NUMBER, self.WARRANT_TYPE,
            self.GUARANTEED_AMOUNT, self.MORT_STATUS, self.STATEDATE)


# 定义对象:
class CCopyrightSoftware(Base1):
    # 表的名字:
    __tablename__ = 'C_COPYRIGHT_INFO'
    # 表的结构:
    ID = Column(String(50), nullable=False, primary_key=True)
    COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
    COPYRIGHT_NAME = Column(String(128))
    REGISTER_NUMBER = Column(String(64))
    VERSION_NUMBER = Column(String(64))
    CLASSIFICATION_NUMBER = Column(String(64))
    WORKS_TYPE = Column(String(255))
    WORKS_FINISH_DATE = Column(Date)
    REGISTER_DATE = Column(Date)
    SOFTWARE_ABBREVIATION = Column(String(128))
    COPYRIGHT_AUTHOR = Column(String(128))
    FIRST_PUBLIC_DATE = Column(Date)
    COPYRIGHT_TYPE = Column(String(15))
    OLD_TAB_ID = Column(String(32))
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)

    baseInfo = relationship("BaseInfo",
                            backref=backref('copyrightSoftwareRel', order_by=COMPANY_ID, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, companyId: {1}, softwareName: {2}, registerNumber: {3}, versionNumber: {4}, classificationNumber: {5}, " \
               "registerDate: {6}, softwareAbbreviation: {7}, copyright: {8}, firstPublicDate: {9}, updtTime: {10}".format(
            self.ID, self.COMPANY_ID, self.COPYRIGHT_NAME, self.REGISTER_NUMBER, self.VERSION_NUMBER, self.CLASSIFICATION_NUMBER,
            self.REGISTER_DATE, self.SOFTWARE_ABBREVIATION, self.COPYRIGHT_AUTHOR, self.WORKS_FINISH_DATE, self.STATEDATE)


# 定义对象:
# class CopyrightWork(Base):
#     # 表的名字:
#     __tablename__ = 'C_COPYRIGHT_INFO'
#     # 表的结构:
#     ID = Column(String(50), nullable=False, primary_key=True)
#     COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
#     COPYRIGHT_NAME = Column(String(128))
#     REGISTER_NUMBER = Column(String(64))
#     VERSION_NUMBER = Column(String(64))
#     CLASSIFICATION_NUMBER = Column(String(64))
#     WORKS_TYPE = Column(String(255))
#     WORKS_FINISH_DATE = Column(Date)
#     REGISTER_DATE = Column(Date)
#     SOFTWARE_ABBREVIATION = Column(String(128))
#     COPYRIGHT_AUTHOR = Column(String(128))
#     FIRST_PUBLIC_DATE = Column(Date)
#     COPYRIGHT_TYPE = Column(String(15))
#     OLD_TAB_ID = Column(String(32))
#     STATE = Column(String(15))
#     STATEDATE = Column(DateTime)
#
#     baseInfo = relationship("BaseInfo", backref=backref('copyrightWorkRel', order_by=id, cascade="all, delete-orphan"))
#
#     def __repr__(self):
#         return "id: {0}, companyId: {1}, worksName: {2}, registerNumber: {3}, worksType: {4}, worksFinishDate: {5}, registerDate: {6}, firstPublicDate: {7}, updtTime: {8}".format(
#             self.id, self.COMPANY_ID, self.COPYRIGHT_NAME, self.REGISTER_NUMBER, self.WORKS_TYPE, self.WORKS_FINISH_DATE, self.REGISTER_DATE,
#             self.FIRST_PUBLIC_DATE, self.STATEDATE)


# 定义对象:
class CCourtAuto(Base1):
    # 表的名字:
    __tablename__ = 'C_COURT_PUBLIC_INFO'
    # 表的结构:
    ID = Column(String(50), nullable=False, primary_key=True)
    COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
    LITIGANT = Column(String(3072))
    ANNOUNCE_TYPE = Column(String(3072))
    PUBLIC_DATE = Column(Date)
    PUBLISH_PAGE = Column(String(32))
    PUBLIC_CONTEXT = Column(Text)
    CASE_REASON = Column(String(512))
    CASE_NUMBER = Column(String(255))
    APPELLANT = Column(String(3072))
    DEFENDANT = Column(String(3072))
    COURT = Column(String(50))
    ANNOUNCE_NUM = Column(String(64))
    PUBLIC_TYPE = Column(String(15))
    OLD_TAB_ID = Column(String(32))
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)

    baseInfo = relationship("BaseInfo", backref=backref('courtAutoRel', order_by=COMPANY_ID, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, companyId: {1}, announcementDate: {2}, caseReason: {3}, appellant: {4}, defendant: {5}, caseNumber: {6}, court: {7}, updtTime: {8}".format(
            self.ID, self.COMPANY_ID, self.PUBLIC_DATE, self.CASE_REASON, self.APPELLANT, self.DEFENDANT, self.CASE_NUMBER,
            self.COURT, self.STATEDATE)


# 定义对象:
# class CourtNotice(Base):
#     # 表的名字:
#     __tablename__ = 'C_COURT_PUBLIC_INFO'
#     # 表的结构:
#     ID = Column(String(50), nullable=False, primary_key=True)
#     COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
#     LITIGANT = Column(String(3072))
#     ANNOUNCE_TYPE = Column(3072)
#     PUBLIC_DATE = Column(Date)
#     PUBLISH_PAGE = Column(String(32))
#     PUBLIC_CONTEXT = Column(Text)
#     CASE_REASON = Column(String(512))
#     CASE_NUMBER = Column(String(255))
#     APPELLANT = Column(String(3072))
#     DEFENDANT = Column(String(3072))
#     COURT = Column(String(50))
#     ANNOUNCE_NUM = Column(String(64))
#     PUBLIC_TYPE = Column(String(15))
#     OLD_TAB_ID = Column(String(32))
#     STATE = Column(String(15))
#     STATEDATE = Column(DateTime)
#     baseInfo = relationship("BaseInfo", backref=backref('courtNoticeRel', order_by=id, cascade="all, delete-orphan"))
#
#     def __repr__(self):
#         return "id: {0}, companyId: {1}, publicDate: {2}, publicType: {3}, publicContext: {4}, appellant: {5}, defendant: {6}, court: {7}, updtTime: {8}".format(
#             self.ID, self.COMPANY_ID, self.PUBLIC_DATE, self.ANNOUNCE_TYPE, self.PUBLIC_CONTEXT, self.APPELLANT, self.DEFENDANT,
#             self.COURT_ID, self.STATEDATE)


# 定义对象:
class CDishonestInfo(Base1):
    # 表的名字:
    __tablename__ = 'C_EXECUTED_PERSON_INFO'
    # 表的结构:
    ID = Column(String(50), nullable=False,  primary_key=True)
    COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
    PERSON_ID = Column(String(50))
    IMPLEMENT_TARGET = Column(String(32))
    IMPLEMENT_COURT = Column(String(128))
    SET_DATE = Column(Date)
    CASE_NUMBER = Column(String(32))
    PUBLISH_DATE = Column(Date)
    PROVINCE = Column(String(32))
    PERFORM_NUMBER = Column(String(86))
    GIST_UNIT = Column(String(64))
    DUTY = Column(Text)
    PERFORM_STATE = Column(String(128))
    DISRUPTTYPE_NAME = Column(String(1024))
    END_DATE = Column(Date)
    OUTSTANDING_AMOUNT = Column(String(32))
    DISHONEST_TYPE = Column(String(15))
    OLD_TAB_ID = Column(String(32))
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)

    baseInfo = relationship("BaseInfo", backref=backref('dishonestInfoRel', order_by=COMPANY_ID, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, companyId: {1}, setDate: {2}, caseNumber: {3}, performNumber: {4}, implementCourt: {5}, performState: {6}, updtTime: {7}".format(
            self.ID, self.COMPANY_ID, self.SET_DATE, self.CASE_NUMBER, self.PERFORM_NUMBER, self.IMPLEMENT_COURT, self.PERFORM_STATE,
            self.STATEDATE)


# # 定义对象:
# class EquityChange(Base):
#     # 表的名字:
#     __tablename__ = 'C_CHANGE_MESSAGE_INFO'
#     # 表的结构:
#     ID = Column(String(50), nullable=False, primary_key=True)
#     COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
#     CHANGE_ITEM = Column(Text)
#     BEFORE_CHANGE = Column(Text)
#     AFTER_CHANGE = Column(Text)
#     CHANGE_TIME = Column(Date)
#     STATE = Column(String(15))
#     STATEDATE = Column(DateTime)
#     OLD_TAB_ID = Column(String(32))
#
#     baseInfo = relationship("BaseInfo", backref=backref('changeInfoRel', order_by=id, cascade="all, delete-orphan"))
#
#     def __repr__(self):
#         return "id: {0}, c_id: {1}, shareholder: {2}, alt_date: {3}, trans_before: {4}, trans_after: {5}, publish_date: {6}, KEY: {7}".format(
#             self.id, self.c_id, self.shareholder, self.alt_date, self.trans_before, self.trans_after, self.publish_date,
#             self.KEY)


# 定义对象:
# class EquityPledge(Base):
#     # 表的名字:
#     __tablename__ = 'C_CHATTEL_MORTGAGE_INFO'
#     # 表的结构:
#     ID = Column(String(50), nullable=False, primary_key=True)
#     COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
#     MORTGAGE_NAME = Column(String(128))
#     IDENTIFY_NUMBER = Column(String(64))
#     REGISTER_NUMBER = Column(String(64))
#     REGISTER_DATE = Column(Date)
#     REGISTER_OFFICE = Column(String(64))
#     GUARANTEED_AMOUNT = Column(String(64))
#     PUBLIC_DATA = Column(Date)
#     CURRENCY = Column(String(32))
#     CANCEL_DATA = Column(Date)
#     CANCEL_REASON = Column(String(85))
#     WARRANT_TYPE = Column(String(32))
#     TERM = Column(String(255))
#     SCOPE = Column(String(255))
#     MORT_STATUS = Column(String(32))
#     NOTE = Column(Text)
#     CANCEL_AUTHORITY = Column(String(255))
#     PEOPLE_NAME = Column(String(128))
#     PLEDGEE_IDENTIFY_NUMBER = Column(String(32))
#     QUALITY_TYPE = Column(String(15))
#     OLD_TAB_ID = Column(String(32))
#     STATE = Column(String(15))
#     STATEDATE = Column(DateTime)
#
#     baseInfo = relationship("BaseInfo", backref=backref('equityPledgeRel', order_by=id, cascade="all, delete-orphan"))
#
#     def __repr__(self):
#         return "id: {0}, companyId: {1}, registerDate: {2}, registerNumber: {3}, pledgor: {4}, pledgee: {5}, state: {6}, equityAmount: {7}, updtTime: {8}".format(
#             self.ID, self.COMPANY_ID, self.REGISTER_DATE, self.REGISTER_NUMBER, self.MORTGAGE_NAME, self.PEOPLE_NAME, self.MORT_STATUS,
#             self.GUARANTEED_AMOUNT, self.STATEDATE)


# 定义对象:
# class IllegalInfo(Base):
#     # 表的名字:
#     __tablename__ = 'C_ILLEGAL_INFO'
#     # 表的结构:
#     ID = Column(String(50), nullable=False, primary_key=True)
#     COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
#     PUT_REASON = Column(String(512))
#     INCLUDED_DATE = Column(Date)
#     PUT_OFFICE = Column(String(255))
#     REMOVED_REASON = Column(String(512))
#     REMOVED_DATE = Column(Date)
#     REMOVED_OFFICE = Column(String(255))
#     TYPE = Column(String(15))
#     OLD_TAB_ID = Column(String(32))
#     STATE = Column(String(15))
#     STATEDATE = Column(DateTime)
#
#     baseInfo = relationship("BaseInfo", backref=backref('illegalInfoRel', order_by=id, cascade="all, delete-orphan"))
#
#     def __repr__(self):
#         return "id: {0}, companyId: {1}, putReason: {2}, type: {3}, includedDate: {4}, removedReason: {5}, removedDate: {6}, removedOffice: {7}, updtTime: {8}".format(
#             self.ID, self.COMPANY_ID, self.TYPE, self.INCLUDED_DATE, self.REMOVED_REASON, self.REMOVED_DATE,
#             self.REMOVED_OFFICE, self.STATEDATE)


# 定义对象:
class CImExportBase(Base1):
    # 表的名字:
    __tablename__ = 'C_IMPORT_EXPORT_INFO'
    # 表的结构:
    ID = Column(String(50), nullable=False, primary_key=True)
    COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
    CUSTOMS_REGISTERED_NUMBER = Column(String(64))
    REGISTERED_DATE = Column(Date)
    REGISTERED_CUSTOMS = Column(String(32))
    ADMIN_AREA = Column(String(128))
    ECONOMY_AREA = Column(String(64))
    MANAGE_TYPE = Column(String(64))
    SPECIAL_AREA = Column(String(64))
    INDUSTRY_TYPE = Column(String(64))
    EFFECTIVE_DATE = Column(DateTime)
    CUSTOMS_LOGOUT = Column(String(64))
    YEAR_RESULT = Column(String(64))
    BUSINESS_TYPE = Column(String(255))
    CREDIT_LEVEL = Column(String(32))
    AUTH_NUMBER = Column(String(255))
    AUTH_DATE = Column(Date)
    OLD_TAB_ID = Column(String(32))
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)

    baseInfo = relationship("BaseInfo", backref=backref('imExportBaseRel', order_by=COMPANY_ID, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, companyId: {1}, registeredDate: {2}, customsRegisteredNumber: {3}, \
        registeredCustoms: {4}, adminArea: {5}, economyArea: {6}, manageType: {7}, specialArea: {8}, \
        industryType: {9}, effectiveDate: {10}, customsLogout: {11}, yearResult: {12}, \
        businessType: {13}, authDate: {14}, authNumber: {15}, creditLevel: {16}, updtTime: {17}".format(
            self.ID, self.COMPANY_ID, self.REGISTERED_DATE, self.CUSTOMS_REGISTERED_NUMBER, self.REGISTERED_CUSTOMS,
            self.ADMIN_AREA, self.ECONOMY_AREA, self.MANAGE_TYPE, self.SPECIAL_AREA,
            self.INDUSTRY_TYPE, self.EFFECTIVE_DATE, self.CUSTOMS_LOGOUT, self.YEAR_RESULT, self.BUSINESS_TYPE, self.CREDIT_LEVEL,
            self.AUTH_DATE, self.AUTH_NUMBER, self.STATEDATE)


# # 定义对象:
# class ImExportCredit(Base):
#     # 表的名字:
#     __tablename__ = 'im_export_credit'
#     # 表的结构:
#     id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
#     c_id = Column(Integer, ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
#     credit_rating = Column(String(48))
#     authentication_code = Column(String(255))
#     identification_time = Column(DateTime)
#
#     baseInfo = relationship("BaseInfo", backref=backref('imExportCreditRel', order_by=id, cascade="all, delete-orphan"))
#
#     def __repr__(self):
#         return "id: {0}, c_id: {1}, credit_rating: {2}, authentication_code: {3}, identification_time: {4}, KEY: {5}".format(
#             self.id, self.c_id, self.credit_rating, self.authentication_code, self.identification_time, self.KEY)


# 定义对象:
# class ImExportPunish(Base):
#     # 表的名字:
#     __tablename__ = 'im_export_punish'
#     # 表的结构:
#     id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
#     c_id = Column(Integer, ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
#     decision_number = Column(String(28))
#     penalty_date = Column(DateTime)
#     party = Column(String(255))
#     nature_of_case = Column(String(64))
#
#     baseInfo = relationship("BaseInfo", backref=backref('imExportPunishRel', order_by=id, cascade="all, delete-orphan"))
#
#     def __repr__(self):
#         return "id: {0}, c_id: {1}, decision_number: {2}, penalty_date: {3}, party: {4}, nature_of_case: {5}, KEY: {6}".format(
#             self.id, self.c_id, self.decision_number, self.penalty_date, self.party, self.nature_of_case, self.KEY)


# 定义对象:
class CInvest(Base1):
    # 表的名字:
    __tablename__ = 'C_INVEST_INFO'
    # 表的结构:
    ID = Column(String(50), nullable=False,  primary_key=True)
    COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
    INVEST_COMPANY_ID = Column(String(50))
    INVEST_COMPANY = Column(String(128))
    CREDIT_CODE = Column(String(64))
    LEGAL_PERSON=Column(String(255))
    FOUNDED_DATE=Column(Date)
    REGISTERED_CAPITAL=Column(String(255))
    BUSINESS_STATUS=Column(String(255))
    INVEST_NUMBER = Column(String(32))
    INVEST_PROPORTION = Column(String(32))
    ALIAS = Column(String(32))
    OLD_TAB_ID = Column(String(32))
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)


    baseInfo = relationship("BaseInfo", backref=backref('investRel', order_by=COMPANY_ID, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, companyId: {1}, investCompany: {2}, investNumber: {3}, investProportion: {4}, updtTime: {5}".format(
            self.ID, self.COMPANY_ID, self.INVEST_COMPANY, self.INVEST_NUMBER, self.INVEST_PROPORTION, self.STATEDATE)


# 定义对象:
# class JudicialAssistance(Base):
#     # 表的名字:
#     __tablename__ = 'dishonest_info'
#     # 表的结构:
#     ID = Column(String(50), nullable=False, primary_key=True)
#     COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
#     PERSON_ID = Column(String(50))
#     IMPLEMENT_TARGET = Column(String(32))
#     IMPLEMENT_COURT = Column(String(128))
#     SET_DATE = Column(Date)
#     CASE_NUMBER = Column(String(32))
#     PUBLISH_DATE = Column(Date)
#     PROVINCE = Column(String(32))
#     PERFORM_NUMBER = Column(String(86))
#     GIST_UNIT = Column(String(64))
#     DUTY = Column(Text)
#     PERFORM_STATE = Column(String(128))
#     DISRUPTTYPE_NAME = Column(String(1024))
#     END_DATE = Column(Date)
#     OUTSTANDING_AMOUNT = Column(String(32))
#     DISHONEST_TYPE = Column(String(15))
#     OLD_TAB_ID = Column(String(32))
#     STATE = Column(String(15))
#     STATEDATE = Column(DateTime)
#
#     baseInfo = relationship("BaseInfo",
#                             backref=backref('judicialAssistanceRel', order_by=id, cascade="all, delete-orphan"))
#
#     def __repr__(self):
#         return "id: {0}, c_id: {1}, public_date: {2}, executed: {3}, equity_amount: {4}, equity_state: {5}, execute_notice: {6}, execute_court: {7}, execute_list: {8}, execute_order: {9}, license_type: {10}, license_number: {11}, from_date: {12}, to_date: {13}, period: {14}, KEY: {15}".format(
#             self.id, self.c_id, self.public_date, self.executed, self.equity_amount, self.equity_state,
#             self.execute_notice, self.execute_court, self.execute_list, self.execute_order, self.license_type,
#             self.license_number, self.from_date, self.to_date, self.period, self.KEY)


# 定义对象:
# class JudicialSale(Base):
#     # 表的名字:
#     __tablename__ = 'C_COURT_PUBLIC_INFO'
#     # 表的结构:
#     ID = Column(String(50), nullable=False, primary_key=True)
#     COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
#     LITIGANT = Column(String(3072))
#     ANNOUNCE_TYPE = Column(3072)
#     PUBLIC_DATE = Column(Date)
#     PUBLISH_PAGE = Column(String(32))
#     PUBLIC_CONTEXT = Column(Text)
#     CASE_REASON = Column(String(512))
#     CASE_NUMBER = Column(String(255))
#     APPELLANT = Column(String(3072))
#     DEFENDANT = Column(String(3072))
#     COURT = Column(String(50))
#     ANNOUNCE_NUM = Column(String(64))
#     PUBLIC_TYPE = Column(String(15))
#     OLD_TAB_ID = Column(String(32))
#     STATE = Column(String(15))
#     STATEDATE = Column(DateTime)
#
#     baseInfo = relationship("BaseInfo", backref=backref('judicialSaleRel', order_by=id, cascade="all, delete-orphan"))
#
#     def __repr__(self):
#         return "id: {0}, companyId: {1}, auctionNotice: {2}, noticeDate: {3}, implementCourt: {4}, auctionTarget: {5}, updtTime: {6}".format(
#             self.ID, self.COMPANY_ID, self.LITIGANT, self.PUBLIC_DATE, self.COURT_ID, self.ANNOUNCE_TYPE, self.STATEDATE)


# 定义对象:
class CLawsuitBasic(Base1):
    # 表的名字:
    __tablename__ = 'C_LEGAL_PROCEEDINGS_INFO'
    # 表的结构:
    ID = Column(String(50), nullable=False, primary_key=True)
    COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
    CASE_NAME = Column(String(255))
    CASE_TYPE = Column(String(128))
    SENTENCE_DATE = Column(Date)
    CASE_REASON = Column(String(512))
    CASE_NUMBER = Column(String(512))
    PLAINTIFF = Column(String(3072))
    DEFENDANT = Column(String(3072))
    CASE_DETAIL = Column(LONGTEXT)
    COURT = Column(String(128))
    DECISION_TIME = Column(Date)
    DECISION_REASON = Column(Text)
    RESULT = Column(Text)
    OLD_TAB_ID = Column(String(32))
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)

    baseInfo = relationship("BaseInfo", backref=backref('lawsuitBasicRel', order_by=COMPANY_ID, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, companyId: {1}, sentenceDate: {2}, plaintiff: {3}, defendant: {4},caseType: {5}, " \
               "caseNumber: {6}, sentenceContext: {7}, sentenceResult: {8}, updtTime: {9}".format(
            self.ID, self.COMPANY_ID, self.SENTENCE_DATE, self.PLAINTIFF, self.DEFENDANT, self.CASE_TYPE, self.CASE_NUMBER,
            self.CASE_DETAIL, self.RESULT, self.STATEDATE)


# 定义对象:
class CLicenceInfo(Base1):
    # 表的名字:
    __tablename__ = 'C_AUTHENTICATION_CLASS_INFO'
    # 表的结构:
    ID = Column(String(50), nullable=False, primary_key=True)
    COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
    AUTHENTICATION_NUMBER = Column(String(255))
    AUTHENTICATION_NAME = Column(String(128))
    AUTHENTICATION_TEXT = Column(Text)
    AUTHENTICATION_OFFICE = Column(String(128))
    AUTHENTICATION_EXPIRY = Column(Date)
    AUTHENTICATION_DATE = Column(Date)
    CERTIFICATE_TYPE = Column(String(64))
    AUTHENTICATION_TYPE = Column(String(15))
    UPDT_TIME = Column(DateTime)
    OLD_TAB_ID = Column(String(32))
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)

    baseInfo = relationship("BaseInfo", backref=backref('licenceInfoRel', order_by=COMPANY_ID, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, companyId: {1}, administrativeLicensingName: {2}, administrativeLicensingContext: {3}, administrativeLicensingNumber: {4}, " \
               "administrativeLicensingOffice: {5}, administrativeLicensingExpiry: {6}, administrativeLicensingEnd: {7}, updtTime: {8}".format(
            self.ID, self.COMPANY_ID, self.AUTHENTICATION_NAME, self.AUTHENTICATION_TEXT, self.AUTHENTICATION_NUMBER, self.AUTHENTICATION_OFFICE, self.AUTHENTICATION_EXPIRY,
            self.AUTHENTICATION_DATE, self.STATEDATE)


# 定义对象:
class CMembers(Base1):
    # 表的名字:
    __tablename__ = 'C_P_RELATION_TABLE'
    # 表的结构:
    ID = Column(String(50), nullable=False, primary_key=True)
    PERSON_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
    COMPANY_ID = Column(String(50))
    RELATION_TYPE = Column(String(15))
    POSITION=Column(String(255))
    OLD_TAB_ID=Column(String(64))
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)


    baseInfo = relationship("BaseInfo", backref=backref('membersRel', order_by=COMPANY_ID, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, companyId: {1}, name: {2}, position: {3}, updtTime: {4}".format(self.ID, self.COMPANY_ID,
                                                                                      self.PERSON_ID, self.RELATION_TYPE, self.STATEDATE)


# 定义对象:
class COwingTax(Base1):
    # 表的名字:
    __tablename__ = 'C_TAX_INFO'
    # 表的结构:
    ID = Column(String(32), nullable=False, primary_key=True)
    COMPANY_ID = Column(String(32), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
    TAXPAYER_NUMBER = Column(String(64))
    PUBLIC_DATE = Column(Date)
    YEARS = Column(String(15))
    TAX_TYPE = Column(String(64))
    TAX_OWED = Column(String(64))
    CURRENT_TAX_OWED = Column(String(64))
    OFFICE = Column(String(128))
    GRADE = Column(String(15))
    TAX_RATING = Column(String(15))
    OLD_TAB_ID = Column(String(32))
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)

    baseInfo = relationship("BaseInfo", backref=backref('owingTaxRel', order_by=COMPANY_ID, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, companyId: {1}, publicDate: {2}, taxpayerNumber: {3}, taxType: {4}, taxArrears: {5}, over: {6}, office: {7}, updtTime: {8}".format(
            self.ID, self.COMPANY_ID, self.PUBLIC_DATE, self.TAXPAYER_NUMBER, self.TAX_TYPE, self.TAX_OWED,
            self.CURRENT_TAX_OWED, self.OFFICE, self.STATEDATE)


# 定义对象:
class CPatent(Base1):
    # 表的名字:
    __tablename__ = 'C_PATENT_INFO'
    # 表的结构:
    ID = Column(String(32), nullable=False, primary_key=True)
    COMPANY_ID = Column(String(32), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
    INVENTION = Column(Text)
    APPLY_NUMBER = Column(String(50))
    PUBLIC_NUM = Column(String(50))
    CLASIFICATION_NUM = Column(String(50))
    APPLY_DATE = Column(Date)
    APPLY_PUBLIC_DATE = Column(Date)
    APPLY_PERSON = Column(String(128))
    INVENTOR = Column(String(256))
    AGENT = Column(String(64))
    AGENCY = Column(String(128))
    ADDRESS = Column(String(1024))
    SUMMARY = Column(Text)
    IMG_URL = Column(String(128))
    OLD_TAB_ID = Column(String(32))
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)

    baseInfo = relationship("BaseInfo", backref=backref('patentRel', order_by=COMPANY_ID, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, companyId: {1}, applyNumber: {2}, summary: {3}, inventor: {4}, invention: {5}, applyPerson: {6}, applyDate: {7}, applyPublicDate: {8}, agency: {9}, agent: {10}, address: {11}, updtTime: {12}".format(
            self.ID, self.COMPANY_ID, self.APPLY_NUMBER, self.SUMMARY, self.INVENTOR, self.INVENTION, self.APPLY_PERSON,
            self.APPLY_DATE, self.APPLY_PUBLIC_DATE, self.AGENCY, self.AGENT, self.ADDRESS, self.STATEDATE)


# 定义对象:
# class Pledgereg(Base):
#     # 表的名字:
#     __tablename__ = 'pledgereg'
#     # 表的结构:
#     id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
#     c_id = Column(Integer, ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
#     reg_number = Column(Integer)
#     ent_name = Column(String(255))
#     kinds = Column(String(255))
#     pledgor_name = Column(String(255))
#     pledge_from = Column(DateTime)
#     pledge_to = Column(DateTime)
#     public_date = Column(DateTime)
#     tm_name = Column(String(255))
#     state = Column(String(255))
#     pledgee_name = Column(String(255))
#
#     baseInfo = relationship("BaseInfo", backref=backref('pledgeregRel', order_by=id, cascade="all, delete-orphan"))
#
#     def __repr__(self):
#         return "id: {0}, c_id: {1}, reg_number: {2}, ent_name: {3}, kinds: {4}, pledgor_name: {5}, pledge_from: {6}, pledge_to: {7}, public_date: {8}, tm_name: {9}, state: {10}, pledgee_name: {11}, KEY: {12}".format(
#             self.id, self.c_id, self.reg_number, self.ent_name, self.kinds, self.pledgor_name, self.pledge_from,
#             self.pledge_to, self.public_date, self.tm_name, self.state, self.pledgee_name, self.KEY)


# 定义对象:
class CProduct(Base1):
    # 表的名字:
    __tablename__ = 'C_GOODS_INFO'
    # 表的结构:
    ID = Column(String(32), nullable=False, primary_key=True)
    COMPANY_ID = Column(String(32), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
    PRODUCT_NAME = Column(String(128))
    FILTER_NAME = Column(String(32))
    CLASSES = Column(String(32))
    BRIEF = Column(String(3072))
    ICON = Column(String(255))
    PRODUCT_TYPE = Column(String(32))
    OLD_TAB_ID = Column(String(32))
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)

    baseInfo = relationship("BaseInfo", backref=backref('productRel', order_by=COMPANY_ID, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, companyId: {1}, name: {2}, classes: {3}, brief: {4}, icon: {5}, productType: {6}, updtTime: {7}".format(
            self.ID, self.COMPANY_ID, self.PRODUCT_NAME, self.CLASSES, self.BRIEF, self.ICON, self.PRODUCT_TYPE, self.STATEDATE)


# 定义对象:
class CPunishment(Base1):
    # 表的名字:
    __tablename__ = 'C_OFFICE_PUNISH_INFO'
    # 表的结构:
    ID = Column(String(50), nullable=False, primary_key=True)
    COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
    DECISION_NUMBER = Column(String(1024))
    ILLEGAL_TYPE = Column(Text)
    PUNISH_TEXT = Column(LONGTEXT)
    DECISION_OFFICE = Column(String(128))
    DECISION_DATE = Column(Date)
    PUNISH_NAME = Column(String(128))
    PUNISH_TYPE = Column(String(85))
    PUNISH_TYPE_SEC = Column(String(85))
    EVIDENCE = Column(Text)
    OLD_TAB_ID = Column(String(32))
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)

    baseInfo = relationship("BaseInfo", backref=backref('punishmentRel', order_by=COMPANY_ID, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, companyId: {1}, decisionNumber: {2}, punishType: {3}, punishText: {4}, decisionDate: {5}, decisionOffice: {6}, updtTime: {7}".format(
            self.ID, self.COMPANY_ID, self.DECISION_NUMBER, self.PUNISH_TYPE, self.PUNISH_TEXT, self.DECISION_DATE,
            self.DECISION_OFFICE, self.STATEDATE)


# 定义对象:
# class Qualification(Base):
#     # 表的名字:
#     __tablename__ = 'C_AUTHENTICATION_CLASS_INFO'
#     # 表的结构:
#     ID = Column(String(50), nullable=False, primary_key=True)
#     COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
#     AUTHENTICATION_NUMBER = Column(String(255))
#     AUTHENTICATION_NAME = Column(String(128))
#     AUTHENTICATION_TEXT = Column(Text)
#     AUTHENTICATION_OFFICE = Column(String(128))
#     AUTHENTICATION_EXPIRY = Column(Date)
#     AUTHENTICATION_DATE = Column(Date)
#     CERTIFICATE_TYPE = Column(String(64))
#     AUTHENTICATION_TYPE = Column(String(15))
#     UPDT_TIME = Column(DateTime)
#     OLD_TAB_ID = Column(String(32))
#     STATE = Column(String(15))
#     STATEDATE = Column(DateTime)
#
#     baseInfo = relationship("BaseInfo", backref=backref('qualificationRel', order_by=id, cascade="all, delete-orphan"))
#
#     def __repr__(self):
#         return "id: {0}, companyId: {1}, certificateType: {2}, certificateNumber: {3}, issueDate: {4}, expiredDate: {5}, updtTime: {6}".format(
#             self.ID, self.COMPANY_ID, self.CERTIFICATE_TYPE, self.AUTHENTICATION_NUMBER, self.AUTHENTICATION_DATE, self.AUTHENTICATION_EXPIRY, self.STATEDATE)


# 定义对象:
class CShareholder(Base1):
    # 表的名字:
    __tablename__ = 'C_SHAREHOLDER_INFO'
    # 表的结构:
    ID = Column(String(50), nullable=False,primary_key=True)
    COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
    SHAREHOLDER = Column(String(255))
    SHAREHOLDER_TYPE = Column(String(32))
    BLIC_TYPE = Column(String(32))
    BLIC_NUMBER = Column(String(32))
    ENT_TYPE = Column(String(64))
    SUBSCRIBED_CAPITAL = Column(String(255))
    SUBSCRIBED_DATE = Column(Date)
    PAID_IN_CAPITAL = Column(String(32))
    PAID_IN_CAPITAL_DATA = Column(String(32))
    SUBSCRIBED_PROPORTION = Column(String(255))
    CURRENCY = Column(String(45))
    NATIONALITY = Column(String(45))
    OLD_TAB_ID = Column(String(32))
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)

    baseInfo = relationship("BaseInfo", backref=backref('shareholderRel', order_by=COMPANY_ID, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, companyId: {1}, shareholder: {2}, subscribedCapital: {3}, subscribedDate: {4}, " \
               "subscribedProportion: {5}, currency: {6}, nationality: {7}, updtTime: {8}".format(
            self.ID, self.COMPANY_ID, self.SHAREHOLDER, self.SUBSCRIBED_CAPITAL, self.SUBSCRIBED_DATE, self.SUBSCRIBED_PROPORTION,
            self.CURRENCY, self.NATIONALITY, self.STATEDATE)


# 定义对象:
# class Taxcred(Base):
#     # 表的名字:
#     __tablename__ = 'C_TAX_INFO'
#     # 表的结构:
#     ID = Column(String(32), nullable=False, primary_key=True)
#     COMPANY_ID = Column(String(32), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
#     TAXPAYER_NUMBER = Column(String(64))
#     PUBLIC_DATE = Column(Date)
#     YEARS = Column(String(15))
#     TAX_TYPE = Column(String(64))
#     TAX_OWED = Column(String(64))
#     CURRENT_TAX_OWED = Column(String(64))
#     OFFICE = Column(String(128))
#     GRADE = Column(String(15))
#     TAX_RATING = Column(String(15))
#     OLD_TAB_ID = Column(String(32))
#     STATE = Column(String(15))
#     STATEDATE = Column(DateTime)
#
#     baseInfo = relationship("BaseInfo", backref=backref('taxcredRel', order_by=id, cascade="all, delete-orphan"))
#
#     def __repr__(self):
#         return "id: {0}, companyId: {1}, year: {2}, taxLevel: {3}, type: {4}, taxpayerNumber: {5}, office: {6}, updtTime: {7}".format(
#             self.ID, self.COMPANY_ID, self.YEARS, self.GRADE, self.TAX_TYPE, self.TAXPAYER_NUMBER, self.OFFICE, self.STATEDATE)
#

# 定义对象:
class CTmInfo(Base1):
    # 表的名字:
    __tablename__ = 'C_TRADEMARK_INFO'
    # 表的结构:
    ID = Column(String(50), nullable=False, primary_key=True)
    COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
    TRADEMARK_NAME = Column(String(255))
    REGISTER_NUMBER = Column(String(32))
    TRADEMARK_TYPE = Column(String(32))
    REG_ANNC_DATE = Column(Date)
    REG_ANNC_ISSUE = Column(String(255))
    PROPERTY_BGN_DATE = Column(Date)
    PROPERTY_END_DATE = Column(Date)
    SERVICE_LIST = Column(Text)
    APPLY_DATE = Column(Date)
    TRADEMARK_STATE = Column(String(255))
    APPLICANT = Column(String(128))
    APPLY_PROCESS = Column(Text)
    TRADEMARK_PIC = Column(String(255))
    OLD_TAB_ID = Column(String(32))
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)

    baseInfo = relationship("BaseInfo", backref=backref('tmInfoRel', order_by=COMPANY_ID, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, companyId: {1}, trademarkPic: {2}, trademarkName: {3}, registerNumber: {4}, serviceList: {5}, state: {6}, applyDate: {7}, trademarkType: {8}, updtTime: {9}".format(
            self.ID, self.COMPANY_ID, self.TRADEMARK_PIC, self.TRADEMARK_NAME, self.REGISTER_NUMBER, self.SERVICE_LIST, self.TRADEMARK_STATE,
            self.APPLY_DATE, self.TRADEMARK_TYPE, self.STATEDATE)


# 定义对象:
# class ToExecute(Base):
#     # 表的名字:
#     __tablename__ = 'C_EXECUTED_PERSON_INFO'
#     # 表的结构:
#     ID = Column(String(50), nullable=False, primary_key=True)
#     COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
#     PERSON_ID = Column(String(50))
#     IMPLEMENT_TARGET = Column(String(32))
#     IMPLEMENT_COURT = Column(String(128))
#     SET_DATE = Column(Date)
#     CASE_NUMBER = Column(String(32))
#     PUBLISH_DATE = Column(Date)
#     PROVINCE = Column(String(32))
#     PERFORM_NUMBER = Column(String(86))
#     GIST_UNIT = Column(String(64))
#     DUTY = Column(Text)
#     PERFORM_STATE = Column(String(128))
#     DISRUPTTYPE_NAME = Column(String(1024))
#     END_DATE = Column(Date)
#     OUTSTANDING_AMOUNT = Column(String(32))
#     DISHONEST_TYPE = Column(String(15))
#     OLD_TAB_ID = Column(String(32))
#     STATE = Column(String(15))
#     STATEDATE = Column(DateTime)
#
#     baseInfo = relationship("BaseInfo", backref=backref('toExecuteRel', order_by=id, cascade="all, delete-orphan"))
#
#     def __repr__(self):
#         return "id: {0}, companyId: {1}, setDate: {2}, caseNumber: {3}, implementTarget: {4}, implementCourt: {5}, updtTime: {6}".format(
#             self.ID, self.COMPANY_ID, self.SET_DATE, self.CASE_NUMBER, self.IMPLEMENT_TARGET, self.IMPLEMENT_COURT, self.STATEDATE)


# 定义对象:
class CWebsiteInfo(Base1):
    # 表的名字:
    __tablename__ = 'C_DOMAIN_NAME_INFO'
    # 表的结构:
    ID = Column(String(50), nullable=False, primary_key=True)
    COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
    WEB_HOME = Column(String(255))
    WEB_NAME = Column(String(128))
    CASE_NUMBER = Column(String(32))
    AUDIT_DATE = Column(Date)
    DOMAIN_NAME = Column(String(128))
    COMPANY_TYPE = Column(String(32))
    OLD_TAB_ID = Column(String(32))
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)

    baseInfo = relationship("BaseInfo", backref=backref('websiteInfoRel', order_by=COMPANY_ID, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, companyId: {1}, webHome: {2}, webName: {3}, caseNumber: {4}, auditDate: {5}, domainName: {6}, companyType: {7}, updtTime:{8}".format(
            self.ID, self.COMPANY_ID, self.WEB_HOME, self.WEB_NAME, self.CASE_NUMBER, self.AUDIT_DATE, self.DOMAIN_NAME,
            self.COMPANY_TYPE, self.STATEDATE)


# 定义对象:
class CYearReport(Base1):
    # 表的名字:
    __tablename__ = 'C_YEAR_REPORT_INFO'
    # 表的结构:
    ID = Column(String(50), nullable=False, primary_key=True)
    COMPANY_ID = Column(String(50), ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
    COMPANY_NAME = Column(String(64))
    YEAR = Column(String(32))
    REG_NUMBER = Column(String(32))
    MANAGE_STATE = Column(String(32))
    EMPLOYEE_NUM = Column(String(64))
    PHONE_NUMBER = Column(String(1024))
    EMAIL = Column(String(64))
    POSTAL_ADDRESS = Column(String(255))
    POSTCODE = Column(String(32))
    CAPITAL_TOTAL = Column(String(64))
    MAIN_TOTAL = Column(String(64))
    OWNER_TOTAL = Column(String(64))
    NET_PROFIT = Column(String(64))
    BUSINESS_TOTAL = Column(String(64))
    TAX_TOTAL = Column(String(64))
    PROFIT_TOTAL = Column(String(64))
    LIABILITIES_TOTAL = Column(String(64))
    ENDOWMENT_INSURANCE = Column(String(32))
    MEDICAL_INSURANCE = Column(String(32))
    MATERNIT_INSURANCE = Column(String(32))
    UNEMPLOYMENT_INSURANCE = Column(String(32))
    EMPLOYMENTINJURY_INSURANCE = Column(String(32))
    ENDOWMENT_INSURANCE_BASE = Column(String(64))
    MEDICAL_INSURANCE_BASE = Column(String(64))
    MATERNIT_INSURANCE_BASE = Column(String(64))
    UNEMPLOYMENT_INSURANCE_BASE = Column(String(64))
    EMPLOYMENTINJURY_INSURANCE_BASE = Column(String(64))
    ENDOWMENT_INSURANCE_PAYAMOUNT = Column(String(64))
    MEDICAL_INSURANCE_PAYAMOUNT = Column(String(64))
    MATERNIT_INSURANCE_PAYAMOUNT = Column(String(64))
    UNEMPLOYMENT_INSURANCE_PAYAMOUNT = Column(String(64))
    EMPLOYMENTINJURY_INSURANCE_PAYAMOUNT = Column(String(64))
    ENDOWMENT_INSURANCE_OWEAMOUNT = Column(String(64))
    MEDICAL_INSURANCE_OWEAMOUNT = Column(String(64))
    MATERNIT_INSURANCE_OWEAMOUNT = Column(String(64))
    UNEMPLOYMENT_INSURANCE_OWEAMOUNT = Column(String(64))
    EMINSURANCE_OWEAMOUNT = Column(String(64))
    WEB_NAME = Column(String(128))
    WEB_TYPE = Column(String(32))
    WEB_SITE = Column(String(255))
    OLD_TAB_ID = Column(String(32))
    STATE = Column(String(15))
    STATEDATE = Column(DateTime)


    baseInfo = relationship("BaseInfo", backref=backref('yearReportRel', order_by=COMPANY_ID, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, companyId: {1}, year: {2}, capitalTotal: {3}, mainTotal: {4}, ownerTotal: {5}, netProfit: {6}, " \
               "businessTotal: {7}, taxTotal: {8}, profitTotal: {9}, liabilitiesTotal: {10}, updtTime: {11}".format(
            self.ID, self.COMPANY_ID, self.YEAR, self.CAPITAL_TOTAL, self.MAIN_TOTAL, self.OWNER_TOTAL,
            self.NET_PROFIT, self.BUSINESS_TOTAL, self.TAX_TOTAL, self.PROFIT_TOTAL, self.LIABILITIES_TOTAL, self.STATEDATE)


# 定义对象:
# class YearReportAssert(Base):
#     # 表的名字:
#     __tablename__ = 'year_report_assert'
#     # 表的结构:
#     id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
#     c_id = Column(Integer, ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
#     total_assets = Column(String(64))
#     total_equity = Column(String(64))
#     total_sales = Column(String(64))
#     total_profit = Column(String(64))
#     prime_busprofit = Column(String(64))
#     retained_profit = Column(String(64))
#     total_tax = Column(String(64))
#     total_liability = Column(String(64))
#     report_year = Column(String(64))
#
#     baseInfo = relationship("BaseInfo",
#                             backref=backref('yearReportAssertRel', order_by=id, cascade="all, delete-orphan"))
#
#     def __repr__(self):
#         return "id: {0}, c_id: {1}, total_assets: {2}, total_equity: {3}, total_sales: {4}, total_profit: {5}, prime_busprofit: {6}, retained_profit: {7}, total_tax: {8}, total_liability: {9}, report_year: {10}, KEY: {11}".format(
#             self.id, self.c_id, self.total_assets, self.total_equity, self.total_sales, self.total_profit,
#             self.prime_busprofit, self.retained_profit, self.total_tax, self.total_liability, self.report_year,
#             self.KEY)


# 定义对象:
# class YearReportSocialSecurity(Base):
#     # 表的名字:
#     __tablename__ = 'year_report_social_security'
#     # 表的结构:
#     id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
#     c_id = Column(Integer, ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
#     endowment_insurance = Column(String(28))
#     medical_insurance = Column(String(28))
#     maternit_insurance = Column(String(28))
#     unemployment_insurance = Column(String(28))
#     employmentinjury_insurance = Column(String(28))
#     endowment_insurance_base = Column(String(64))
#     medical_insurance_base = Column(String(64))
#     maternit_insurance_base = Column(String(64))
#     unemployment_insurance_base = Column(String(64))
#     employmentinjury_insurance_base = Column(String(64))
#     endowment_insurance_payamount = Column(String(64))
#     medical_insurance_payamount = Column(String(64))
#     maternit_insurance_payamount = Column(String(64))
#     unemployment_insurance_payamount = Column(String(64))
#     employmentinjury_insurance_payamount = Column(String(64))
#     endowment_insurance_oweamount = Column(String(64))
#     medical_insurance_oweamount = Column(String(64))
#     maternit_insurance_oweamount = Column(String(64))
#     unemployment_insurance_oweamount = Column(String(64))
#     employmentinjury_insurance_oweamount = Column(String(64))
#     report_year = Column(String(28))
#
#     baseInfo = relationship("BaseInfo",
#                             backref=backref('yearReportSocialSecurityRel', order_by=id, cascade="all, delete-orphan"))
#
#     def __repr__(self):
#         return "id: {0}, c_id: {1}, endowment_insurance: {2}, medical_insurance: {3}, maternit_insurance: {4}, unemployment_insurance: {5}, employmentinjury_insurance: {6}, endowment_insurance_base: {7}, medical_insurance_base: {8}, maternit_insurance_base: {9}, unemployment_insurance_base: {10}, employmentinjury_insurance_base: {11}, endowment_insurance_payamount: {12}, medical_insurance_payamount: {13}, maternit_insurance_payamount: {14}, unemployment_insurance_payamount: {15}, employmentinjury_insurance_payamount: {16}, endowment_insurance_oweamount: {17}, medical_insurance_oweamount: {18}, maternit_insurance_oweamount: {19}, unemployment_insurance_oweamount: {20}, employmentinjury_insurance_oweamount: {21}, report_year: {22}, KEY: {23}".format(
#             self.id, self.c_id, self.endowment_insurance, self.medical_insurance, self.maternit_insurance,
#             self.unemployment_insurance, self.employmentinjury_insurance, self.endowment_insurance_base,
#             self.medical_insurance_base, self.maternit_insurance_base, self.unemployment_insurance_base,
#             self.employmentinjury_insurance_base, self.endowment_insurance_payamount, self.medical_insurance_payamount,
#             self.maternit_insurance_payamount, self.unemployment_insurance_payamount,
#             self.employmentinjury_insurance_payamount, self.endowment_insurance_oweamount,
#             self.medical_insurance_oweamount, self.maternit_insurance_oweamount, self.unemployment_insurance_oweamount,
#             self.employmentinjury_insurance_oweamount, self.report_year, self.KEY)


# 定义对象:
# class YearReportStore(Base):
#     # 表的名字:
#     __tablename__ = 'year_report_store'
#     # 表的结构:
#     id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
#     c_id = Column(Integer, ForeignKey("C_BASIC_INFO.COMPANY_ID", ondelete="CASCADE"), nullable=False)
#     web_name = Column(String(64))
#     web_type = Column(String(28))
#     web_site = Column(String(255))
#     report_year = Column(String(28))
#
#     baseInfo = relationship("BaseInfo",
#                             backref=backref('yearReportStoreRel', order_by=id, cascade="all, delete-orphan"))
#
#     def __repr__(self):
#         return "id: {0}, c_id: {1}, web_name: {2}, web_type: {3}, web_site: {4}, report_year: {5}, KEY: {6}".format(
#             self.id, self.c_id, self.web_name, self.web_type, self.web_site, self.report_year, self.KEY)
