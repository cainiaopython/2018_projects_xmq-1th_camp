# Author:Yuki
# -*- coding: gb18030 -*-

import json
from urllib.parse import urlencode
import datetime
import requests
from requests import RequestException
import csv
import time
def get_page_index(city, keyword, pageNo):
    data = {
        'city': city,
        'positionName': keyword,
        'pageNo': pageNo,
        'pageSize': 15
    }
    url = 'http://m.lagou.com/search.json?' + urlencode(data)
    try:
        response = requests.get(url, timeout = 2.0)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求出错')
        return None

def parse_page_index(html):
    data = json.loads(html)
    if 'result' in data['content']['data']['page']:
        for item in data['content']['data']['page'].get('result'):
            yield {
                '公司全称': item.get('companyFullName'),
                '城市': item.get('city'),
                '岗位': item.get('positionName'),
                '薪资': item.get('salary'),
                '发布时间':item.get('createTime')
            }

def main():
    keyword = input("输入你想要搜索的岗位:")
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    string = keyword + '.csv'
    with open(string, 'w', newline='') as f:
        fieldnames = ['公司全称', '城市', '岗位', '薪资','发布时间']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for pageNo in range(1, 650):
            html = get_page_index('全国', keyword, pageNo)
            for url in parse_page_index(html):
                if '今天' in url['发布时间']:
                    url['发布时间'] = str(today)
                if '昨天' in url['发布时间']:
                    url['发布时间'] = str(yesterday)
                print(url)
                writer.writerow({'公司全称':url['公司全称'],
                              '城市':url['城市'],'岗位':url['岗位'], '薪资':url['薪资'],
                                '发布时间':url['发布时间']})
    f.close()

if __name__ == '__main__':
    t1 = time.time()
    main()
    print(time.time() - t1)
#56s