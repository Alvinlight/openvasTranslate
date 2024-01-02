import requests
from translate.utils.AuthV3Util import addAuthParams
import json


# 您的应用ID
APP_KEY = ''
# 您的应用密钥
APP_SECRET = ''


def createRequest(q):
    '''
    note: 将下列变量替换为需要请求的参数
    '''
    # q = 'medium general '
    lang_from = 'en'
    lang_to = 'zh-CHS'
    vocab_id = '您的用户词表ID'

    data = {'q': q, 'from': lang_from, 'to': lang_to, 'vocabId': vocab_id}

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/api', header, data, 'post')
    # print(str(res.content, 'utf-8'))
    bytes_result = res.content
    dic_result = convert_bytes_to_dict(bytes_result)  # 将翻译结果转换为字典
    # print(dic_result)
       
    return dic_result

def convert_bytes_to_dict(data):
    try:
        # 将字节串解码为字符串
        decoded_data = data.decode('utf-8')
        # print(decoded_data)
        # 将字符串转换为字典
        dictionary = json.loads(decoded_data)
        return dictionary
    except ValueError:
        print("无法将数据转换为字典格式")
        return None


def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, header)

# 网易有道智云翻译服务api调用demo
# api接口: https://openapi.youdao.com/api
# if __name__ == '__main__':
#     q = 'medium general '
#     createRequest(q)
