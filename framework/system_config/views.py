# encoding:utf-8
from common.mymako import render_mako_context
from common.mymako import render_json
import json
import crawl_template


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
    request_body = json.loads(request.body)
    print type(request_body)
    print request.body
    return render_json(None)


def delete_crawl(request):
    """
    根据ID删除爬虫配置信息
    :param request:
    :return:
    """
    request_body = json.loads(request.body)
    print request_body
    return render_json(None)


def get_crawls(request):
    """
    获取爬虫配置信息
    :param request:
    :return:
    """
    request_body = json.loads(request.body)
    print request_body
    return render_json(None)


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
