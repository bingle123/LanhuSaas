# encoding:utf-8
from conf.default import MEASURES_API_ADDRESS
from conf.default import LOG_API_ADDRESS
from shell_app.tools import success_result
from shell_app.tools import error_result
import requests
import json


class IqubeInterface():
    """
    一体化平台
    """
    def __init__(self):
        pass

    @classmethod
    def get_api_type(cls, api_address):
        """

        :return:
        """
        # 请求地址,测试数据
        # api_address = LOG_API_ADDRESS
        # 返回列表
        return_list = []
        # 请求结果
        try:
            api_result = json.loads(requests.get(api_address).content)
            if api_result['code'] == '000000':
                for i in api_result['data']:
                    map = {}
                    # 度量值列表
                    measures_list = api_result['data'][i].split('|')[1].split(',')
                    map[i] = measures_list
                    return_list.append(map)
                return success_result(return_list)
            else:
                return error_result([])
        except Exception as e:
            return error_result(str(e))



