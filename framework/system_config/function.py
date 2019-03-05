# encoding:utf-8
from shell_app.tools import success_result
from shell_app.tools import error_result
from shell_app.tools import get_active_user
from models import CrawlerConfig
from models import CrawlContent
from models import SceneType
from django.db.models import Q
import json
import datetime
from crawl_template import crawl_temp
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from market_day import celery_opt as co
from django.forms.models import model_to_dict
import uuid
import sys
import math
from logmanagement.function import add_log, make_log_info, get_active_user


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
    url_pre = request_body['url_pre']
    active_user_dict = get_active_user(request)
    # 接收人为字符串，以@隔开
    receivers = 'zork'
    # 新增
    if crawl_id == '':
        create_user = active_user_dict['data']['bk_username']
        try:
            res = CrawlerConfig.objects.create(crawl_name=crawl_name, crawl_url=crawl_url, period=period,
                                               crawl_keyword=crawl_keyword, crawl_no_keyword=crawl_no_keyword,
                                               total_xpath=total_xpath, title_xpath=title_xpath, time_xpath=time_xpath,
                                               url_xpath=url_xpath, create_user=create_user, update_user=create_user,
                                               receivers=receivers, url_pre=url_pre)
            info = make_log_info(u'增加爬虫配置', u'业务日志', u'CrawlerConfig', sys._getframe().f_code.co_name,
                                 get_active_user(request)['data']['bk_username'], '成功', '无')
            add_log(info)
            return success_result('新增爬虫配置成功')
        except Exception as e:
            info = make_log_info(u'增加爬虫配置', u'业务日志', u'CrawlerConfig', sys._getframe().f_code.co_name,
                                 get_active_user(request)['data']['bk_username'], '失败', repr(e))
            add_log(info)
            return error_result('新增爬虫配置信息失败' + e)
    # 修改
    else:
        update_user = active_user_dict['data']['bk_username']
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
                                                                   receivers=receivers, url_pre=url_pre,
                                                                   update_time=datetime.datetime.now())
            info = make_log_info(u'编辑爬虫配置', u'业务日志', u'CrawlerConfig', sys._getframe().f_code.co_name,
                                 get_active_user(request)['data']['bk_username'], '成功', '无')
            add_log(info)
            return success_result(u'修改爬虫配置成功')
        except Exception as e:
            info = make_log_info(u'编辑爬虫配置', u'业务日志', u'CrawlerConfig', sys._getframe().f_code.co_name,
                                 get_active_user(request)['data']['bk_username'], '失败', repr(e))
            add_log(info)
            return error_result(e)


def get_crawls_config(request):
    """
    获取爬虫配置信息
    :param request:
    :return:
    """
    request_body = json.loads(request.body)
    page = request_body['page']
    limit = request_body['limit']
    count = CrawlerConfig.objects.all()
    page_count = int(math.ceil(len(count) / limit))
    start_page = (page - 1) * limit
    try:
        res = CrawlerConfig.objects.all().order_by('-update_time').values()[start_page:start_page + limit]
        result_list = []
        for i in res:
            i['create_time'] = i['create_time'].strftime("%Y-%m-%d %H:%M:%S")
            i['update_time'] = i['update_time'].strftime("%Y-%m-%d %H:%M:%S")
            i['page'] = page
            i['page_count'] = page_count
            result_list.append(i)
        print result_list.__len__()
        return success_result(result_list)
    except Exception as e:
        return error_result('获取爬虫配置信息失败' + e)


def get_crawl_by_name(request):
    """
    根据crawl的名字查询信息
    :param request:
    :return:
    """
    request_body = json.loads(request.body)
    page = request_body['page']
    limit = request_body['limit']
    keyword = request_body['keyword']
    count = CrawlerConfig.objects.filter(Q(crawl_name__contains=keyword))
    page_count = int(math.ceil(len(count) / limit))
    start_page = (page - 1) * limit
    try:

        res = CrawlerConfig.objects.filter(Q(crawl_name__contains=keyword)).order_by('-update_time').values()[
              start_page:start_page + limit]
        result_list = []
        for i in res:
            i['create_time'] = i['create_time'].strftime("%Y-%m-%d %H:%M:%S")
            i['update_time'] = i['update_time'].strftime("%Y-%m-%d %H:%M:%S")
            i['page'] = page
            i['page_count'] = page_count
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
        info = make_log_info(u'删除爬虫配置', u'业务日志', u'CrawlerConfig', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], u'成功', u'无')
        add_log(info)
        return success_result(u'删除爬虫配置信息成功')
    except Exception as e:
        info = make_log_info(u'删除爬虫配置', u'业务日志', u'CrawlerConfig', sys._getframe().f_code.co_name,
                             get_active_user(request)['data']['bk_username'], u'失败', repr(e))
        add_log(info)
        return error_result(u'删除爬虫配置信息失败' + e)


