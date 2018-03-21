'''
在单位改的版本
重点解决问题：
1.提取发布日期数据，并转换成绝对日期
2.增加异常处理，把json崩的数据页面打印出来
'''
#-*- coding:utf-8 -*-
import sys
import time
import json
import datetime
import re

from fake_useragent import UserAgent
import requests
import pandas as pd
from threading import Thread#使用多线程同时爬取python java JS GO四门语言

#print(sys.version)
job_li = ['python', 'java', 'GO', 'JS']
END_PAGE = 500#最多爬取500页数据

headers = {
    'Cookie':'JSESSIONID=ABAAABAAAIAACBI83C0FEA0F53ED7B6FA600089BD3D1BB4; SEARCH_ID=8931b1f2f285465791125b473fb5cf1c; user_trace_token=20171207195919-4987e748-43ae-4a1e-9e06-37146c72d779; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1512647972; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1512647972; LGSID=20171207195919-0e80ffdd-db46-11e7-9c4d-5254005c3644; PRE_UTM=; PRE_HOST=static.dcxueyuan.com; PRE_SITE=https%3A%2F%2Fstatic.dcxueyuan.com%2Fcontent%2Fdisk%2Ftrain%2Fother%2F70b2c405-138b-4862-ad49-138656aef0d6.html; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E7%2588%25AC%25E8%2599%25AB%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; LGRID=20171207195919-0e810180-db46-11e7-9c4d-5254005c3644; LGUID=20171207195919-0e8101ea-db46-11e7-9c4d-5254005c3644; _ga=GA1.2.1616202485.1512647972; _gid=GA1.2.823794854.1512647972; TG-TRACK-CODE=search_code',
    'Referer':'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput='
}

def date_change(create_time):#create_time是直接从网上获取的时间相关数据
	cre_date = ''
	today = datetime.date.today() #获得今天的日期
	if re.match(r'\d+天', create_time):#筛选出“XX天前发布”的格式
		delay_days = int(re.match(r'\d+', create_time).group())
		cre_date = today - datetime.timedelta(days=delay_days)
		cre_date = cre_date.strftime('%Y-%m-%d')#将datetime.date类型转换为字符串
	elif re.match(r'\d+:', create_time):#筛选出XX：XX发布的格式
		cre_date = today
		cre_date = cre_date.strftime('%Y-%m-%d')#将datetime.date类型转换为字符串
	else:#筛选出类似“2018-03-01”的格式
		cre_date = create_time
	return cre_date

def get_job_info(start_page, kd):
    df_li = []
    i = start_page
    url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'
    while True:
        if i >= END_PAGE:
        	print('this is the End Page')
        	break
        payload = {
            'first':'false',
            'pn':i,
            'kd':kd
        }
        ua = UserAgent()
        headers['User-Agent'] = ua.random
        response = requests.post(url, data = payload, headers = headers)
        if response.status_code == 200:
            py_data = response.json()['content']['positionResult']['result']
            if py_data:#不为空，即该页有数据
	            js_data = json.dumps(py_data)
	            df = pd.read_json(js_data).loc[:,['positionName','companyFullName','salary','city','companySize',\
	                'workYear','education','industryField','formatCreateTime']]
	            for j in range(len(df)):
	            	df.formatCreateTime[j] = date_change(df.formatCreateTime[j])
	            df_li.append(df)
	            #pd.read_json(json_data):将json格式的数据转化成dataframe格式
	            print('正在爬取%s第%d页数据...' %(kd, (i)))
	            i = i+1
            else:
                print('%sfinished' %kd)
                break
        else:
            print('someting is wrong with %s' %kd)


        #df.to_csv('job.csv', mode = 'a', encoding = 'GB18030')
        time.sleep(1)
    if len(df_li) >= 1:
        df = pd.concat(df_li)
        df.to_csv('job_%s.csv' %kd, encoding = 'GB18030')
    #print(df)

def multi_work(start_page):#建立4个线程，分别爬取4种岗位
    ts = [Thread(target=get_job_info, args=(start_page, kd)) for kd in job_li]
    t1 = time.time()
    for t in ts:
        t.start()
    for t in ts:
        t.join()


if __name__ == '__main__':
    multi_work(1)
