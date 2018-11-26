# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1543225165.987167
_enable_loop = True
_template_filename = '/Users/zhanglibing/vagrant/django18/LanhuSaas/framework/templates/home_application/contact.html'
_template_uri = '/home_application/contact.html'
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
        STATIC_URL = context.get('STATIC_URL', UNDEFINED)
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
        STATIC_URL = context.get('STATIC_URL', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n    <style type="text/css">\n        #footer{\n            position: relative;\n            bottom: -40px;\n        }\n    </style>\n    <div class="page-contactus">\n        <!-- \u5185\u5bb9 start-->\n        <!--comtactus-detail -->\n        <div class="container" >\n            <div class="tc" id="contactus">\n                <div class="weixin-img-arrow">\n                    <div>\n                        <img class="weixin-img " src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'img/weixin_icom.png">\n                    </div>\n                    <p>\u5173\u6ce8\u6211\u4eec</p>\n                </div>\n                <div class="comtactus-way-arrow tc mt50">\n                    <div class="dbi border-right tc" style="width: 280px; padding-left: 60px">\n                        <div class="img-arrow">\n                            <img  class="" src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'img/icom_01.png">\n                        </div>\n                        <p class="mt20">\u6df1\u5733\u5e02\u5357\u5c71\u533a\u79d1\u5174\u5b66\u56edC2</p>\n                    </div>\n                    <div class="dbi border-right tc" style="width: 180px">\n                        <div class="img-arrow">\n                            <img src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'img/icom_02.png">\n                        </div>\n                        <p class="mt20">\u4f01\u4e1aQQ\uff1a800802001</p>\n                    </div>\n                    <div class="dbi tc" style="width: 280px">\n                        <div class="img-arrow">\n                            <img src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'img/icom_03.png">\n                        </div>\n                        <p class="mt20">\u90ae\u7bb1\uff1acontactus_bk@tencent.com</p>\n                    </div>\n                </div>\n            </div>\n\n        </div>\n        <!-- \u5185\u5bb9 start-->\n    </div>\n')
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
{"source_encoding": "utf-8", "line_map": {"64": 24, "65": 30, "66": 30, "67": 36, "68": 36, "37": 1, "42": 46, "47": 49, "80": 47, "74": 47, "53": 3, "86": 80, "27": 0, "60": 3, "61": 17, "62": 17, "63": 24}, "uri": "/home_application/contact.html", "filename": "/Users/zhanglibing/vagrant/django18/LanhuSaas/framework/templates/home_application/contact.html"}
__M_END_METADATA
"""
