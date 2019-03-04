#!usr/bin/ebv python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from celery import task
from system_config.crawl_template import crawl_temp
from system_config.function import *
from celery.task import periodic_task
from system_config.models import SendMailLog as sml
from djcelery import models as celery_models
import logging
import time
from gatherData import function
from monitor_item.models import Monitor
from django.db.models import Q
from django.forms import model_to_dict
from monitor_item import tools
from celery.schedules import crontab
import market_day.celery_opt as co
from account.models import BkUser
from blueking.component.shortcuts import get_client_by_user
from datetime import datetime
from customProcess.function import clear_execute_status
import function

@task
def crawl_task(**i):
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
    # 开始爬虫
    crawl_result = crawl_temp(crawl_url, total_xpath, title_xpath, time_xpath, url_xpath)
    # 爬虫成功，且有数据
    print crawl_result
    if crawl_result['code'] == 0 and crawl_result['results'].__len__() != 0:
        send_result = []
        for j in range(crawl_result['results'].__len__()):
            # 增加爬虫配置ID
            crawl_result['results'][j].update(crawl_id=id)
            # 增加爬虫推送人---用户名需要转换成邮箱地址
            crawl_result['results'][j].update(receivers=receivers)
            # 拼接URL
            if crawl_result['results'][j]['resource'][0:4] == 'http':
                # 若resource自带http则不操作
                pass
            else:
                # 若resource不自带http则增加前缀
                crawl_result['results'][j]['resource'] = url_pre + crawl_result['results'][j]['resource']
            # 爬取内容包含关键字并且不包含非关键字的数据，并加入到结果集
            if crawl_keyword in crawl_result['results'][j]['title'] and crawl_no_keyword not in \
                    crawl_result['results'][j]['title']:
                res = CrawlContent.objects.filter(title_content=crawl_result['results'][j]['title'])
                # 爬取内容筛选数据库中不存在的内容增加到result_all
                if len(res) == 0:
                    # 增加到结果集
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
            receivers_mail = ['761494073@qq.com', 'liaomingtao@zork.com.cn']
            theme = crawl_name + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + u'的爬虫信息'
            send_content = change_to_html(send_result)
            mail_send(theme, send_content, receivers_mail)
            sml.objects.create(link_id=id, message_title=theme, message_content=send_content)
            logging.error(u'消息日志保存成功')
    return 'success'

#基本监控项和图标监控项的采集task
@task
def gather_data_task_one(**i):
    # 调用基本监控项和图标监控项数据采集的方法
    area_id=i['area_id']
    if function.check_jobday(area_id):
        function.gather_data(**i)
    else:
        pass

#作业监控项的采集task
@task
def gather_data_task_two(**i):
    print '采集开始'
    # 调用作业监控项数据采集的方法
    if function.check_jobday(area_id):
        tools.job_interface(res=i)
    else:
        pass

#流程监控项的采集task
@task
def gather_data_task_thrid(**i):
    print '采集开始'
    # 调用流程监控项数据采集的方法
    if check_jobday(area_id):
        tools.flow_gather_task(**i)
    else:
        pass
@task
def start_flow_task(**info):
    #得到client对象，方便调用接口
    if function.check_jobday(area_id):
        user_account = BkUser.objects.filter(id=1).get()
        client = get_client_by_user(user_account)
        client.set_bk_api_ver('v2')
        template_id=info['template_list']['id']
        constants_temp = info['constants']
        constants = {}
        for temp in constants_temp:
            constants[temp['key']] = temp['value']
        strnow = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        name=info['template_list']['name']+strnow
        param = {
            "bk_biz_id": "2",
            "template_id": template_id,
            'name': name,
            'constants':constants
        }
        res=client.sops.create_task(param)
        #调用接口创建任务并得到任务的id
        task_id=res['data']['task_id']
        #调用接口启动任务，开始执行任务
        param = {
            "bk_biz_id": "2",
            'task_id':task_id
        }
        res=client.sops.start_task(param)
        flag=res['result']
        status=0
        #如果启动任务成功创建一个定时查看节点状态的任务
        if flag:
            node_times = info['node_times']
            starthour = str(node_times[-1]['starttime']).split(':')[0]
            endhour = str(node_times[0]['endtime'])[:2].split(':')[0]
            period=info['period']
            args = {
                'item_id': info['id'],
                'task_id': task_id,  # 启动流程的任务id
                'node_times': node_times,
                'period': period,
                'task_name':info['template_list']['name'] + '_check_status_test'
            }
            ctime = {
                'hour': starthour + '-' + endhour,
                'minute': '*/1',
            }
            co.create_task_crontab(name=info['template_list']['name']+'_check_status', task='market_day.tasks.gather_data_task_thrid', crontab_time=ctime,
                                   task_args=args, desc=name)
            status=1
            for time in node_times:
                Flow_Node(flow_id=item_id, node_name=time['node_name'], start_time=time['starttime'],
                          end_time=time['endtime']).save()
        Flow(instance_id=task_id, status=flag, test_flag=0, flow_id=item_id).save()
    else:
        pass
# 定时任务测试
@task
def count_time(**i):
    return i['x'] * i['y']

@periodic_task(run_every=crontab(hour=0,minute=0))
def clear_status_task():
    print '开始清理状态'
    if function.check_jobday(area_id):
        clear_execute_status()
    else:
        pass




