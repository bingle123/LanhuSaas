# -*- coding: utf-8 -*-
from blueking.component.shortcuts import get_client_by_request
import time
import pytz
import datetime
from settings import *
import requests
import json
from suds.client import Client
from suds.transport.https import HttpAuthenticated


def error_result(e):
    """
    失败统一JSON
    :param e:   异常
    :return:    json数据
    """
    result = {
        "result": False,
        "message": u"失败 %s" % e,
        "code": 1,
        "results": None
    }
    return result


def success_result(results):
    """
    成功统一JSON
    :param results:
    :return:
    """
    result = {
        "result": True,
        "message": u'成功',
        "code": 0,
        "results": results,
    }
    return result


def page_paging(request, limit):
    """
    分页方法
    :param request:
    :param limit:   页面容量
    :return:        页面起始页码
    """
    click_page_unicode = request.GET.get("clickPage")  # 获取页面页码数
    if click_page_unicode is None or click_page_unicode == "":  # 页码数是否为空，空时赋值为第一页
        click_page = 1
    else:
        click_page = int(click_page_unicode.encode("utf-8"))  # 对页码进行转码
    start_page = (click_page - 1) * limit  # 接口参数:数据起始页码
    return start_page


def interface_param(request):
    """
    返回client对象
    :param request:
    :return:
    """
    client = get_client_by_request(request)  # 获取code、secret参数
    client.set_bk_api_ver('v2')  # 以v2版本调用接口
    return client


# UTCS时间转换为时间戳 2016-07-31T16:00:00Z
def utc_to_local(utc_time_str, utc_format='%Y-%m-%dT%H:%M:%SZ'):
    utc_time_str = "2016-07-31T16:00:00Z"
    utc_time_str = "2019-01-02T06:54:09.000Z"
    local_tz = pytz.timezone('Asia/Shanghai')
    local_format = "%Y-%m-%d %H:%M"
    utc_dt = datetime.datetime.strptime(utc_time_str, utc_format)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    time_str = local_dt.strftime(local_format)
    print time.mktime(time.strptime(time_str, local_format))
    return int(time.mktime(time.strptime(time_str, local_format)))


def get_active_user(request):
    """
    通过蓝鲸获取当前用户
    :param request:
    :return:            dict
    """
    client = interface_param(request)
    res = client.bk_login.get_user({})
    return res


# 获取微信公众号token
def wechat_access_token():
    """
    获取微信全局接口的凭证(默认有效期俩个小时)
    如果不每天请求次数过多, 通过设置缓存即可
    """
    result = requests.get(
        url="https://api.weixin.qq.com/cgi-bin/token",
        params={
            "grant_type": "client_credential",
            "appid": WECHAT_APP_ID,
            "secret": WECHAT_SECRETE,
        }
    ).json()
    if result.get("access_token"):
        access_token = result.get('access_token')
    else:
        access_token = None
    return access_token


# 微信公众号发送内容到指定openid用户
def wechat_send_msg(access_token, openid, msg):
    print "OPEN_ID: %s" % openid
    body = {
        "touser": openid,
        "msgtype": "text",
        "text": {
            "content": msg
        }
    }
    unicode_str = json.dumps(body, ensure_ascii=False)
    utf8_str = unicode_str.encode('utf-8')
    # print 'UNICODE: %s'% unicode_str
    # print 'UTF8: %s' % utf8_str
    response = requests.post(
        url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
        params={
            'access_token': access_token
        },
        data=utf8_str
    )
    # 这里可根据回执code进行判定是否发送成功(也可以根据code根据错误信息)
    result = response.json()
    print result
    if 0 == int(result['errcode']):
        print "WeChat Message Send Success!"
        return None
    else:
        print "WeChat Message Send Error: %s" % result['errmsg']
        return result['errmsg']


# 微信公众号群发功能：只有服务号可用，订阅号不可用
def wechat_batch_send_msg(access_token, openids, msg):
    print "OPEN_IDS: %s" % openids
    body = {
        "touser": openids,
        "msgtype": "text",
        "text": {
            "content": msg
        }
    }
    unicode_str = json.dumps(body, ensure_ascii=False)
    utf8_str = unicode_str.encode('utf-8')
    # print 'UNICODE: %s'% unicode_str
    # print 'UTF8: %s' % utf8_str
    response = requests.post(
        url="https://api.weixin.qq.com/cgi-bin/message/mass/send",
        params={
            'access_token': access_token
        },
        data=utf8_str
    )
    # 这里可根据回执code进行判定是否发送成功(也可以根据code根据错误信息)
    result = response.json()
    if 0 == int(result['errcode']):
        print "WeChat Message Send Success!"
    else:
        print "WeChat Message Send Error: %s" % result['errmsg']



# 使用登飞平台发送邮件通知
# mail_receivers是一个list，包含多个dict，每个dict包含name和content，name是中文姓名，content是邮箱帐号
def mail_send_msg(mail_title, mail_content, mail_receivers):
    auth = HttpAuthenticated(username=DENGFEI_USERNAME, password=DENGFEI_PASSWORD)
    client = Client(url=DENGFEI_WS, transport=auth)

    params = dict()
    params['type'] = 'M'
    params['sysFlag'] = '测试系统标识'
    params['moduleFlag'] = '测试模块标识'
    params['formatType'] = 'T'
    params['title'] = mail_title
    params['content'] = mail_content
    params['roadFlag'] = '测试消息通道标识'
    params['sender'] = dict()
    params['sender']['name'] = '测试姓名'
    params['sender']['mailaddr'] = 'test@test.com'
    params['recivers'] = mail_receivers

    json_params = json.dumps(params, ensure_ascii=False)
    json_params = json_params.encode('utf8')

    response = client.service.receiveMsg(json_params)
    # 打印接口调用返回信息
    print response


# 使用登飞平台发送短信通知
# sms_receivers是一个list，包含多个dict，每个dict包含name和content，name是中文姓名，content是手机号码
def sms_send_msg(sms_content, sms_receivers):
    auth = HttpAuthenticated(username=DENGFEI_USERNAME, password=DENGFEI_PASSWORD)
    client = Client(url=DENGFEI_WS, transport=auth)

    params = dict()
    params['type'] = 'S'
    params['sysFlag'] = '测试系统标识'
    params['moduleFlag'] = '测试模块标识'
    params['sType'] = 'S'
    params['content'] = sms_content
    params['roadFlag'] = '测试消息通道标识'
    params['recivers'] = sms_receivers

    json_params = json.dumps(params, ensure_ascii=False)
    json_params = json_params.encode('utf8')

    response = client.service.receiveMsg(json_params)
    # 打印接口调用返回信息
    print response
