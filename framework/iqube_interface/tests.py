# encoding:utf-8
from django.test import TestCase

# Create your tests here.

from conf.default import MEASURES_API_ADDRESS
from conf.default import LOG_API_ADDRESS
import requests
import json


def get_measures_type():
    """
    获取指标类型
    :return:
    """
    # 请求地址
    api_address = LOG_API_ADDRESS
    # 返回列表
    return_list = []
    # 请求结果
    try:
        api_result = json.loads(requests.get(api_address).content)
        if api_result['code'] == '000000':
            for i in api_result['data']:
                map = {}
                measures_list = api_result['data'][i].split('|')[1].split(',')
                map[i] = measures_list
                return_list.append(map)
            print return_list
        else:
            return []
    except Exception as e:
       pass





get_measures_type()