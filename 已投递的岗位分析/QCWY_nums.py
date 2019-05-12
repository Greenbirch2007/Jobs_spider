#! -*- coding:utf-8 -*-
import datetime
import time

import pymysql
import requests
from lxml import etree
from selenium import webdriver

driver = webdriver.Chrome()
# 把find_elements 改为　find_element
def get_first_page():

    url = 'https://login.51job.com/login.php?lang=c'
    driver.get(url)
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="loginname"]').clear()
    driver.find_element_by_xpath('//*[@id="loginname"]').send_keys("")#用户名
    driver.find_element_by_xpath('//*[@id="password"]').clear()
    driver.find_element_by_xpath('//*[@id="password"]').send_keys("")#密码
    driver.find_element_by_xpath('//*[@id="login_btn"]').click()
    driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div[2]/div[2]/a').click()
    html = driver.page_source
    return html





# 把首页和翻页处理？

def next_page():
    for i in range(1,196):  # selenium 循环翻页成功！
        driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div/div/div/ul/li[last()]/a').click()
        time.sleep(1)
        html = driver.page_source
        return html



def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    big_list = []
    selector = etree.HTML(html)
    jobs = selector.xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div/div/a[1]/text()')
    job_link  =selector.xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div/div/a[1]/@href')
    firms = selector.xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div/div/a[2]/text()')
    salary = selector.xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div/div/span[1]/text()')
    nums = selector.xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div/div[3]/div/span/text()')
    page_nums = selector.xpath('//*[@id="jump_page"]/@value')
    f_page_nums = len(jobs)*page_nums

    long_tuple = (i for i in zip(jobs, job_link,firms, salary, nums,f_page_nums))
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
        cursor.executemany('insert into QCWY_NUM (jobs,job_link,firms,salary,nums,f_page_nums) values (%s,%s,%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration:
        pass





if __name__ == '__main__':
        html = get_first_page()
        time.sleep(1)
        content = parse_html(html)
        time.sleep(1)
        insertDB(content)
        while True:
            html = next_page()
            content = parse_html(html)
            insertDB(content)
            print(datetime.datetime.now())


# #
# create table QCWY_NUM(
# id int not null primary key auto_increment,
# jobs varchar(50),
# job_link varchar(100),
# firms varchar(80),
# salary varchar(16),
# nums varchar(8),
# f_page_nums varchar(6)
# ) engine=InnoDB  charset=utf8;

# drop table QCWY_NUM;

