# 导入: 
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Float, Boolean, DECIMAL, Enum, Date, DateTime, Time, Text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类: 
Base = declarative_base()


# 定义对象: 
class ToExecute(Base):
    # 表的名字:
    __tablename__ = 'to_execute'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id"))
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

    # baseInfo = relationship("BaseInfo", backref = backref('baiduToExecuteRel', order_by = id))

    def __repr__(self):
        return "id: {0}, c_id: {1}, executed: {2}, org_code: {3}, exec_money: {4}, exec_court: {5}, case_create_date: {6}, publish_date: {7}, case_number: {8}, sex: {9}, province: {10}, gist_num: {11}, gist_unit: {12}, duty: {13}, performance: {14}, disrupttype_name: {15}, end_date: {16}, unexectued: {17}, legal_person: {18}".format(
            self.id, self.c_id, self.executed, self.org_code, self.exec_money, self.exec_court, self.case_create_date, self.publish_date, self.case_number, self.sex,
            self.province, self.gist_num, self.gist_unit, self.duty, self.performance, self.disrupttype_name, self.end_date, self.unexectued, self.legal_person)


# 定义对象:
class CourtNotice(Base):
    # 表的名字:
    __tablename__ = 'court_notice'
    # 表的结构:
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    c_id = Column(Integer, ForeignKey("base_info.id"))
    litigant = Column(Text)
    announce_type = Column(String(32))
    publish_date = Column(DateTime)
    publish_page = Column(String(32))
    appellant = Column(String(126))
    court = Column(String(32))
    content = Column(LONGTEXT)
    province = Column(String(32))
    announce_num = Column(String(64))

    # baseInfo = relationship("BaseInfo", backref = backref('courtNoticeRel', order_by = id))

    def __repr__(self):
        return "id: {0}, c_id: {1}, litigant: {2}, announce_type: {3}, publish_date: {4}, publish_page: {5}, appellant: {6}, court: {7}, content: {8}, province: {9}, announce_num: {10}".format(
            self.id, self.c_id, self.litigant, self.announce_type, self.publish_date, self.publish_page, self.appellant, self.court, self.content, self.province,
            self.announce_num)
