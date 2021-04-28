import re
import importlib
# from memory_profiler import profile
# from guppy import hpy
import objgraph
import gc


# @profile
def jump2Object(fromSql):
    # hp = hpy()
    objgraph.show_growth()
    fields = {}
    for field in [x for x in dir(fromSql) if not x.startswith('_') and x != 'metadata' and x != 'companyMortgage' and x != 'baseInfo']:
        data = fromSql.__getattribute__(field)
        fields[field] = data
    base = type(fromSql)()
    del fromSql
    for k, v in fields.items():
        if isinstance(v, list):
            temp = []
            for ssub in v:
                new_suub = tessss(ssub)
                temp.append(new_suub)
            setattr(base, k, temp)
        else:
            if not k.endswith('id'):
                setattr(base, k, v)
    # print('Heap at the end of the function ', hp.heap())
    print('after jump')
    objgraph.show_growth()
    # objgraph.show_backrefs(objgraph.by_type('BaseInfo')[0], max_depth=10, filename='Bidref.png')
    gc.collect()
    return base


def jump2Object22(fromSql):
    fields = {}
    for field in [x for x in dir(fromSql) if not x.startswith('_') and x != 'metadata' and x != 'companyMortgage' and x != 'baseInfo']:
        data = fromSql.__getattribute__(field)
        fields[field] = data
    base = type(fromSql)()
    del fromSql
    for k, v in fields.items():
        if isinstance(v, list):
            temp = []
            for ssub in v:
                pass
                # new_suub = jump2Object(ssub)
                # temp.append(new_suub)
            del v
            setattr(base, k, temp)
        else:
            if not k.endswith('id'):
                setattr(base, k, v)
    # print(base)
    return base


def tessss(fromSql):
    fields = {}
    # for key, value in vars(fromSql).items():
    for field in [x for x in dir(fromSql) if not x.startswith('_') and x != 'metadata' and x != 'companyMortgage' and x != 'baseInfo']:
        data = fromSql.__getattribute__(field)
        fields[field] = data
    base = type(fromSql)()
    del fromSql
    for k, v in fields.items():
        if isinstance(v, list):
            temp = []
            for ssub in v:
                new_suub = tessss(ssub)
                temp.append(new_suub)
            del v
            setattr(base, k, temp)
        else:
            if not k.endswith('id'):
                setattr(base, k, v)
    # print(base)
    return base


def creatNewList(fromList):
    new = []
    if fromList:
        field = [x for x in dir(fromList[0]) if not x.startswith('_') and x != 'metadata' and x != 'baseInfo' and x != 'companyMortgage']
        for entity in fromList:
            fields = {}
            for f in field:
                data = entity.__getattribute__(f)
                fields[f] = data
            base = type(entity)()
            for k, v in fields.items():
                if isinstance(v, list):
                    sub_list = creatNewList(v)
                    setattr(base, k, sub_list)
                elif not k.endswith('id'):
                    setattr(base, k, v)
            new.append(base)
    return new


def reflectFromType(typeName):
    kk = re.findall("'(.*)\.model.(.*?)\'", typeName)
    print(kk)
    rpath = kk[0][0]
    aMod = importlib.import_module(rpath)
    ob = getattr(aMod, 'model')
    ob = getattr(ob, kk[0][1])
    return ob()

# host = "192.168.10.68"
# port = 3306
# username = "root"
# password = "123456"
# dbname = "tyc"
# databaseService = DatabaseService(host, port, username, password, dbname)
# a = databaseService.session.query(BaseInfo).filter(BaseInfo.Enterprise_name == '福建雅客食品有限公司').order_by(BaseInfo.id.desc()).first()
# jj=JsonSerialize(a)
#
# print(jj)
