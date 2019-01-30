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
    开始爬虫,并筛选数据(关键字和非关键字,数据库比对)
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
            send_result = []
            for j in range(crawl_result['results'].__len__()):
                # 增加爬虫配置ID
                crawl_result['results'][j].update(crawl_id=id)
                # 增加爬虫推送人---用户名需要转换成邮箱地址
                crawl_result['results'][j].update(receivers=receivers)
                # 拼接URL
                crawl_result['results'][j]['resource'] = url_pre + crawl_result['results'][j]['resource']
                # 爬取内容包含关键字并且不包含非关键字的数据，并加入到结果集
                if crawl_keyword in crawl_result['results'][j]['title'] and crawl_no_keyword not in \
                        crawl_result['results'][j]['title']:
                    res = CrawlContent.objects.filter(title_content=crawl_result['results'][j]['title'])
                    # 爬取内容筛选数据库中不存在的内容增加到result_all
                    if len(res) == 0:
                        # 增加到结果集
                        result_all.append(crawl_result['results'][j])
                        crawl_id = crawl_result['results'][j]['crawl_id']
                        title = crawl_result['results'][j]['title']
                        resource = crawl_result['results'][j]['resource']
                        time = crawl_result['results'][j]['time']
                        # 保存爬虫内容
                        CrawlContent.objects.create(crawl_id=crawl_id, title_content=title, url_content=resource,
                                                    time_content=time)
                        # 此处为接收人的邮箱日后需要从清算园里查询出来,这里为测试数据
                        receivers_mail = ['761494073@qq.com', 'liaomingtao@zork.com.cn']
                        send_result.append(crawl_result['results'][j])
                        # send_content = change_to_html(crawl_result['results'][j])
                        # theme = crawl_name + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + u'的爬虫信息'
                        # mail_send(theme, send_content, receivers_mail)
            if len(send_result) == 0:
                # 内容为空，不需要发送
                pass
            else:
                # print send_result
                send_content = change_to_html(send_result)
                receivers_mail = ['761494073@qq.com', 'liaomingtao@zork.com.cn']
                theme = crawl_name + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + u'的爬虫信息'
                mail_send(theme, send_content, receivers_mail)
        # 爬虫成功，没有数据
        elif crawl_result['results'].__len__() == 0:
            # 此处应该写入错误我日志
            message = crawl_name + u'没有获取到数据，请检查配置是否正确!'
            result_error.append(message)
        # 爬虫失败,返回错误信息
        elif crawl_result['code'] != 0:
            message = crawl_name + u'获取数据失败' + crawl_result['results']
            result_error.append(message)
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
            result += '<a href="'+resource+'" target="_blank">'+title+'</a>'+'<span>'+time+'<span>'+'</br>'
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
            except Exception as e:
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
