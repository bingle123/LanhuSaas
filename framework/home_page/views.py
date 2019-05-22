# -*- coding: utf-8 -*-


from common.mymako import render_json
import function


def get_time(request):
    """

    :param request:
    :return:
    """
    res = function.get_time(request)
    return render_json(res)


def scenes_alert(request):
    """

    :param request:
    :return:
    """
    #隐藏旧方法 彭英杰2019-5-11 start
    bing_res = function.scenes_alert(request)
    res={
        "alert_data":[], # 告警列表
        "sences_list":[],  # 当前用户所有场景信息
        "bing_res":[],
    }
    res["bing_res"] = bing_res;
    res["alert_data"] = function.query_alert_data(request);
    res["sences_list"] = function.query_curr_sences(request);
    #彭英杰 2019-5-11 end
    return render_json(res)
def select_all(request):
    """

    :param request:
    :return:
    """
    res = function.select_All(request)
    print type(res)
    return render_json(res)


def scenes_item_list(request):
    """
    场景类型查询监控项列表数据
    :param request:
    :return:
    """
    #scenes_id = request.POST.get("scenes_id")
    return render_json(function.scenes_item_list(request))