# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1555586692.012
_enable_loop = True
_template_filename = 'D:/py-workspace/LanhuSaas/framework/templates/logmanagement/logmanagement.html'
_template_uri = './logmanagement/logmanagement.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        STATIC_URL = context.get('STATIC_URL', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'<html>\r\n<head>\r\n    <meta charset="UTF-8">\r\n    <title>\u64cd\u4f5c\u65e5\u5fd7</title>\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/vue.development.js"></script>\r\n    <!-- \u751f\u4ea7\u73af\u5883\u7248\u672c\uff0c\u4f18\u5316\u4e86\u5c3a\u5bf8\u548c\u901f\u5ea6 \u529f\u80fd\u5b8c\u5584\u540e\u8bf7\u5c06vue.development.js\u8be5\u4e3avue.js-->\r\n    <!--<script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/vue.js"></script>-->\r\n    <!-- element UI\u5f15\u5165\u6837\u5f0f -->\r\n    <link href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/element-2.4.11/index.css" rel="stylesheet">\r\n    <!-- element UI\u5f15\u5165\u7ec4\u4ef6\u5e93 -->\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/element-2.4.11/index.js"></script>\r\n    <!-- vue\u7684ajax\u4f9d\u8d56-->\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/axios.min.js"></script>\r\n</head>\r\n<body>\r\n<div class="content">\r\n        <div class="body">\r\n        <el-card shadow="always">\r\n            <div>\r\n                <div id="pagetitle">\r\n                    \u64cd\u4f5c\u65e5\u5fd7\u67e5\u8be2\r\n                </div>\r\n                <hr id="hr">\r\n                <el-row type="flex" justify="space-between" align="center" class="row">\r\n                    <el-col :span="12">\r\n                        <el-col :span="9">\r\n                            <el-input v-model="search" placeholder="\u8bf7\u8f93\u5165\u5185\u5bb9"></el-input>\r\n                        </el-col>\r\n                        <el-col :span="3">\r\n                            <el-button type="primary" icon="el-icon-search" v-on:click="select_log">\u641c\u7d22</el-button>\r\n                        </el-col>\r\n                    </el-col>\r\n                </el-row>\r\n                <el-table :data="Operatelog"  style="width: 150%">\r\n                    <el-table-column prop="id" label="id" width="100" align="center">\r\n                    </el-table-column>\r\n                    <el-table-column prop="log_type" label="\u64cd\u4f5c\u7c7b\u578b" width="220" align="center">\r\n                    </el-table-column>\r\n                    <el-table-column prop="log_name" label="\u65e5\u5fd7\u540d\u79f0" width="150" align="center">\r\n                    </el-table-column>\r\n                    <el-table-column prop="user_name" label="\u7528\u6237\u540d\u79f0" width="150" align="center">\r\n                    </el-table-column>\r\n                    <el-table-column prop="class_name" label="\u7c7b\u540d\u79f0" width="150" align="center">\r\n                    </el-table-column>\r\n                    <el-table-column prop="method" label="\u65b9\u6cd5\u540d\u79f0" width="150" align="center">\r\n                    </el-table-column>\r\n                    <el-table-column prop="create_time" label="\u521b\u5efa\u65f6\u95f4" width="200" align="center">\r\n                    </el-table-column>\r\n                    <el-table-column prop="is_success" label="\u662f\u5426\u6210\u529f" width="150" align="center">\r\n                    </el-table-column>\r\n                    <el-table-column prop="message" label="\u5907\u6ce8" width="800" align="center">\r\n                    </el-table-column>\r\n                </el-table>\r\n                <el-pagination :page-count="page_count" background layout="prev, pager, next" style="float:right"\r\n                               @current-change="current_change" :current-page="page"></el-pagination>\r\n            </div>\r\n        </el-card>\r\n    </div>\r\n\r\n</div>\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'js/logmanagement/logmanagement.js"></script>\r\n</body>\r\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"32": 13, "33": 61, "34": 61, "40": 34, "16": 0, "22": 1, "23": 5, "24": 5, "25": 7, "26": 7, "27": 9, "28": 9, "29": 11, "30": 11, "31": 13}, "uri": "./logmanagement/logmanagement.html", "filename": "D:/py-workspace/LanhuSaas/framework/templates/logmanagement/logmanagement.html"}
__M_END_METADATA
"""
