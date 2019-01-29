# encoding:utf-8
from shell_app.tools import success_result
from shell_app.tools import error_result
from models import CrawlerConfig
from django.db.models import Q
import json
import datetime


def crawl_manage(request):
    """
    爬虫信息新增与修改
    :param request:
    :return:
    """
    print request.body
    request_body = json.loads(request.body)
    crawl_id = request_body['id']
    crawl_name = request_body['crawl_name']
    crawl_url = request_body['crawl_url']
    period = request_body['period']
    crawl_keyword = request_body['crawl_keyword']
    crawl_no_keyword = request_body['crawl_keyword']
    total_xpath = request_body['total_xpath']
    title_xpath = request_body['title_xpath']
    time_xpath = request_body['time_xpath']
    url_xpath = request_body['url_xpath']
    create_user = 'zork'
    update_user = 'zork'
    receivers = 'zork'
    # 新增
    if crawl_id == '':
        try:
            res = CrawlerConfig.objects.create(crawl_name=crawl_name, crawl_url=crawl_url, period=period,
                                               crawl_keyword=crawl_keyword, crawl_no_keyword=crawl_no_keyword,
                                               total_xpath=total_xpath, title_xpath=title_xpath, time_xpath=time_xpath,
                                               url_xpath=url_xpath, create_user=create_user, update_user=update_user,
                                               receivers=receivers)
            return success_result('新增爬虫配置成功')
        except Exception as e:
            return error_result('新增爬虫配置信息失败' + e)
    # 修改
    else:
        try:
            print 2
            res = CrawlerConfig.objects.filter(id=crawl_id).update(crawl_name=crawl_name, crawl_url=crawl_url,
                                                                   period=period,
                                                                   crawl_keyword=crawl_keyword,
                                                                   crawl_no_keyword=crawl_no_keyword,
                                                                   total_xpath=total_xpath, title_xpath=title_xpath,
                                                                   time_xpath=time_xpath,
                                                                   url_xpath=url_xpath,
                                                                   update_user=update_user,
                                                                   receivers=receivers, update_time=datetime.datetime.now())
            return success_result('修改爬虫配置成功')
        except Exception as e:
            return error_result(e)


def get_crawls_config(request):
    """
    获取爬虫配置信息
    :param request:
    :return:
    """
    try:
        res = CrawlerConfig.objects.all().order_by('-update_time').values()
        result_list = []
        for i in res:
            i['create_time'] = i['create_time'].strftime("%Y-%m-%d %H:%M:%S")
            i['update_time'] = i['update_time'].strftime("%Y-%m-%d %H:%M:%S")
            result_list.append(i)
        return success_result(result_list)
    except Exception as e:
        return error_result('获取爬虫配置信息失败' + e)


def get_crawl_by_name(request):
    """
    根据crawl的名字查询信息
    :param request:
    :return:
    """
    if request.body is None or request.body == '':
        keyword = ''
    else:
        keyword = request.body
    try:
        res = CrawlerConfig.objects.filter(Q(crawl_name__contains=keyword)).order_by('-update_time').values()
        result_list = []
        for i in res:
            i['create_time'] = i['create_time'].strftime("%Y-%m-%d %H:%M:%S")
            i['update_time'] = i['update_time'].strftime("%Y-%m-%d %H:%M:%S")
            result_list.append(i)
        return success_result(result_list)
    except Exception as e:
        return error_result('获取爬虫配置信息失败' + e)


def delete_crawl_config_id(request):
    """
    通过crawl_id删除爬虫配置信息
    :param request:
    :return:
    """
    request_body = json.loads(request.body)
    crawl_id = request_body['id']
    try:
        res = CrawlerConfig.objects.filter(id=crawl_id).delete()
        return success_result('删除爬虫配置信息成功')
    except Exception as e:
        return error_result('删除爬虫配置信息失败' + e)
