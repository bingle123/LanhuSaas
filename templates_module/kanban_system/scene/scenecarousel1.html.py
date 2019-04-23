# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1555586659.434
_enable_loop = True
_template_filename = 'D:/py-workspace/LanhuSaas/framework/templates/scene/scenecarousel1.html'
_template_uri = './scene/scenecarousel1.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        STATIC_URL = context.get('STATIC_URL', UNDEFINED)
        SITE_URL = context.get('SITE_URL', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'<!DOCTYPE html>\r\n<head>\r\n    <meta charset="UTF-8">\r\n    <title>Title</title>\r\n    <script type="text/javascript" src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'js/Component-based.js"></script>\r\n    <script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script>\r\n    <!-- \u5f00\u53d1\u73af\u5883\u7248\u672c\uff0c\u5305\u542b\u4e86\u6709\u5e2e\u52a9\u7684\u547d\u4ee4\u884c\u8b66\u544a--2.5.51 ')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/-->\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/vue.development.js"></script>\r\n    <!-- \u751f\u4ea7\u73af\u5883\u7248\u672c\uff0c\u4f18\u5316\u4e86\u5c3a\u5bf8\u548c\u901f\u5ea6 \u529f\u80fd\u5b8c\u5584\u540e\u8bf7\u5c06vue.development.js\u8be5\u4e3avue.js-->\r\n    <!--<script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/vue.js"></script>-->\r\n    <!-- element UI\u5f15\u5165\u6837\u5f0f -->\r\n    <link href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/element-2.4.11/index.css" rel="stylesheet">\r\n    <!-- element UI\u5f15\u5165\u7ec4\u4ef6\u5e93 -->\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/element-2.4.11/index.js"></script>\r\n    <!-- vue\u7684ajax\u4f9d\u8d56-->\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/axios.min.js"></script>\r\n    <!--jQuery\u5e93\u4f7f\u7528\u65f6\u8bf7\u4f7f\u7528\u6807\u51c6jQuery\u8bed\u6cd5-->\r\n    <!--<script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/jquery/jquery-3.1.1.min.js"></script>-->\r\n    <!--\u9875\u9762\u521d\u59cb\u5316css(Tencent)-->\r\n    <link href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'css/common/init.css" rel="stylesheet">\r\n    <!--\u672c\u9875\u9762css-->\r\n    <link href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'css/common/main.css" rel="stylesheet">\r\n    <!--\u963f\u91cc\u5df4\u5df4\u77e2\u91cf\u56fe\u6807\u5e93--\u9879\u76ee\u5b8c\u6210\u540e\u8bf7\u4e0b\u8f7dcss\u5e76\u4e0b\u8f7dcss\u5f15\u7528\u7684\u5b57\u4f53\u6587\u4ef6-->\r\n    <link href="http://at.alicdn.com/t/font_997278_ptr5bdmor4j.css" rel="stylesheet">\r\n    <!--\u4ee5\u4e0b\u4e3a\u540e\u53f0\u53c2\u6570-->\r\n    <!--\r\n    "')
        __M_writer(unicode(SITE_URL))
        __M_writer(u'";\t        // app\u7684url\u524d\u7f00,\u5728ajax\u8c03\u7528\u7684\u65f6\u5019\uff0c\u5e94\u8be5\u52a0\u4e0a\u8be5\u524d\u7f00\r\n    "')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'";       // \u9759\u6001\u8d44\u6e90\u524d\u7f00\r\n    **/--->\r\n    <link type="text/css" href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'css/monitorScene/style.css" rel="stylesheet">\r\n    <script src="https://cdn.jsdelivr.net/npm/v-charts/lib/index.min.js"></script>\r\n    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/v-charts/lib/style.min.css">\r\n    <link href="https://magicbox.bk.tencent.com/static_api/v3/bk/css/bk.css" rel="stylesheet">\r\n    <link href="https://magicbox.bk.tencent.com/static_api/v3/assets/jrange/css/jquery.range.css" rel="stylesheet">\r\n    <script src="https://magicbox.bk.tencent.com/static_api/v3/assets/js/jquery-1.10.2.min.js"></script>\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'js/jquery.range-min.js"></script>\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'js/scene/scene_carousel_test.js"></script>\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'js/csrftoken.js"></script>\r\n\r\n    <link rel="stylesheet" href="https://magicbox.bk.tencent.com/static_api/v3/assets/bk-icon-2.0/iconfont.css">\r\n    <script type="text/javascript" src="https://magicbox.bk.tencent.com/static_api/v3/assets/dataflow-2.0/js/jsplumb.min.js"></script>\r\n    <link rel="stylesheet" href="https://magicbox.bk.tencent.com/static_api/v3/assets/dataflow-2.0/css/jsPlumbToolkit-defaults.css" />\r\n    <script type="text/javascript" src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'js/dataflow/dataflow2.0.js"></script>\r\n    <link rel="stylesheet" href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'css/monitorScene/dataflow-index.css">\r\n    <style>\r\n        .Drigging {\r\n            color: gray;\r\n            position: absolute;\r\n            border-radius: 0;\r\n            border: 1px solid #AAAAAA;\r\n        }\r\n    </style>\r\n</head>\r\n<body style="height: 100%">\r\n<div id="main">\r\n    <el-menu\r\n\r\n            class="el-menu-demo"\r\n            mode="horizontal"\r\n            background-color="#fafafa"\r\n            text-color="#fff"\r\n            active-text-color="#ffd04b">\r\n        <el-form :inline="true" class="demo-form-inline" style="margin: 50px 20px;">\r\n\r\n            <el-form-item label="\u5c97\u4f4d\u540d\u79f0:" size="mini"  prop="users">\r\n                <el-select v-model="position" placeholder="\u8bf7\u9009\u62e9\u5c97\u4f4d" >\r\n                    <el-option v-for="item in options" :label="item.label" :key="item.value"\r\n                               :value="item.value"></el-option>\r\n                </el-select>\r\n            </el-form-item>\r\n            <el-form-item label="\u8d77\u59cb\u65f6\u95f4:" size="mini">\r\n                <el-time-picker v-model="start" placeholder="\u5f00\u59cb\u65f6\u95f4\u70b9" format="HH:mm" value-format="HH:mm" >\r\n                </el-time-picker>\r\n                <el-time-picker v-model="end" placeholder="\u7ed3\u675f\u65f6\u95f4\u70b9" format="HH:mm" value-format="HH:mm" >\r\n                </el-time-picker>\r\n            </el-form-item>\r\n            <el-button type="info" v-on:click="alternate_play_test">\u6d4b\u8bd5</el-button>\r\n        </el-form>\r\n    </el-menu>\r\n    <template>\r\n        <div class="block">\r\n            <!-- \u9009\u62e9\u5458\u5de5\u4fe1\u606f strat -->\r\n            <div style="width: 100%;">\r\n\r\n            </div>\r\n            <!-- \u9009\u62e9\u5458\u5de5\u4fe1\u606f end -->\r\n            <!--<span class="demonstration">Click \u6307\u793a\u5668\u89e6\u53d1</span>-->\r\n            <!-- \u6bcf\u969410\u79d2\u5207\u6362\u4e00\u6b21\u8d70\u9a6c\u706f -->\r\n            <el-carousel :interval="10000" trigger="click" @change="scene_change" :height="imgHeight">\r\n                <el-carousel-item v-for="(item,index) in imgList" :key="index">\r\n                    <el-row>\r\n                        <el-col :span="24">\r\n                            <div ref="imgHeight" :src="item.idView" :id="item.scene_id" :class="\'scene_content\'+index" style="position: relative;">\r\n                            </div>\r\n                        </el-col>\r\n                    </el-row>\r\n                </el-carousel-item>\r\n            </el-carousel>\r\n        </div>\r\n    </template>\r\n</div>\r\n<!--\u6682\u65f6\u7684css\u6837\u5f0f-->\r\n<style>\r\n    .el-carousel__item h3 {\r\n        color: #475669;\r\n        font-size: 14px;\r\n        opacity: 0.75;\r\n        line-height: 150px;\r\n        margin: 0;\r\n    }\r\n\r\n    .el-carousel__item {\r\n        background-image: url("/static/img/scene_content_bg.png");\r\n        background-size: 100% 100%;\r\n    }\r\n    .score_input{\r\n            font-size: 16px;\r\n            position: absolute;\r\n            background: rgba(255,255,255,0.1);\r\n            top: -36px;\r\n            left: 0;\r\n            width: 50px;\r\n            height: 36px;\r\n            display: none;\r\n        }\r\n    .right_click{\r\n        position: absolute;\r\n        width: 100px;\r\n        display: none;\r\n    }\r\n    .right_click span{\r\n        width: 100px;\r\n        display: inline-block;\r\n        font-size: 16px;\r\n        line-height: 36px;\r\n    }\r\n    .keepOn{\r\n        position: absolute;\r\n        top: 32px;\r\n        right: 0;\r\n        width: 115px;\r\n        height: 60px;\r\n    }\r\n    .keepOn p{\r\n        margin-top: 5px;\r\n        line-height: 20px;\r\n        color: black;\r\n    }\r\n    .keepOn span{\r\n        width: 20%;\r\n        margin: 0 20px;\r\n        color: black;\r\n        background: #00baff;\r\n    }\r\n</style>\r\n</body>\r\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"16": 0, "23": 1, "24": 5, "25": 5, "26": 7, "27": 7, "28": 8, "29": 8, "30": 10, "31": 10, "32": 12, "33": 12, "34": 14, "35": 14, "36": 16, "37": 16, "38": 18, "39": 18, "40": 20, "41": 20, "42": 22, "43": 22, "44": 27, "45": 27, "46": 28, "47": 28, "48": 30, "49": 30, "50": 36, "51": 36, "52": 37, "53": 37, "54": 38, "55": 38, "56": 43, "57": 43, "58": 44, "59": 44, "65": 59}, "uri": "./scene/scenecarousel1.html", "filename": "D:/py-workspace/LanhuSaas/framework/templates/scene/scenecarousel1.html"}
__M_END_METADATA
"""
