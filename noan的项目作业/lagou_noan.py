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
        print('�������')
        return None

def parse_page_index(html):
    data = json.loads(html)
    if 'result' in data['content']['data']['page']:
        for item in data['content']['data']['page'].get('result'):
            yield {
                '��˾ȫ��': item.get('companyFullName'),
                '����': item.get('city'),
                '��λ': item.get('positionName'),
                'н��': item.get('salary'),
                '����ʱ��':item.get('createTime')
            }

def main():
    keyword = input("��������Ҫ�����ĸ�λ:")
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    string = keyword + '.csv'
    with open(string, 'w', newline='') as f:
        fieldnames = ['��˾ȫ��', '����', '��λ', 'н��','����ʱ��']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for pageNo in range(1, 650):
            html = get_page_index('ȫ��', keyword, pageNo)
            for url in parse_page_index(html):
                if '����' in url['����ʱ��']:
                    url['����ʱ��'] = str(today)
                if '����' in url['����ʱ��']:
                    url['����ʱ��'] = str(yesterday)
                print(url)
                writer.writerow({'��˾ȫ��':url['��˾ȫ��'],
                              '����':url['����'],'��λ':url['��λ'], 'н��':url['н��'],
                                '����ʱ��':url['����ʱ��']})
    f.close()

if __name__ == '__main__':
    t1 = time.time()
    main()
    print(time.time() - t1)
#56s