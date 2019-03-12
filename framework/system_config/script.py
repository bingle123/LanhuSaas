# encoding:utf-8
import os
import json
import socket
import re
import datetime
import glob


def find_new_file(folder_directory):
    """
    当前目录最新log文件
    :param folder_directory:        文件目录
    :return:                        最新文件名称
    """
    file_name = max(glob.iglob(folder_directory+'/*.log'), key=os.path.getmtime)
    return folder_directory + '/' + file_name.split('\\')[1]


def read_log(address, keyword):
    """
    读取日志文件的最后一条记录信息
    :param address:                 文件地址
    :return:                        日志一行包含 :[ 的最后一条记录数据
    """
    with open(address, 'r') as file_to_read:
        result = ''
        while True:
            lines = file_to_read.readline().decode("gb2312")
            if ':[' in lines and '][' in lines and keyword in lines:
                result = lines
            if not lines:
                break
    return result


def log_return_measures(log_string, log_string_tow):
    """

    :param log_string:
    :param log_string_tow:
    :return:
    """
    measures = {}
    status = re.search('\:\[.*\]\[', log_string, flags=0).group()[2:-2]
    system_id = re.search('\]\[.*\]', log_string, flags=0).group()[2:-1]
    if status == 'error':
        measures[system_id] = 1
    else:
        measures[system_id] = 0
    status = re.search('\:\[.*\]\[', log_string_tow, flags=0).group()[2:-2]
    system_id = re.search('\]\[.*\]', log_string_tow, flags=0).group()[2:-1]
    if status == 'error':
        measures[system_id] = 1
    else:
        measures[system_id] = 0
    return measures


def json_log(measures, metricsetname, appsystem):
    """
    日志转json
    :param measures:            度量值字典
    :param metricsetname:       指标名称
    :param appsystem:           系统名称
    :return:
    """
    # 主机名
    my_hostname = socket.getfqdn(socket.gethostname())
    # 主机IP
    my_ip = socket.gethostbyname(my_hostname)
    # 返回结果集
    map = {}
    # 描述信息
    dimensions = {}
    # 指标值
    dimensions["ip"] = my_ip
    dimensions["appsystem"] = appsystem
    dimensions["hostname"] = my_hostname
    map["dimensions"] = dimensions
    map["metricsetname"] = metricsetname
    map["measures"] = measures
    map["timestamp"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    return json.dumps(map)


# def log_return_json(log_string, metricsetname, measures_name, appsystem):
#     """
#     日志文件转json
#     :param log_string:  log字符串
#     :param metricsetname: 指标名称
#     :param measures_name: 指标集
#     :param appsystem:  系统名称
#     :return:
#     """
#     # 主机名
#     my_hostname = socket.getfqdn(socket.gethostname())
#     # 主机IP
#     my_ip = socket.gethostbyname(my_hostname)
#     # 返回结果集
#     map = {}
#     # 描述信息
#     dimensions = {}
#     # 指标值
#     measures = {}
#     dimensions["ip"] = my_ip
#     dimensions["appsystem"] = appsystem
#     dimensions["hostname"] = my_hostname
#     map["dimensions"] = dimensions
#     map["metricsetname"] = metricsetname
#     # 存在记录数
#     if log_string is not '':
#         # 处理字符串
#         arr = log_string.split(' ')
#         result_arr = []
#         for s in arr:
#             if s == '':
#                 continue
#             else:
#                 result_arr.append(s)
#         # 时间戳
#         timestamp = result_arr[0] + ' ' + result_arr[1][:12]
#         # 状态码
#         status = re.search('\:\[.*\]\[', log_string, flags=0).group()[2:-2]
#         system_id = re.search('\]\[.*\]', log_string, flags=0).group()[2:-1]
#         if status == 'error':
#             measures[system_id] = 1
#         else:
#             measures[system_id] = 0
#         map["measures"] = measures
#         map["timestamp"] = timestamp.encode('ascii')
#         return json.dumps(map)
#     else:
#         timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         measures[measures_name] = 0
#         map["measures"] = measures
#         map["timestamp"] = timestamp.encode('ascii')
#         return json.dumps(map)


if __name__ == "__main__":
    # 此处要配置路径
    folder_dir = 'd:/log'
    file_dir = find_new_file(folder_dir)
    log_string_result = read_log(file_dir, 'zy-shangpin-startBPJ')
    log_string_result2 = read_log(file_dir, 'zy-shangpin-initial')
    measures = log_return_measures(log_string_result, log_string_result2)
    print json_log(measures, 'O32_system_open', 'O32System')
