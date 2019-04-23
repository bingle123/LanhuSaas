# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1555586677.237
_enable_loop = True
_template_filename = 'D:/py-workspace/LanhuSaas/framework/templates/position/position.html'
_template_uri = './position/position.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        STATIC_URL = context.get('STATIC_URL', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'<html>\r\n\r\n<head>\r\n    <meta charset="UTF-8">\r\n    <title>\u5c97\u4f4d\u7ba1\u7406</title>\r\n    <script src="')
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
        __M_writer(u'assets/jquery/jquery-3.1.1.min.js"></script>\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/vue-router.js"></script>-->\r\n    <style>\r\n        input {\r\n            width: 250px;\r\n            height: 30px;\r\n        }\r\n\r\n        .el-table--border th {\r\n            padding: 5px\r\n        }\r\n    </style>\r\n</head>\r\n\r\n<body>\r\n<div class="content">\r\n    <el-dialog title="\u65b0\u589e\u5c97\u4f4d\u4eba\u5458" :visible.sync="dialogFormVisible" width="70%" :before-close="handleDialogClose">\r\n        <el-form :model="form">\r\n            <el-form-item label="">\r\n                <template>\r\n                    <template>\r\n                        <el-transfer\r\n                                filterable\r\n                                :filter-method="filterMethod"\r\n                                filter-placeholder="\u8bf7\u8f93\u5165\u641c\u7d22\u5185\u5bb9"\r\n                                v-model="value2"\r\n                                :titles="[\'\u9009\u62e9\u4eba\u5458\', jobname]"\r\n                                :data="data2"\r\n                                @change="">\r\n                        </el-transfer>\r\n                    </template>\r\n                </template>\r\n            </el-form-item>\r\n        </el-form>\r\n        <div slot="footer" class="dialog-footer">\r\n            <el-button @click="add_person()" type="primary">\u4fdd\u5b58</el-button>\r\n            <el-button @click="ref()">\u53d6\u6d88</el-button>\r\n        </div>\r\n    </el-dialog>\r\n\r\n    <el-dialog title="\u7f16\u8f91\u5c97\u4f4d" :visible.sync="dialogFormVisible2">\r\n        <el-form :model="form2" ref="form2" :rules="rules2">\r\n            <el-form-item label="\u5c97\u4f4d\u540d\uff1a" prop="tempjobname">\r\n                <el-input placeholder="\u8bf7\u8f93\u5165\u5c97\u4f4d\u540d" v-model="form2.tempjobname" style="width: 60%"></el-input>\r\n            </el-form-item>\r\n        </el-form>\r\n        <span slot="footer" class="dialog-footer">\r\n            <el-button @click=" edit_pos(\'form2\')" type="primary">\u4fdd\u5b58</el-button>\r\n            <el-button @click="dialogFormVisible2 = false">\u53d6\u6d88</el-button>\r\n        </span>\r\n\r\n    </el-dialog>\r\n\r\n    <el-dialog title="\u65b0\u589e\u5c97\u4f4d" :visible.sync="dialogFormVisible3">\r\n        <el-form :model="form" ref="form" :rules="rules">\r\n            <el-form-item label="\u5c97\u4f4d\u540d\u79f0:" prop=\'pos_name\'>\r\n                <el-input v-model="form.pos_name"></el-input>\r\n            </el-form-item>\r\n        </el-form>\r\n        <div slot="footer" class="dialog-footer">\r\n            <el-button @click="add_pos(\'form\')" type="primary">\u4fdd\u5b58</el-button>\r\n            <el-button @click="dialogFormVisible3 = false">\u53d6\u6d88</el-button>\r\n        </div>\r\n    </el-dialog>\r\n\r\n    <div class="header">\r\n        <el-breadcrumb class="route" separator-class="el-icon-arrow-right">\r\n            <el-breadcrumb-item>\u770b\u677f\u7cfb\u7edf\u914d\u7f6e</el-breadcrumb-item>\r\n            <el-breadcrumb-item>\u5c97\u4f4d\u7ba1\u7406</el-breadcrumb-item>\r\n        </el-breadcrumb>\r\n    </div>\r\n    <div class="body">\r\n        <el-card shadow="always">\r\n            <div>\r\n                <div id="pagetitle">\r\n                    \u5c97\u4f4d\u7ba1\u7406\r\n                </div>\r\n                <hr id="hr">\r\n                <el-row type="flex" justify="space-between" align="center" class="row">\r\n                    <el-col :span="12">\r\n                        <el-col :span="9">\r\n                            <el-input v-model="search" placeholder="\u8bf7\u8f93\u5165\u5185\u5bb9"></el-input>\r\n                        </el-col>\r\n                        <el-col :span="3">\r\n                            <el-button type="primary" icon="el-icon-search" v-on:click="select_pos">\u641c\u7d22</el-button>\r\n                        </el-col>\r\n                    </el-col>\r\n                    <el-col :span="3">\r\n                        <el-button type="button" @click="dialogFormVisible3 = true">\u65b0\u589e\u5c97\u4f4d</el-button>\r\n                    </el-col>\r\n                </el-row>\r\n                <el-table :data="positiontable" style="width: 100%;margin-top: 20px">\r\n                    <el-table-column prop="pos_name" label="\u5c97\u4f4d\u540d\u79f0" style="width: 10%" align="center">\r\n                    </el-table-column>\r\n                    <el-table-column prop="user_name" label="\u5c97\u4f4d\u4eba\u5458" style="width: 40%;" align="center">\r\n                    </el-table-column>\r\n                    <el-table-column prop="creator" label="\u521b\u5efa\u4eba" style="width: 10%;" align="center">\r\n                    </el-table-column>\r\n                    <el-table-column prop="create_time" label="\u521b\u5efa\u65f6\u95f4" style="width: 10%;" align="center">\r\n                    </el-table-column>\r\n                    <el-table-column prop="editor" label="\u6700\u540e\u4fee\u6539\u4eba" style="width: 10%;" align="center">\r\n                    </el-table-column>\r\n                    <el-table-column prop="edit_time" label="\u6700\u540e\u4fee\u6539\u65f6\u95f4" style="width: 10%;" align="center">\r\n                    </el-table-column>\r\n                    <el-table-column prop="operation" label="\u64cd\u4f5c" style="width: 10%">\r\n                        <template slot-scope="scope">\r\n                            <el-button type="text" @click="show_pos(scope.row)" size="small">\u52a0\u4eba</el-button>\r\n                            <el-button type="text" @click="edit_posname(scope.row)" size="small">\u7f16\u8f91</el-button>\r\n                            <el-button type="text" @click="deletePosition(scope.row.id)" size="small">\u5220\u9664</el-button>\r\n                        </template>\r\n                    </el-table-column>\r\n                </el-table>\r\n                <el-pagination :page-count="page_count" background layout="prev, pager, next" style="float:right"\r\n                               @current-change="current_change1" :current-page="page"></el-pagination>\r\n            </div>\r\n\r\n        </el-card>\r\n\r\n    </div>\r\n    <el-input placeholder="\u8f93\u5165\u5173\u952e\u5b57\u8fdb\u884c\u8fc7\u6ee4" v-model="filterText"></el-input>\r\n    <el-tree class="filter-tree" :data="data3" :props="defaultProps" default-expand-all show-checkbox\r\n             :filter-node-method="filterNode" ref="tree2"></el-tree>\r\n</div>\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'js/position/position.js"></script>\r\n</body>\r\n\r\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"32": 14, "33": 16, "34": 16, "35": 17, "36": 17, "37": 139, "38": 139, "44": 38, "16": 0, "22": 1, "23": 6, "24": 6, "25": 8, "26": 8, "27": 10, "28": 10, "29": 12, "30": 12, "31": 14}, "uri": "./position/position.html", "filename": "D:/py-workspace/LanhuSaas/framework/templates/position/position.html"}
__M_END_METADATA
"""
