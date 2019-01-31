# encoding:utf-8
import re
import logging
import requests
from lxml import etree
from shell_app.tools import error_result
from shell_app.tools import success_result

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



