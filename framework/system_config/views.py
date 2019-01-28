# encoding:utf-8
from common.mymako import render_mako_context
from common.mymako import render_json
import json
import crawl_template
import function


# Create your views here.
def crawl_config_html(request):
    """
    网页抓取配置页面
    :param request:
    :return:
    """
    return render_mako_context(request, './system_config/crawl_config.html')


def manage_crawl(request):
    """
    爬虫信息新增和修改
    :param request:
    :return:
    """
    res = function.crawl_manage(request)
    return render_json(res)


def delete_crawl(request):
    """
    根据ID删除爬虫配置信息
    :param request:
    :return:
    """
    res = function.delete_crawl_config_id(request)
    return render_json(res)


def get_crawls(request):
    """
    获取爬虫配置信息
    :param request:
    :return:
    """
    res = function.get_crawls_config(request)
    return render_json(res)


def get_crawl_by_name(request):
    """
    条件查询
    :param request:
    :return:
    """
    res = function.get_crawl_by_name(request)
    return render_json(res)


def crawl(request):
    """
    爬虫测试
    :param request:
    :return:
    """
    url = 'http://www.sse.com.cn/services/tradingservice/tradingtech/newnotice/'
    total_xpath = '//div[@class="sse_list_1 js_listPage"]//dl//dd'
    title_xpath = 'a/text()'
    time_xpath = 'span/text()'
    url_xpath = 'a/@href'
    res = crawl_template.crawl_temp(url, total_xpath, time_xpath, title_xpath, url_xpath)
    return render_json(res)
