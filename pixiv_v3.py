# 此版本使用异步处理下载
import requests
import re
import json
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
# 打开日榜
dailyList = "https://www.pixiv.net/ranking.php"
list_page = 1
sum_all = 0
# 图片类型查找正则,或许可以稍后查找
# findtype = re.compile(r'"illust_page_count":"(\d)"')
# 图片id查找正则
# findid = re.compile('"illust_id":(\d*?),')
# find_title = re.compile(r'<title>(.*?)</title>')
save_path = "爬虫进阶/output/"
# 获取排行榜信息的函数

def get_src_list():
    global list_page
    param = {  # 设置参数
        "p": list_page,
        "format": "json"
    }
    resp = requests.get(url=dailyList, params=param)
    # resp.close()
    list_page = list_page+1
    # data = resp.json
    dict=json.loads(resp.text)['contents']
    print(type(dict))
    return dict
# print(list_page)

# 解析排行榜信息


# def get_rank_list(doc):
#     rank_id_list = re.findall(findid, doc)
#     rank_page_list = re.findall(findtype, doc)
#     rank_list = [list(t) for t in zip(rank_id_list, rank_page_list)]
#     return rank_list

def get_rank_list_bydict(dict):
    rank_list = []
    for item in dict:
        rank_list.append([item['illust_id'],item['illust_page_count'],item['title']])
    return rank_list


# 下载单个img


def dowload_singal_img(origin_img_url, download_path):
    head = {  # 模拟头部发送消息
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        "referer": "https://www.pixiv.net/",
    }
    # img = requests.get(origin_img_url, headers=head)
    # with open(download_path, "wb") as f:
    #     f.write(img.content)
    #     f.close()
    #     img.close()

# 解析一个插画有多少页

async def download_original_img(origin_img_url, download_path):
    header = {  # 模拟头部发送消息
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        "referer": "https://www.pixiv.net/",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(origin_img_url,headers = header) as resp:
             with open(download_path,"wb") as f:
                 f.write(resp.content)
                 

    # img = requests.get(origin_img_url, headers=head)
    # with open(download_path, "wb") as f:
    #     f.write(img.content)
    #     f.close()
    #     img.close()


def get_singal_url_src(illust, numb):
    # print(1)
    resp = requests.get(f"https://www.pixiv.net/artworks/{illust[0]}")
    global sum_all
    illust[2] = illust[2].replace(' ','')
    # print(resp.status_code)
    sum_all += illust[1]
    if illust[1] != 1:
        # print(illust[1])
        find_origin_url = re.compile(r'"original":"(.*?)"')
        origin_url = re.findall(find_origin_url, resp.text)[0]
        # title = f"#{numb}"+re.findall(find_title, resp.text)[0].split(' ')[1]
        # print(1)
        final_path = save_path+f"#{numb}_{illust[0]}_{illust[2]}"
        end = origin_url[-4::]
        for i in range(illust[1]):
            tmp = origin_url.replace("p0.", f"p{i}.")
            dowload_singal_img(tmp, final_path+f"_p{i+1}"+end)
    else:
        find_origin_url = re.compile(r'"original":"(.*?)"')
        origin_url = re.findall(find_origin_url, resp.text)[0]
        final_path = save_path+f"#{numb}_{illust[0]}_{illust[2]}{origin_url[-4::]}"
        dowload_singal_img(origin_url, final_path)
    resp.close()
    # print(final_path)
    print(f"第{numb}张已下载完成")


# 创建文件
# def mkdir(folder):
#     # folder = save_path+path
#     # print(folder)
#     is_exist = os.path.exists(folder)
#     if not is_exist:  # 判断是否存在文件夹如果不存在则创建为文件夹
#         os.makedirs(folder)  # makedirs 创建文件时如果路径不存在会创建这个路径
#         print(f"new folder: {folder}")
#     else:
#         print("---  There is this folder!  ---")


# file = "testmakenew"
# mkdir(file)  # 调用函数


# tmp = ['95430270', 1]
# get_singal_url_src(tmp,1)
# print("----end----")
def using_thread(rank_list):
    with ThreadPoolExecutor(10) as t:
        i = 1
        for illust in rank_list:
            illust[1] = int(illust[1])
            t.submit(get_singal_url_src, illust=illust, numb=i)
            i += 1
    print(f"下载完成,共{len(rank_list)}份插画,共{sum_all}张")


def main():
    dict = get_src_list()
    # print(html)
    rank_list = get_rank_list_bydict(dict)
    print(rank_list)
    print(len(rank_list))
    # for i in rank_list:
    #     print (i[1])

    using_thread(rank_list)

    # for illust in rank_list:
    #     print(illust)
    #     get_singal_url_src(illust, nownumb)
    #     nownumb = nownumb+1

    # print(rank_list)


main()
