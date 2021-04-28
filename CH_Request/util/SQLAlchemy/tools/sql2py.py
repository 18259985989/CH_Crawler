import os
import re


class SqlFileInfo:
    def __init__(self, filename):
        self.filename = filename
        self.tableList = []


class SqlTableInfo:
    def __init__(self, table, startLine=None, endLine=None):
        self.table = table
        self.startLine = startLine
        self.endLine = endLine


class SqlColumnInfo:
    def __init__(self, column, type, len=None, nullable=False, primary=False, autoincrement=False):
        self.column = column
        if type == "int":
            self.type = "Integer"
            len = None
        elif type == "varchar":
            self.type = "String"
        elif type == "text":
            self.type = "Text"
        elif type == "longtext":
            self.type = "LONGTEXT"
        elif type == "datetime":
            self.type = "DateTime"
        elif type == "date":
            self.type = "Date"
        else:
            print("error type:%s" % (type))

        if len is not None:
            self.len = int(len)
        else:
            self.len = None

        self.nullable = nullable
        self.primary = primary
        self.autoincrement = autoincrement


class Sql2py:
    def __init__(self):
        self.sqlPath = "sql/"
        self.pyPath = "py/"
        self.absPath = os.path.dirname(os.path.abspath(__file__))
        print(self.absPath)
        self.sqlFileList = self.getFileList(self.sqlPath, ".sql")
        self.transformTableList = self.getTransformTableList()

    def getFileList(self, path, fileType):
        files = []
        path = self.absPath + "/" + path
        print(path)
        for f in os.listdir(path):

            if f.endswith(fileType):
                file = os.path.join(path, f)
                print(file)
                if fileType == ".sql":
                    tmpFile = SqlFileInfo(file)
                    tmpFile.tableList = self.getSqlTable(file)
                    files.append(tmpFile)
                else:
                    files.append(file)
        print(files)
        return files

    def getSqlTable(self, file):
        command = "cat -n %s | grep 'CREATE TABLE' " % (file)
        res = os.popen(command).read()
        lineList = res.strip().split("\n")
        tables = []
        for line in lineList:
            print('line', line)
            tableName = line.strip().split(" ")[2].replace("`", "")
            startline = int(line.strip().split("\t")[0]) + 1
            endCommand = "cat -n %s | tail -n +%d | grep ') ENGINE'" % (file, startline)
            endRes = os.popen(endCommand).read()
            endLine = int(endRes.strip().split("\n")[0].strip().split("\t")[0]) - 1
            table = SqlTableInfo(tableName, startline, endLine)
            tables.append(table)
        return tables

    def getTransformTableList(self):
        path = self.absPath + "/" + self.pyPath
        transformTables = []
        for file in self.sqlFileList:
            transformTable = SqlFileInfo(file.filename)
            for table in file.tableList:
                pyFile = os.path.join(path, (self.str2Hump(table.table) + ".py"))
                transformTable.tableList.append(table)
            if len(transformTable.tableList) > 0:
                transformTables.append(transformTable)

        return transformTables

    def str2Hump(self, text, headUpper=False):
        arr = filter(None, text.lower().split('_'))
        res = ''
        for i in arr:
            res = res + i[0].upper() + i[1:]

        if headUpper == True:
            return res

        res = res[0].lower() + res[1:]
        return res

    def lowerFirstLetter(self, text):
        if isinstance(text, str):
            text = text[0].lower() + text[1:]
            return text

    def doTransfrom(self):
        for file in self.transformTableList:
            newPyname = re.findall('tools/sql/(.*?).sql', file.filename)[0]
            # 创建新文件
            path = self.absPath + "/" + self.pyPath
            # newPyname = newPyname + ".py"
            newPyname = "model.py"
            pyFile = open(os.path.join(path, newPyname), "w+")
            # 导入文件头
            pyFile.write("# 导入: \n")
            pyFile.write(
                "from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Float, Boolean, DECIMAL, Enum, Date, DateTime, Time, Text\n")
            pyFile.write("from sqlalchemy.dialects.mysql import LONGTEXT\n")
            pyFile.write("from sqlalchemy.orm import sessionmaker, relationship, backref \n")
            pyFile.write("from sqlalchemy.ext.declarative import declarative_base \n")
            pyFile.write("\n")
            pyFile.write("# 创建对象的基类: \n")
            pyFile.write("Base = declarative_base() \n")
            tabList = file.tableList
            # for table in tabList:
            # print("table:   ", table.table)
            self.tansfromTable(file.filename, pyFile, tabList)

    def tansfromTable(self, filename, pyFile, tabList):
        for tableInfo in tabList:
            print("table:   ", tableInfo.table)
            # 开始定义对象
            pyFile.write("\n")
            pyFile.write("# 定义对象: \n")
            pyFile.write("class %s(Base): \n" % (self.str2Hump(tableInfo.table, True)))
            pyFile.write("\t# 表的名字:\n")
            pyFile.write("\t__tablename__ = \'%s\' \n" % (tableInfo.table))
            pyFile.write("\t# 表的结构:\n")

            # 读取对应文件信息
            command = "sed -n '%d, %dp' %s" % (tableInfo.startLine, tableInfo.endLine, filename)
            res = os.popen(command).read().strip().split("\n")
            columnList = []
            for line in res:
                element = line.strip().split(" ")
                # 主键处理
                if element[0] == "PRIMARY":
                    primaryKey = element[2].replace("(", "").replace(")", "").replace("`", "")
                    primaryKeys = primaryKey.split(",")
                    for column in columnList:
                        if column.column in primaryKeys:
                            column.primary = True

                    continue

                # 第一元素为column
                column = element[0].replace("`", "")
                # 第二元素为type, 有的会携带长度，有的不会
                lenIndex = element[1].find("(")
                columnLen = None
                if lenIndex == -1:
                    type = element[1].replace(",", "")
                else:
                    type = element[1][:lenIndex].replace(",", "")
                    columnLen = element[1][lenIndex + 1: len(element[1]) - 1]

                # 第三/四个元素可能NOT NULL/DEFAULT NULL
                nullable = True
                if (len(element) > 4):
                    if element[3] == "NULL":
                        if element[2] == "NOT":
                            nullable = False

                autoincrement = False
                if line.find("AUTO_INCREMENT") != -1:
                    autoincrement = True

                columnInfo = SqlColumnInfo(column, type, columnLen, nullable, None, autoincrement)
                columnList.append(columnInfo)

            relationFlag = False
            company_m_relationFlag = False
            # 开始插入元素
            for column in columnList:
                print('column:  ', column.column)
                if column.column == 'KEY':
                    continue
                textLine = "\t%s = Column(%s" % (column.column, column.type)
                if column.len is not None:
                    textLine = textLine + ("(%d)" % (column.len))
                if column.nullable == False:
                    textLine = textLine + (", nullable = False")
                if column.autoincrement == True:
                    textLine = textLine + (", autoincrement = True")
                if column.primary == True:
                    textLine = textLine + (", primary_key = True")
                if column.column == "c_id":
                    textLine = textLine + ", ForeignKey(\"base_info.id\",ondelete=\"CASCADE\"), nullable=False"
                    relationFlag = True
                if column.column == "reg_id":
                    textLine = textLine + ", ForeignKey(\"company_mortgage.reg_number\",ondelete=\"CASCADE\"), nullable=False"
                    company_m_relationFlag = True
                textLine = textLine + ")\n"
                pyFile.write(textLine)

            # if self.str2Hump(tableInfo.table, True) == 'BaseInfo':
            #     for t in tabList:
            #         if self.str2Hump(t.table, True) not in (
            #                 'BaseInfo', 'CompanyMortgageChange', 'CompanyMortgageCollateral', 'CompanyMortgagePledgee'):
            #             pyFile.write("\n")
            #             pyFile.write(
            #                 "\t%s = relationship(\"%s\", backref = backref('%sRel', order_by = id),cascade=\"all, delete-orphan\",passive_deletes = True)\n" % (
            #                     t.table, self.str2Hump(t.table, True),
            #                     self.str2Hump(t.table, True)))
            # if self.str2Hump(tableInfo.table, True) == 'CompanyMortgage':
            #     for t in tabList:
            #         if self.str2Hump(t.table, True) in (
            #                 'CompanyMortgageChange', 'CompanyMortgageCollateral', 'CompanyMortgagePledgee'):
            #             pyFile.write("\n")
            #             pyFile.write(
            #                 "\t%s = relationship(\"%s\", backref = backref('%sRel', order_by = id),cascade=\"all, delete-orphan\",passive_deletes = True)\n" % (
            #                     t.table, self.str2Hump(t.table, True),
            #                     self.str2Hump(t.table, True)))
            # 构建关系表
            if relationFlag:
                pyFile.write("\n")
                pyFile.write(
                    "\tbaseInfo = relationship(\"BaseInfo\", backref = backref('%sRel', order_by = id,cascade=\"all, delete-orphan\"))\n" % (
                        self.str2Hump(tableInfo.table)))
            if company_m_relationFlag:
                pyFile.write("\n")
                pyFile.write(
                    "\tcompanyMortgage = relationship(\"CompanyMortgage\", backref = backref('%sRel', order_by = id,cascade=\"all, delete-orphan\"))\n" % (
                        self.str2Hump(tableInfo.table)))

            # 定义debug输出操作
            pyFile.write("\n")
            pyFile.write("\tdef __repr__(self): \n")

            returnLine = ""
            i = 0
            for column in columnList:
                returnLine = returnLine + ("%s: {%d}, " % (column.column, i))
                i = i + 1
            returnLine = returnLine[:len(returnLine) - 2]
            formatLine = ""
            for column in columnList:
                formatLine = formatLine + ("self.%s, " % (column.column))
            # 去除最后的,和空格
            formatLine = formatLine[:len(formatLine) - 2]
            resLine = "\t\treturn \"%s\".format(%s)\n" % (returnLine, formatLine)
            pyFile.write(resLine)


if __name__ == '__main__':
    sql2py = Sql2py()
    sql2py.doTransfrom()
