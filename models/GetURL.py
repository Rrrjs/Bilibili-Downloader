import requests
import json
import time
from models.Wbi import wbi
import models.AnaInfo

try:
    with open('config.json') as file:
        data = json.load(file)
    SESSDATA = data['SESSDATA']
except:
    print('检查config.json文件')
    input()
    exit(1)

def select_qn():
    print()
    print('清晰度列表: ')
    return_value = []
    dict1 = {'num': 1, 'title': '240P', 'qn': 6, 'fourk': 0}
    return_value.append(dict1)
    print('\033[0;33;40m1.240P\033[0m')
    dict2 = {'num': 2, 'title': '360P', 'qn': 16, 'fourk': 0}
    return_value.append(dict2)
    print('\033[0;33;40m2.360P\033[0m')
    dict3 = {'num': 3, 'title': '480P', 'qn': 32, 'fourk': 0}
    return_value.append(dict3)
    print('\033[0;33;40m3.480P\033[0m')
    dict4 = {'num': 4, 'title': '720P', 'qn': 64, 'fourk': 0}
    return_value.append(dict4)
    print('\033[0;33;40m4.720P\033[0m')
    dict5 = {'num': 5, 'title': '720P60', 'qn': 74, 'fourk': 0}
    return_value.append(dict5)
    print('\033[0;33;40m5.720P60\033[0m')
    dict6 = {'num': 6, 'title': '1080p', 'qn': 80, 'fourk': 0}
    return_value.append(dict6)
    print('\033[0;33;40m6.1080P\033[0m')
    dict7 = {'num': 7, 'title': '1080p+', 'qn': 112, 'fourk': 0}
    return_value.append(dict7)
    print('\033[0;33;40m7.1080P+\033[0m')
    dict8 = {'num': 8, 'title': '1080p60', 'qn': 116, 'fourk': 0}
    return_value.append(dict8)
    print('\033[0;33;40m8.1080P60\033[0m')
    dict9 = {'num': 9, 'title': '4K', 'qn':120, 'fourk': 1}
    return_value.append(dict9)
    print('\033[0;33;40m9.4K\033[0m')
    print()
    while True:
        try:
            select = int(input('\033[0;32;40m选择优先清晰度序号: \033[0m'))
            if select in range(1,10):
                qn = return_value[select-1]['qn']
                fourk = return_value[select-1]['fourk']
                qn_fourk = []
                qn_fourk.append(qn)
                qn_fourk.append(fourk)
                break
            else:
                print('\033[0;31;40m输入有误, \033[0m')
                continue
        except:
            print('\033[0;31;40m输入有误, \033[0m', end='')
            continue
    return qn_fourk

#获取WBI关键数据
m = 0
while m <= 15:
    try:
        signed_params = wbi()
        bar = signed_params['bar']
        baz = signed_params['baz']
        foo = signed_params['foo']
        wts = signed_params['wts']
        w_rid = signed_params['w_rid']
        break
    except:
        continue

if m > 15:
    print('key获取失败, 请检查网络设置 exit(1)')
    input("按回车键结束")
    exit(1)

def geturl(info):
    cid = info[0]
    bvid = info[1]
    #获取时间戳
    time_value = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    time_value = time_value+'\n'

    #绑定requests参数
    url = "https://api.bilibili.com/x/player/wbi/playurl"

    params_value = {
        "bvid": bvid,
        "cid": cid,
        "qn": qn,
        "fourk": fourk,
        "bar": bar,
        "foo": foo,
        "baz": baz,
        "wts": wts
    }

    headers_value = {
        'User-Agent': browser
    }

    cookies_value = {
        "SESSDATA": SESSDATA
    }

    #requests循环
    n = 0
    while n<10 :
        try:
            response = requests.get(url, params = params_value, cookies = cookies_value, headers = headers_value)
            url_data = response.json()
            
            json_content = json.dumps(url_data, indent=4)
            with open("./logs/URL.json", "w") as file:
                file.write(time_value)
                file.write(json_content)
        except:
            n = n+1
            print("请求失败,正在重试",n)
            time.sleep(1)
            continue

        if url_data["code"] == 0:
            if "v_voucher" in url_data["data"]:
                n = n+1
                print("响应无效,检查SESSDATA ",n)
                time.sleep(1)
                continue
            else:
                qn_avalable = url_data['data']['accept_quality']
                down_url = url_data['data']['durl'][0]['backup_url'][1]
                url_return = [down_url, qn_avalable]
                return url_return
        else:
            n = n+1
            print("响应失败",n)
            print("错误代码:", url_data["code"])
            print("https://www.bilibili.com/video/BV1G64y1N7nn/?spm_id_from=333.337.search-card.all.click......")
            time.sleep(1)
    if n >=10:
        print("尝试次数过多, exit(1)")
        input("按回车键结束")
        exit(1)


#前置变量
infos = models.AnaInfo.get_cid_bvid()
qn_fourk = select_qn()
qn = qn_fourk[0]
fourk = qn_fourk[1]
browser = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'

print('API请求中......')
url_returns = []
for info in infos:
    url_return = geturl(info)
    url_returns.append(url_return)

count = len([lst for lst in url_returns if isinstance(lst, list)])

print()
if count == 0:
    print('\033[0;31;40mAPI请求关键性错误\033[0m')
    input()
    exit(1)
print("\033[0;32;40mAPI响应成功 \033[0m", "响应计数器 ", count,sep='')
print()
print('返回可接受清晰度: ')
qn_avalable = url_returns[0][1]
for every_qn in qn_avalable:
    if every_qn == 6:
        print('\033[0;33;40m240P\033[0m',sep = ' ')
    elif every_qn == 16:
        print('\033[0;33;40m360P\033[0m',sep = ' ')
    elif every_qn == 32:
        print('\033[0;33;40m480P\033[0m',sep = ' ')
    elif every_qn == 64:
        print('\033[0;33;40m720P\033[0m',sep = ' ')
    elif every_qn == 74:
        print('\033[0;33;40m720P60\033[0m',sep = ' ')
    elif every_qn == 80:
        print('\033[0;33;40m1080P\033[0m',sep = ' ')
    elif every_qn == 112:
        print('\033[0;33;40m1080P+\033[0m',sep = ' ')
    elif every_qn == 116:
        print('\033[0;33;40m1080P60\033[0m',sep = ' ')
    elif every_qn == 120:
        print('\033[0;33;40m4K\033[0m',sep = ' ')
