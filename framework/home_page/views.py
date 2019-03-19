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
    res = function.scenes_alert(request)
    return render_json(res)

