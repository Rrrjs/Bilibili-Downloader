import requests
import json
import time
import os
import subprocess
from models.GetBV import get_bv
import psutil

def is_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False

# 检测终端是否在运行
if is_process_running("WindowsTerminal.exe"):
    pass
else:
    if not os.path.exists('bin'):
        print('检测到ansicon缺失, 正在拉取')
        os.makedirs('bin')
        url1 = 'https://download.rrrjs.cn/Files/ansicon/ansicon.exe'
        res1 = requests.get(url1)
        with open('./bin/ansicon.exe', 'wb') as f:
            f.write(res1.content)

        url2 = 'https://download.rrrjs.cn/Files/ansicon/ANSI32.dll'
        res2 = requests.get(url2)
        with open('./bin/ANSI32.dll', 'wb') as f:
            f.write(res2.content)

        url3 = 'https://download.rrrjs.cn/Files/ansicon/ANSI64.dll'
        res3 = requests.get(url3)
        with open('./bin/ANSI64.dll', 'wb') as f:
            f.write(res3.content)
            print('成功')
    try:
        # 执行ansicon二进制文件
        executable = './bin/ansicon.exe'
        arguments = ['-i']

        # 使用subprocess模块执行可执行文件并传递参数
        subprocess.run([executable] + arguments)
    except:
        print('ansicon加载失败, 可能会出现乱码')

if not os.path.exists('logs'):
    os.makedirs('logs')
    

#创建config.json文件
file_path = "config.json"
data = {
    "SESSDATA": ""
}
if not os.path.isfile(file_path):
    with open(file_path, "w") as file:
        file.write(json.dumps(data, indent=4) + "\n")
    print('正在创建config.json')
    print()
    print('\033[0;31;40m未填入SESSDATA: \033[0m')

with open('config.json') as file:
    data = json.load(file)
    if data['SESSDATA'] == '':
        print('检查config.json文件')
        input()
        exit(1)

#读取JSON
try:
    with open('config.json') as file:
        data = json.load(file)
    SESSDATA = data['SESSDATA']
except:
    print('检查config.json文件')
    input()
    exit(1)

#获取当前时间
time_value = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
time_value = time_value+'\n'

#获取bvid
while True:
    video_url = input('\033[0;32;40m输入待抓取之URL: \033[0m')
    print()
    bvid = get_bv(video_url)
    if bvid is None:
        print('\033[0;31;40mURL格式错误,请重新输入: \033[0m')
    else:
        print('\033[0;32;40mURL识别成功, 正在处理...\033[0m')
        break


url = "https://api.bilibili.com/x/web-interface/view" 


params_value = {
    "bvid": bvid
}

headers_value = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
}

cookies_value = {
    "SESSDATA": SESSDATA
}

n = 0
while n<10 :
    try:
        response = requests.get(url, params = params_value, cookies = cookies_value, headers = headers_value)
        data = response.json()
        
        json_content = json.dumps(data, indent=4)
        with open("./logs/info.json", "w") as file:
            file.write(time_value)
            file.write(json_content)
    except:
        n = n+1
        print("请求失败,重试中...... ",n)
        time.sleep(1)
        continue

    if data["code"] == 0:
            if "v_voucher" in data["data"]:
                print("请求失败,重试中...... ",n)
                time.sleep(1)
                continue
            else:
                print("\033[0;32;40m响应INFO成功\033[0m")
                break
    else:
        n = n+1
        print("请求失败",n)
        print("错误代码:", data["code"])
        print("重试中......")
        time.sleep(1)
if n >=10:
    print("尝试次数过多, exit(1)")
    input("按回车键结束")
    exit(1)
else:
    pass