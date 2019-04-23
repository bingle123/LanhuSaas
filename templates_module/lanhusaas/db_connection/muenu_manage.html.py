# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1554290233.712
_enable_loop = True
_template_filename = 'D:/py-workspace/LanhuSaas/framework/templates/db_connection/muenu_manage.html'
_template_uri = './db_connection/muenu_manage.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        STATIC_URL = context.get('STATIC_URL', UNDEFINED)
        SITE_URL = context.get('SITE_URL', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'<!DOCTYPE html>\r\n<html>\r\n<head>\r\n    <meta charset="UTF-8">\r\n    <!-- \u5f00\u53d1\u73af\u5883\u7248\u672c\uff0c\u5305\u542b\u4e86\u6709\u5e2e\u52a9\u7684\u547d\u4ee4\u884c\u8b66\u544a--2.5.51 -->\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/vue.development.js"></script>\r\n    <!-- element UI\u5f15\u5165\u6837\u5f0f -->\r\n    <link rel="stylesheet" href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/element-2.4.11/index.css">\r\n    <!-- element UI\u5f15\u5165\u7ec4\u4ef6\u5e93 -->\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/element-2.4.11/index.js"></script>\r\n    <!--axios.min.js--vue.js\u7684ajax\u652f\u6301-->\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/axios.min.js"></script>\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/jquery/jquery-3.1.1.min.js"></script>\r\n    <link type="text/css" href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'css/home.css" rel="stylesheet">\r\n    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/v-charts/lib/style.min.css">\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'js/muenu_manage/muenu_manage.js"></script>\r\n</head>\r\n\r\n<body>\r\n<input id="siteUrl" type="hidden" value="')
        __M_writer(unicode(SITE_URL))
        __M_writer(u'">\r\n<div class="content" id="main">\r\n    <div class="header">\r\n        <el-breadcrumb class="route" separator-class="el-icon-arrow-right">\r\n            <el-breadcrumb-item>\u9996\u9875</el-breadcrumb-item>\r\n            <el-breadcrumb-item>\u83dc\u5355\u7ba1\u7406</el-breadcrumb-item>\r\n        </el-breadcrumb>\r\n    </div>\r\n\r\n    <div class="body">\r\n        <el-card shadow="always">\r\n            <!--\u8868\u5355\u5c55\u793a-->\r\n            <div v-if="isAdd == \'1\'">\r\n                <div id="pagetitle">\r\n                    \u83dc\u5355\u7ba1\u7406\r\n                </div>\r\n                <hr id="hr">\r\n                <el-row type="flex" justify="space-between" class="row">\r\n                    <el-col :span="12">\r\n                        <el-col :span="9">\r\n                            <el-input v-model="menusearch" placeholder="\u8bf7\u8f93\u5165\u5185\u5bb9"></el-input>\r\n                        </el-col>\r\n                        <el-col :span="3">\r\n                            <el-button type="primary" icon="el-icon-search" v-on:click="select_table">\u641c\u7d22</el-button>\r\n                        </el-col>\r\n                    </el-col>\r\n                    <el-col :span=\'6\'>\r\n                        <el-button type=\'primary\' @click=\'show\'>\u65b0\u589e\u83dc\u5355</el-button>\r\n                        <el-button type=\'primary\' @click=\'get_roleAmuenus\'>\u6743\u9650\u5206\u914d</el-button>\r\n                    </el-col>\r\n                </el-row>\r\n\r\n                <el-table :data="tableData" :header-cell-style="rowClass" style="width: 100%">\r\n                    <el-table-column prop="id" label="\u5e8f\u53f7" width="80px">\r\n                    </el-table-column>\r\n                    <el-table-column prop="mname" label="\u83dc\u5355\u540d\u79f0" style="width: 25%">\r\n                    </el-table-column>\r\n                    m\r\n                    <el-table-column prop="url" label="\u83dc\u5355\u5730\u5740" style="width: 25%">\r\n                    </el-table-column>\r\n                    <el-table-column prop="operation" label="\u64cd\u4f5c">\r\n                        <template slot-scope="scope">\r\n                            <el-button type="text" @click="showe(scope.row)" size="small">\u7f16\u8f91</el-button>\r\n                            <el-button type="text" @click="delete_muenu(scope.row.id,scope.$index,tableData)"\r\n                                       size="small">\u5220\u9664\r\n                            </el-button>\r\n                        </template>\r\n                    </el-table-column>\r\n                </el-table>\r\n                <el-pagination :page-count="page_count" :current-page="currentPage" background layout="prev, pager, next" style="float:right"\r\n                               @current-change="current_change"></el-pagination>\r\n            </div>\r\n\r\n            <!--\u65b0\u589e-->\r\n            <div v-else-if="isAdd == \'2\'">\r\n                <div id="pagetitle">\r\n                    \u65b0\u589e\u83dc\u5355\r\n                </div>\r\n                <hr id="hr">\r\n                <el-form label-width="140px" :model="addmuenus" ref="addmuenus" :rules="rules" class="demo-ruleForm">\r\n                    <el-row type="flex" class="row-bg" justify="space-around">\r\n                        <el-col :span="9">\r\n                            <el-form-item label="\u83dc\u5355\u540d\u79f0\uff1a" prop="mname">\r\n                                <el-input v-model="addmuenus.mname"></el-input>\r\n                            </el-form-item>\r\n                        </el-col>\r\n                        <el-col :span="9">\r\n                            <el-form-item label="url\u5730\u5740\uff1a" prop="url">\r\n                                <el-input v-model="addmuenus.url"></el-input>\r\n                            </el-form-item>\r\n                        </el-col>\r\n                    </el-row>\r\n                </el-form>\r\n                <el-row type="flex" class="row-bg" justify="center">\r\n                    <el-col :span="2">\r\n                        <el-button type="primary" id="button" @click="savemuenu(\'addmuenus\')">\u4fdd\u5b58</el-button>\r\n                    </el-col>\r\n                    <el-col :span="2">\r\n                        <el-button @click="hide()" id="button">\u53d6\u6d88</el-button>\r\n                    </el-col>\r\n                </el-row>\r\n            </div>\r\n\r\n\r\n            <!--\u6743\u9650\u5206\u914d-->\r\n            <div v-else-if="isAdd == \'4\'">\r\n                <div id="pagetitle">\r\n                    \u6743\u9650\u5206\u914d\r\n                </div>\r\n                <hr id="hr">\r\n                <el-tree :data="dataCk" ref="tree" show-checkbox :default-checked-keys="checkedKeys" node-key="id"\r\n                         @check="checked"\r\n                >\r\n                </el-tree>\r\n                <el-button type="primary" @click="savemnus()">\u4fdd\u5b58</el-button>\r\n                <el-button @click="hide()">\u53d6\u6d88</el-button>\r\n            </div>\r\n\r\n            <!--\u7f16\u8f91-->\r\n            <div v-else="isAdd == \'3\'">\r\n                <div id="pagetitle">\r\n                    \u7f16\u8f91\u83dc\u5355\r\n                </div>\r\n                <hr id="hr">\r\n                <el-form label-width="140px" :model="editMuenu" ref="editMuenu" :rules="rules" class="demo-ruleForm">\r\n                    <el-row type="flex" class="row-bg" justify="space-around">\r\n                        <el-col :span="9">\r\n                            <el-form-item label="\u83dc\u5355\u540d\u79f0\uff1a" prop="mname">\r\n                                <el-input v-model="editMuenu.mname"></el-input>\r\n                            </el-form-item>\r\n                        </el-col>\r\n                        <el-col :span="9">\r\n                            <el-form-item label="url\u5730\u5740\uff1a" prop="url">\r\n                                <el-input v-model="editMuenu.url"></el-input>\r\n                            </el-form-item>\r\n                        </el-col>\r\n                    </el-row>\r\n                </el-form>\r\n                <el-row type="flex" class="row-bg" justify="center">\r\n                    <el-col :span="2">\r\n                        <el-button type="primary" @click="edit_muenu(\'editMuenu\')">\u4fee\u6539</el-button>\r\n                    </el-col>\r\n                    <el-col :span="2">\r\n                        <el-button @click="hide()">\u53d6\u6d88</el-button>\r\n                    </el-col>\r\n                </el-row>\r\n            </div>\r\n            <!--||||||||||||||||-->\r\n\r\n\r\n        </el-card>\r\n    </div>\r\n\r\n</div>\r\n\r\n\r\n</body>\r\n</html>\r\n\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"32": 13, "33": 13, "34": 14, "35": 14, "36": 16, "37": 16, "38": 20, "39": 20, "45": 39, "16": 0, "23": 1, "24": 6, "25": 6, "26": 8, "27": 8, "28": 10, "29": 10, "30": 12, "31": 12}, "uri": "./db_connection/muenu_manage.html", "filename": "D:/py-workspace/LanhuSaas/framework/templates/db_connection/muenu_manage.html"}
__M_END_METADATA
"""
