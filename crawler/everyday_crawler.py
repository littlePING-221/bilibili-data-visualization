import requests as rq
from pandas import DataFrame
import os
from os import path
import datetime as dt
import json
import time, random

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
rank_api = 'https://api.bilibili.com/x/web-interface/ranking/v2'
names = ['动画', '音乐', '舞蹈', '游戏', '知识', '数码', '汽车', '生活', '美食', '动物圈', '鬼畜', '时尚', '娱乐', '影视']
rid = [1, 3, 129, 4, 36, 188, 223, 160, 211, 217, 119, 155, 5, 181]
today = str(dt.date.today())
try:
    os.mkdir(today)
except FileExistsError:
    pass
# 爬取排行榜视频列表
params_list = [{'rid':str(rid[i]), 'type':'all'} for i in range(len(rid)) if names[i]+'.json' not in os.listdir(today)]
res_list = [rq.get(rank_api, headers=headers, params=i) for i in params_list]
#写文件
for i in range(len(res_list)):
    with open( path.join(today, names[i]+'.json'), 'w') as f:
        f.write(res_list[i].text)
#读取
aids = {}
for name in names:
    with open(path.join(today, name+'.json'), 'r') as f:
        video_list = json.load(f).get('data').get('list')
    aids[name] = [video['stat']['aid'] for video in video_list]

#用api爬取单个视频的信息
from bilibili_api import video
from bilibili_api.exceptions import BilibiliException
dir_name = today+'single'
try:
    os.mkdir(dir_name)
except FileExistsError:
    pass

for name in names:
    if name+'.json' in os.listdir(dir_name):
        continue
    res_list = []
    for av in aids[name]:
        try:
            data = video.get_video_info(aid=av, is_simple=False)
            res_list.append(data)
        except BaseException as e:
            with open('./error.log','a') as f:
                f.writelines(today+ name+ str(av)+ str(e))
            time.sleep(10)
        sleep_time = random.random()*2
        time.sleep(sleep_time)
    with open( path.join(dir_name, name+'.json'), 'w') as f:
        json.dump(res_list, f,ensure_ascii=False)