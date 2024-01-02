import os
import sys
import json
from lxml import etree
from translate.translate import createRequest
import time
import re
import parse_openvas_xml

xml_path = os.getcwd() + '/report.xml'

def fetch_data(xml_path):
    list_hole = parse_openvas_xml.parse_openvas_xml_report(xml_path)  # 借用xml文件解析函数
    # print(hole)
    for dic_hole in list_hole:
        list_replace = ['name', 'summary', 'solution', 'evidence']
        for key in list_replace: # 遍历待翻译的key值，进行判断，key值符合则进行翻译然后替换dic
            dic_replace = {}  # 创建一个字典用于翻译前后数据替换
            if key in dic_hole:
                result_trans = translate_data(dic_hole[key])  # 调用翻译模块
                if isinstance(result_trans, list):
                    result_trans = ''.join(result_trans)
                    dic_replace[key] = result_trans
                else:
                    dic_replace[key] = result_trans
                dic_hole[key] = dic_replace[key]
    return list_hole


def translate_data(str):
    dic_trans = {}
    dic_trans['errorCode'] = 500
    count = 0
    while count < 5 and int(dic_trans['errorCode']) != 0:
        flag = 0
        dic_trans = createRequest(str)  # 调用翻译模块，返回字典数据
        if 'errorCode' in dic_trans:
            if int(dic_trans['errorCode']) == 0:
                if 'translation' in dic_trans:
                    return dic_trans['translation']
                    flag = 1
            else:
                time.sleep(1)
                print("循环次数：", count, "状态码：", dic_trans['errorCode'], "411报错原因：访问频率受限,请稍后访问")   
        else:
            time.sleep(0.5)
            print("循环次数：", count, "\n报错字段：", i, "\n报错原因：", dic_trans, "\n\n\n")
        count = count + 1
    else:
        if flag == 0:
            return str

def json_write(write_trans):
    json_trans = {}
    json_trans['total'] = write_trans[0]    
    json_trans['hole'] = write_trans[1:]
    
    # 由于文件写入时只能是字符串类型，所以要转成JSON对象，ensure_ascii=False 原样写入内容（中文）
    json_trans = json.dumps(json_trans, ensure_ascii=False)  
    with open('./translate.json', 'w', encoding='utf-8') as fp:
        fp.write(json_trans)


# if __name__ == "__main__":
#     report = fetch_data(xml_path)
#     json_write(report)

def start():
    report = fetch_data(xml_path)
    json_write(report)