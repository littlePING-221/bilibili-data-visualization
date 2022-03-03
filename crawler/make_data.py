import json
import os
from os import path
from pandas import DataFrame

# ### 生成时间线柱状图所用的数据格式
names = ['动画', '音乐', '舞蹈', '游戏', '知识', '数码', '汽车',
         '生活', '美食', '动物圈', '鬼畜', '时尚', '娱乐', '影视']
dir_names = ['2022-01-16single', '2022-01-17single', '2022-01-18single', '2022-01-19single', '2022-01-22single', '2022-01-23single', '2022-01-24single', '2022-01-25single', '2022-01-26single', '2022-01-28single', '2022-01-29single', '2022-01-30single', '2022-01-31single', '2022-02-01single', '2022-02-02single',
             '2022-02-03single', '2022-02-04single', '2022-02-05single', '2022-02-06single', '2022-02-07single', '2022-02-08single', '2022-02-09single', '2022-02-10single', '2022-02-11single', '2022-02-12single', '2022-02-13single', '2022-02-14single', '2022-02-15single', '2022-02-16single', '2022-02-17single']
sum_data = {}
normal_data = {}
for dir_name in dir_names:
    videos = []
    for i in range(len(names)):
        with open(path.join(dir_name, names[i]+'.json'), 'r') as f:
            t = json.load(f)
        for vid in t:
            d = {'section': names[i], 'duration': vid['duration']}
            d.update(vid['stat'])
            videos.append(d)
    videos = DataFrame(videos).iloc[:, [0, 1, 3, 4, 5, 6, 7, 8, 11]]
    # 总量数据
    videos_sum = videos.groupby('section').sum()
    videos_sum_dict = videos_sum.to_dict(orient='index')
    for k, v in videos_sum_dict.items():
        v['section'] = k
    key_name = dir_name.replace('single', '')
    sum_data[key_name] = list(videos_sum_dict.values())
    # 归一化数据
    normal_sum = videos_sum.div(videos_sum['view'], axis=0)*100
    normal_sum = normal_sum.iloc[:, 2:]
    normal_sum_dict = normal_sum.to_dict(orient='index')
    for k, v in normal_sum_dict.items():
        v['section'] = k
    key_name = dir_name.replace('single', '')
    normal_data[key_name] = list(normal_sum_dict.values())
with open('sum_data.json', 'w') as f:
    json.dump(sum_data, f, ensure_ascii=False)
with open('normal_data.json', 'w') as f:
    json.dump(normal_data, f, ensure_ascii=False)

# ### 散点图所用的数据格式
names = ['动画', '音乐', '舞蹈', '游戏', '知识', '数码', '汽车',
         '生活', '美食', '动物圈', '鬼畜', '时尚', '娱乐', '影视']
dir_name = '2022-02-01single'
videos = []
for i in range(len(names)):
    with open(path.join(dir_name, names[i]+'.json'), 'r') as f:
        t = json.load(f)
    for rank, vid in enumerate(t):
        d = {'section': names[i], 'duration': vid['duration'], 'title': vid['title'],
             'pic': vid['pic'], 'bvid': vid['bvid'], 'rank': rank+1}
        d.update(vid['stat'])
        videos.append(d)
DataFrame(videos)

videos = DataFrame(videos).loc[:, ['duration', 'view', 'danmaku', 'reply',
                                   'favorite', 'coin', 'share', 'like', 'section', 'title', 'pic', 'bvid', 'rank']]
data = {}
for name in names:
    data[name] = [list(i.values())
                  for i in videos.loc[videos['section'] == name].to_dict(orient='records')]
with open('scatter_data.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)
