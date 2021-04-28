from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Float, Boolean, DECIMAL, Enum, Date, DateTime, Time, Text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


class BaseInfo(Base):
    # def __init__(self, **entry):
    #     self.__dict__.update(entry)

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

    def __repr__(self):
        return "id: {0}, Enterprise_name: {1}, Enterprise_tyshxydm: {2}, Legalrepresentative: {3}, Enterprise_zzjgdm: {4}, Enterprise_gszch: {5}, rtime: {6}, registered_address: {7}, gslx: {8}, jyzt: {9}, op_from: {10}, op_to: {11}, approval_date: {12}, djjg: {13}, f_body: {14}, cancel_date: {15}, reasons_cancel: {16}, zczb: {17}, paid_in_capital: {18}, ygrs: {19}, social_staff_num: {20}, industry: {21}, Contact_number: {22}, email: {23}, z_body: {24}, source_update_time: {25}, local_update_time: {26}".format(
            self.id, self.Enterprise_name, self.Enterprise_tyshxydm, self.Legalrepresentative, self.Enterprise_zzjgdm, self.Enterprise_gszch, self.rtime,
            self.registered_address, self.gslx, self.jyzt, self.op_from, self.op_to, self.approval_date, self.djjg, self.f_body, self.cancel_date, self.reasons_cancel,
            self.zczb, self.paid_in_capital, self.ygrs, self.social_staff_num, self.industry, self.Contact_number, self.email, self.z_body, self.source_update_time,
            self.local_update_time)
