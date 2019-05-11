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
   # res = function.scenes_alert(request)
    res={
        "alert_data":[], # 告警列表
    }
    res["alert_data"] = function.query_alert_data();
    return render_json(res)

