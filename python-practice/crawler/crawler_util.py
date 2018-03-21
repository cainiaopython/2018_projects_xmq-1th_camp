#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2018/3/6 19:53
# @Author  : xinheng-cqb
# @Software: PyCharm Community Edition
# @introduce: 爬虫工具包
import os
import requests
import random
import time
import xlwt


class CrawlerUtil(object):
    def __init__(self):
        pass

    @staticmethod
    def mk_dirs(dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    @staticmethod
    def get_document_str(city, position, page_no=1, page_size=15, try_count=3):
        try_num = 0
        url = 'https://m.lagou.com/search.json?city={0}&positionName={1}&pageNo={2}&pageSize={3}'.format(city, position,
                                                                                                         page_no,
                                                                                                         page_size)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
        while try_num < try_count:
            try:
                time.sleep(random.randint(0, 3000) / 1000.0)
                res = requests.get(url, headers=headers, timeout=30)
                if not 200 == res.status_code:
                    print('ERROR CODE:', res.status_code)
                    return None
                return res.content
            except Exception as e:
                print(e)
                if try_count == try_num:
                    return None
            try_num += 1
        pass

    @staticmethod
    def export_excel(content_list, path='test.xls', rotate=False):
        '''
        :param content_list: 每一行中用分号来分隔
        :param path: 不要用默认的路径，需要指定
        :param rotate: 是否需要将行列进行转换
        '''
        style = xlwt.easyxf('align: vertical center, horizontal center')
        w_book = xlwt.Workbook(encoding='utf-8')  # 指定编码,解决文件内容中文问题
        w_sheet = w_book.add_sheet('data')
        for x_index, line in enumerate(content_list):
            for y_index, value in enumerate(line.split(';')):
                if not rotate:
                    w_sheet.write(x_index, y_index, value, style)
                else:
                    w_sheet.write(y_index, x_index, value, style)
        try:
            w_book.save(path)
        except Exception as e:
            print(e)
        else:
            print('save excel file success, path :', path)
