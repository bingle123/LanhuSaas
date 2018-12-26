# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1545818817.029
_enable_loop = True
_template_filename = 'F:/Users/DeleMing/Desktop/Lanhu/framework/templates/db_connection_manage/index.html'
_template_uri = '/db_connection_manage/index.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        STATIC_URL = context.get('STATIC_URL', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'<!DOCTYPE html>\r\n<html>\r\n<head>\r\n<meta charset="UTF-8" />\r\n<title>Hello React!</title>\r\n<script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/react/react.production.min.js"></script>\r\n<script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/react/react-dom.production.min.js"></script>\r\n<script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/react/babel.min.js"></script>\r\n<script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/antd/antd.min.js"></script>\r\n<link src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/antd/antd.min.css">\r\n</head>\r\n<body>\r\n\r\n<div id="example"></div>\r\n<script type="text/babel">\r\nReactDOM.render(\r\n    <h1>Hello, world!</h1>,\r\n    document.getElementById(\'example\')\r\n);\r\n</script>\r\n\r\n</body>\r\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"32": 10, "38": 32, "16": 0, "22": 1, "23": 6, "24": 6, "25": 7, "26": 7, "27": 8, "28": 8, "29": 9, "30": 9, "31": 10}, "uri": "/db_connection_manage/index.html", "filename": "F:/Users/DeleMing/Desktop/Lanhu/framework/templates/db_connection_manage/index.html"}
__M_END_METADATA
"""
