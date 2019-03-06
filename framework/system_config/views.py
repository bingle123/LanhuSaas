# encoding:utf-8
from common.mymako import render_mako_context
from common.mymako import render_json
from shell_app import tools
import json
import crawl_template
import function
import sys
from logmanagement.function import add_log,make_log_info,get_active_user


# Create your views here.
def crawl_config_html(request):
    """
    网页抓取配置页面
    :param request:
    :return:
    """
    return render_mako_context(request, './system_config/crawl_config.html')


def scene_type_html(request):
    """
    场景分组配置
    :param request:
    :return:
    """
    return render_mako_context(request, './system_config/scene_type.html')


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
    # 上交所
    # url = 'http://www.sse.com.cn/services/tradingservice/tradingtech/newnotice/'
    # total_xpath = '//div[@class="sse_list_1 js_listPage"]//dl//dd'
    # title_xpath = 'a/text()'
    # time_xpath = 'span/text()'
    # url_xpath = 'a/@href'

    # 深交所
    url = 'http://www.szse.cn/aboutus/trends/news/index.html'
    total_xpath = '//div[@class="article-list"]//div[@class="g-content-list"]//ul//li//div[@class="title"]'
    title_xpath = 'a/@title'
    time_xpath = 'span/text()'  # yes
    url_xpath = 'a/@href'

    # china clear
    # url = 'http://www.chinaclear.cn/zdjs/gszb/center_clist.shtml'
    # total_xpath = '//div[@class="pageTabContent"]//ul//li'
    # title_xpath = 'a/@title'
    # # time_xpath = ''  # yes
    # time_xpath = 'span/text()'  # yes
    # # url_xpath = 'a/@href'
    # url_xpath = ''
    res = crawl_template.crawl_temp(url, total_xpath, title_xpath, time_xpath, url_xpath)
    return render_json(res)


def start_crawl(request):
    """
    开始爬虫
    :param request:
    :return:
    """
    res = function.start_crawl(request)
    return render_json(res)


def crawl_test(request):
    """
    用户爬虫测试
    :param request:
    :return:
    """
    res = function.crawl_test(request)
    return render_json(res)


def json_test(request):
    """
    josn测试
    :param request:
    :return:
    """
    res = function.add_crawl_message(request)
    return render_json(res)


def mail_send(request):
    """
    邮件发送
    :param request:
    :return:
    """
    res = function.send(request)
    return render_json(res)


def get_scene_type(request):
    """
    获取场景信息
    :param request:
    :return:
    """
    request_body = json.loads(request.body)
    page = request_body['page']
    limit = request_body['limit']
    if request_body['query_name'] is None or request_body['query_name'] == '':
        res = function.get_scene_type('', page, limit)
        return render_json(res)
    else:
        query_name = json.loads(request.body)['query_name']
        print query_name
        res = function.get_scene_type(query_name, page, limit)
        return render_json(res)


def add_scene_type(request):
    """
    新增场景类型
    :param request:
    :return:
    """
    try:
        request_body = json.loads(request.body)
        scene_type_name = request_body['name']
        client = tools.interface_param(request)
        user = client.bk_login.get_user({})
        res = function.add_scene_type(user['data']['bk_username'], scene_type_name)
        info = make_log_info(u'增加场景类型', u'业务日志', u'SceneType', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '成功', '无')
    except Exception as e:
        info = make_log_info(u'增加场景类型', u'业务日志', u'SceneType', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '失败', repr(e))
    add_log(info)
    return render_json(res)


def edit_scene_type_by_uuid(request):
    """
    修改场景分组
    :param request:
    :return:
    """
    try:
        request_body = json.loads(request.body)
        scene_type_name = request_body['name']
        uuid = request_body['uuid']
        client = tools.interface_param(request)
        user = client.bk_login.get_user({})
        res = function.edit_scene_type_by_uuid(uuid, user['data']['bk_username'], scene_type_name)
        info = make_log_info(u'编辑场景类型', u'业务日志', u'SceneType', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '成功', '无')
    except Exception as e:
        info = make_log_info(u'编辑场景类型', u'业务日志', u'SceneType', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '失败', repr(e))
    add_log(info)
    return render_json(res)


def delete_scene_by_uuid(request):
    """
    删除场景分组
    :param request:
    :return:
    """
    try:
        print request.body
        print request
        request_body = json.loads(request.body)
        uuid = request_body['uuid']
        res = function.delete_scene_by_uuid(uuid)
        info = make_log_info(u'删除场景分组', u'业务日志', u'SceneType', sys._getframe().f_code.co_name,
                         get_active_user(request)['data']['bk_username'], '成功', '无')
    except Exception as e:
        info = make_log_info(u'删除场景分组', u'业务日志', u'SceneType', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], '失败', repr(e))
    add_log(info)
    return render_json(res)
