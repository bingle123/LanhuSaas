# encoding:utf-8
import re
import logging
import requests
from lxml import etree
from shell_app.tools import error_result
from shell_app.tools import success_result
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


logger = logging.getLogger(__name__)


def crawl_temp(url, total_xpath, title_xpath, time_xpath, url_xpath):
    """
    爬虫模板
    :param url:             爬虫目标URL
    :param total_xpath:     总Xpath
    :param title_xpath:     标题Xpath
    :param time_xpath:      时间Xpath
    :param url_xpath:       资源Xpath
    :return:
    """
    logger.info(u'begin crawl info......')
    res = requests.get(url)
    status_code = res.status_code       # 请求状态码
    if status_code == 200:
        try:
            # 返回etree格式HTML
            response_html = etree.HTML(res.content)
            html_list = response_html.xpath(total_xpath)
            temp_list = []
            for temp in html_list:
                temp_dict = {}
                time = temp.xpath(time_xpath)[0]
                title = temp.xpath(title_xpath)[0]
                resource = temp.xpath(url_xpath)[0]
                temp_dict['time'] = time
                temp_dict['title'] = title
                temp_dict['resource'] = resource
                temp_list.append(temp_dict)
            return success_result(temp_list)
        except Exception as e:
            return error_result(str(e)+u'Xpath配置异常')
    elif status_code == 403:
        return error_result("你没有权限,URL拒绝访问")
    elif status_code == 404:
        return error_result("请检查你的URL,找不到URL")
    elif status_code == 500:
        return error_result("URL系统错误")


def crawl_temp_test(url, total_xpath, title_xpath, time_xpath, url_xpath):
    """
    爬虫模板测试用例
    :param url:             爬虫目标URL
    :param total_xpath:     总Xpath
    :param title_xpath:     标题Xpath
    :param time_xpath:      时间Xpath
    :param url_xpath:       资源Xpath
    :return:
    """
    logger.info(u'begin crawl info......')

    # 指明phantomjs的执行路径
    driver = webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    driver.get(url)

    # 方法1：显式给3秒加载时间
    time.sleep(3)

    # 方法2：让 Selenium 不断地检查某个元素是否存在，以此确定页面是否已经完全加载(需要导入库)
    try:
        # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "loadedButton")))
        pass
    finally:
        # print(driver.page_source)
        pass
    res = requests.get(url)
    status_code = res.status_code       # 请求状态码
    if status_code == 200:
        try:
            # 返回etree格式HTML
            # response_html = etree.HTML(res.content)
            response_html = etree.HTML(driver.page_source)
            html_list = response_html.xpath(total_xpath)
            temp_list = []
            # print res.content
            for temp in html_list:
                temp_dict = {}
                time1 = temp.xpath(time_xpath)[0]
                title = temp.xpath(title_xpath)[0]
                resource = temp.xpath(url_xpath)[0]
                res = change_url(resource)
                print res
                temp_dict['time'] = time1
                temp_dict['title'] = title
                temp_dict['resource'] = resource
                temp_list.append(temp_dict)
            return success_result(temp_list)
        except Exception as e:
            return error_result(str(e)+u'Xpath配置异常')
    elif status_code == 403:
        return error_result("你没有权限,URL拒绝访问")
    elif status_code == 404:
        return error_result("请检查你的URL,找不到URL")
    elif status_code == 500:
        return error_result("URL系统错误")


def change_url(string):
    """
    去除URL的‘.’字符
    :param string:
    :return:
    """
    result = string[:1]
    # print result
    if result == '.':
        return change_url(string.lstrip('.'))
    if result == '/':
        return string



