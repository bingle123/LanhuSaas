# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1555550563.238
_enable_loop = True
_template_filename = 'D:/py-workspace/LanhuSaas/framework/templates/common/main.html'
_template_uri = './common/main.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        STATIC_URL = context.get('STATIC_URL', UNDEFINED)
        SITE_URL = context.get('SITE_URL', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'<!DOCTYPE html>\r\n<head>\r\n    <meta charset="UTF-8">\r\n    <title>\u770b\u677f\u7cfb\u7edf\u9996\u9875</title>\r\n    <!-- \u5f00\u53d1\u73af\u5883\u7248\u672c\uff0c\u5305\u542b\u4e86\u6709\u5e2e\u52a9\u7684\u547d\u4ee4\u884c\u8b66\u544a--2.5.51 ')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/-->\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/vue.development.js"></script>\r\n    <!-- \u751f\u4ea7\u73af\u5883\u7248 \u672c\uff0c\u4f18\u5316\u4e86\u5c3a\u5bf8\u548c\u901f\u5ea6 \u529f\u80fd\u5b8c\u5584\u540e\u8bf7\u5c06vue.development.js\u8be5\u4e3avue.js-->\r\n    <!--<script src="')
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
        __M_writer(u'";       // \u9759\u6001\u8d44\u6e90\u524d\u7f00\r\n    **/--->\r\n</head>\r\n<body style="overflow: visible">\r\n<!--start html-->\r\n<div id="index">\r\n    <!--start container-->\r\n    <el-container style="height: 100%">\r\n\r\n        <!--start left-->\r\n        <el-row class="tac" :style="height">\r\n            <el-menu :style="height" class="el-menu-vertical-demo" @open="handleOpen"\r\n                     @close="handleClose" :collapse="isCollapse">\r\n                <el-menu-item index="1000" class="title_item">\r\n                    <i class=""></i>\r\n                    <li slot="title" style="font-size: 18px;">\u770b\u677f\u9879\u76ee</li>\r\n                </el-menu-item>\r\n\r\n                <el-menu-item v-for="(i,index) in muenus" :index="index+\'\'" style="line-height: 56px;font-size: 18px;"\r\n                              v-on:click="testClick(i.url)">\r\n                    <i class="iconfont icon-zhuye"></i>\r\n                    <span slot="title">{{ i.mname }}</span>\r\n                </el-menu-item>\r\n\r\n                <div index="10000" style="line-height: 56px; margin-top: 1000px;margin-left: 20px;">\r\n                    <i class="el-icon-question"></i>\r\n                    <span slot="title"><a href="http://baidu.com">\u5e2e\u52a9</a></span>\r\n                </div>\r\n            </el-menu>\r\n        </el-row>\r\n        <!--end left-->\r\n\r\n        <!--start right-->\r\n        <el-container>\r\n            <!--start right header-->\r\n            <el-header class="header_item" height="62px">\r\n                <el-row :gutter="20">\r\n                    <el-col :span="6">\r\n                        <i class="iconfont icon-yincang" :style="display1" @click="changeCollapse"\r\n                           style="color: #555759;font-size: 30px;margin-top: 5px;"></i>\r\n                        <i class="iconfont icon-icon--" :style="display2" @click="changeCollapse"\r\n                           style="color: #555759;font-size: 25px;"></i>\r\n                        <span style="color: #555759; font-size: 16px; etter-spacing: 0.23px;">\u5f53\u524d\u4e1a\u52a1:</span>\r\n                        <span style="color: #555759; etter-spacing: 0.23px;">{{ business.name }}</span>\r\n                    </el-col>\r\n                    <el-col :span="6" :offset="12" style="color: #000;">\r\n                        <div style="float: right">\r\n                            <span style="color: #555759; etter-spacing: 0.23px;">\u5f53\u524d\u7528\u6237\uff1a</span>\r\n                            <span style="color: #555759; etter-spacing: 0.23px;">{{ user.name }}</span>\r\n                            <el-dropdown :hide-on-click="false"  @command="logout">\r\n                                <span class="el-dropdown-link">\r\n                                  &nbsp;&nbsp;|&nbsp;\u5e2e\u52a9\u4e2d\u5fc3<i class="el-icon-caret-bottom el-icon--right"></i>\r\n                                </span>\r\n                                <el-dropdown-menu slot="dropdown">\r\n                                    <el-dropdown-item command="a">\u6ce8\u9500</el-dropdown-item>\r\n                                </el-dropdown-menu>\r\n                            </el-dropdown>\r\n                        </div>\r\n                    </el-col>\r\n                </el-row>\r\n            </el-header>\r\n            <!--end right header-->\r\n            <!--start right body-->\r\n            <el-main>\r\n                <template>\r\n                    <div id="app">\r\n                            <iframe  v-show="isarr" class="ifa" scrolling=auto\r\n                            :src="\'')
        __M_writer(unicode(SITE_URL))
        __M_writer(u'\'+clickhtml"\r\n                            frameborder="0"></iframe>\r\n                    </div>\r\n                </template>\r\n            </el-main>\r\n            <!--end right body-->\r\n        </el-container>\r\n        <!--end right-->\r\n\r\n    </el-container>\r\n    <!--end container-->\r\n</div>\r\n<!--end html-->\r\n\r\n<script type="text/javascript">\r\n     axios.interceptors.request.use((config) => {\r\n        config.headers[\'X-Requested-With\'] = \'XMLHttpRequest\';\r\n        let regex = /.*csrftoken=([^;.]*).*$/; // \u7528\u4e8e\u4ececookie\u4e2d\u5339\u914d csrftoken\u503c\r\n        config.headers[\'X-CSRFToken\'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];\r\n        return config\r\n    });\r\n    let vm = new Vue({\r\n        el: \'#index\',\r\n        data: {\r\n            muenus: [],\r\n            isCollapse: false,  //\u662f\u5426\u6298\u53e0\r\n            height: {           //css\r\n                height: \'\',\r\n            },\r\n            display1: {\r\n                display: \'inline-block\',\r\n            },\r\n            display2: {\r\n                display: \'none\',\r\n            },\r\n            business: {         //\u4e1a\u52a1\u6570\u636e\r\n                name: "\u770b\u677f\u9879\u76ee",\r\n            },\r\n            user: {             //\u7528\u6237\u6570\u636e\r\n                name: "",\r\n            },\r\n\r\n            clickhtml:\'index\',\r\n            isarr:true,\r\n            /**activeName: \'first\',//\u9ed8\u8ba4iframe\u9009\u9879\r\n             ifArr: {            //\u6240\u6709iframe\u9875\u9762\uff0c\u4fdd\u7559\u4e00\u4e2a\u4e3atrue\uff0c\u5176\u4f59\u5747\u4e3afalse\r\n                first: true,\r\n                second: false,\r\n                third: false\r\n            }**/\r\n\r\n\r\n        },\r\n        created() {\r\n            //this.get_height()\r\n        },\r\n        methods: {\r\n            handleOpen(key, keyPath) {  //\u624b\u98ce\u7434\u6253\u5f00\r\n                console.log(key, keyPath);\r\n            },\r\n            handleClose(key, keyPath) { //\u624b\u98ce\u7434\u5173\u95ed\r\n                console.log(key, keyPath);\r\n            },\r\n            //\u9000\u51fa\u767b\u5f55\r\n            logout(){\r\n                axios.get(\'')
        __M_writer(unicode(SITE_URL))
        __M_writer(u"position/get_logout_address').then((res)=>{\r\n                    //\u4ece\u914d\u7f6e\u6587\u4ef6\u83b7\u53d6\u9000\u51fa\u767b\u5f55\u5730\u5740\r\n                    var login_address = res.data.message;\r\n                    window.location.href=login_address;\r\n                });\r\n            },\r\n            changeCollapse() {          //\u66f4\u6539\u4f38\u7f29\u72b6\u6001\r\n                let res = this.isCollapse;\r\n                if (res) {\r\n                    this.display1.display = 'inline-block';\r\n                    this.display2.display = 'none';\r\n                } else {\r\n                    this.display1.display = 'none';\r\n                    this.display2.display = 'inline-block';\r\n                }\r\n                this.isCollapse = res ? false : true;\r\n            },\r\n            get_user_name(){\r\n                axios.get('")
        __M_writer(unicode(SITE_URL))
        __M_writer(u"position/get_active_user').then((res)=>{\r\n                    console.log(res)\r\n                    vm.user.name=res.data.message\r\n                });\r\n            },\r\n            testClick(res) {            //\u66f4\u65b0iframe\u663e\u793a\u9875\u9762\r\n                vm.clickhtml = res\r\n             },\r\n\r\n            //\u83b7\u53d6\u89d2\u8272\u5bf9\u5e94\u7684\u6240\u6709\u83dc\u5355\u540d\u79f0\r\n            get_Muenu() {\r\n                axios.post('")
        __M_writer(unicode(SITE_URL))
        __M_writer(u"db_connection/get_user_muenu/')\r\n                    .then((res) => {\r\n                        console.log(res)\r\n                        vm.muenus = res.data.results;\r\n                    })\r\n            }\r\n        }\r\n    });\r\n    vm.get_Muenu();\r\n    vm.get_user_name()\r\n</script>\r\n</body>\r\n</html>\r\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"16": 0, "23": 1, "24": 5, "25": 5, "26": 6, "27": 6, "28": 8, "29": 8, "30": 10, "31": 10, "32": 12, "33": 12, "34": 14, "35": 14, "36": 16, "37": 16, "38": 18, "39": 18, "40": 20, "41": 20, "42": 25, "43": 25, "44": 26, "45": 26, "46": 93, "47": 93, "48": 158, "49": 158, "50": 176, "51": 176, "52": 187, "53": 187, "59": 53}, "uri": "./common/main.html", "filename": "D:/py-workspace/LanhuSaas/framework/templates/common/main.html"}
__M_END_METADATA
"""
