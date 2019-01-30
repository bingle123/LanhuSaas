# encoding:utf-8
from shell_app.tools import success_result
from shell_app.tools import error_result
from models import CrawlerConfig
from models import CrawlContent
from django.db.models import Q
import json
import datetime
from crawl_template import crawl_temp
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings


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
                                                                   receivers=receivers,
                                                                   update_time=datetime.datetime.now())
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


def start_crawl(request):
    """
    开始爬虫,并筛选数据(关键字和非关键字)
    :param request:
    :return:
    """
    res = get_crawls_config(request)['results']
    result_all = []
    result_error = []
    for i in res:
        id = i['id']
        crawl_url = i['crawl_url']
        crawl_name = i['crawl_name']
        total_xpath = i['total_xpath']
        title_xpath = i['title_xpath']
        url_xpath = i['url_xpath']
        time_xpath = i['time_xpath']
        crawl_keyword = i['crawl_keyword']
        crawl_no_keyword = i['crawl_no_keyword']
        url_pre = i['url_pre']
        # 接收人--列表
        receivers = i['receivers'].split('@')
        crawl_result = crawl_temp(crawl_url, total_xpath, title_xpath, time_xpath, url_xpath)
        # 爬虫成功，且有数据
        if crawl_result['code'] == 0 and crawl_result['results'].__len__() != 0:
            for j in range(crawl_result['results'].__len__()):
                # 增加爬虫配置ID
                crawl_result['results'][j].update(crawl_id=id)
                # 增加爬虫推送人
                crawl_result['results'][j].update(receivers=receivers)
                # 拼接URL
                crawl_result['results'][j]['resource'] = url_pre + crawl_result['results'][j]['resource']
                # 爬取内容包含关键字并且不包含非关键字的数据，并加入到结果集
                if crawl_keyword in crawl_result['results'][j]['title'] and crawl_no_keyword not in \
                        crawl_result['results'][j]['title']:
                    # 增加到结果集
                    result_all.append(crawl_result['results'][j])
        # 爬虫成功，没有数据
        elif crawl_result['results'].__len__() == 0:
            message = crawl_name + u'没有获取到数据，请检查配置是否正确!'
            result_error.append(message)
        # 爬虫失败,返回错误信息
        elif crawl_result['code'] != 0:
            message = crawl_name + u'获取数据失败' + crawl_result['results']
            result_error.append(message)
    return {
        "result": True,
        "message": u'成功',
        "code": 0,
        "results": result_all,
        "error_result": result_error,
    }


def add_crawl_message(request):
    """
    增加爬虫信息
    :param request:
    :return:
    """
    # 测试数据
    temp = start_crawl(request)
    result_all = []
    for i in range(temp['results'].__len__()):
        title_content = temp['results'][i]['title']
        receivers = temp['results'][i]['receivers']
        res = CrawlContent.objects.filter(title_content=title_content)
        if len(res) == 0:
            try:
                # 事物回滚
                with transaction.atomic():
                    crawl_id = temp['results'][i]['crawl_id']
                    time_content = temp['results'][i]['time']
                    resource = temp['results'][i]['resource']
                    CrawlContent.objects.create(crawl_id=crawl_id, time_content=time_content,
                                                title_content=title_content, url_content=resource)
                    result_all.append(
                        {'time_content': time_content, 'resource': resource, 'title_content': title_content,
                         'receivers': receivers})
            except Exception as e:
                return error_result(e)
    if len(result_all) == 0:
        result_all = u'没要需要保存的信息'
        return error_result(result_all)
    return success_result(result_all)


# 发送邮件
def send(request):
    """
    发送邮件测试
    :param request:
    :return:
    """
    msg = '<a href="http://www.baidu.com" target="_blank">点击激活</a>'
    send_mail(u'测试邮件', '', settings.DEFAULT_FROM_EMAIL, [u'收件箱'], html_message = msg)
    return success_result(u'成功')
