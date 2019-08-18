import datetime
import re
import time

import pymysql
import requests
from lxml import etree
from requests.exceptions import RequestException
from bs4 import BeautifulSoup


def call_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

# 正则和lxml混用
def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    big_list = []
    selector = etree.HTML(html)
    jobs = selector.xpath("/html/body/div[3]/div[2]/div[2]/div/div[1]/h1/@title")
    salary = selector.xpath("/html/body/div[3]/div[2]/div[2]/div/div[1]/strong/text()")
    firms = selector.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a[1]/@title')
    all_descs = selector.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div/p/text()')

    all_descs_str = "".join(all_descs)
    all_descs_str_list = str(all_descs_str)
    str_list = [("".join(all_descs_str_list))] #直接用中括号进行列表化，而不要使用list　前者直接对整体处理，后者要细分
    patt1 = re.compile('title="(.*?)&nbsp;')
    nums1 = re.findall(patt1, html)
    nums_1 = nums1[0:1]
    patt2 = re.compile('&nbsp;招(.*?)人&nbsp;',re.S)
    nums2 = re.findall(patt2,html)
    nums_2 = nums2[0:1]
    long_list = jobs + salary + firms + nums_1 + nums_2 + str_list
    long_list_tuple = [tuple(long_list)]

    for i in long_list:
        big_list.append(i)

    return long_list_tuple









def Python_sel_Mysql():
    # 使用cursor()方法获取操作游标
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='JOB',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cur = connection.cursor()
    #sql 语句
    for i in range(1,1597):
        sql = 'select link from C_plus__finance1 where id = %s ' % i
        # #执行sql语句
        cur.execute(sql)
        # #获取所有记录列表
        data = cur.fetchone()
        url = data['link']
        yield url

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='JOB',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        cursor.executemany('insert into C_plus__finance2 (jobs, salary,firms, location,nums,str_list) values (%s,%s,%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass



if __name__ == '__main__':
    for url_str in Python_sel_Mysql():
        html = call_page(url_str)
        try:

            content = parse_html(html)
            insertDB(content)
            print(datetime.datetime.now())
        except ValueError :
            pass


#
#
# create table C_plus__finance2(
# id int not null primary key auto_increment,
# jobs varchar(80),
# salary varchar(88),
# firms varchar(80),
# location varchar(80),
# nums varchar(8),
# str_list text
# ) engine=InnoDB  charset=utf8;
#
# drop table C_plus__finance2;