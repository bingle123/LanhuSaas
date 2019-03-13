# -*- coding: utf-8 -*-

from models import *
from position.models import *
from django.forms.models import model_to_dict
from shell_app.tools import *
from django.core.paginator import *


# 获取所有定制过程节点
def select_all_nodes():
    node_info = TbCustProcess.objects.order_by('seq').all()
    node_list = []
    for node in node_info:
        dic1 = model_to_dict(node)
        # 获取该节点对应的节点状态
        temp = TdCustProcessLog.objects.filter(node_id=node.id).get()
        # 临时保存节点的执行时间
        do_time_ori = temp.do_time
        # 节点执行时间置空，防止datetime类型在model_to_dict时转换报错
        temp.do_time = None
        dic2 = model_to_dict(temp)
        # 由于model_to_dict方法不支持datetime类型的数据直接转换字典，手动转换
        if do_time_ori is None:
            dic2['do_time'] = ''
        else:
            dic2['do_time'] = do_time_ori.strftime('%Y-%m-%d %H:%M:%S')
        # 将节点状态放置到节点的status字段中
        dic1['status'] = dic2
        # 将当前遍历的节点添加到列表中
        node_list.append(dic1)
    return node_list


# 分页获取定制过程节点
def select_nodes_pagination(node_info):
    result_dict = dict()
    list_set = list()
    # 获取前台传递的参数：需要第几页的数据
    page = node_info['page']
    # 获取前台传递的参数：每页有多少条数据
    limit = node_info['limit']
    # 获取当前所有节点
    nodes_list = TbCustProcess.objects.all()
    # 对所有节点进行分页处理
    paginator = Paginator(nodes_list, limit)
    # 获取指定页的数据
    try:
        selected_set = paginator.page(page)
    except PageNotAnInteger:
        selected_set = paginator.page(1)
    except EmptyPage:
        selected_set = paginator.page(paginator.num_pages)
    # 将当前页所有数据转换为字典对象，并添加到list中，统一传递到前端
    for selected_data in selected_set:
        temp = model_to_dict(selected_data)
        list_set.append(temp)
    # 当前页的所有数据
    result_dict['items'] = list_set
    # 当前的总页数
    result_dict['pages'] = paginator.num_pages
    return result_dict


# 添加或修改一个定制过程节点
def add_node(node):
    status_dic = dict()
    # 添加/删除节点
    TbCustProcess(**node).save()
    # 获取当前操作的节点
    last_node = TbCustProcess.objects.last()
    # 判断该节点是否存在节点状态信息
    has_record = TdCustProcessLog.objects.filter(node_id=last_node.id).count()
    # 如果该节点还没有状态信息则为添加的情况，新增一个状态信息，默认为未开始执行
    if 0 == has_record:
        TdCustProcessLog(node_id=last_node.id).save()
    # 获取当前所有节点的数量
    items_count = TbCustProcess.objects.count()
    # 默认每页5条记录，获取总页数
    pages = items_count // 5
    if 0 != items_count % 5:
        pages = pages + 1
    status_dic['message'] = 'ok'
    status_dic['total_pages'] = pages
    return status_dic


# 获取所有已设置通知方式的蓝鲸用户信息
def select_all_bkusers():
    users_list = list()
    bk_users = user_info.objects.all().filter(notice_style__isnull=False)
    for bk_user in bk_users:
        if bk_user.notice_style not in ('wechat','sms','email'):
            continue
        user_dict = model_to_dict(bk_user)
        users_list.append(user_dict)
    return users_list


# 修改指定节点id的节点信息
def update_node_status(node):
    selected_status = TdCustProcessLog.objects.get(node_id=node['node_id'])
    selected_status.is_done = node['is_done']
    selected_status.do_time = node['do_time']
    selected_status.do_person = node['do_person']
    selected_status.save()
    return "ok"


# 修改指定节点id的节点状态
def change_status_flag(node):
    selected_status = TdCustProcessLog.objects.get(node_id=node['node_id'])
    selected_status.is_done = node['is_done']
    selected_status.save()
    return "ok"


