from models.GetInfo import data, video_url
from models.GetBV import get_p

def multi_cid():
    info_list = data['data']['ugc_season']['sections']
    info_list = info_list[0]['episodes']

    result_dict_list = []
    n = 0
    print()
    for dict in info_list:
        n = n+1
        cid = dict['cid']
        title = dict['title']
        bvid = dict['bvid']
        result_dict = {'num': n, 'title': title, 'cid': cid, 'bvid': bvid}
        result_dict_list.append(result_dict)
        print(n,'.',title,sep='')
    print()
    while True:
        try:
            i = input("\033[0;32;40m输入需要抓取的序号/列表(如1,2,3)/范围(如1-3): \033[0m")
            if '-' in i:
                i_range = i.split("-")
                z = int(i_range[0])
                x = int(i_range[1])
                i_list = []
                for i in range(z,x+1):
                    i_list.append(i)
            else:
                if ',' in i and '，' in i:
                    print("\033[0;31;40m输入格式有误,\033[0m",end='')
                    continue
                elif ',' in i:
                    i_list = i.split(",")
                else:
                    i_list = i.split("，")
            return_values = []
            m = 0
            failure = False
            for i in i_list:
                m = m + 1
                i = int(i)
                d = i - 1
                if i <= n and i>0:
                    download_list = result_dict_list[d]
                    print(d+1,'.', download_list['title'],sep='')
                    cid = download_list['cid']
                    bvid = download_list['bvid']
                    return_value = []
                    return_value.append(cid)
                    return_value.append(bvid)
                    return_values.append(return_value)
                else:
                    print('\033[0;31;40m输入范围有误,\033[0m',end='')
                    failure = True
                    break
            if failure:
                continue
            else:
                break
        except:
            print('\033[0;31;40m输入逻辑有误,\033[0m',end='')
            continue
    return return_values

def other_cid():
    info_list = data['data']['pages']
    result_dict_list = []
    n = 0
    print()
    for dict in info_list:
        n = n+1
        cid = dict['cid']
        title = dict['part']
        result_dict = {'num': n, 'title': title, 'cid': cid}
        result_dict_list.append(result_dict)
        print(n,'.',title,sep='')
    print()
    while True:
        try:
            i = input('\033[0;32;40m输入需要抓取的序号/列表(如1,2,3)/范围(如1-3): \033[0m')
            if '-' in i:
                i_range = i.split("-")
                z = int(i_range[0])
                x = int(i_range[1])
                i_list = []
                for i in range(z,x+1):
                    i_list.append(i)
            else:
                if ',' in i and '，' in i:
                    print("\033[0;31;40m输入格式有误,\033[0m",end='')
                    continue
                elif ',' in i:
                    i_list = i.split(",")
                else:
                    i_list = i.split("，")
            return_values = []
            m = 0
            failure = False
            for i in i_list:
                m = m + 1
                i = int(i)
                d = i - 1
                if i <= n and i>0:
                    download_list = result_dict_list[d]
                    print(d+1,'.', download_list['title'],sep='')
                    cid = download_list['cid']
                    bvid = data['data']['bvid']
                    return_value = []
                    return_value.append(cid)
                    return_value.append(bvid)
                    return_values.append(return_value)
                else:
                    print('\033[0;31;40m输入范围有误,\033[0m',end='')
                    failure = True
                    break
            if failure:
                continue
            else:
                break
        except:
            print('\033[0;31;40m输入逻辑有误,\033[0m',end='')
            continue
    return return_values

def other_single_cid():
    numberp = get_p(video_url)
    numberp = int(numberp)-1
    info_list = data['data']['pages']
    result_dict_list = []
    return_values = []
    n = 0
    print()
    for dict in info_list:
        n = n+1
        cid = dict['cid']
        title = dict['part']
        result_dict = {'num': n, 'title': title, 'cid': cid}
        result_dict_list.append(result_dict)
    print()
    download_list = result_dict_list[numberp]
    print(numberp+1,'.', download_list['title'],sep='')
    cid = download_list['cid']
    bvid = data['data']['bvid']
    return_value = []
    return_value.append(cid)
    return_value.append(bvid)
    return_values.append(return_value)
    return return_values

def single_cid():
    cid = data['data']['pages'][0]['cid']
    bvid = data['data']['bvid']
    return_value = []
    return_values = []
    return_value.append(cid)
    return_value.append(bvid)
    return_values.append(return_value)
    return return_values

def get_cid_bvid():
    info_list = data['data']
    if 'ugc_season' in info_list:
        print()
        print('该链接为合集视频, 选择抓取方式: ')
        print('\033[0;33;40m1.抓取当前视频\033[0m')
        print('\033[0;33;40m2.展开视频合集\033[0m')
        while True:
            select = input('\033[0;32;40m输入对应选项序号: \033[0m')
            if select == "1":
                return_value = single_cid()
                break
            elif select == "2":
                return_value = multi_cid()
                break
            else:
                print('\033[0;31;40m输入有误,\033[0m',end='')
                continue
    elif data['data']['videos'] != 1:
        print()
        numberp = get_p(video_url)
        print('\033[0;32;40mURL检测到分集: %s\033[0m'%numberp,sep='')
        print('该链接为合集视频, 选择抓取方式: ')
        print('\033[0;33;40m1.抓取当前视频\033[0m')
        print('\033[0;33;40m2.展开视频合集\033[0m')
        while True:
            select = input('\033[0;32;40m输入对应选项序号: \033[0m')
            if select == "1":
                return_value = other_single_cid()
                break
            elif select == "2":
                return_value = other_cid()
                break
            else:
                print('\033[0;31;40m输入有误,\033[0m',end='')
                continue

    else:
        return_value = single_cid()
    return return_value