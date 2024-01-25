from models.GetURL import count, url_returns
import requests
import time
import os
from tqdm import tqdm
import psutil
import subprocess

def is_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False

if not os.path.exists('download'):
    os.makedirs('download')

time.sleep(1)
print()
print()
print('\033[0;33;40m开始下载\033[0m')
#获取当前时间
time_value = time.strftime('%Y-%m-%d-%H%M%S', time.localtime())
print(time_value)

def download(url: str, fname: str):
    # 用流stream的方式获取url的数据
    headers_value = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    'referer': 'https://www.bilibili.com' 
    }
    resp = requests.get(url, stream=True, headers = headers_value)
    # 拿到文件的长度，并把total初始化为0
    total = int(resp.headers.get('content-length', 0))
    # 打开当前目录的fname文件(名字你来传入)
    # 初始化tqdm，传入总数，文件名等数据，接着就是写入，更新等操作了
    with open(fname, 'wb') as file, tqdm(
        desc=fname,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

if __name__ == "__main__":
    try:
        if count != 1:
            folder_path = os.path.join("./download/", time_value)
            os.mkdir(folder_path)
            dn = 0
            for url_return in url_returns:
                try:
                    dn = dn + 1
                    url = url_return[0]
                    strdn = str(dn)
                    title = './download/'+time_value+'/'+strdn+'-'+time_value+'.mp4'
                    print('下载 ','\033[0;32;40m%s\033[0m'%strdn,'\033[0;32;40m/\033[0m','\033[0;32;40m%s\033[0m'%count,sep='')
                    download(url, title)
                except:
                    print('\033[0;31;40m下载出错\033[0m')
            print('\033[0;32;40m视频下载完成\033[0m')
            print('\033[0;32;40m保存于download文件夹\033[0m')
            input()
        else:
            url = url_returns[0][0]
            title = './download/'+time_value+'.mp4'
            download(url, title)
            print('\033[0;32;40m视频下载完成\033[0m')
            print('\033[0;32;40m保存于download文件夹\033[0m')
            # 检测终端是否在运行
            if is_process_running("WindowsTerminal.exe"):
                pass
            else:
                try:
                    # 执行ansicon二进制文件
                    executable = './bin/ansicon.exe'
                    arguments = ['-u']

                    # 使用subprocess模块执行可执行文件并传递参数
                    subprocess.run([executable] + arguments)
                except:
                    pass
            input()
    except:
        print('\033[0;31;40m下载关键性错误\033[0m')
        # 检测终端是否在运行
        if is_process_running("WindowsTerminal.exe"):
            pass
        else:
            try:
                # 执行ansicon二进制文件
                executable = './bin/ansicon.exe'
                arguments = ['-u']

                # 使用subprocess模块执行可执行文件并传递参数
                subprocess.run([executable] + arguments)
            except:
                pass
        input()