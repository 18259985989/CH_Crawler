# 导入:
from sqlalchemy import ForeignKey, Column, Integer, String, \
    DateTime, Text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义对象:
class Abnormal(Base):
    # 表的名字:
    __tablename__ = 'abnormal'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    put_date = Column(DateTime)
    put_reason = Column(String(100))
    put_department = Column(String(50))
    remove_date = Column(DateTime)
    remove_reason = Column(Text)
    remove_department = Column(String(50))

    baseInfo = relationship("BaseInfo", backref=backref('abnormalRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, put_date: {2}, put_reason: {3}, put_department: {4}, remove_date: {5}, remove_reason: {6}, remove_department: {7}".format(
            self.id,
            self.c_id,
            self.put_date,
            self.put_reason,
            self.put_department,
            self.remove_date,
            self.remove_reason,
            self.remove_department)


# 定义对象:
class BaseInfo(Base):
    # 表的名字:
    __tablename__ = 'base_info'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    Enterprise_name = Column(String(120), nullable=False)
    Enterprise_tyshxydm = Column(String(32))
    Legalrepresentative = Column(String(120))
    Enterprise_zzjgdm = Column(String(32))
    Enterprise_gszch = Column(String(32))
    rtime = Column(DateTime)
    registered_address = Column(String(255))
    gslx = Column(String(64))
    jyzt = Column(String(32))
    op_from = Column(DateTime)
    op_to = Column(DateTime)
    approval_date = Column(DateTime)
    djjg = Column(String(126))
    f_body = Column(LONGTEXT)
    cancel_date = Column(DateTime)
    reasons_cancel = Column(LONGTEXT)
    zczb = Column(String(32))
    paid_in_capital = Column(String(32))
    ygrs = Column(String(32))
    social_staff_num = Column(String(32))
    industry = Column(String(32))
    Contact_number = Column(String(64))
    email = Column(String(64))
    z_body = Column(LONGTEXT)
    source_update_time = Column(DateTime)
    local_update_time = Column(DateTime)
    score = Column(String(64))
    logo = Column(String(255))

    def __repr__(self):
        return "id: {0}, Enterprise_name: {1}, Enterprise_tyshxydm: {2}, Legalrepresentative: {3}, Enterprise_zzjgdm: {4}, Enterprise_gszch: {5}, rtime: {6}, registered_address: {7}, gslx: {8}, jyzt: {9}, op_from: {10}, op_to: {11}, approval_date: {12}, djjg: {13}, f_body: {14}, cancel_date: {15}, reasons_cancel: {16}, zczb: {17}, paid_in_capital: {18}, ygrs: {19}, social_staff_num: {20}, industry: {21}, Contact_number: {22}, email: {23}, z_body: {24}, source_update_time: {25}, local_update_time: {26}, score: {27}".format(
            self.id, self.Enterprise_name, self.Enterprise_tyshxydm, self.Legalrepresentative, self.Enterprise_zzjgdm,
            self.Enterprise_gszch, self.rtime,
            self.registered_address, self.gslx, self.jyzt, self.op_from, self.op_to, self.approval_date, self.djjg,
            self.f_body, self.cancel_date, self.reasons_cancel,
            self.zczb, self.paid_in_capital, self.ygrs, self.social_staff_num, self.industry, self.Contact_number,
            self.email, self.z_body, self.source_update_time,
            self.local_update_time, self.score)


# 定义对象:
class BidInfo(Base):
    # 表的名字:
    __tablename__ = 'bid_info'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    title = Column(Text)
    publish_date = Column(DateTime)
    purchaser = Column(String(255))
    proxy = Column(String(100))
    content = Column(LONGTEXT)

    baseInfo = relationship("BaseInfo", backref=backref('bidInfoRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, title: {2}, publish_date: {3}, purchaser: {4}, proxy: {5}, content: {6}".format(
            self.id, self.c_id, self.title, self.publish_date,
            self.purchaser, self.proxy, self.content)


# 定义对象:
class Branch(Base):
    # 表的名字:
    __tablename__ = 'branch'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    branch_name = Column(String(120))
    credit_code = Column(String(64))
    Enterprise_gszch = Column(String(32))
    reg_authority = Column(String(64))
    legal_person = Column(String(64))
    industry = Column(String(64))
    estiblish_date = Column(DateTime)
    business_state = Column(String(32))

    baseInfo = relationship("BaseInfo", backref=backref('branchRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, branch_name: {2}, credit_code: {3}, Enterprise_gszch: {4}, reg_authority: {5}, legal_person: {6}, industry: {7}, estiblish_date: {8}, business_state: {9}".format(
            self.id, self.c_id, self.branch_name, self.credit_code, self.Enterprise_gszch, self.reg_authority,
            self.legal_person, self.industry, self.estiblish_date,
            self.business_state)


# 定义对象:
class ChangeInfo(Base):
    # 表的名字:
    __tablename__ = 'change_info'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    change_item = Column(Text)
    before_change = Column(Text)
    after_change = Column(Text)
    change_date = Column(DateTime)

    baseInfo = relationship("BaseInfo", backref=backref('changeInfoRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, change_item: {2}, before_change: {3}, after_change: {4}, change_date: {5}".format(
            self.id, self.c_id, self.change_item,
            self.before_change, self.after_change,
            self.change_date)


# 定义对象:
class CheckInfo(Base):
    # 表的名字:
    __tablename__ = 'check_info'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    check_authority = Column(String(64))
    check_date = Column(DateTime)
    check_result = Column(Text)
    check_type = Column(String(64))

    baseInfo = relationship("BaseInfo", backref=backref('checkInfoRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, check_authority: {2}, check_date: {3}, check_result: {4}, check_type: {5}".format(
            self.id, self.c_id, self.check_authority,
            self.check_date, self.check_result, self.check_type)


# 定义对象:
class CompanyMortgage(Base):
    # 表的名字:
    __tablename__ = 'company_mortgage'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    mortgage_name = Column(String(64))
    licence_type = Column(String(64))
    identify_number = Column(String(64))
    mortgage_type = Column(String(62))
    address = Column(String(255))
    reg_number = Column(String(50))
    reg_date = Column(DateTime)
    reg_authority = Column(String(50))
    guaranteed_amount = Column(String(50))
    public_date = Column(String(25))
    currency = Column(String(25))
    cancel_date = Column(String(25))
    cancel_authority = Column(String(255))
    cancel_reason = Column(String(80))
    warrant_type = Column(String(25))
    term = Column(String(25))
    scope = Column(String(255))
    status = Column(String(28))
    note = Column(Text)

    baseInfo = relationship("BaseInfo",
                            backref=backref('companyMortgageRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, mortgage_name: {2}, licence_type: {3}, identify_number: {4}, mortgage_type: {5}, address: {6}, reg_number: {7}, reg_date: {8}, reg_authority: {9}, guaranteed_amount: {10}, public_date: {11}, currency: {12}, cancel_date: {13}, cancel_authority: {14}, cancel_reason: {15}, warrant_type: {16}, term: {17}, scope: {18}, status: {19}, note: {20}".format(
            self.id, self.c_id, self.mortgage_name, self.licence_type, self.identify_number, self.mortgage_type,
            self.address, self.reg_number, self.reg_date,
            self.reg_authority, self.guaranteed_amount, self.public_date, self.currency, self.cancel_date,
            self.cancel_authority, self.cancel_reason, self.warrant_type,
            self.term, self.scope, self.status, self.note)


# 定义对象:
class CompanyMortgageChange(Base):
    # 表的名字:
    __tablename__ = 'company_mortgage_change'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    reg_id = Column(String(32), ForeignKey("company_mortgage.reg_number", ondelete="CASCADE"), nullable=False)
    change_date = Column(DateTime)
    change_content = Column(Text)

    companyMortgage = relationship("CompanyMortgage", backref=backref('companyMortgageChangeRel', order_by=id,
                                                                      cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, reg_id: {1}, change_date: {2}, change_content: {3}".format(self.id, self.reg_id,
                                                                                    self.change_date,
                                                                                    self.change_content)


# 定义对象:
class CompanyMortgageCollateral(Base):
    # 表的名字:
    __tablename__ = 'company_mortgage_collateral'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    reg_id = Column(String(32), ForeignKey("company_mortgage.reg_number", ondelete="CASCADE"), nullable=False)
    collateral = Column(String(255))
    belong = Column(String(120))
    summary = Column(LONGTEXT)

    companyMortgage = relationship("CompanyMortgage", backref=backref('companyMortgageCollateralRel', order_by=id,
                                                                      cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, reg_id: {1}, collateral: {2}, belong: {3}, summary: {4}".format(self.id, self.reg_id,
                                                                                         self.collateral, self.belong,
                                                                                         self.summary)


# 定义对象:
class CompanyMortgagePledgee(Base):
    # 表的名字:
    __tablename__ = 'company_mortgage_pledgee'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    reg_id = Column(String(32), ForeignKey("company_mortgage.reg_number", ondelete="CASCADE"), nullable=False)
    people_name = Column(String(64))
    licence_type = Column(String(32))
    identify_number = Column(String(32))
    address = Column(String(255))

    companyMortgage = relationship("CompanyMortgage", backref=backref('companyMortgagePledgeeRel', order_by=id,
                                                                      cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, reg_id: {1}, people_name: {2}, licence_type: {3}, identify_number: {4}, address: {5}".format(
            self.id, self.reg_id, self.people_name,
            self.licence_type, self.identify_number,
            self.address)


# 定义对象:
class CopyrightSoftware(Base):
    # 表的名字:
    __tablename__ = 'copyright_software'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    software_name = Column(String(162))
    reg_number = Column(String(32))
    work_type = Column(String(32))
    finish_date = Column(String(32))
    publish_date = Column(DateTime)
    reg_date = Column(DateTime)
    simple_name = Column(String(162))
    cat_number = Column(String(64))
    version = Column(String(24))
    author = Column(Text)

    baseInfo = relationship("BaseInfo",
                            backref=backref('copyrightSoftwareRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, software_name: {2}, reg_number: {3}, work_type: {4}, finish_date: {5}, publish_date: {6}, reg_date: {7}, simple_name: {8}, cat_number: {9}, version: {10}, author: {11}".format(
            self.id, self.c_id, self.software_name, self.reg_number, self.work_type, self.finish_date,
            self.publish_date, self.reg_date, self.simple_name,
            self.cat_number, self.version, self.author)


# 定义对象:
class CopyrightWork(Base):
    # 表的名字:
    __tablename__ = 'copyright_work'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    work_name = Column(String(255))
    reg_number = Column(String(255))
    work_type = Column(String(255))
    finish_date = Column(DateTime)
    publish_date = Column(DateTime)
    reg_date = Column(DateTime)
    author = Column(String(255))

    baseInfo = relationship("BaseInfo", backref=backref('copyrightWorkRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, work_name: {2}, reg_number: {3}, work_type: {4}, finish_date: {5}, publish_date: {6}, reg_date: {7}, author: {8}".format(
            self.id,
            self.c_id,
            self.work_name,
            self.reg_number,
            self.work_type,
            self.finish_date,
            self.publish_date,
            self.reg_date,
            self.author)


# 定义对象:
class CourtAuto(Base):
    # 表的名字:
    __tablename__ = 'court_auto'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    start_date = Column(String(50))
    case_reason = Column(Text)
    case_number = Column(String(255))
    litigant = Column(Text)
    plaintiff = Column(Text)
    defendant = Column(Text)
    court = Column(String(255))
    courtroom = Column(String(255))

    baseInfo = relationship("BaseInfo", backref=backref('courtAutoRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, start_date: {2}, case_reason: {3}, case_number: {4}, litigant: {5}, plaintiff: {6}, defendant: {7}, court: {8}, courtroom: {9}".format(
            self.id, self.c_id, self.start_date, self.case_reason, self.case_number, self.litigant, self.plaintiff,
            self.defendant, self.court, self.courtroom)


# 定义对象:
class CourtNotice(Base):
    # 表的名字:
    __tablename__ = 'court_notice'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    litigant = Column(Text)
    announce_type = Column(LONGTEXT)
    publish_date = Column(DateTime)
    publish_page = Column(String(32))
    appellant = Column(String(126))
    court = Column(String(32))
    content = Column(LONGTEXT)
    province = Column(String(32))
    announce_num = Column(String(64))

    baseInfo = relationship("BaseInfo", backref=backref('courtNoticeRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, litigant: {2}, announce_type: {3}, publish_date: {4}, publish_page: {5}, appellant: {6}, court: {7}, content: {8}, province: {9}, announce_num: {10}".format(
            self.id, self.c_id, self.litigant, self.announce_type, self.publish_date, self.publish_page, self.appellant,
            self.court, self.content, self.province,
            self.announce_num)


# 定义对象:
class DishonestInfo(Base):
    # 表的名字:
    __tablename__ = 'dishonest_info'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    ent_name = Column(String(120))
    card_number = Column(String(32))
    area = Column(String(64))
    reg_date = Column(DateTime)
    publish_date = Column(DateTime)
    gist_unit = Column(String(64))
    court = Column(String(64))
    gist_num = Column(String(86))
    case_code = Column(String(32))
    duty = Column(Text)
    performance = Column(Text)
    disrupttype_name = Column(Text)

    baseInfo = relationship("BaseInfo", backref=backref('dishonestInfoRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, ent_name: {2}, card_number: {3}, area: {4}, reg_date: {5}, publish_date: {6}, gist_unit: {7}, court: {8}, gist_num: {9}, case_code: {10}, duty: {11}, performance: {12}, disrupttype_name: {13}".format(
            self.id, self.c_id, self.ent_name, self.card_number, self.area, self.reg_date, self.publish_date,
            self.gist_unit, self.court, self.gist_num, self.case_code,
            self.duty, self.performance, self.disrupttype_name)


# 定义对象:
class EquityChange(Base):
    # 表的名字:
    __tablename__ = 'equity_change'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    shareholder = Column(String(32))
    alt_date = Column(String(24))
    trans_before = Column(String(24))
    trans_after = Column(String(24))
    publish_date = Column(String(32))

    baseInfo = relationship("BaseInfo", backref=backref('equityChangeRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, shareholder: {2}, alt_date: {3}, trans_before: {4}, trans_after: {5}, publish_date: {6}".format(
            self.id, self.c_id, self.shareholder,
            self.alt_date, self.trans_before,
            self.trans_after, self.publish_date)


# 定义对象:
class EquityPledge(Base):
    # 表的名字:
    __tablename__ = 'equity_pledge'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    reg_number = Column(String(50))
    reg_date = Column(String(25))
    pledgor = Column(String(100))
    pledge_equity = Column(String(25))
    pledgee = Column(String(100))
    pledgee_type = Column(String(25))
    state = Column(String(25))
    currency = Column(String(25))
    cancel_date = Column(String(25))
    cancel_reason = Column(String(50))
    certif_number_gor = Column(String(50))
    certif_number_gee = Column(String(50))

    baseInfo = relationship("BaseInfo", backref=backref('equityPledgeRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, reg_number: {2}, reg_date: {3}, pledgor: {4}, pledge_equity: {5}, pledgee: {6}, pledgee_type: {7}, state: {8}, currency: {9}, cancel_date: {10}, cancel_reason: {11}, certif_number_gor: {12}, certif_number_gee: {13}".format(
            self.id, self.c_id, self.reg_number, self.reg_date, self.pledgor, self.pledge_equity, self.pledgee,
            self.pledgee_type, self.state, self.currency,
            self.cancel_date, self.cancel_reason, self.certif_number_gor, self.certif_number_gee)


# 定义对象:
class IllegalInfo(Base):
    # 表的名字:
    __tablename__ = 'illegal_info'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    put_date = Column(DateTime)
    put_reason = Column(Text)
    put_department = Column(String(64))
    remove_date = Column(DateTime)
    remove_reason = Column(Text)
    remove_department = Column(String(64))

    baseInfo = relationship("BaseInfo", backref=backref('illegalInfoRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, put_date: {2}, put_reason: {3}, put_department: {4}, remove_date: {5}, remove_reason: {6}, remove_department: {7}".format(
            self.id,
            self.c_id,
            self.put_date,
            self.put_reason,
            self.put_department,
            self.remove_date,
            self.remove_reason,
            self.remove_department)


# 定义对象:
class ImExportBase(Base):
    # 表的名字:
    __tablename__ = 'im_export_base'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    crcode = Column(String(64))
    record_date = Column(DateTime)
    customs_registered_address = Column(String(64))
    administrative_division = Column(String(128))
    economic_division = Column(String(64))
    management_category = Column(String(64))
    special_trade_area = Column(String(64))
    industry_category = Column(String(64))
    validity_date = Column(DateTime)
    status = Column(String(64))
    annual_report = Column(String(64))
    types = Column(String(255))

    baseInfo = relationship("BaseInfo", backref=backref('imExportBaseRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, crcode: {2}, record_date: {3}, customs_registered_address: {4}, administrative_division: {5}, economic_division: {6}, management_category: {7}, special_trade_area: {8}, industry_category: {9}, validity_date: {10}, status: {11}, annual_report: {12}, types: {13}".format(
            self.id, self.c_id, self.crcode, self.record_date, self.customs_registered_address,
            self.administrative_division, self.economic_division,
            self.management_category, self.special_trade_area, self.industry_category, self.validity_date, self.status,
            self.annual_report, self.types)


# 定义对象:
class ImExportCredit(Base):
    # 表的名字:
    __tablename__ = 'im_export_credit'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    credit_rating = Column(String(48))
    authentication_code = Column(String(255))
    identification_time = Column(DateTime)

    baseInfo = relationship("BaseInfo", backref=backref('imExportCreditRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, credit_rating: {2}, authentication_code: {3}, identification_time: {4}".format(
            self.id, self.c_id, self.credit_rating,
            self.authentication_code, self.identification_time)


# 定义对象:
class ImExportPunish(Base):
    # 表的名字:
    __tablename__ = 'im_export_punish'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    decision_number = Column(String(28))
    penalty_date = Column(DateTime)
    party = Column(String(255))
    nature_of_case = Column(String(64))

    baseInfo = relationship("BaseInfo", backref=backref('imExportPunishRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, decision_number: {2}, penalty_date: {3}, party: {4}, nature_of_case: {5}".format(
            self.id, self.c_id, self.decision_number,
            self.penalty_date, self.party, self.nature_of_case)


# 定义对象:
class Invest(Base):
    # 表的名字:
    __tablename__ = 'invest'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    ent_name = Column(String(50))
    credit_code = Column(String(50))
    invest_amount = Column(String(25))
    invest_percent = Column(String(25))
    ent_type = Column(String(255))
    business_scope = Column(Text)
    business_state = Column(String(50))
    alias = Column(String(25))
    estiblish_date = Column(String(25))
    legal_person = Column(String(50))
    industry = Column(String(50))
    reg_capital = Column(String(50))
    state = Column(String(50))

    baseInfo = relationship("BaseInfo", backref=backref('investRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, ent_name: {2}, credit_code: {3}, invest_amount: {4}, invest_percent: {5}, ent_type: {6}, business_scope: {7}, business_state: {8}, alias: {9}, estiblish_date: {10}, legal_person: {11}, industry: {12}, reg_capital: {13}, state: {14}".format(
            self.id, self.c_id, self.ent_name, self.credit_code, self.invest_amount, self.invest_percent, self.ent_type,
            self.business_scope, self.business_state,
            self.alias, self.estiblish_date, self.legal_person, self.industry, self.reg_capital, self.state)


# 定义对象:
class JudicialAssistance(Base):
    # 表的名字:
    __tablename__ = 'judicial_assistance'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    public_date = Column(DateTime)
    executed = Column(String(64))
    equity_amount = Column(String(32))
    equity_state = Column(String(16))
    execute_notice = Column(String(255))
    execute_court = Column(String(86))
    execute_list = Column(Text)
    execute_order = Column(String(32))
    license_type = Column(String(32))
    license_number = Column(String(32))
    from_date = Column(DateTime)
    to_date = Column(DateTime)
    period = Column(String(64))

    baseInfo = relationship("BaseInfo",
                            backref=backref('judicialAssistanceRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, public_date: {2}, executed: {3}, equity_amount: {4}, equity_state: {5}, execute_notice: {6}, execute_court: {7}, execute_list: {8}, execute_order: {9}, license_type: {10}, license_number: {11}, from_date: {12}, to_date: {13}, period: {14}".format(
            self.id, self.c_id, self.public_date, self.executed, self.equity_amount, self.equity_state,
            self.execute_notice, self.execute_court, self.execute_list,
            self.execute_order, self.license_type, self.license_number, self.from_date, self.to_date, self.period)


# 定义对象:
class JudicialSale(Base):
    # 表的名字:
    __tablename__ = 'judicial_sale'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255))
    title_money = Column(String(255))
    court = Column(String(255))
    public_date = Column(DateTime)
    initial_price = Column(String(25))
    consult_price = Column(String(25))

    baseInfo = relationship("BaseInfo", backref=backref('judicialSaleRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, title: {2}, title_money: {3}, court: {4}, public_date: {5}, initial_price: {6}, consult_price: {7}".format(
            self.id, self.c_id,
            self.title,
            self.title_money,
            self.court,
            self.public_date,
            self.initial_price,
            self.consult_price)


# 定义对象:
class LawsuitBasic(Base):
    # 表的名字:
    __tablename__ = 'lawsuit_basic'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255))
    case_type = Column(String(64))
    submittime = Column(DateTime)
    casereason = Column(String(64))
    plaintiff = Column(Text)
    defendants = Column(Text)
    caseno = Column(String(255))
    lawsuit_detail = Column(LONGTEXT)

    baseInfo = relationship("BaseInfo", backref=backref('lawsuitBasicRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, title: {2}, case_type: {3}, submittime: {4}, casereason: {5}, plaintiff: {6}, defendants: {7}, caseno: {8}, lawsuit_detail: {9}".format(
            self.id, self.c_id, self.title, self.case_type, self.submittime, self.casereason, self.plaintiff,
            self.defendants, self.caseno, self.lawsuit_detail)


# 定义对象:
class LicenceInfo(Base):
    # 表的名字:
    __tablename__ = 'licence_info'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    licence_number = Column(String(255))
    licence_name = Column(String(255))
    licence_anth = Column(String(64))
    from_date = Column(DateTime)
    to_date = Column(DateTime)
    licence_content = Column(Text)
    legal_person = Column(String(64))
    audit_type = Column(String(64))

    baseInfo = relationship("BaseInfo", backref=backref('licenceInfoRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, licence_number: {2}, licence_name: {3}, licence_anth: {4}, from_date: {5}, to_date: {6}, licence_content: {7}, legal_person: {8}, audit_type: {9}".format(
            self.id, self.c_id, self.licence_number, self.licence_name, self.licence_anth, self.from_date, self.to_date,
            self.licence_content, self.legal_person,
            self.audit_type)


# 定义对象:
class Members(Base):
    # 表的名字:
    __tablename__ = 'members'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    person_name = Column(String(64))
    position = Column(String(64))

    baseInfo = relationship("BaseInfo", backref=backref('membersRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, person_name: {2}, position: {3}".format(self.id, self.c_id, self.person_name,
                                                                            self.position)


# 定义对象:
class OwingTax(Base):
    # 表的名字:
    __tablename__ = 'owing_tax'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    tax_id_number = Column(String(64))
    publish_date = Column(DateTime)
    tax_category = Column(String(64))
    own_tax_balance = Column(String(64))
    new_own_tax_balance = Column(String(64))
    department = Column(String(128))

    baseInfo = relationship("BaseInfo", backref=backref('owingTaxRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, tax_id_number: {2}, publish_date: {3}, tax_category: {4}, own_tax_balance: {5}, new_own_tax_balance: {6}, department: {7}".format(
            self.id, self.c_id, self.tax_id_number, self.publish_date, self.tax_category, self.own_tax_balance,
            self.new_own_tax_balance, self.department)


# 定义对象:
class Patent(Base):
    # 表的名字:
    __tablename__ = 'patent'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    patent_name = Column(Text)
    apply_number = Column(String(50))
    pub_number = Column(String(50))
    cat_number = Column(String(50))
    apply_date = Column(String(25))
    app_publish_date = Column(String(25))
    applicant_name = Column(String(128))
    inventor = Column(String(256))
    agent = Column(String(64))
    agency = Column(String(128))
    address = Column(Text)
    abstracts = Column(Text)
    img_url = Column(String(128))

    baseInfo = relationship("BaseInfo", backref=backref('patentRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, patent_name: {2}, apply_number: {3}, pub_number: {4}, cat_number: {5}, apply_date: {6}, app_publish_date: {7}, applicant_name: {8}, inventor: {9}, agent: {10}, agency: {11}, address: {12}, abstracts: {13}, img_url: {14}".format(
            self.id, self.c_id, self.patent_name, self.apply_number, self.pub_number, self.cat_number, self.apply_date,
            self.app_publish_date, self.applicant_name,
            self.inventor, self.agent, self.agency, self.address, self.abstracts, self.img_url)


# 定义对象:
class Pledgereg(Base):
    # 表的名字:
    __tablename__ = 'pledgereg'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    reg_number = Column(Integer)
    ent_name = Column(String(255))
    kinds = Column(String(255))
    pledgor_name = Column(String(255))
    pledge_from = Column(DateTime)
    pledge_to = Column(DateTime)
    public_date = Column(DateTime)
    tm_name = Column(String(255))
    state = Column(String(255))
    pledgee_name = Column(String(255))

    baseInfo = relationship("BaseInfo", backref=backref('pledgeregRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, reg_number: {2}, ent_name: {3}, kinds: {4}, pledgor_name: {5}, pledge_from: {6}, pledge_to: {7}, public_date: {8}, tm_name: {9}, state: {10}, pledgee_name: {11}".format(
            self.id, self.c_id, self.reg_number, self.ent_name, self.kinds, self.pledgor_name, self.pledge_from,
            self.pledge_to, self.public_date, self.tm_name,
            self.state, self.pledgee_name)


# 定义对象:
class Product(Base):
    # 表的名字:
    __tablename__ = 'product'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    app_name = Column(String(50))
    filter_name = Column(String(25))
    classes = Column(String(25))
    brief = Column(Text)
    icon = Column(String(255))
    pro_type = Column(String(50))

    baseInfo = relationship("BaseInfo", backref=backref('productRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, app_name: {2}, filter_name: {3}, classes: {4}, brief: {5}, icon: {6}, pro_type: {7}".format(
            self.id, self.c_id, self.app_name,
            self.filter_name, self.classes,
            self.brief, self.icon, self.pro_type)


# 定义对象:
class Punishment(Base):
    # 表的名字:
    __tablename__ = 'punishment'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    penish_dec_num = Column(Text)
    illeg_type = Column(Text)
    punish_content = Column(LONGTEXT)
    punish_auth = Column(String(100))
    decision_date = Column(DateTime)
    punish_name = Column(String(100))
    punish_type = Column(String(80))
    punish_type_second = Column(String(80))
    evidence = Column(Text)

    baseInfo = relationship("BaseInfo", backref=backref('punishmentRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, penish_dec_num: {2}, illeg_type: {3}, punish_content: {4}, punish_auth: {5}, decision_date: {6}, punish_name: {7}, punish_type: {8}, punish_type_second: {9}, evidence: {10}".format(
            self.id, self.c_id, self.penish_dec_num, self.illeg_type, self.punish_content, self.punish_auth,
            self.decision_date, self.punish_name, self.punish_type,
            self.punish_type_second, self.evidence)


# 定义对象:
class Qualification(Base):
    # 表的名字:
    __tablename__ = 'qualification'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    certificate_name = Column(String(50))
    cert_number = Column(String(50))
    start_date = Column(String(25))
    end_date = Column(String(25))

    baseInfo = relationship("BaseInfo", backref=backref('qualificationRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, certificate_name: {2}, cert_number: {3}, start_date: {4}, end_date: {5}".format(
            self.id, self.c_id, self.certificate_name,
            self.cert_number, self.start_date, self.end_date)


# 定义对象:
class Shareholder(Base):
    # 表的名字:
    __tablename__ = 'shareholder'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    shareholder = Column(String(86))
    shareholder_type = Column(String(32))
    blic_type = Column(String(32))
    blic_number = Column(String(32))
    ent_type = Column(String(64))
    con_capital = Column(String(32))
    con_capital_date = Column(DateTime)
    con_paid_in_capital = Column(String(32))
    paid_in_capital_date = Column(DateTime)
    share_ratio = Column(String(32))
    currency = Column(String(255))
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)

    baseInfo = relationship("BaseInfo", backref=backref('shareholderRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, shareholder: {1}, shareholder_type: {2}, blic_type: {3}, blic_number: {4}, ent_type: {5}, con_capital: {6}, con_capital_date: {7}, con_paid_in_capital: {8}, paid_in_capital_date: {9}, share_ratio: {10}, currency: {11}, c_id: {12}".format(
            self.id, self.shareholder, self.shareholder_type, self.blic_type, self.blic_number, self.ent_type,
            self.con_capital, self.con_capital_date,
            self.con_paid_in_capital, self.paid_in_capital_date, self.share_ratio, self.currency, self.c_id)


# 定义对象:
class Taxcred(Base):
    # 表的名字:
    __tablename__ = 'taxcred'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    id_number = Column(String(50))
    years = Column(String(50))
    eval_department = Column(String(86))
    grade = Column(String(25))
    eval_type = Column(String(25))

    baseInfo = relationship("BaseInfo", backref=backref('taxcredRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, id_number: {2}, years: {3}, eval_department: {4}, grade: {5}, eval_type: {6}".format(
            self.id, self.c_id, self.id_number, self.years,
            self.eval_department, self.grade, self.eval_type)


# 定义对象:
class TmInfo(Base):
    # 表的名字:
    __tablename__ = 'tm_info'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    tm_name = Column(String(255))
    reg_number = Column(String(20))
    tm_type = Column(String(25))
    reg_annc_date = Column(String(255))
    reg_annc_issue = Column(String(255))
    property_bgn_date = Column(String(255))
    property_end_date = Column(String(255))
    goods_name = Column(Text)
    apply_date = Column(String(255))
    state = Column(String(255))
    applicant = Column(String(255))
    apply_process = Column(Text)
    pic_url = Column(String(255))

    baseInfo = relationship("BaseInfo", backref=backref('tmInfoRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, tm_name: {2}, reg_number: {3}, tm_type: {4}, reg_annc_date: {5}, reg_annc_issue: {6}, property_bgn_date: {7}, property_end_date: {8}, goods_name: {9}, apply_date: {10}, state: {11}, applicant: {12}, apply_process: {13}, pic_url: {14}".format(
            self.id, self.c_id, self.tm_name, self.reg_number, self.tm_type, self.reg_annc_date, self.reg_annc_issue,
            self.property_bgn_date, self.property_end_date,
            self.goods_name, self.apply_date, self.state, self.applicant, self.apply_process, self.pic_url)


# 定义对象:
class ToExecute(Base):
    # 表的名字:
    __tablename__ = 'to_execute'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    executed = Column(String(64))
    org_code = Column(String(32))
    exec_money = Column(String(32))
    exec_court = Column(String(32))
    case_create_date = Column(DateTime)
    publish_date = Column(DateTime)
    case_number = Column(String(32))
    sex = Column(String(16))
    province = Column(String(16))
    gist_num = Column(String(255))
    gist_unit = Column(String(64))
    duty = Column(Text)
    performance = Column(Text)
    disrupttype_name = Column(Text)
    end_date = Column(DateTime)
    unexectued = Column(Text)
    legal_person = Column(String(64))

    baseInfo = relationship("BaseInfo", backref=backref('toExecuteRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, executed: {2}, org_code: {3}, exec_money: {4}, exec_court: {5}, case_create_date: {6}, publish_date: {7}, case_number: {8}, sex: {9}, province: {10}, gist_num: {11}, gist_unit: {12}, duty: {13}, performance: {14}, disrupttype_name: {15}, end_date: {16}, unexectued: {17}, legal_person: {18}".format(
            self.id, self.c_id, self.executed, self.org_code, self.exec_money, self.exec_court, self.case_create_date,
            self.publish_date, self.case_number, self.sex,
            self.province, self.gist_num, self.gist_unit, self.duty, self.performance, self.disrupttype_name,
            self.end_date, self.unexectued, self.legal_person)


# 定义对象:
class WebsiteInfo(Base):
    # 表的名字:
    __tablename__ = 'website_info'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    web_name = Column(String(64))
    web_site = Column(String(255))
    examine_date = Column(DateTime)
    liscense = Column(String(32))
    company_type = Column(String(32))
    ym = Column(String(112))

    baseInfo = relationship("BaseInfo", backref=backref('websiteInfoRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, web_name: {2}, web_site: {3}, examine_date: {4}, liscense: {5}, company_type: {6}, ym: {7}".format(
            self.id, self.c_id, self.web_name,
            self.web_site, self.examine_date,
            self.liscense, self.company_type,
            self.ym)


# 定义对象:
class YearReport(Base):
    # 表的名字:
    __tablename__ = 'year_report'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    company_name = Column(String(64))
    report_year = Column(String(28))
    reg_number = Column(String(28))
    manage_state = Column(String(28))
    employee_num = Column(String(64))
    phone_number = Column(Text)
    email = Column(String(64))
    postal_address = Column(String(255))
    postcode = Column(String(28))

    baseInfo = relationship("BaseInfo", backref=backref('yearReportRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, company_name: {2}, report_year: {3}, reg_number: {4}, manage_state: {5}, employee_num: {6}, phone_number: {7}, email: {8}, postal_address: {9}, postcode: {10}".format(
            self.id, self.c_id, self.company_name, self.report_year, self.reg_number, self.manage_state,
            self.employee_num, self.phone_number, self.email,
            self.postal_address, self.postcode)


# 定义对象:
class YearReportAssert(Base):
    # 表的名字:
    __tablename__ = 'year_report_assert'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    total_assets = Column(String(64))
    total_equity = Column(String(64))
    total_sales = Column(String(64))
    total_profit = Column(String(64))
    prime_busprofit = Column(String(64))
    retained_profit = Column(String(64))
    total_tax = Column(String(64))
    total_liability = Column(String(64))
    report_year = Column(String(64))

    baseInfo = relationship("BaseInfo",
                            backref=backref('yearReportAssertRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, total_assets: {2}, total_equity: {3}, total_sales: {4}, total_profit: {5}, prime_busprofit: {6}, retained_profit: {7}, total_tax: {8}, total_liability: {9}, report_year: {10}".format(
            self.id, self.c_id, self.total_assets, self.total_equity, self.total_sales, self.total_profit,
            self.prime_busprofit, self.retained_profit, self.total_tax,
            self.total_liability, self.report_year)


# 定义对象:
class YearReportSocialSecurity(Base):
    # 表的名字:
    __tablename__ = 'year_report_social_security'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    endowment_insurance = Column(String(28))
    medical_insurance = Column(String(28))
    maternit_insurance = Column(String(28))
    unemployment_insurance = Column(String(28))
    employmentinjury_insurance = Column(String(28))
    endowment_insurance_base = Column(String(64))
    medical_insurance_base = Column(String(64))
    maternit_insurance_base = Column(String(64))
    unemployment_insurance_base = Column(String(64))
    employmentinjury_insurance_base = Column(String(64))
    endowment_insurance_payamount = Column(String(64))
    medical_insurance_payamount = Column(String(64))
    maternit_insurance_payamount = Column(String(64))
    unemployment_insurance_payamount = Column(String(64))
    employmentinjury_insurance_payamount = Column(String(64))
    endowment_insurance_oweamount = Column(String(64))
    medical_insurance_oweamount = Column(String(64))
    maternit_insurance_oweamount = Column(String(64))
    unemployment_insurance_oweamount = Column(String(64))
    employmentinjury_insurance_oweamount = Column(String(64))
    report_year = Column(String(28))

    baseInfo = relationship("BaseInfo",
                            backref=backref('yearReportSocialSecurityRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, endowment_insurance: {2}, medical_insurance: {3}, maternit_insurance: {4}, unemployment_insurance: {5}, employmentinjury_insurance: {6}, endowment_insurance_base: {7}, medical_insurance_base: {8}, maternit_insurance_base: {9}, unemployment_insurance_base: {10}, employmentinjury_insurance_base: {11}, endowment_insurance_payamount: {12}, medical_insurance_payamount: {13}, maternit_insurance_payamount: {14}, unemployment_insurance_payamount: {15}, employmentinjury_insurance_payamount: {16}, endowment_insurance_oweamount: {17}, medical_insurance_oweamount: {18}, maternit_insurance_oweamount: {19}, unemployment_insurance_oweamount: {20}, employmentinjury_insurance_oweamount: {21}, report_year: {22}".format(
            self.id, self.c_id, self.endowment_insurance, self.medical_insurance, self.maternit_insurance,
            self.unemployment_insurance, self.employmentinjury_insurance,
            self.endowment_insurance_base, self.medical_insurance_base, self.maternit_insurance_base,
            self.unemployment_insurance_base,
            self.employmentinjury_insurance_base, self.endowment_insurance_payamount, self.medical_insurance_payamount,
            self.maternit_insurance_payamount,
            self.unemployment_insurance_payamount, self.employmentinjury_insurance_payamount,
            self.endowment_insurance_oweamount, self.medical_insurance_oweamount,
            self.maternit_insurance_oweamount, self.unemployment_insurance_oweamount,
            self.employmentinjury_insurance_oweamount, self.report_year)


# 定义对象:
class YearReportStore(Base):
    # 表的名字:
    __tablename__ = 'year_report_store'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id", ondelete="CASCADE"), nullable=False)
    web_name = Column(String(64))
    web_type = Column(String(28))
    web_site = Column(String(255))
    report_year = Column(String(28))

    baseInfo = relationship("BaseInfo",
                            backref=backref('yearReportStoreRel', order_by=id, cascade="all, delete-orphan"))

    def __repr__(self):
        return "id: {0}, c_id: {1}, web_name: {2}, web_type: {3}, web_site: {4}, report_year: {5}".format(self.id,
                                                                                                          self.c_id,
                                                                                                          self.web_name,
                                                                                                          self.web_type,
                                                                                                          self.web_site,
                                                                                                          self.report_year)
