#! -*- coding:utf-8 -*-
import datetime
import time

import pymysql
import requests
from lxml import etree
from selenium import webdriver

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
    driver.find_element_by_xpath('//*[@id="topIndex"]/div/p/a[2]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="kwdselectid"]').send_keys("go")  #可以针对其他岗位进行统计分析
    # 还要剔除本地选项　　（“”）
    # 剔除本地，选择全国范围
    driver.find_element_by_xpath('//*[@id="work_position_input"]').click()
    driver.find_element_by_xpath('//*[@id="work_position_click_multiple_selected_each_110900"]/em').click()
    driver.find_element_by_xpath('//*[@id="work_position_click_bottom_save"]').click()
    driver.find_element_by_xpath('/html/body/div[2]/form/div/div[1]/button').click()
    time.sleep(1)



    # 搜索按钮


    html = driver.page_source
    return html




# 把首页和翻页处理？

def next_page():
    for i in range(1,111):  # selenium 循环翻页成功！
        driver.find_element_by_xpath('//*[@id="resultList"]/div[55]/div/div/div/ul/li[last()]/a').click()
        time.sleep(2)
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


def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456',
                                 db='JOB',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into GO_link (jobs,link,firms) values (%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration:
        pass





if __name__ == '__main__':
    driver = webdriver.Chrome()

    html = get_first_page()
    content = parse_html(html)
    time.sleep(1)
    insertDB(content)
    while True:
        try:

            html = next_page()
            content = parse_html(html)
            insertDB(content)
            print(datetime.datetime.now())
            time.sleep(1)
        except:
            pass


# # jobs,link
# create table GO_link(
# id int not null primary key auto_increment,
# jobs varchar(100),
# link varchar(88),
# firms varchar(80)
# ) engine=InnoDB  charset=utf8;

# drop  table GO_link;