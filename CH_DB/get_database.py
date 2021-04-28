import pymysql
import json
import threading
import operator
import time
import datetime
# import date
# from pybloom_live import ScalableBloomFilter
import re
# from zhon.hanzi import punctuation


class DateEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        # elif isinstance(obj, date):
        #     return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


class MyThread(threading.Thread):

    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None


class databaseTool:
    @staticmethod
    def collection_base_field(list, key):
        field = None
        temp = None
        for json in list:
            if json:
                if key in json:
                    if json[key]:
                        if isinstance(json[key], datetime.datetime):
                            if not temp:
                                temp = json[key]
                            else:
                                print((temp - json[key]).total_seconds())
                                if (temp - json[key]).total_seconds() < 0:
                                    temp = json[key]
                            field = temp
                        else:
                            field = json[key]
                            break
        return field

    @staticmethod
    def teeest(list, json, delKey):
        if list:
            for obj in list:
                for k, v in obj.items():
                    # if k != delKey:
                    if obj[k] is None:
                        obj[k] = json[k]
        else:
            list.append(json)
        for obj in list:
            # for k in delKey:
            if delKey in obj:
                obj.pop(delKey)
        return list

    @staticmethod
    def collection_field(*args):
        field = None
        temp = None
        for arg in args:
            # print("TYPE OF ARG :",type(arg))
            # print("ARG :", (arg))
            if arg:
                # print("11111111111111111111111")
                if isinstance(arg, datetime.datetime):
                    # print("2222222222222222222222")
                    if not temp:
                        # print("333333333333333333333")
                        temp = arg
                    else:
                        # print("44444444444444444444")
                        # print("temp", temp)
                        # print("arg ", arg)
                        # print("arg-temp :", temp - arg)
                        print((temp - arg).total_seconds())
                        if (temp - arg).total_seconds() < 0:
                            temp = arg
                    field = temp
                else:
                    field = arg
                    break
        return field

    @staticmethod
    def change_character(item):
        new_item = {}
        for k, v in item.items():
            new_item[k] = databaseTool.change(item[k])
        return new_item

    @staticmethod
    def change(string):
        if isinstance(string, str):
            # replace("(", "（").replace(")", "）").
            string = string.replace("<", "（").replace(">", "）")
            string = string.strip()
        return string

    @staticmethod
    def select_main_field(*args):
        main_field = None
        for arg in args:
            if arg:
                main_field = arg
                break
        print("main_field : ", main_field)
        return main_field

    @staticmethod
    def field_append(*args):
        list = databaseTool.removeDuplicate(*args)
        field = ""
        if list[0][0]:
            field += str(list[0][0]) + \
                     "(" + databaseTool.get_tag(list[0][1]) + ")"
        flag = True
        for i in range(1, len(list)):
            if list[i][0]:
                if list[i][0] != "None":
                    flag = False
                    field += str(list[i][0]) + "(" + \
                             databaseTool.get_tag(list[i][1]) + ")"
        if flag:
            if "None" in field:
                field = ''
        return field

    @staticmethod
    def get_tag(num):
        tag = ""
        if num == 0:
            tag = "GX"
        if num == 1:
            tag = "TYC"
        return tag

    @staticmethod
    def ExistOrNot(obj):
        if obj:
            return obj
        return None

    @staticmethod
    def collection_list_field(list, data, main_field):
        if list:
            bloom = ScalableBloomFilter(
                mode=ScalableBloomFilter.SMALL_SET_GROWTH)
            for l in list:
                bloom.add(l)
            if data not in bloom:
                flag = True
                for l in list:
                    if l[main_field] == data[main_field] and data[main_field] is not None:
                        flag = False
                        list.remove(l)
                        item = {}
                        for k, v in l.items():
                            item[k] = databaseTool.collection_field(databaseTool.is_field_dict(l, k),
                                                                    databaseTool.is_field_dict(data, k))
                        list.append(item)
                        break
                if flag:
                    list.append(data)
        else:
            list.append(data)
        return list

    @staticmethod
    def is_difference_all_None(dict1, dict2):
        dict1 = databaseTool.dict_removePunctuation(dict1)
        dict2 = databaseTool.dict_removePunctuation(dict2)
        flag = False
        diff = dict1.keys() & dict2
        diff_vals = [(k, dict1[k], dict2[k])
                     for k in diff if dict1[k] != dict2[k]]
        index = 0
        for d in diff_vals:
            if d[1] is None or d[2] is None:
                index += 1
        if index == len(diff_vals):
            flag = True
        return flag

    @staticmethod
    def change_character_en_cn(text):
        if '(' in text:
            text = text.replace('(', "（").replace(')', "）")
        elif "（" in text:
            text = text.replace('（', '(').replace('）', ')')
        return text

    @staticmethod
    def dict_removePunctuation(dict):
        item = {}
        for k, v in dict.items():
            item[k] = databaseTool.removePunctuation(dict[k])
        return item

    @staticmethod
    def removePunctuation(text):
        if isinstance(text, str):
            # 去除中文标签
            text = re.sub(r'[{}]+'.format(punctuation), '', text)
            # 去除英文标签
            punctuation_eng = '!,;:.&^\_\-\=\+\/$*?\'\""\'()'
            text = re.sub(r'[{}]+'.format(punctuation_eng), '', text)
            # 去掉换行
            text = text.replace('\n', '')
            text = text.replace(' ', '').strip().lower()
            if len(text) == 1:
                if text == '无' or text == 'None' or text == '':
                    text = None
        if isinstance(text, datetime.datetime):
            text = text.strftime("%Y-%m-%d %H:%M:%S")
        return text

    @staticmethod
    def remove_field_from_dict(dict, *delKey):
        for key in delKey:
            if key in dict:
                dict.pop(key)
        return dict

    @staticmethod
    def collection_list_without_main_field(list, data, *same_field):
        if list:
            bloom = ScalableBloomFilter(
                mode=ScalableBloomFilter.SMALL_SET_GROWTH)
            for l in list:
                bloom.add(l)
            if data not in bloom:
                flag = True
                for l in list:
                    index = 0
                    for same in same_field:
                        if l[same] == data[same] and l[same] is not None and data[same] is not None:
                            index += 1

                    # 满足至少n个字段值相同且相同的值为None时小于n个
                    # differ = set(l.items()) ^ set(data.items())
                    # same_None_num = databaseTool.get_None_number(l, data)
                    # if (len(differ) / 2) <= (len(l) - same_num) and len(differ) > 0 and same_None_num < same_num - 1:
                    #     print("diffNum qualified ")
                    #     list.remove(l)
                    #     item = {}
                    #     for k, v in l.items():
                    #         item[k] = databaseTool.collection_field(databaseTool.is_field_dict(l, k),
                    #                                                 databaseTool.is_field_dict(data, k))
                    #     list.append(item)
                    #     break
                    '''
                    除去值为None的字段后,其他字段都相同,则进行合并
                    '''
                    if databaseTool.is_difference_all_None(l, data):
                        flag = False
                        list.remove(l)
                        item = {}
                        for k, v in l.items():
                            item[k] = databaseTool.collection_field(databaseTool.is_field_dict(l, k),
                                                                    databaseTool.is_field_dict(data, k))
                        list.append(item)
                        break
                    elif len(same_field) == index and index != 0:
                        flag = False
                        print(" same field qualified")
                        list.remove(l)
                        item = {}
                        for k, v in l.items():
                            item[k] = databaseTool.collection_field(databaseTool.is_field_dict(l, k),
                                                                    databaseTool.is_field_dict(data, k))
                        list.append(item)
                        break
                if flag:
                    list.append(data)
        if len(list) == 0:
            list.append(data)
        return list

    @staticmethod
    def removeDuplicate(*args):
        field_item = {}
        for i in range(len(args) - 1, -1, -1):
            field_item.update({args[i]: i})
        sortedDist = sorted(field_item.items(),
                            key=operator.itemgetter(1), reverse=False)
        return sortedDist

    @staticmethod
    def get_None_number(a, b):
        same = 0
        for k, v in a.items():
            if a[k] == b[k] and a[k] == None:
                same += 1
        return same

    @staticmethod
    def is_field_dict(d, f):
        if d:
            if f in d:
                # print("d[f] : ", d[f])
                return databaseTool.clear_field(d[f])
            else:
                return None
        else:
            return None

    @staticmethod
    def clear_field(obj):
        clear_obj = obj
        if obj == "None":
            clear_obj = None
        if obj == "-":
            clear_obj = None
        if isinstance(clear_obj, str):
            clear_obj.replace("\n", "")
            if clear_obj.isdigit():
                if len(clear_obj) == 13:
                    timeStamp = float(int(clear_obj) / 1000)
                    timeArray = time.localtime(timeStamp)
                    otherStyleTime = time.strftime(
                        "%Y-%m-%d %H:%M:%S", timeArray)
                    clear_obj = str(otherStyleTime)
        if clear_obj == "":
            clear_obj = None
        return clear_obj

    @staticmethod
    def unify_character(o):
        if isinstance(o, str):
            o = o.strip()

            o = o.replace("（", "(").replace("）", ")").replace(
                "<", "(").replace(">", ")")
            if o.startswith("` "):
                o = o[1:len(o)]
            if o.startswith("^"):
                o = o[1:len(o)]
            if o.endswith(","):
                o = o[0:len(o) - 1]
            if o.endswith("、"):
                o = o[0:len(o) - 1]
            if o == "None":
                o = None
            if o == "":
                o = None
            if o == '无':
                o = None
            if o and '&nbsp;' in o:
                o = o.replace('&nbsp;', " ")
            if o and '<BR/>' in o:
                o = o.replace("<BR/>", "\n")

        return o

    @staticmethod
    def unify_character_from_list(list):
        new_list = []
        for item in list:
            new_item = databaseTool.unify_character_from_item(item)
            new_list.append(new_item)
        return new_list

    @staticmethod
    def unify_character_from_item(item):
        new_item = {}
        for k, v in item.items():
            new_item[k] = databaseTool.unify_character(item[k])
        return new_item

    # 重复字典分组
    @staticmethod
    def dup_divide(item_list):
        a = []
        x = []
        for i in range(0, len(item_list)):
            if i + 1 < len(item_list):
                if item_list[i]['shareholder'] == item_list[i + 1]['shareholder']:
                    x.append(item_list[i])
                else:
                    x.append(item_list[i])
                    a.append(x)
                    x = []
            else:
                x.append(item_list[len(item_list) - 1])
                a.append(x)
        print(a)
        return a

    @staticmethod
    def is_chinese(string):
        for chart in string:
            if '\u4e00' <= chart <= '\u9fa5':
                return True
        return False

    @staticmethod
    def stripTagSimple(htmlStr):
        '''
        最简单的过滤html <>标签的方法    注意必须是<任意字符>  而不能单纯是<>
        :param htmlStr:
        '''
        htmlStr = htmlStr
        #         dr =re.compile(r'<[^>]+>',re.S)
        dr = re.compile(r'</?\w+[^>]*>', re.S)
        htmlStr = re.sub(dr, '', htmlStr)
        return htmlStr

