import function
from common.mymako import render_json, render_mako_context


# Create your views here.

def index(request):
    """

    :param request:
    :return:
    """
    return render_mako_context(request, './position/position.html')


def show(request):
    """

    :param request:
    :return:
    """
    res = function.show(request)
    return render_json(res)


def select_pos(request):
    """

    :param request:
    :return:
    """
    res = function.select_pos(request)
    return render_json(res)


def delete_pos(request):
    """

    :param request:
    :return:
    """
    res = function.delete_pos(request)
    return render_json(res)


def add_pos(request):
    """

    :param request:
    :return:
    """
    r = function.add_pos(request)
    return render_json(r)


def add_person(request):
    """

    :param request:
    :return:
    """
    function.add_person(request)
    return render_json(0)


def edit_pos(request):
    """

    :param request:
    :return:
    """
    r = function.edit_pos(request)
    return render_json(r)


def filter_user(request):
    """

    :param request:
    :return:
    """
    r = function.filter_user(request)
    return render_json(r)


def get_tree(request):
    r = function.get_tree(request)
    return render_json(r)


def synchronize(request):
    r = function.synchronize(request)
    return render_json(r)

def get_active_user(req):
    bk_username = req.user.username
    return render_json(bk_username)