# 删除指定节点id的节点
def del_node(node_id):
    TbCustProcess.objects.filter(id=node_id['id']).delete()
    return "ok"


# 获取指定节点id的节点
def select_node(node_id):
    node = TbCustProcess.objects.filter(id=node_id['id']).get()
    node_list = []
    dic = model_to_dict(node)
    node_list.append(dic)
    return node_list


# 删除所有已存在的过程通知节点
def truncate_node():
    TbCustProcess.objects.all().delete()
    return "ok"


# 清除所有过程通知节点的执行状态信息
def clear_execute_status():
    nodes_status = TdCustProcessLog.objects.all()
    for status in nodes_status:
        status.is_done = 'n'
        status.do_time = None
        status.do_person = None
        status.save()
    return "ok"


def send_notification(notification):

    # 是否存在发送错误的标志位
    send_flag = True
    # 保存发送完成的信息，以及发送是否存在错误，返回前端
    status = dict()
    # 获取接收者账号名称信息，以list保存
    if -1 != notification['receivers'].find(','):
        receivers = notification['receivers'].split(',')
    else:
        receivers = list()
        receivers.append(notification['receivers'])
    # 保存发送完成的信息
    infos = list()
    # 获取的微信token
    access_token = None
    # 短信发送列表
    sms_send_list = None
    # 邮件发送列表
    mail_send_list = None
    # 遍历前端传递的接收者列表
    for receiver in receivers:
        # 获取当前账户名称的用户信息
        rec_info = user_info.objects.filter(user_name=receiver).get()
        # 当用户的通知方式为微信通知方式的情况下--由于微信端限制，非服务号无法使用群发，因此只能在遍历用户时发送，不能统一发送
        if 'wechat' == rec_info.notice_style:
            # 如果当前为第一次获取token信息
            if None is access_token:
                access_token = wechat_access_token()
                # token获取异常，检查APPID和secret是否正确
            if None is access_token:
                print 'Wechat access token get fail'
                send_flag = False
                infos.append(u'微信发送失败!Token获取异常!')
                break
            # 根据获取的当前用户的openid和获取的token发送指定内容的推送消息给用户
            if None is rec_info.open_id or '' == rec_info.open_id.strip():
                infos.append(u'%s：微信发送失败!用户openid未设置' % receiver)
                send_flag = False
                continue
            res = wechat_send_msg(access_token, rec_info.open_id, notification['content'])
            # 函数返回为None说明发送正常，否则将返回错误信息
            if None is not res:
                infos.append(u'%s: 微信通知发送失败! %s' % (receiver, res))
                # send_flag标志位置False告诉前端有发送失败的任务，前端将会以error框展示
                send_flag = False
        # 当用户的通知方式为短信通知方式的情况下
        elif 'sms' == rec_info.notice_style:
            # 如果当前是第一次添加短信接收者信息，新建一个list用于保存
            if None is sms_send_list:
                sms_send_list = list()
            sms_send_list.append(receiver)
        # 当用户的通知方式为邮件通知方式的情况下
        elif 'email' == rec_info.notice_style:
            # 如果当前是第一次添加邮箱接收者信息，新建一个list用于保存
            if None is mail_send_list:
                mail_send_list = list()
            mail_send_list.append(receiver)
    # 短信发送列表如果不为空，则发送短信给列表中的接收者
    if None is not sms_send_list:
        sms_send_msg(notification['content'], sms_send_list)
    # 邮件发送列表如果不为空，则发送邮件给列表中的接收者
    if None is not mail_send_list:
        mail_send_msg(u'过程通知信息', notification['content'], mail_send_list)
    # 根据当前发送状态标志位，返回前端一个相应的发送状态，用于前端判断发送是否存在问题
    if send_flag:
        status['message'] = 'ok'
        status['info'] = u'通知发送成功!'
    else:
        status['message'] = 'error'
        status['info'] = infos
    # 返回发送的状态信息给前端
    return status
