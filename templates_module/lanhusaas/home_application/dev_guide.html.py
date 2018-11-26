# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1543225157.804642
_enable_loop = True
_template_filename = '/Users/zhanglibing/vagrant/django18/LanhuSaas/framework/templates/home_application/dev_guide.html'
_template_uri = '/home_application/dev_guide.html'
_source_encoding = 'utf-8'
_exports = [u'content', u'footerline']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base.html', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        def content():
            return render_content(context._locals(__M_locals))
        def footerline():
            return render_footerline(context._locals(__M_locals))
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'content'):
            context['self'].content(**pageargs)
        

        __M_writer(u'\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'footerline'):
            context['self'].footerline(**pageargs)
        

        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_content(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def content():
            return render_content(context)
        __M_writer = context.writer()
        __M_writer(u'\n<div class="page_index">\n\t<!-- banner start -->\n\t<div class="getheadimg-box">\n\t\t<p class="guide-banner-title">\u5f00\u53d1\u6307\u5f15</p>\n\t\t<p class="guide-banner-word">\u4e86\u89e3\u84dd\u9cb8\u5f00\u53d1\u6846\u67b6\uff0c\u4ece\u8fd9\u91cc\u5f00\u59cb</p>\n\n\t</div>\n\t<!-- banner end -->\n\t<div class="container">\n\t<ul class="king-step3 king-step-primary">\n\t    <li class="process-doing mt50 clearfix">\n\t    \t<span class="outer-circle"></span>\n\t        <div class="step-num step-num-top-line">1</div>\n\t        <div class="step-text step-text-top">\n\t            <h4>\u672c\u5730\u5f00\u53d1\u73af\u5883\u5b89\u88c5</h4>\n\t\t        <div class="mt10 mb20 wm lh2">\n\t\t\t\t\t1.\u672c\u5730\u73af\u5883\u642d\u5efa\u955c\u50cf\n\t\t\t\t\t<a href="http://bkopen-10032816.file.myqcloud.com/paas/bk-django1.8-u2.box" target="_blank">\u70b9\u51fb\u4e0b\u8f7d</a>\n\t\t\t\t\t<br>\n\t\t\t\t\t2.\u4f7f\u7528\u6587\u6863\n\t\t\t\t\t<a href="http://bkopen-10032816.file.myqcloud.com/paas/\u84dd\u9cb8\u667a\u4e91\u7edf\u4e00\u5f00\u53d1\u73af\u5883\u642d\u5efa\u6307\u5357.docx" target="_blank">\u70b9\u51fb\u4e0b\u8f7d</a>\n\t\t\t\t\t<br>\n\t\t\t\t\t<p class="text-notice">\u6ce8\u610f\uff1a\u5e94\u7528\u6d4b\u8bd5\u3001\u6b63\u5f0f\u90e8\u7f72\u65f6\u4f1a\u81ea\u52a8\u5b89\u88c5\u8fd0\u884c\u73af\u5883\uff0c\u5e76\u90e8\u7f72\u5e94\u7528\n\t\t\t\t\t</p>\n\t\t\t\t</div>\n\t        </div>\n\t    </li>\n\t    <li class="process-doing clearfix">\n\t    \t<span class="outer-circle"></span>\n\t        <div class="step-num">2</div>\n\t        <div class="step-text">\n\t            <h4>\u5f00\u53d1\u9879\u76ee</h4>\n\t            <div class="mt10 mb20 wm lh2">\n\t\t\t\t\t<strong>1.\u914d\u7f6e\u4fee\u6539</strong><br>\n\t\t\t\t\t\uff081\uff09conf/default.py \u6587\u4ef6\uff1aAPP_ID \\ APP_TOKEN \uff08\u84dd\u9cb8\u667a\u4e91\u5f00\u53d1\u8005\u4e2d\u5fc3 -&gt; \u70b9\u51fb\u5e94\u7528ID -&gt; \u57fa\u672c\u4fe1\u606f \u4e2d\u53ef\u4ee5\u67e5\u770b\u5230\u8fd9\u4e24\u4e2a\u503c\u7684\u4fe1\u606f\uff09<br>\n\t\t\t\t\t\uff082\uff09conf/default.py \u6587\u4ef6\uff1aBK_PAAS_HOST\uff08\u84dd\u9cb8\u667a\u4e91\u5f00\u53d1\u8005\u4e2d\u5fc3\u7684\u57df\u540d\uff0c\u5f62\u5982\uff1ahttp://paas.bking.com\uff09<br>\n\t\t\t\t\t\uff083\uff09conf/settings_development.py \u6587\u4ef6\uff1aDATABASES\uff08\u8bf7\u521b\u5efa\u672c\u5730\u5f00\u53d1\u6570\u636e\u5e93\uff0c\u5e76\u4fee\u6539\u914d\u7f6e\u4fe1\u606f\uff09<br>\n\t\t\t\t\t\uff084\uff09conf/settings_testing.py \u6587\u4ef6\uff1aDATABASES\uff08\u8bf7\u521b\u5efa\u6d4b\u8bd5\u6570\u636e\u5e93\uff0c\u5e76\u4fee\u6539\u914d\u7f6e\u4fe1\u606f\uff09<br>\n\t\t\t\t\t\uff085\uff09conf/settings_production.py \u6587\u4ef6\uff1aDATABASES\uff08\u8bf7\u521b\u5efa\u6b63\u5f0f\u6570\u636e\u5e93\uff0c\u5e76\u4fee\u6539\u914d\u7f6e\u4fe1\u606f\uff09<br>\n\t\t\t\t\t<p class="text-notice">\u6ce8\u610f\uff1a\u6d4b\u8bd5\u73af\u5883 \u548c \u6b63\u5f0f\u73af\u5883 \u7684\u6570\u636e\u5e93\u9700\u8981\u5bf9 AppServer \u6388\u6743</p>\n\t\t\t\t\t<br>\n\t\t\t\t\t<strong>2.celery \u914d\u7f6e</strong><br>\n\t\t\t\t\t\u82e5\u9700\u8981\u4f7f\u7528 celery\uff0c\u8bf7\u4fee\u6539\u4ee5\u4e0b\u914d\u7f6e\uff1a\uff08<a href="http://bkopen-10032816.file.myqcloud.com/paas/celery_packages.zip">\u70b9\u51fb\u4e0b\u8f7d celery \u5f00\u53d1\u6307\u5f15</a>\uff09<br>\n\t\t\t\t\t\uff081\uff09conf/default.py \u6587\u4ef6\uff1aIS_USE_CELERY \u7684\u503c\u8bbe\u7f6e\u4e3a: <span class="text-notice">True</span><br>\n\t\t\t\t\t\uff082\uff09conf/default.py \u6587\u4ef6\uff1aBROKER_URL_DEV\uff08\u8bf7\u521b\u5efa\u672c\u5730\u5f00\u53d1\u7684 celery\u6d88\u606f\u961f\u5217\uff0c\u5e76\u4fee\u6539\u914d\u7f6e\u4fe1\u606f\uff0c\u63a8\u8350\u4f7f\u7528 RabbitMQ\uff09<br>\n\t\t\t\t\t\uff083\uff09conf/default.py \u6587\u4ef6\uff1aCELERY_IMPORTS\uff08\u6dfb\u52a0celery\u4efb\u52a1\u6a21\u5757\uff09<br>\n\t\t\t\t\t<strong>3.\u6570\u636e\u5e93\u64cd\u4f5c</strong><br>\n\t\t\t\t\tDjango1.8 Migration\u7684\u4f7f\u7528\u65b9\u6cd5\u5982\u4e0b:<br>\n\t\t\t\t\t\uff081\uff09\u6267\u884c manage.py migrate\uff08Django\u9ed8\u8ba4\u8868\u521b\u5efa\uff09\u3002<br>\n\t\t\t\t\t\uff082\uff09\u6267\u884c manage.py startapp yourappname\u3001\u6dfb\u52a0yourappname\u5230conf/default.py\u6587\u4ef6\u7684"INSTALLED_APPS_CUSTOM"\u53d8\u91cf\u4e2d\u3002<br>\n\t\t\t\t\t\uff083\uff09\u5728Application\u7684models.py\u4e2d\u5efa\u7acb\u6570\u636e\u5e93\u6a21\u578b\uff0c\u6267\u884cmanage.py makemigrations yourappname\u3002<br>\n\t\t\t\t\t\uff084\uff09\u6267\u884cmanage.py migrate yourappname\u3002<br>\n\t\t\t\t</div>\n\t        </div>\n\t    </li>\n\t    <li class="process-doing clearfix">\n\t    <span class="outer-circle"></span>\n\t        <div class="step-num">3</div>\n\t        <div class="step-text-button-line">\n\t            <h4>\u90e8\u7f72\u9879\u76ee</h4>\n\t            <div class="mt10 mb20 wm lh2">\n\t\t\t\t\t<strong>\u901a\u8fc7\u84dd\u9cb8\u667a\u4e91\u5f00\u53d1\u8005\u4e2d\u5fc3\u63d0\u4f9b\u7684\u201c\u6d4b\u8bd5\u90e8\u7f72\u201d\u3001\u201c\u6b63\u5f0f\u90e8\u7f72\u201d\u670d\u52a1\u5c06\u5e94\u7528\u90e8\u7f72\u5230\u6d4b\u8bd5\\\u6b63\u5f0f\u73af\u5883\u4e2d\u3002</strong><br>\n\t\t\t\t\t\u64cd\u4f5c\u5165\u53e3\uff1a\u84dd\u9cb8\u667a\u4e91\u5f00\u53d1\u8005\u4e2d\u5fc3 -&gt; \u70b9\u51fb\u5e94\u7528\u540d\u79f0 -&gt; \u5e94\u7528\u90e8\u7f72\u3002 <br>\n\t\t\t\t\t\uff081\uff09\u6d4b\u8bd5\u90e8\u7f72\uff1a\u5c06\u5e94\u7528\u4ee3\u7801\u5728\u6d4b\u8bd5\u73af\u5883\u4e0a\u8fdb\u884c\u90e8\u7f72\uff0c\u90e8\u7f72\u6210\u529f\u540e\u5c31\u53ef\u4ee5\u5728\u6d4b\u8bd5\u73af\u5883\u4e2d\u4f7f\u7528\u60a8\u7684\u5e94\u7528\u3002<br>\n\t\t\t\t\t\uff082\uff09\u6b63\u5f0f\u90e8\u7f72\uff1a\u5c06\u5e94\u7528\u4ee3\u7801\u5728\u6b63\u5f0f\u73af\u5883\u4e0a\u8fdb\u884c\u90e8\u7f72\uff0c\u90e8\u7f72\u6210\u529f\u540e\u5c31\u53ef\u4ee5\u5728\u6b63\u5f0f\u73af\u5883\u4e2d\u4f7f\u7528\u60a8\u7684\u5e94\u7528\u3002<br>\n\t\t\t\t\t\uff083\uff09\u4e0b\u67b6\u64cd\u4f5c\uff1a\u7cfb\u7edf\u5c06\u5e94\u7528\u4ee3\u7801\u4ece\u60a8\u9009\u62e9\u7684\u73af\u5883\u4e0a\u64a4\u9500\u90e8\u7f72\uff0c\u5c4a\u65f6\u7528\u6237\u5c06\u65e0\u6cd5\u8bbf\u95ee\u8be5\u5e94\u7528\uff0c\u4f46\u662f\u8be5\u5e94\u7528\u7684\u6570\u636e\u5e93\u4f9d\u7136\u4fdd\u7559\u3002<br>\n\t\t\t\t</div>\n\t        </div>\n\t    </li>\n\t</ul>\n\t</div>\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_footerline(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def footerline():
            return render_footerline(context)
        __M_writer = context.writer()
        __M_writer(u'\n    <hr class="guide-cutting-line">\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"64": 77, "36": 1, "70": 77, "41": 76, "76": 70, "46": 79, "52": 3, "58": 3, "27": 0}, "uri": "/home_application/dev_guide.html", "filename": "/Users/zhanglibing/vagrant/django18/LanhuSaas/framework/templates/home_application/dev_guide.html"}
__M_END_METADATA
"""
