#! -*- coding:utf-8 -*-
import datetime
import time

import pymysql
import requests
from lxml import etree
from selenium import webdriver

# 把find_elements 改为　find_element
def get_first_page():

    url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,golang,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    return html





# 把首页和翻页处理？

def next_page():
    for i in range(1,44):  # selenium 循环翻页成功！
        driver.find_element_by_xpath('//*[@id="resultList"]/div[55]/div/div/div/ul/li[last()]/a').click()
        time.sleep(1)
        html = driver.page_source
        return html



def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    big_list = []
    selector = etree.HTML(html)
    jobs = selector.xpath("//div[@class='dw_table']/div/p/span[1]/a/@title")
    link = selector.xpath("//div[@class='dw_table']/div/p/span[1]/a/@href")
    firms = selector.xpath('//*[@id="resultList"]/div/span[1]/a/text()')
    long_tuple = (i for i in zip(jobs, link, firms))
    for i in long_tuple:
        big_list.append(i)
    return big_list


        # 存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456',
                                 db='JOB',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into all_golang (jobs,link,firms) values (%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration:
        pass





if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)

    html = get_first_page()
    content = parse_html(html)
    time.sleep(1)
    insertDB(content)
    while True:
        html = next_page()
        content = parse_html(html)
        insertDB(content)
        print(datetime.datetime.now())
        time.sleep(1)


# #
# create table all_golang(
# id int not null primary key auto_increment,
# jobs varchar(80),
# link varchar(88),
# firms varchar(80)
# ) engine=InnoDB  charset=utf8;