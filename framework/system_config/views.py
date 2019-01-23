# encoding:utf-8
from common.mymako import render_mako_context


# Create your views here.
def crawl_config_html(request):
    """
    网页抓取配置页面
    :param request:
    :return:
    """
    return render_mako_context(request, './system_config/crawl_config.html')

