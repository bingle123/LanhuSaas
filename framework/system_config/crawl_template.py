# encoding:utf-8
import re
import logging
import requests
from shell_app.tools import error_result
from shell_app.tools import success_result
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# 请暂时删除
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
import time
import datetime

logger = logging.getLogger(__name__)


def crawl_temp(url, total_xpath, title_xpath, time_xpath, url_xpath):
    """
    爬虫模板方案一
    :param url:             爬虫目标URL
    :param total_xpath:     总Xpath
    :param title_xpath:     标题Xpath
    :param time_xpath:      时间Xpath
    :param url_xpath:       资源Xpath
    :return:
    """
    # logger.info(u'begin crawl info......')
    #     # res = requests.get(url)
    #     # status_code = res.status_code       # 请求状态码
    #     # if status_code == 200:
    #     #     try:
    #     #         # 返回etree格式HTML
    #     #         response_html = etree.HTML(res.content)
    #     #         html_list = response_html.xpath(total_xpath)
    #     #         temp_list = []
    #     #         for temp in html_list:
    #     #             temp_dict = {}
    #     #             if time_xpath.strip():
    #     #                 time1 = temp.xpath(time_xpath)[0]
    #     #                 temp_dict['time'] = time1
    #     #             else:
    #     #                 temp_dict['time'] = 'Null'
    #     #             if title_xpath.strip():
    #     #                 title = temp.xpath(title_xpath)[0]
    #     #                 temp_dict['title'] = title
    #     #             else:
    #     #                 temp_dict['title'] = 'Null'
    #     #             if url_xpath.strip():
    #     #                 resource = temp.xpath(url_xpath)[0]
    #     #                 res = remove_dot(resource)
    #     #                 temp_dict['resource'] = res
    #     #             else:
    #     #                 temp_dict['resource'] = 'Null'
    #     #             temp_list.append(temp_dict)
    #     #         return success_result(temp_list)
    #     #     except Exception as e:
    #     #         return crawl_temp_second(url, total_xpath, title_xpath, time_xpath, url_xpath)
    #     # elif status_code == 403:
    #     #     return error_result("你没有权限,URL拒绝访问")
    #     # elif status_code == 404:
    #     #     return error_result("请检查你的URL,找不到URL")
    #     # elif status_code == 500:
    #     #     return error_result("URL系统错误")


def crawl_temp_second(url, total_xpath, title_xpath, time_xpath, url_xpath):
    """
    # 爬虫模板方案二
    # :param url:
    # :param total_xpath:
    # :param title_xpath:
    # :param time_xpath:
    # :param url_xpath:
    # :return:
    # """
    # logger.info(u'begin crawl info......')
    # # 指明phantomjs的执行路径
    # driver = webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    # driver.get(url)
    #
    # # 方法1：显式给3秒加载时间
    # # time.sleep(3)
    #
    # # 方法2：让 Selenium 不断地检查某个元素是否存在，以此确定页面是否已经完全加载(需要导入库)
    # try:
    #     element = driver.find_elements_by_xpath(total_xpath + change_string(time_xpath))
    #     element = driver.find_elements_by_xpath(total_xpath + change_string(title_xpath))
    #     element = driver.find_elements_by_xpath(total_xpath + change_string(url_xpath))
    #     res = requests.get(url)
    #     status_code = res.status_code  # 请求状态码
    #     if status_code == 200:
    #         try:
    #             # 返回etree格式HTML
    #             response_html = etree.HTML(driver.page_source)
    #             html_list = response_html.xpath(total_xpath)
    #             temp_list = []
    #             # print res.content
    #             for temp in html_list:
    #                 temp_dict = {}
    #                 if time_xpath.strip():
    #                     time1 = temp.xpath(time_xpath)[0]
    #                     temp_dict['time'] = time1
    #                 else:
    #                     temp_dict['time'] = 'Null'
    #                 if title_xpath.strip():
    #                     title = temp.xpath(title_xpath)[0]
    #                     temp_dict['title'] = title
    #                 else:
    #                     temp_dict['title'] = 'Null'
    #                 if url_xpath.strip():
    #                     resource = temp.xpath(url_xpath)[0]
    #                     res = remove_dot(resource)
    #                     temp_dict['resource'] = res
    #                 else:
    #                     temp_dict['resource'] = 'Null'
    #                 temp_list.append(temp_dict)
    #             return success_result(temp_list)
    #         except Exception as e:
    #             return error_result(str(e) + u'Xpath配置异常')
    #     elif status_code == 403:
    #         return error_result("你没有权限,URL拒绝访问")
    #     elif status_code == 404:
    #         return error_result("请检查你的URL,找不到URL")
    #     elif status_code == 500:
    #         return error_result("URL系统错误")
    # finally:
    #     # print(driver.page_source)
    #     # 关闭驱动
    #     logger.info(u'关闭驱动')
    #     driver.close()


