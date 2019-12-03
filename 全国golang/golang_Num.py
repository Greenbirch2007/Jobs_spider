import datetime
import re
import time
from selenium import webdriver
import pymysql
import requests
from lxml import etree
from requests.exceptions import RequestException

def call_page(url):
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    return html
# 正则和lxml混用
def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    big_list = []
    selector = etree.HTML(html)
    jobs = selector.xpath("/html/body/div[3]/div[2]/div[2]/div/div[1]/h1/@title")
    salary = selector.xpath("/html/body/div[3]/div[2]/div[2]/div/div[1]/strong/text()")
    firms = selector.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a[1]/@title')
    patt = re.compile('&nbsp;招(.*?)人&nbsp;',re.S)
    nums = re.findall(patt,html)
    nums0 = nums[0:1]
    long_tuple = (i for i in zip(jobs, salary,firms, nums0))
    for i in long_tuple:
        big_list.append(i)
    return big_list








def Python_sel_Mysql():
    # 使用cursor()方法获取操作游标
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='JOB',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cur = connection.cursor()
    #sql 语句
    for i in range(1,2127):
        sql = 'select link from all_golang where id = %s ' % i
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
        cursor.executemany('insert into all_golang_NUm (jobs, salary,firms, nums0) values (%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass



if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)
    for url_str in Python_sel_Mysql():
        html = call_page(url_str)
        time.sleep(3)
        big_list = []
        selector = etree.HTML(html)
        jobs = selector.xpath("/html/body/div[3]/div[2]/div[2]/div/div[1]/h1/@title")
        salary = selector.xpath("/html/body/div[3]/div[2]/div[2]/div/div[1]/strong/text()")
        firms = selector.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a[1]/@title')
        big_list

        print(big_list)

        # insertDB(content)
        print(datetime.datetime.now())






# create table all_golang_NUm(
# id int not null primary key auto_increment,
# jobs varchar(80),
# firms varchar(80),
# salary varchar(88)
# ) engine=InnoDB  charset=utf8;