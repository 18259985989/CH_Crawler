import json
from datetime import datetime, date
from sqlalchemy.ext.declarative import DeclarativeMeta
# from memory_profiler import profile


# enhance为True时, 重新封装relationship的参数

class SerializeEnhancer():
    def __init__(self, enhance=False, obj=None):
        self.enhance = enhance
        self.name = obj.__class__.__name__
        if isinstance(obj, list) and len(obj) > 0:
            self.name = obj[0].__class__.__name__


def JsonSerialize(obj, enhance=True):
    # cls 为特殊参数的转换器
    serializeEnhancer = SerializeEnhancer(enhance, obj)
    return json.dumps(obj, cls=AlchemyEncoderService(enhancer=serializeEnhancer), ensure_ascii=False)


def AlchemyEncoderService(_visited_objs=None, enhancer=SerializeEnhancer()):
    if _visited_objs is None:
        _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)

                # an SQLAlchemy class
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                    data = obj.__getattribute__(field)
                    try:
                        if isinstance(data, datetime):
                            data = data.strftime('%Y-%m-%d %H:%M:%S')
                        # list直接序列化后 会变成string
                        if not isinstance(data, list):
                            json.dumps(data)  # this will fail on non-encodable values, like other classes
                        fields[field] = data
                    except TypeError:
                        if data not in _visited_objs:
                            fields[field] = json.dumps(data, cls=AlchemyEncoderService(_visited_objs), ensure_ascii=False)

                # 重整Rel参数
                if enhancer.enhance == True and enhancer.name == obj.__class__.__name__:
                    fieldsEnhance = {}
                    fieldsEnhance[obj.__class__.__name__] = fields
                    for field in list(fields.keys()):
                        if field.endswith("Rel"):
                            # 首字母大写，转成类名
                            fieldEnhance = field.replace("Rel", "")[0].upper() + field.replace("Rel", "")[1:]
                            if isinstance(fields[field], list) and len(fields[field]) == 0:
                                fieldsEnhance[fieldEnhance] = None
                            else:
                                fieldsEnhance[fieldEnhance] = fields[field]
                            del fields[field]
                    return fieldsEnhance

                return fields

            return json.JSONEncoder.default(self, obj)

    return AlchemyEncoder

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def queryResult2Json(query_result):
    msgs = []

    if query_result is None:
        return None
    if isinstance(query_result, list):
        for items in query_result:
            msga = {}
            for key, val in zip(items._fields, items):
                msga[key] = val

            msgs.append(msga)
        msgs = distinctJson(msgs)
        # print(msg[0])
    else:
        msga = {}
        for key, val in zip(query_result._fields, query_result):
            msga[key] = val

        msgs = msga
    # print(msgs)
    return json.dumps(msgs, ensure_ascii=False, cls=ComplexEncoder)

def distinctJson(msgsList):
    listValue = []
    jsonResult=[]
    for item in msgsList:
        temValue=''
        for (key, val) in item.items():
            if key != 'id':
                temValue = temValue + str(val)
        if temValue not in listValue:
            jsonResult.append(item)
            listValue.append(temValue)
    return jsonResult


if __name__ == '__main__':
    jsonList = [{'patent_name':'123445', 'apply_number':'123','pub_number':'章程1','cat_number':'', 'inventor':''},{'id':'123445', 'companyId':'123','changeItem':'章程1'},{'id':'123445', 'companyId':'123','changeItem':'章程2'}]
    jsonReslut=distinctJson(jsonList)
    print(jsonReslut)