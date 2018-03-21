'''
有关代理商的实用函数，例如请求头，查询域名等等
'''

from config import config
from hashlib import md5, sha1
import time
import grequests
import requests
import json


def get_headers(agent_id=config.AGENT_ID, password=config.PASSWORD, public_key=config.PUBLIB_KEY):
    # 获取请求头
    # 输入字典形式的请求头
    password_md5 = md5(password.encode()).hexdigest()
    timestamp = str(int(time.time()))
    s = password_md5 + agent_id + public_key + timestamp
    signature = sha1(s.encode()).hexdigest()
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'multipart/form-data',
        'agent-id': agent_id,
        'timestamp': timestamp,
        'signature': signature
    }
    return headers


def is_registered(domains):
    # 检查域名是否注册
    # 输入域名组成的列表
    # 输出的status有0，1，-1三种，-1代表查不到
    domains200 = [domains[i * 200:i * 200 + 200] for i in range((len(domains) - 1) // 200 + 1)]
    dic = {}
    for i in domains200:
        tasks = [grequests.get('http://dms.10.com/api/v1/agent/domain/check?keyword=' + j, headers=get_headers()) for j
                 in i]
        respones = zip(i, grequests.map(tasks))
        for k in respones:
            if k[1] and k[1].status_code < 400:
                k[1].close()
                try:
                    dic[k[0]] = json.loads(k[1].text)['data']['in_use']
                except:
                    dic[k[0]] = -1
            else:
                dic[k[0]] = -1
    return [{'domain': i, 'status': dic[i]} for i in dic]


def register_domain(domains):
    # 注册域名
    # 输入域名组成的列表，由于代理商服务器的关系，域名数量最好不要超过128
    # 输出的status中1代表注册成功,0代表失败，-1代表一般程序错误，-2代表requests.exceptions.ConnectionError
    dic = {}
    for i in domains:
        try:
            out_put = requests.post(
                'http://dms.10.com/api/v1/agent/domain/register?period=1&contact_template_id=2011300215&keyword=' + i,
                headers=get_headers())

        # 如果返回链接断开，则提前返回，因为api接口不稳定所以采用的权宜之计
        except requests.exceptions.ConnectionError:
            dic[i] = -2
            break
        except:
            dic[i] = -1
            continue

        out_put.close()

        try:
            ot = json.loads(out_put.text)
        except:
            ot = None
            dic[i] = -1
        if ot:
            if ot['register_status'] == 'SUCCESSFUL':
                dic[i] = 1
            elif ot['register_status'] == 'FAILED':
                dic[i] = 0
            else:
                dic[i] = -1
        else:
            dic[i] = -1

    return [{'domain': i, 'status': dic[i]} for i in dic]


if __name__ == '__main__':
    # print(is_registered(['10.com', '001472.com']))
    print(register_domain(['10.com']))
    # print(get_headers())
    # print(register_domain2(['014421.com']))
    # print(register_domain2(['310750.com']))
    # print(requests.post(
    #     'http://dms.10.com/api/v1/agent/domain/register?period=1&contact_template_id=2011300215&keyword=10.com',
    #     headers=get_headers()).json())