def crawl_temp_test(url, total_xpath, title_xpath, time_xpath, url_xpath):
    ""
    # 爬虫模板测试用例
    # :param url:             爬虫目标URL
    # :param total_xpath:     总Xpath
    # :param title_xpath:     标题Xpath
    # :param time_xpath:      时间Xpath
    # :param url_xpath:       资源Xpath
    # :return:
    # """
    # logger.info(u'begin crawl info......')
    # # 指明phantomjs的执行路径
    # driver = webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    # driver.get(url)
    #
    # # 方法1：显式给3秒加载时间
    # # time.sleep(3)
    #
    # # 方法2：让 Selenium 不断地检查某个元素是否存在，以此确定页面是否已经完全加载(需要导入库)
    # try:
    #     # 判断页面是否完全加载，没加载则爬出异常，终止爬虫
    #     WebDriverWait(driver, 10).until(driver.find_elements_by_xpath(total_xpath + change_string(time_xpath)))
    #     WebDriverWait(driver, 10).until(driver.find_elements_by_xpath(total_xpath + change_string(title_xpath)))
    #     WebDriverWait(driver, 10).until(driver.find_elements_by_xpath(total_xpath + change_string(url_xpath)))
    #     res = requests.get(url)
    #     status_code = res.status_code  # 请求状态码
    #     if status_code == 200:
    #         try:
    #             # 返回etree格式HTML
    #             response_html = etree.HTML(driver.page_source)
    #             html_list = response_html.xpath(total_xpath)
    #             temp_list = []
    #             # print res.content
    #             for temp in html_list:
    #                 temp_dict = {}
    #                 if time_xpath.strip():
    #                     time1 = temp.xpath(time_xpath)[0]
    #                     temp_dict['time'] = time1
    #                 else:
    #                     temp_dict['time'] = 'Null'
    #                 if title_xpath.strip():
    #                     title = temp.xpath(title_xpath)[0]
    #                     temp_dict['title'] = title
    #                 else:
    #                     temp_dict['title'] = 'Null'
    #                 if url_xpath.strip():
    #                     resource = temp.xpath(url_xpath)[0]
    #                     res = remove_dot(resource)
    #                     temp_dict['resource'] = res
    #                 else:
    #                     temp_dict['resource'] = 'Null'
    #                 temp_list.append(temp_dict)
    #             return success_result(temp_list)
    #         except Exception as e:
    #             return error_result(str(e) + u'Xpath配置异常')
    #     elif status_code == 403:
    #         return error_result("你没有权限,URL拒绝访问")
    #     elif status_code == 404:
    #         return error_result("请检查你的URL,找不到URL")
    #     elif status_code == 500:
    #         return error_result("URL系统错误")
    # finally:
    #     # print(driver.page_source)
    #     # 关闭驱动
    #     logger.info(u'关闭驱动')
    #     driver.close()


def remove_dot(string):
    """
    去除URL的‘.’字符
    :param string:
    :return:
    """
    first = string[:1]
    second = string[:2]
    if first == '.':
        return remove_dot(string.lstrip('.'))
    if second == '/.':
        return remove_dot(string.lstrip('/'))
    if first == '/':
        return string
    if first == 'h':
        return string


def change_string(string):
    """
    去除xpath中的‘@’和它之后的字母，去除以()结尾的xpath
    :param string:
    :return:
    """
    if not string.strip():
        return string
    if '@' in string:
        result = "//"+str(string.split('@'))
        return result[0][:-1]
    if ')' in string:
        return "//"+str(string[:-7])





