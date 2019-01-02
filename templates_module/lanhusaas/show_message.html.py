# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1546391310.917727
_enable_loop = True
_template_filename = '/Users/zhanglibing/vagrant/django18/LanhuSaas/framework/templates/show_message.html'
_template_uri = 'show_message.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        STATIC_URL = context.get('STATIC_URL', UNDEFINED)
        SITE_URL = context.get('SITE_URL', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'<html>\n<head>\n    <!-- \u5f00\u53d1\u73af\u5883\u7248\u672c\uff0c\u5305\u542b\u4e86\u6709\u5e2e\u52a9\u7684\u547d\u4ee4\u884c\u8b66\u544a--2.5.51 -->\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/vue.development.js"></script>\n    <!-- element UI\u5f15\u5165\u6837\u5f0f -->\n    <link rel="stylesheet" href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/element-2.4.11/index.css">\n    <!-- element UI\u5f15\u5165\u7ec4\u4ef6\u5e93 -->\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/element-2.4.11/index.js"></script>\n    <!--axios.min.js--vue.js\u7684ajax\u652f\u6301-->\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/axios.min.js"></script>\n<style>\n    .div3{\n\n        width: 550px;\n        height: 80%;\n        background-color: yellow;\n        position: relative;\n        left: 80%;\n        top: 10px;\n    }\n    .div1{\n        width: 79%;\n        position:relative;\n        left: 400px;\n        top: 200px;\n    }\n    input{\n\n        width: 250px;\n        height: 30px;\n    }\n</style>\n</head>\n\n<body>\n<div id="div1" style="height: 100%;width: 100%">\n  <div class="div1" id="div1">\n    <div id="div2">\n        <input type="text" placeholder="\u8bf7\u8f93\u5165\u641c\u7d20\u5185\u5bb9" v-model="content">\n        <el-button type="primary" icon="el-icon-search" v-on:click="aaa">\u641c\u7d22</el-button>\n          <el-popover placement="top-start"  width="200" trigger="hover" content="\u65b0\u589e\u4e00\u4e2a\u5355\u5143\u3002">\n            <el-button slot="reference">\u65b0\u589e</el-button>\n          </el-popover>\n\n    </div>\n        <!--<table class="table mb0 pr15 ranger-box2" id="table1"  >\n          <thead>\n          <tr>\n              <th style="width: 100px;">\u5e8f\u53f7</th>\n              <th style="width: 15%;">\u5355\u5143\u540d\u79f0</th>\n              <th style="width: 15%;">\u5355\u5143\u7c7b\u578b</th>\n              <th style="width: 15%;">\u7f16\u8f91\u4eba</th>\n              <th style="width: 15%;">\u7f16\u8f91\u65f6\u95f4</th>\n              <th>\u64cd\u4f5c</th>\n          </tr>\n          </thead>\n          <tbody>\n                    <tr v-for="site in sites">\n                        <td style="width: 100px;">{{ site.id }}</td>\n                        <td style="width: 15%;">{{ site.unit_name }}</td>\n                        <td style="width: 15%;">{{ site.unit_type }}</td>\n                        <td style="width: 15%;">{{ site.editor }}</td>\n                        <td style="width: 15%;">{{ site.edit_time }}</td>\n                        <td>\n                            <button class="btn btn-xs btn-warning" onclick="func()">\u7f16\u8f91</button>\n                            <button class="btn btn-xs btn-danger">\u5220\u9664</button>\n                        </td>\n                    </tr>\n          </tbody>\n      </table>-->\n      <div id="div5">\n      <el-table :data="sites" style="width: 100%" :default-sort="{prop: \'date\', order: \'descending\'}">\n    <el-table-column prop="id" label="\u5e8f\u53f7" sortable width="180">\n    </el-table-column>\n    <el-table-column prop="unit_name" label="\u59d3\u540d" sortable width="180">\n    </el-table-column>\n    <el-table-column prop="editor" label="\u5730\u5740" sortable width="180">\n    </el-table-column>\n      <el-table-column prop="editor" label="\u5730\u5740" sortable width="180">\n    </el-table-column>\n      <el-table-column prop="editor" label="\u5730\u5740" sortable width="180">\n    </el-table-column>\n          <el-button type="primary" icon="el-icon-edit"></el-button>\n          <el-button type="primary" icon="el-icon-delete"></el-button>\n  </el-table>\n    </div>\n  </div>\n</div>\n</body>\n\n<script>\n    var vm=  new Vue({\n        el: \'#div1\',\n        data: {\n            sites:[\n            ],\n        },\n        methods: {\n            a() {\n                axios({\n                    method: \'post\',\n                    url: \'')
        __M_writer(unicode(SITE_URL))
        __M_writer(u"test/',\n                }).then((res) => {\n                    vm.sites = res.data.message;\n                    console.log(vm.sites)\n                })\n            },\n            aaa() {\n                axios({\n                    method: 'post',\n                    url: '")
        __M_writer(unicode(SITE_URL))
        __M_writer(u"test1/',\n                    data: this.content,\n                }).then((res)=>{\n                    vm.sites = res.data.message\n                    console.log(res)\n                })\n            }\n        }\n    });\n    vm.a()\n</script>\n\n\n\n\n\n</html>")
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"32": 102, "33": 102, "34": 111, "35": 111, "41": 35, "16": 0, "23": 1, "24": 4, "25": 4, "26": 6, "27": 6, "28": 8, "29": 8, "30": 10, "31": 10}, "uri": "show_message.html", "filename": "/Users/zhanglibing/vagrant/django18/LanhuSaas/framework/templates/show_message.html"}
__M_END_METADATA
"""
