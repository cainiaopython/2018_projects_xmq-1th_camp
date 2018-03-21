# coding=utf-8
import requests
import json
import time
import random
import pandas as pd
from IPython.core.display import clear_output
from warnings import warn
from threading import Thread
# @author=lufay

def get_page(url, cookies, headers, data):
    try:
        page = requests.post(url=url, cookies=cookies, headers=headers, data=data)
        page.encoding = 'utf-8'
        if page.status_code == 200:
            result = page.json()
            return result
        else:
            warn('Status code not 200, please check!')
    except RecursionError:
        return None
    # print(result)


def get_page_num(page):
    # total jon count
    total_count = page['content']['positionResult']['totalCount']
    # displayed job count per page
    result_size = page['content']['positionResult']['resultSize']
    # total page count
    page_num = int(total_count) // int(result_size) + 1

    # return the scraping total page count
    return page_num


def parse_job(page):
    # job info
    jobs = page['content']['positionResult']['result']
    # print(jobs)

    results = {}
    company_names = []
    position_names = []
    salaries = []
    cities = []
    create_times = []

    for job in jobs:
        company_full_name = job['companyFullName']
        print(company_full_name)
        company_names.append(company_full_name)

        position_name = job['positionName']
        print(position_name)
        position_names.append(position_name)

        salary = job['salary']
        print(salary)
        salaries.append(salary)

        create_time = job['formatCreateTime']
        print(create_time)
        create_times.append(create_time)

        city = job['city']
        print(city)
        cities.append(city)

        time.sleep(1)
        print('*' * 50)

    results['company_name'] = company_names
    results['position_name'] = position_names
    results['salary'] = salaries
    results['create_time'] = create_times
    results['city'] = cities

    print(results)

    return results


def save_to_file(content):
    df = pd.DataFrame(content)
    print(df.info())

    # with open('lagou_python.csv', 'a') as f:
    df.to_csv('lagou_python.csv',  mode='a', index=False, header=False, encoding='utf_8_sig')


    print(df)


def main():
    url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'

    headers = {
        'Host': 'www.lagou.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.lagou.com/jobs/list_Python?labelWords=&fromSearch=true&suginput=',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Anit-Forge-Token': 'None',
        'X-Anit-Forge-Code': '0',
        'Content-Length': '26',
        # 'Cookie': 'user_trace_token=20171103191801-9206e24f-9ca2-40ab-95a3-23947c0b972a; _ga=GA1.2.545192972.1509707889; LGUID=20171103191805-a9838dac-c088-11e7-9704-5254005c3644; JSESSIONID=ABAAABAACDBABJB2EE720304E451B2CEFA1723CE83F19CC; _gat=1; LGSID=20171228225143-9edb51dd-ebde-11e7-b670-525400f775ce; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DKkJPgBHAnny1nUKaLpx2oDfUXv9ItIF3kBAWM2-fDNu%26ck%3D3065.1.126.376.140.374.139.129%26shh%3Dwww.baidu.com%26sht%3Dmonline_3_dg%26wd%3D%26eqid%3Db0ec59d100013c7f000000055a4504f6; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGRID=20171228225224-b6cc7abd-ebde-11e7-9f67-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_search; SEARCH_ID=3ec21cea985a4a5fa2ab279d868560c8',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    cookies = {
        'Cookie': 'user_trace_token=20180309150141-1071c3b86d9340849221995337e696ab;'
                  '_ga=GA1.2.26456326.1520578906; _gid=GA1.2.1110652441.1520578906; '
                  'LGUID=20180309150146-bb3feaf5-2367-11e8-a4d0-525400f775ce; _gat=1; '
                  'LGSID=20180309220646-1a31dfca-23a3-11e8-a7fa-525400f775ce; '
                  'PRE_UTM=m_cf_cpt_baidu_pc; '
                  'PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Fs%3Fwd%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26rsv_spt%3D1%26rsv_iqid%3D0xc5bd295800005d78%26issp%3D1%26f%3D8%26rsv_bp%3D0%26rsv_idx%3D2%26ie%3Dutf-8%26tn%3Dbaiduhome_pg%26rsv_enter%3D1%26rsv_sug3%3D4%26rsv_sug1%3D4%26rsv_sug7%3D100; '
                  'PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpt_baidu_pc; '
                  'JSESSIONID=ABAAABAAADEAAFIFD520A39CCC6F8DB23972BE849E096FD; '
                  'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1520578906,1520604405,1520604412; '
                  'index_location_city=%E5%85%A8%E5%9B%BD; hideSliderBanner20180305WithTopBannerC=1; '
                  'TG-TRACK-CODE=index_search; SEARCH_ID=00df79401e894f288caf5da82944a99d; '
                  'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1520604432; '
                  'LGRID=20180309220712-2a00fa16-23a3-11e8-b1a7-5254005c3644',
    }

    data = {
        'first': 'false',
        'pn': 1,
        'kd': 'python',
    }

    # page = get_page(url, cookies, headers, data)
    # page_num = get_page_num(page)
    # pages = [i for i in range(1, page_num)]

    start_time = time.time()
    # moniter parameter
    requests = 0

    for page in range(1, 3):
        # a request would go here
        print('爬取第{}页'.format(page))
        data['pn'] = page
        html = get_page(url, cookies, headers, data)
        time.sleep(random.randint(5, 8))

        requests += 1
        elapsed_time = time.time() - start_time
        print('Request: {}; Frequency: {} requests/s'.format(requests, requests / elapsed_time))
        clear_output(wait=True)
        contents = parse_job(html)
        save_to_file(contents)


if __name__ == '__main__':
    main()