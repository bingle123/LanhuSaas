# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1546416161.411515
_enable_loop = True
_template_filename = u'/Users/zhanglibing/vagrant/django18/LanhuSaas/framework/templates/base.html'
_template_uri = u'/base.html'
_source_encoding = 'utf-8'
_exports = [u'content', u'footerline', u'head']


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        APP_PATH = context.get('APP_PATH', UNDEFINED)
        def head():
            return render_head(context._locals(__M_locals))
        BK_PLAT_HOST = context.get('BK_PLAT_HOST', UNDEFINED)
        STATIC_VERSION = context.get('STATIC_VERSION', UNDEFINED)
        self = context.get('self', UNDEFINED)
        request = context.get('request', UNDEFINED)
        APP_ID = context.get('APP_ID', UNDEFINED)
        STATIC_URL = context.get('STATIC_URL', UNDEFINED)
        SITE_URL = context.get('SITE_URL', UNDEFINED)
        def content():
            return render_content(context._locals(__M_locals))
        LOGOUT_URL = context.get('LOGOUT_URL', UNDEFINED)
        def footerline():
            return render_footerline(context._locals(__M_locals))
        NOW = context.get('NOW', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'<!DOCTYPE html>\n<html>\n  <head>\n    ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'head'):
            context['self'].head(**pageargs)
        

        __M_writer(u'\n  </head>\n\n  <body>\n    <!--\u9876\u90e8\u5bfc\u822a Start-->\n    <nav class="navbar navbar-default king-horizontal-nav2 navbar-mt0" role="navigation">\n        <div class="container" style="width: 100%;">\n            <div class="navbar-header col-md-4 col-sm-4 col-xs-4 logo">\n                <a class="navbar-brand" href="')
        __M_writer(unicode(SITE_URL))
        __M_writer(u'">\n                    \u84dd\u9cb8\u667a\u4e91\u5f00\u53d1\u6846\u67b6\n                </a>\n            </div>\n            <div class="collapse navbar-collapse navbar-responsive-collapse">\n                <ul class="nav navbar-nav">\n                  ')

        home = dev_guide = contactus = ''
        relative_path = APP_PATH
        if relative_path == SITE_URL or relative_path.startswith(SITE_URL + "?"):
          home = 'king-navbar-active'
        elif relative_path.startswith(SITE_URL + "dev-guide/"):
          dev_guide = 'king-navbar-active'
        elif relative_path.startswith(SITE_URL + "contactus/"):
          contactus = 'king-navbar-active'
                          
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['home','relative_path','contactus','dev_guide'] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'\n                  <li class="')
        __M_writer(unicode(home))
        __M_writer(u'"><a href="')
        __M_writer(unicode(SITE_URL))
        __M_writer(u'"><span>\u9996\u9875</span></a></li>\n                  <li class="')
        __M_writer(unicode(dev_guide))
        __M_writer(u'"><a href="')
        __M_writer(unicode(SITE_URL))
        __M_writer(u'dev-guide/"><span>\u5f00\u53d1\u6307\u5f15</span></a></li>\n                  <li class="')
        __M_writer(unicode(contactus))
        __M_writer(u'"><a href="')
        __M_writer(unicode(SITE_URL))
        __M_writer(u'contactus/"><span>\u8054\u7cfb\u6211\u4eec</span></a></li>\n                  <li class="')
        __M_writer(unicode(contactus))
        __M_writer(u'"><a href="')
        __M_writer(unicode(SITE_URL))
        __M_writer(u'guotai/"><span>\u56fd\u6cf0\u541b\u5b89\u81ea\u52a8\u5316\u8fd0\u7ef4\u9879\u76ee</span></a></li>\n                  <li class="')
        __M_writer(unicode(contactus))
        __M_writer(u'"><a href="')
        __M_writer(unicode(SITE_URL))
        __M_writer(u'guotai/test"><span>\u6d4b\u8bd5</span></a></li>\n                </ul>\n                <ul class="nav navbar-nav navbar-right">\n                  <a href="###" class="avatar">\n                    <img src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'img/getheadimg.jpg" width="40" alt="Avatar" class="avatar-img">\n')
        if request.user.is_superuser:
            __M_writer(u'                        <i class="crown"></i>\n')
        __M_writer(u'                    <span>')
        __M_writer(unicode(request.user.username))
        __M_writer(u'</span>\n                  </a>\n                  <!--\u9000\u51fa\u767b\u5f55-->\n                  <a id="logout" href="')
        __M_writer(unicode(LOGOUT_URL))
        __M_writer(u'">\u6ce8\u9500</a>\n                </ul>\n            </div>\n        </div>\n    </nav>\n    <!--\u9876\u90e8\u5bfc\u822a End-->\n    <!-- \u56fa\u5b9a\u5bbd\u5ea6\u5c45\u4e2d start -->\n    ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'content'):
            context['self'].content(**pageargs)
        

        __M_writer(u'\n    <!-- \u56fa\u5b9a\u5bbd\u5ea6\u8868\u5355\u5c45\u4e2d end -->\n    <!-- \u5c3e\u90e8\u58f0\u660e start -->\n    <div class="foot" id="footer">\n        ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'footerline'):
            context['self'].footerline(**pageargs)
        

        __M_writer(u'\n        <ul class="links ft">\n            <li>\n                <a id="contact_us" class="link">QQ\u54a8\u8be2(800802001)</a>\n                | <a href="http://bbs.bk.tencent.com/forum.php" target="_blank" hotrep="hp.footer.feedback" class="link">\u84dd\u9cb8\u8bba\u575b</a>\n                | <a href="http://bk.tencent.com/" target="_blank" hotrep="hp.footer.feedback" class="link">\u84dd\u9cb8\u5b98\u7f51</a>\n                | <a href="')
        __M_writer(unicode(BK_PLAT_HOST))
        __M_writer(u'" target="_blank" hotrep="hp.footer.feedback" class="link">\u84dd\u9cb8\u667a\u4e91\u5de5\u4f5c\u53f0</a>\n            </li>\n            <li><p class="copyright">Copyright \xa9 2012-')
        __M_writer(unicode(NOW.year))
        __M_writer(u' Tencent BlueKing. All Rights Reserved.</p> </li>\n          <li><p class="copyright">\u84dd\u9cb8\u667a\u4e91 \u7248\u6743\u6240\u6709</p> </li>\n        </ul>\n      </div>\n      <!-- \u5c3e\u90e8\u58f0\u660e start -->\n    <!-- jquery js  -->\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'js/jquery-1.10.2.min.js" type="text/javascript"></script>\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'js/jquery.json-2.3.min.js" type="text/javascript"></script>\n    <!-- bootstrap js  -->\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/bootstrap-3.3.4/js/bootstrap.min.js" type="text/javascript"></script>\n    <!--\u914d\u7f6ejs  \u52ff\u5220-->\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'js/settings.js?v=')
        __M_writer(unicode(STATIC_VERSION))
        __M_writer(u'" type="text/javascript"></script>\n    ')
        __M_writer(unicode(self.body()))
        __M_writer(u'\n    <!-- \u517c\u5bb9\u6027\u8bbe\u7f6e -->\n    <!--[if lt IE 6]>\\xe8\\x93\\x9d\\xe9\\xb2\\xb8\\xe6\\x99\\xba\\xe8\\x90\\xa5\\x20\\xe7\\x89\\x88\\xe6\\x9d\\x83\\xe6\\x89\\x80\\xe6\\x9c\\x89<![endif]-->\n  </body>\n</html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_content(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def content():
            return render_content(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_footerline(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def footerline():
            return render_footerline(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_head(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        STATIC_VERSION = context.get('STATIC_VERSION', UNDEFINED)
        def head():
            return render_head(context)
        APP_ID = context.get('APP_ID', UNDEFINED)
        STATIC_URL = context.get('STATIC_URL', UNDEFINED)
        SITE_URL = context.get('SITE_URL', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n        <title>\u5f00\u53d1\u6846\u67b6|\u84dd\u9cb8\u667a\u4e91\u793e\u533a\u7248</title>\n        <meta name="description" content=""/>\n        <meta name="author" content=""/>\n        <link rel="shortcut icon" href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'favicon.ico" type="image/x-icon">\n        <!-- bootstrap css -->\n\t\t    <link href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/bootstrap-3.3.4/css/bootstrap.min.css" rel="stylesheet">\n\t\t    <!-- \u7981\u6b62bootstrap \u54cd\u5e94\u5f0f \uff08app\u6839\u636e\u81ea\u8eab\u9700\u6c42\u542f\u7528\u6216\u7981\u6b62bootstrap\u54cd\u5e94\u5f0f\uff09 -->\n\t\t    <link href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/bootstrap-3.3.4/css/bootstrap_noresponsive.css" rel="stylesheet">\n\t\t    <!--\u81ea\u5b9a\u4e49css-->\n\t\t    <link href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'css/bk.css?v=')
        __M_writer(unicode(STATIC_VERSION))
        __M_writer(u'" rel="stylesheet">\n        <link rel="stylesheet" type="text/css" href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'css/index.css?v=')
        __M_writer(unicode(STATIC_VERSION))
        __M_writer(u'">\n        <!-- \u8fd9\u4e2a\u662f\u5168\u5c40\u914d\u7f6e\uff0c\u5982\u679c\u9700\u8981\u5728js\u4e2d\u4f7f\u7528app_id\u548csite_url,\u5219\u8fd9\u4e2ajavascript\u7247\u6bb5\u4e00\u5b9a\u8981\u4fdd\u7559 -->\n        <script type="text/javascript">\n\t    \t  var app_id = "')
        __M_writer(unicode(APP_ID))
        __M_writer(u'";\n\t\t\t    var site_url = "')
        __M_writer(unicode(SITE_URL))
        __M_writer(u'";\t  // app\u7684url\u524d\u7f00,\u5728ajax\u8c03\u7528\u7684\u65f6\u5019\uff0c\u5e94\u8be5\u52a0\u4e0a\u8be5\u524d\u7f00\n\t\t\t    var static_url = "')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'"; // \u9759\u6001\u8d44\u6e90\u524d\u7f00\n        </script>\n    ')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"130": 73, "171": 21, "141": 4, "16": 0, "151": 4, "152": 9, "153": 9, "154": 11, "155": 11, "156": 13, "157": 13, "158": 15, "159": 15, "160": 15, "161": 15, "162": 16, "163": 16, "164": 16, "37": 1, "166": 19, "167": 19, "168": 20, "169": 20, "42": 23, "43": 31, "44": 31, "45": 37, "177": 171, "58": 46, "59": 47, "60": 47, "61": 47, "62": 47, "63": 48, "64": 48, "65": 48, "66": 48, "67": 49, "68": 49, "69": 49, "70": 49, "71": 50, "72": 50, "73": 50, "74": 50, "75": 51, "76": 51, "77": 51, "78": 51, "79": 55, "80": 55, "81": 56, "82": 57, "83": 59, "84": 59, "85": 59, "86": 62, "87": 62, "92": 69, "165": 16, "97": 73, "98": 79, "99": 79, "100": 81, "101": 81, "102": 87, "103": 87, "104": 88, "105": 88, "106": 90, "107": 90, "108": 92, "109": 92, "110": 92, "111": 92, "112": 93, "113": 93, "119": 69, "170": 21}, "uri": "/base.html", "filename": "/Users/zhanglibing/vagrant/django18/LanhuSaas/framework/templates/base.html"}
__M_END_METADATA
"""
