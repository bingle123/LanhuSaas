# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1543225174.296434
_enable_loop = True
_template_filename = '/Users/zhanglibing/vagrant/django18/LanhuSaas/framework/templates/home_application/helloworld.html'
_template_uri = '/home_application/helloworld.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'<!DOCTYPE <!DOCTYPE html>\n<html>\n<head>\n    <meta charset="utf-8" />\n    <meta http-equiv="X-UA-Compatible" content="IE=edge">\n    <title>Page Title</title>\n    <meta name="viewport" content="width=device-width, initial-scale=1">\n    <link rel="stylesheet" type="text/css" media="screen" href="main.css" />\n    <script src="main.js"></script>\n</head>\n<body>\n    Hello World!!!\n</body>\n</html>>\n\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"16": 0, "27": 21, "21": 1}, "uri": "/home_application/helloworld.html", "filename": "/Users/zhanglibing/vagrant/django18/LanhuSaas/framework/templates/home_application/helloworld.html"}
__M_END_METADATA
"""
