#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2018/3/6 19:42
# @Author  : xinheng-cqb
# @Software: PyCharm Community Edition
# @introduce: 拉勾网数据爬取
from crawler.crawler_util import CrawlerUtil
import json
import datetime


class LaGouCrawler(object):
    def __init__(self):
        self.dir_absolute_path = 'E:\\拉钩网\\'
        self.position_list = ['Java', 'Python']
        self.city_list = ["保定", "北海", "北京", "包头", "滨州", "长春", "成都", "常德", "承德", "重庆", "长沙", "常州", "沧州", "郴州", "滁州",
                          "东莞",
                          "大连", "大理", "德阳", "东营", "德州", "达州", "佛山", "阜阳", "福州", "桂林", "贵阳", "广州", "赣州", "淮安", "邯郸",
                          "哈尔滨",
                          "合肥", "黄冈", "呼和浩特", "海口", "衡阳", "河源", "杭州", "惠州", "湖州", "菏泽", "金华", "江门", "荆门", "济南", "济宁",
                          "嘉兴",
                          "荆州", "昆明", "廊坊", "丽水", "洛阳", "临沂", "连云港", "兰州", "柳州", "泸州", "马鞍山", "绵阳", "梅州", "宁波", "南昌",
                          "南充",
                          "南京", "南宁", "南通", "南阳", "莆田", "青岛", "黔东南", "秦皇岛", "清远", "泉州", "日照", "韶关", "上海", "石家庄", "上饶",
                          "汕头",
                          "绍兴", "沈阳", "三亚", "深圳", "苏州", "泰安", "天津", "唐山", "太原", "台州", "泰州", "潍坊", "武汉", "芜湖", "威海",
                          "乌鲁木齐",
                          "无锡", "温州", "西安", "香港特别行政区", "厦门", "西宁", "新乡", "信阳", "襄阳", "咸阳", "徐州", "银川", "宜昌", "盐城", "营口",
                          "烟台", "岳阳", "扬州", "淄博", "珠海", "镇江", "湛江", "肇庆", "中山", "遵义", "郑州", "漳州", "株洲", "枣庄"]

    def crawl(self):
        error_list = []
        CrawlerUtil.mk_dirs(self.dir_absolute_path)
        for position in self.position_list:
            all_record = ['职位名称;薪资;公司名称;所在城市;发布时间']
            for city in self.city_list:
                document_str = CrawlerUtil.get_document_str(city, position)
                if document_str is None:
                    error_list.append('{0}_{1}_1'.format(position, city))
                json_info = json.loads(document_str)
                result_list = json_info['content']['data']['page']['result']
                all_record.extend(self.extract_info(result_list))
                total_count = int(json_info['content']['data']['page']['totalCount'])
                page_count = total_count // 15 + 1 // 15 if total_count % 15 == 0 else total_count // 15 + 2
                for page_no in range(2, page_count):
                    document_str = CrawlerUtil.get_document_str(city, position, page_no)
                    if document_str is None:
                        error_list.append('{0}_{1}_{2}'.format(position, city, page_no))
                    json_info = json.loads(document_str)
                    result_list = json_info['content']['data']['page']['result']
                    all_record.extend(self.extract_info(result_list))
            CrawlerUtil.export_excel(all_record, '{}{}.xls'.format(self.dir_absolute_path, position))

        # 将获取出错的记录写到本地核查原因
        with open('{0}error.txt'.format(self.dir_absolute_path), 'wb') as error_file:
            for error_info in error_list:
                error_file.write(error_info + '\n')

    @classmethod
    def extract_info(cls, result_list):
        city_record = []
        for result in result_list:
            temp_list = list()
            temp_list.append(result['positionName'])
            temp_list.append(result['salary'])
            temp_list.append(result['companyFullName'])
            temp_list.append(result['city'])
            create_time = result['createTime']
            if create_time.find('今天') >= 0:
                create_time = datetime.datetime.now().strftime('%Y-%m-%d')
            elif create_time.find('昨天') >= 0:
                now = datetime.datetime.now()
                create_time = datetime.date(now.year, now.month, now.day - 1).strftime('%Y-%m-%d')
            temp_list.append(create_time)
            city_record.append(';'.join(temp_list).replace('&nbsp;', '').replace('&amp;', '、'))
        return city_record


if __name__ == '__main__':
    LaGouCrawler().crawl()
