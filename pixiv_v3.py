# 此版本使用异步处理下载
import requests
import re
import json
import asyncio
import aiohttp
import aiofiles
# 打开日榜
dailyList = "https://www.pixiv.net/ranking.php"
list_page = 1
sum_all = 0
tasks = []
# 图片类型查找正则,或许可以稍后查找
# findtype = re.compile(r'"illust_page_count":"(\d)"')
# 图片id查找正则
# findid = re.compile('"illust_id":(\d*?),')
# find_title = re.compile(r'<title>(.*?)</title>')
save_path = ""
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
    # print(type(dict))
    return dict

def get_rank_list_bydict(dict):
    rank_list = []
    for item in dict:
        rank_list.append([item['illust_id'],item['illust_page_count'],item['title']])
    return rank_list


async def download_original_img(origin_img_url, download_path):
    header = {  # 模拟头部发送消息
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        "referer": "https://www.pixiv.net/"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(origin_img_url,headers = header) as resp:
            async with open(download_path,"wb") as f:
                await f.write(await resp.content.read())


async def get_singal_img_url(illust, numb):
    print('running')
    async with aiohttp.ClientSession() as session:
        print('test02')
        async with session.get(f"https://www.pixiv.net/artworks/{illust[0]}") as resp:
            print('test03')
            # resp = requests.get(f"https://www.pixiv.net/artworks/{illust[0]}")
            global sum_all
            illust[2] = illust[2].replace(' ','')
            # print(resp.status_code)
            sum_all += illust[1]
            
            html = await resp.text()
            if illust[1] != 1:
                # print(illust[1])
                find_origin_url = re.compile(r'"original":"(.*?)"')
                origin_url = re.findall(find_origin_url, html)[0]
                # title = f"#{numb}"+re.findall(find_title, resp.text)[0].split(' ')[1]
                # print(1)
                final_path = save_path+f"#{numb}_{illust[0]}_{illust[2]}"
                end = origin_url[-4::]
                for i in range(illust[1]):
                    tmp = origin_url.replace("p0.", f"p{i}.")
                    tasks.append(download_original_img(tmp, final_path+f"_p{i+1}"+end))
            else:
                find_origin_url = re.compile(r'"original":"(.*?)"')
                origin_url = re.findall(find_origin_url, html)[0]
                final_path = save_path+f"#{numb}_{illust[0]}_{illust[2]}{origin_url[-4::]}"
                tasks.append(download_original_img(origin_url, final_path))
            print(f"第{numb}张已下载完成")


if __name__ =='__main__':
    id_page_title_list = get_rank_list_bydict(get_src_list())
    illust = "96271793"
    numb = '1'
    asyncio.run(get_singal_img_url(illust, numb))
    