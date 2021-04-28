# 导入: 
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Float, Boolean, DECIMAL, Enum, Date, DateTime, Time, Text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import sessionmaker, relationship, backref 
from sqlalchemy.ext.declarative import declarative_base 

# 创建对象的基类: 
Base = declarative_base() 

# 定义对象: 
class BusinessDirectory(Base): 
	# 表的名字:
	__tablename__ = 'business_directory' 
	# 表的结构:
	company = Column(String(200), primary_key = True)
	address = Column(String(200))
	scode = Column(String(64))
	regCapital = Column(String(64))
	area = Column(String(64))
	date = Column(DateTime)
	scope = Column(LONGTEXT)
	legal_person = Column(String(100))
	province = Column(String(16))
	industry = Column(String(16))
	update_time = Column(DateTime)
	data_acquisition_time = Column(DateTime)
	id = Column(Integer, nullable = False, autoincrement = True, primary_key = True)
	tyc_time = Column(DateTime)
	fygg_time = Column(DateTime)
	bzxr_time = Column(DateTime)
	qcc_time = Column(DateTime)

	def __repr__(self): 
		return "company: {0}, address: {1}, scode: {2}, regCapital: {3}, area: {4}, date: {5}, scope: {6}, legal_person: {7}, province: {8}, industry: {9}, update_time: {10}, data_acquisition_time: {11}, id: {12}, tyc_time: {13}, fygg_time: {14}, bzxr_time: {15}".format(self.company, self.address, self.scode, self.regCapital, self.area, self.date, self.scope, self.legal_person, self.province, self.industry, self.update_time, self.data_acquisition_time, self.id, self.tyc_time, self.fygg_time, self.bzxr_time)
