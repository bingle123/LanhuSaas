# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1555586709.057
_enable_loop = True
_template_filename = 'D:/py-workspace/LanhuSaas/framework/templates/system_config/crawl_content.html'
_template_uri = './system_config/crawl_content.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        STATIC_URL = context.get('STATIC_URL', UNDEFINED)
        SITE_URL = context.get('SITE_URL', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'<!DOCTYPE html>\r\n<html lang="en">\r\n<head>\r\n    <meta charset="UTF-8">\r\n    <title>\u722c\u866b\u5185\u5bb9\u67e5\u770b</title>\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/vue.development.js"></script>\r\n    <!-- \u751f\u4ea7\u73af\u5883\u7248\u672c\uff0c\u4f18\u5316\u4e86\u5c3a\u5bf8\u548c\u901f\u5ea6 \u529f\u80fd\u5b8c\u5584\u540e\u8bf7\u5c06vue.development.js\u8be5\u4e3avue.js-->\r\n    <!--<script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/vue.js"></script>-->\r\n    <!-- vue\u7684ajax\u4f9d\u8d56-->\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/axios.min.js"></script>\r\n    <!-- element UI\u5f15\u5165\u6837\u5f0f -->\r\n    <link href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/element-2.4.11/index.css" rel="stylesheet">\r\n    <!-- element UI\u5f15\u5165\u7ec4\u4ef6\u5e93 -->\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/element-2.4.11/index.js"></script>\r\n    <script src=\'')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u"js/jquery.min.js'></script>\r\n    <script src='")
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'js/jquery-ui.js\'></script>\r\n    <!--jQuery\u5e93\u4f7f\u7528\u65f6\u8bf7\u4f7f\u7528\u6807\u51c6jQuery\u8bed\u6cd5-->\r\n    <!--<script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/jquery/jquery-3.1.1.min.js"></script>-->\r\n    <!--\u9875\u9762\u521d\u59cb\u5316css(Tencent)-->\r\n    <link href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'css/init.css" rel="stylesheet">\r\n</head>\r\n<body>\r\n<div id="main">\r\n    <!--start \u9762\u5305\u5c51-->\r\n    <el-breadcrumb separator-class="el-icon-arrow-right" separator="/" style="padding: 20px;">\r\n        <el-breadcrumb-item><a href="/">\u7cfb\u7edf\u914d\u7f6e</a></el-breadcrumb-item>\r\n        <el-breadcrumb-item>\u722c\u866b\u5185\u5bb9\u67e5\u770b</el-breadcrumb-item>\r\n    </el-breadcrumb>\r\n    <!--end \u9762\u5305\u5c51-->\r\n\r\n    <!--start \u5361\u7247 \u5217\u8868\u9875-->\r\n    <el-card class="box-card" style="margin: 20px;" style="height: 100%">\r\n        <div slot="header" class="clearfix">\r\n            <div class="grid-content bg-purple"><h2>\u722c\u866b\u5185\u5bb9\u67e5\u770b</h2></div>\r\n            <br>\r\n            <el-row :gutter="20">\r\n                <el-col :span="20">\r\n                    <el-form :inline="true" class="demo-form-inline">\r\n                        <el-form-item label="\u722c\u866b\u540d\u79f0\uff1a">\r\n                            <el-input placeholder="\u8bf7\u8f93\u5165\u722c\u866b\u540d\u79f0" v-model="crawl_name"></el-input>\r\n                        </el-form-item>\r\n                        <el-form-item label="\u722c\u866b\u5185\u5bb9\u6807\u9898\u540d\u79f0\uff1a">\r\n                            <el-input placeholder="\u8bf7\u8f93\u5165\u6807\u9898\u540d\u79f0" v-model="title_content"></el-input>\r\n                        </el-form-item>\r\n                        <el-form-item>\r\n                            <el-button type="primary" @click="query">\u67e5\u8be2</el-button>\r\n                        </el-form-item>\r\n                    </el-form>\r\n                </el-col>\r\n            </el-row>\r\n        </div>\r\n        <template>\r\n            <el-table\r\n                    :data="tableData"\r\n                    stripe\r\n                    style="width: 100%">\r\n                <el-table-column\r\n                        prop="crawl_name"\r\n                        label="\u722c\u866b\u540d\u79f0"\r\n                        width="200">\r\n                </el-table-column>\r\n                <el-table-column label="\u722c\u866b\u5185\u5bb9\u67e5\u770b" width="600">\r\n                    <template slot-scope="scope">\r\n                        <el-button size="mini" type="text"\r\n                                   v-on:click="open_url(scope.row.url_content)">{{ scope.row.title_content }}</el-button>\r\n                    </template>\r\n                </el-table-column>\r\n                <el-table-column\r\n                        prop="url_content"\r\n                        label="\u5730\u5740"\r\n                        width="400">\r\n                </el-table-column>\r\n                <el-table-column\r\n                        prop="time_content"\r\n                        label="\u65f6\u95f4"\r\n                        width="180">\r\n                </el-table-column>\r\n                <el-table-column\r\n                        prop="save_time"\r\n                        label="\u4fdd\u5b58\u65f6\u95f4"\r\n                        width="180">\r\n                </el-table-column>\r\n            </el-table>\r\n            <el-pagination :page-count="page_count" background layout="sizes, prev, pager, next" style="float:right"\r\n                           @current-change="changePage"  @size-change="changeSize" :page-sizes="[5, 10, 20, 50]" :page-size="5"></el-pagination>\r\n        </template>\r\n\r\n    </el-card>\r\n    <!--end \u5361\u7247 \u5217\u8868\u9875-->\r\n</div>\r\n\r\n<script>\r\n    //csrf\u9a8c\u8bc1\r\n    axios.interceptors.request.use((config) => {\r\n        config.headers[\'X-Requested-With\'] = \'XMLHttpRequest\';\r\n        let regex = /.*csrftoken=([^;.]*).*$/; // \u7528\u4e8e\u4ececookie\u4e2d\u5339\u914d csrftoken\u503c\r\n        config.headers[\'X-CSRFToken\'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];\r\n        return config\r\n    });\r\n    let vm = new Vue({\r\n        el: \'#main\',\r\n        data: {\r\n            title_content: \'\',\r\n            crawl_name: \'\',\r\n            page: 1,\r\n            page_count: 1,\r\n            limit: 5,\r\n            tableData: [],\r\n        },\r\n        methods: {\r\n            changeSize(value){\r\n                vm.limit = value;\r\n                vm.query();\r\n            },\r\n            query() {\r\n                vm.page= 1;\r\n                axios({\r\n                    url: \'')
        __M_writer(unicode(SITE_URL))
        __M_writer(u"system_config/get_crawl_content/',\r\n                    method: 'post',\r\n                    data: {title_content: vm.title_content, crawl_name: vm.crawl_name, page: vm.page, limit: vm.limit}\r\n                }).then((res) => {\r\n                    console.log(res);\r\n                    if (res.code != 0) {\r\n                        if (res.data.results.length == 0) {\r\n                            vm.$message.info('\u6ca1\u6709\u6570\u636e')\r\n                        } else {\r\n                            vm.tableData = res.data.results;\r\n                            vm.page_count = res.data.results[0]['page_count']\r\n                        }\r\n                    } else {\r\n                        vm.$message.error('\u83b7\u53d6\u5931\u8d25')\r\n                    }\r\n                }).catch((res) => {\r\n                    console.log(res);\r\n                    vm.$message.error('\u83b7\u53d6\u5931\u8d25' + res)\r\n                })\r\n            },\r\n            changePage(value) {\r\n                vm.page = value;\r\n                vm.query();\r\n            },\r\n            open_url(value) {\r\n                window.location.href = value\r\n            }\r\n\r\n        }\r\n\r\n    });\r\n    vm.query();\r\n</script>\r\n</body>\r\n</html>")
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"16": 0, "23": 1, "24": 6, "25": 6, "26": 8, "27": 8, "28": 10, "29": 10, "30": 12, "31": 12, "32": 14, "33": 14, "34": 15, "35": 15, "36": 16, "37": 16, "38": 18, "39": 18, "40": 20, "41": 20, "42": 118, "43": 118, "49": 43}, "uri": "./system_config/crawl_content.html", "filename": "D:/py-workspace/LanhuSaas/framework/templates/system_config/crawl_content.html"}
__M_END_METADATA
"""
