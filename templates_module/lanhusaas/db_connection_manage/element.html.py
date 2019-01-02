# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1546418244.610193
_enable_loop = True
_template_filename = '/Users/zhanglibing/vagrant/django18/LanhuSaas/framework/templates/db_connection_manage/element.html'
_template_uri = '/db_connection_manage/element.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        STATIC_URL = context.get('STATIC_URL', UNDEFINED)
        SITE_URL = context.get('SITE_URL', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'<!DOCTYPE html>\n<html>\n<head>\n\t<title></title>\n    <!-- \u5f00\u53d1\u73af\u5883\u7248\u672c\uff0c\u5305\u542b\u4e86\u6709\u5e2e\u52a9\u7684\u547d\u4ee4\u884c\u8b66\u544a--2.5.51 -->\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/vue.development.js"></script>\n\t<!-- \u751f\u4ea7\u73af\u5883\u7248\u672c\uff0c\u4f18\u5316\u4e86\u5c3a\u5bf8\u548c\u901f\u5ea6 -->\n\t<!--<script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/vue.js"></script>-->\n\t<!-- element UI\u5f15\u5165\u6837\u5f0f -->\n\t<link rel="stylesheet" href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/element-2.4.11/index.css">\n\t<!-- element UI\u5f15\u5165\u7ec4\u4ef6\u5e93 -->\n\t<script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/element-2.4.11/index.js"></script>\n\n    <!-- vue\u7684ajax\u4f9d\u8d56-->\n    <!--<script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/vue-resource.min.js"></script>-->\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/jquery/jquery-3.1.1.min.js"></script>\n</head>\n<body>\n\n<div id="1myScene" class="myScene">\n    <table>\n        <thead>\n            <th>\u5e8f\u53f7</th>\n            <th>\u573a\u666f\u540d\u79f0</th>\n            <th>\u573a\u666f\u65f6\u95f4</th>\n        </thead>\n        <tbody v-for="s in scenes">\n            <td >{{s.id}}</td>\n            <td >{{s.scene_name}}</td>\n            <td >{{s.scene_default_time}}</td>\n        </tbody>\n    </table>\n</div>\n\n<div id="myScene" class="myScene">\n    <template>\n        <el-table\n        :data="scenes"\n        border\n        style="width: 100%">\n            <el-table-column\n              prop="id"\n              label="\u5e8f\u53f7ID"\n              width="180">\n            </el-table-column>\n            <el-table-column\n              prop="scene_name"\n              label="\u573a\u666f\u540d\u79f0"\n              width="180">\n            </el-table-column>\n            <el-table-column\n              prop="scene_default_time"\n              label="\u573a\u666f\u65f6\u95f4">\n            </el-table-column>\n        </el-table>\n    </template>\n</div>\n\n\n\n\n\n<div>\n    <div id="app2">\n      {{ message }}\n    </div>\n    <div id="app">\n        <template>\n          <div class="block">\n            <el-slider v-model="value8" show-input>\n            </el-slider>\n          </div>\n        </template>\n    </div>\n\n</div>\n\n\n\n\n<div id="app">\n    <template>\n      <div class="block">\n        <el-slider v-model="value8" show-input>\n        </el-slider>\n      </div>\n    </template>\n</div>\n\n<script>\nvar Main = {\n    data() {\n      return {\n        value8: 0\n      }\n    }\n  }\nvar Ctor = Vue.extend(Main)\nnew Ctor().$mount(\'#app\')\n</script>\n\n<script>\nvar app = new Vue({\n  el: \'#app2\',\n  data: {\n    message: \'Hello Vue!\'\n  }\n})\n</script>\n<script>\nwindow.onload = function () {\n    let myScene = new Vue({\n        el:\'#myScene\',\n        data:{\n            scene:\n                [\n                    {id:1,\n                    scene_name:"\u573a\u666f\u540d\u79f0",\n                    scene_default_time:"3000\u6beb\u79d2",},\n                    {id:2,\n                    scene_name:"\u573a\u666f\u540d\u79f02",\n                    scene_default_time:"4000\u6beb\u79d2",},\n                ],\n            scenes:[]\n        },\n\n        methods:{\n            get:function () {\n                this.$http.get(\'')
        __M_writer(unicode(SITE_URL))
        __M_writer(u'get_json_test\').then(function (res) {\n                    console.log(res);\n                    //this.scene = res.results\n                    this.scenes = res.body.results;\n\n                    console.log(res.body.results);\n                })\n\n            }\n        }\n    });\n    myScene.get();\n}\n</script>\n<div id="table">\n<template>\n  <el-table\n    :data="tableData"\n    border\n    style="width: 100%">\n    <el-table-column\n      prop="date"\n      label="\u65e5\u671f"\n      width="180">\n    </el-table-column>\n    <el-table-column\n      prop="name"\n      label="\u59d3\u540d"\n      width="180">\n    </el-table-column>\n    <el-table-column\n      prop="address"\n      label="\u5730\u5740">\n    </el-table-column>\n  </el-table>\n</template>\n</div>\n<script>\n  var Test = {\n    data() {\n      return {\n        tableData: [{\n          date: \'2016-05-02\',\n          name: \'\u738b\u5c0f\u864e\',\n          address: \'\u4e0a\u6d77\u5e02\u666e\u9640\u533a\u91d1\u6c99\u6c5f\u8def 1518 \u5f04\'\n        }, {\n          date: \'2016-05-04\',\n          name: \'\u738b\u5c0f\u864e\',\n          address: \'\u4e0a\u6d77\u5e02\u666e\u9640\u533a\u91d1\u6c99\u6c5f\u8def 1517 \u5f04\'\n        }, {\n          date: \'2016-05-01\',\n          name: \'\u738b\u5c0f\u864e\',\n          address: \'\u4e0a\u6d77\u5e02\u666e\u9640\u533a\u91d1\u6c99\u6c5f\u8def 1519 \u5f04\'\n        }, {\n          date: \'2016-05-03\',\n          name: \'\u738b\u5c0f\u864e\',\n          address: \'\u4e0a\u6d77\u5e02\u666e\u9640\u533a\u91d1\u6c99\u6c5f\u8def 1516 \u5f04\'\n        }]\n      }\n    }\n  }\n  var test = Vue.extend(Test)\n  new test().$mount(\'#table\')\n</script>\n</body>\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"32": 15, "33": 15, "34": 16, "35": 16, "36": 129, "37": 129, "43": 37, "16": 0, "23": 1, "24": 6, "25": 6, "26": 8, "27": 8, "28": 10, "29": 10, "30": 12, "31": 12}, "uri": "/db_connection_manage/element.html", "filename": "/Users/zhanglibing/vagrant/django18/LanhuSaas/framework/templates/db_connection_manage/element.html"}
__M_END_METADATA
"""