def start_crawl(request):
    """
    开始爬虫,并筛选数据(关键字和非关键字,数据库比对)
    :param request:
    :return:
    """
    res = get_crawls_config(request)['results']
    result_all = []
    result_error = []
    for i in res:
        period = i['period']
        interval = {'every': period, 'period': 'seconds'}
        schename = i['crawl_name']
        co.create_task_interval(name=schename, task='market_day.tasks.crawl_task', interval_time=interval, task_args=i,
                                desc=schename)
        # id = i['id']
        # crawl_url = i['crawl_url']
        # crawl_name = i['crawl_name']
        # total_xpath = i['total_xpath']
        # title_xpath = i['title_xpath']
        # url_xpath = i['url_xpath']
        # time_xpath = i['time_xpath']
        # crawl_keyword = i['crawl_keyword']
        # crawl_no_keyword = i['crawl_no_keyword']
        # url_pre = i['url_pre']
        # # 接收人--列表
        # receivers = i['receivers'].split('@')
        # # 开始爬虫
        # crawl_result = crawl_temp(crawl_url, total_xpath, title_xpath, time_xpath, url_xpath)
        # # 爬虫成功，且有数据
        # print crawl_result
        # if crawl_result['code'] == 0 and crawl_result['results'].__len__() != 0:
        #     send_result = []
        #     for j in range(crawl_result['results'].__len__()):
        #         # 增加爬虫配置ID
        #         crawl_result['results'][j].update(crawl_id=id)
        #         # 增加爬虫推送人---用户名需要转换成邮箱地址
        #         crawl_result['results'][j].update(receivers=receivers)
        #         # 拼接URL
        #         crawl_result['results'][j]['resource'] = url_pre + crawl_result['results'][j]['resource']
        #         # 爬取内容包含关键字并且不包含非关键字的数据，并加入到结果集
        #         if crawl_keyword in crawl_result['results'][j]['title'] and crawl_no_keyword not in \
        #                 crawl_result['results'][j]['title']:
        #             res = CrawlContent.objects.filter(title_content=crawl_result['results'][j]['title'])
        #             # 爬取内容筛选数据库中不存在的内容增加到result_all
        #             if len(res) == 0:
        #                 # 增加到结果集
        #                 result_all.append(crawl_result['results'][j])
        #                 crawl_id = crawl_result['results'][j]['crawl_id']
        #                 title = crawl_result['results'][j]['title']
        #                 resource = crawl_result['results'][j]['resource']
        #                 time = crawl_result['results'][j]['time']
        #                 # 保存爬虫内容
        #                 CrawlContent.objects.create(crawl_id=crawl_id, title_content=title, url_content=resource,
        #                                             time_content=time)
        #                 # 此处为接收人的邮箱日后需要从清算园里查询出来,这里为测试数据
        #                 receivers_mail = ['761494073@qq.com', 'liaomingtao@zork.com.cn']
        #                 send_result.append(crawl_result['results'][j])
        #                 # send_content = change_to_html(crawl_result['results'][j])
        #                 # theme = crawl_name + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + u'的爬虫信息'
        #                 # mail_send(theme, send_content, receivers_mail)
        #     if len(send_result) == 0:
        #         # 内容为空，不需要发送
        #         pass
        #     else:
        #         # print send_result
        #         send_content = change_to_html(send_result)
        #         receivers_mail = ['761494073@qq.com', 'liaomingtao@zork.com.cn']
        #         theme = crawl_name + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + u'的爬虫信息'
        #         mail_send(theme, send_content, receivers_mail)
        # 爬虫成功，没有数据
        # elif crawl_result['results'].__len__() == 0:
        #         #     # 此处应该写入错误我日志
        #         #     message = crawl_name + u'没有获取到数据，请检查配置是否正确!'
        #         #     result_error.append(message)
        # 爬虫失败,返回错误信息
        # elif crawl_result['code'] != 0:
        #     message = crawl_name + u'获取数据失败' + crawl_result['results']
        #     result_error.append(message)
        # print result_all
        # if result_all
        # change_to_html(content_list=result_all)
    return {
        "result": True,
        "message": u'成功',
        "code": 0,
        "results": result_all,
        "error_result": result_error,
    }


def change_to_html(content_html):
    """
    将List对象转换成HTML
    :param content_html:    发送的结果集
    :return:                HTML字符串
    """
    result = ''
    # 类似Java中的重载,Python中只支持参数列表不同的重载
    if type(content_html) is list:
        for i in content_html:
            title = i['title']
            resource = i['resource']
            time = i['time']
            result += '<a href="' + resource + '" target="_blank">' + title + '</a>' + '<span>' + time + '<span>' + '</br>'
    elif type(content_html) is dict:
        title = content_html['title']
        resource = content_html['resource']
        time = content_html['time']
        result = '<a href="' + resource + '" target="_blank">' + title + '</a>' + '<span>' + time + '<span>'
    return result


