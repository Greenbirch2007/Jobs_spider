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
    driver.find_element_by_xpath('//*[@id="loginname"]').send_keys("") #用户名
    driver.find_element_by_xpath('//*[@id="password"]').clear()
    driver.find_element_by_xpath('//*[@id="password"]').send_keys("")#密码
    driver.find_element_by_xpath('//*[@id="login_btn"]').click()
    driver.find_element_by_xpath('//*[@id="topIndex"]/div/p/a[2]').click()  #选择搜索职位
    driver.find_element_by_xpath('//*[@id="kwdselectid"]').send_keys("C++")  #搜索内容
    driver.find_element_by_xpath('//*[@id="work_position_input"]').click()#选择全国
    driver.find_element_by_xpath('//*[@id="work_position_click_multiple_selected_each_200200"]/span').click()#选择全国
    driver.find_element_by_xpath('//*[@id="work_position_click_bottom_save"]').click()#选择全国
    driver.find_element_by_xpath('//*[@id="indtype_input"]').click()#金融证券业
    driver.find_element_by_xpath('//*[@id="indtype_click_center_left_each_41"]').click()#金融证券业
    driver.find_element_by_xpath('//*[@id="indtype_click_center_right_list_category_41_03"]').click()#金融证券业
    driver.find_element_by_xpath('//*[@id="indtype_click_bottom_save"]').click()#金融证券业
    driver.find_element_by_xpath('/html/body/div[2]/form/div/div[1]/button').click()#　进行整体搜索操作

    html = driver.page_source
    return html





# 把首页和翻页处理？

def next_page():
    for i in range(1,33):  # selenium 循环翻页成功！
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
        cursor.executemany('insert into C_plus__finance1 (jobs,link,firms) values (%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration:
        pass





if __name__ == '__main__':
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


#
# create table C_plus__finance1(
# id int not null primary key auto_increment,
# jobs varchar(80),
# link varchar(88),
# firms varchar(80)
# ) engine=InnoDB  charset=utf8;