def add_crawl_message(request):
    """
    增加爬虫信息
    :param request:
    :return:
    """
    # 测试数据
    temp = start_crawl(request)
    print temp
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
                info = make_log_info(u'增加爬虫信息', u'业务日志', u'CrawlContent', sys._getframe().f_code.co_name,
                                     get_active_user(request)['data']['bk_username'], '成功', '无')
                add_log(info)
            except Exception as e:
                info = make_log_info(u'增加爬虫信息', u'业务日志', u'CrawlerConfig', sys._getframe().f_code.co_name,
                                     get_active_user(request)['data']['bk_username'], '失败', repr(e))
                add_log(info)
                return error_result(e)
    if len(result_all) == 0:
        result_all = u'没要需要保存的信息'
        return error_result(result_all)
    return success_result(result_all)


# 发送邮件
def mail_send(theme, content, mail_list):
    """
    发送邮件功能
    :param content:                     发送内容--Str
    :param mail_list:                   收件人地址--List
    :return:
    """
    print u'开始发送'
    msg = '<a href="http://www.baidu.com" target="_blank">点击激活</a>'
    send_mail(theme, '', settings.DEFAULT_FROM_EMAIL, mail_list,
              fail_silently=False, html_message=content)
    # try:
    #     send_mail(theme, '', settings.DEFAULT_FROM_EMAIL, mail_list,
    #               fail_silently=False, html_message=content)
    #     print u'结束发送'
    # except Exception as e:
    #     # 发送邮件异常
    #     print u'发送邮件异常'
    #     pass
    return success_result(u'成功')


def crawl_test(request):
    """
    爬虫成功测试
    :param request:
    :return:
    """
    print request.body
    request_body = json.loads(request.body)
    crawl_url = request_body['crawl_url']
    total_xpath = request_body['total_xpath']
    title_xpath = request_body['title_xpath']
    time_xpath = request_body['time_xpath']
    url_xpath = request_body['url_xpath']
    result = crawl_temp(url=crawl_url, total_xpath=total_xpath, time_xpath=time_xpath, url_xpath=url_xpath,
                        title_xpath=title_xpath)
    print result
    return success_result(result['results'])


def get_scene_type(type_name, page, limit):
    """
    获取场景分组类别
    :param type_name:       场景类型名称
    :param page:
    :param limit:
    :return:
    """
    count = SceneType.objects.all().values()
    if limit == 0:
        limit = len(count)
        page_count = 1
    else:
        page_count = int(math.ceil(len(count) / limit) + 1)
    start_page = int(page - 1) * int(limit)
    if type_name != '':
        count = SceneType.objects.filter(Q(scene_type_name__icontains=type_name))
        page_count = int(math.ceil(len(count) / limit) + 1)
    scene_type_list = SceneType.objects.filter(Q(scene_type_name__icontains=type_name)).order_by(
        '-update_time').values()[start_page:start_page + limit]
    result_list = []
    for i in scene_type_list:
        i['create_time'] = i['create_time'].strftime("%Y-%m-%d %H:%M:%S")
        i['update_time'] = i['update_time'].strftime("%Y-%m-%d %H:%M:%S")
        i['page_count'] = page_count
        i['page'] = page
        result_list.append(i)
    return success_result(result_list)


def delete_scene_by_uuid(scene_type_id):
    """
    删除场景
    :param scene_type_id:    场景类型UUID
    :return:
    """
    try:
        with transaction.atomic():
            SceneType.objects.filter(scene_type_id=scene_type_id).delete()
            return success_result('删除成功')
    except Exception as e:
        return error_result(e)


def edit_scene_type_by_uuid(scene_type_id, edit_user, scene_type_name):
    """
    根据UUID修改场景类型
    :param scene_type_id:   场景类型UUID
    :param edit_user:       编辑者
    :param scene_type_name: 场景类型名称
    :return:
    """
    scene_type = SceneType.objects.filter(scene_type_name=scene_type_name)
    if scene_type.__len__() == 0:
        try:
            with transaction.atomic():
                SceneType.objects.filter(scene_type_id=scene_type_id).update(update_user=edit_user,
                                                                             scene_type_name=scene_type_name,
                                                                             update_time=datetime.datetime.now())
                return success_result({})
        except Exception as e:
            return error_result(e)
    else:
        return error_result(u'场景类型已经存在')


def add_scene_type(create_user, scene_type_name):
    """
    新增场景类型
    :param create_user:         创建者
    :param scene_type_name:     场景类型名称
    :return:
    """
    # 生成UUID
    scene_type_id = uuid.uuid1()
    scene_type = SceneType.objects.filter(scene_type_name=scene_type_name)
    print scene_type
    print type(scene_type)
    print (scene_type is None)
    if scene_type.__len__() == 0:
        try:
            with transaction.atomic():
                SceneType.objects.create(scene_type_id=scene_type_id, create_user=create_user,
                                         scene_type_name=scene_type_name, update_user=create_user)
                return success_result(u'新增场景类型成功')
        except Exception as e:
            return error_result(e)
    else:
        return error_result(u'场景类型已经存在')
