# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1546418204.516542
_enable_loop = True
_template_filename = '/Users/zhanglibing/vagrant/django18/LanhuSaas/framework/templates/db_connection_manage/vue_test_add.html'
_template_uri = '/db_connection_manage/vue_test_add.html'
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
        __M_writer(u'assets/vue-2.5.21/vue.development.js"></script>\n    <!-- \u751f\u4ea7\u73af\u5883\u7248\u672c\uff0c\u4f18\u5316\u4e86\u5c3a\u5bf8\u548c\u901f\u5ea6 -->\n    <!--<script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/vue.js"></script>-->\n    <!-- element UI\u5f15\u5165\u6837\u5f0f -->\n    <link rel="stylesheet" href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/element-2.4.11/index.css">\n    <!-- element UI\u5f15\u5165\u7ec4\u4ef6\u5e93 -->\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/element-2.4.11/index.js"></script>\n    <!-- vue\u7684ajax\u4f9d\u8d56-->\n    <!--<script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/vue-resource.min.js"></script>-->\n    <!--<script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/jquery/jquery-3.1.1.min.js"></script>-->\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/axios.min.js"></script>\n</head>\n<body>\n<!--\u8868\u5355-->\n<div id="form">\n    <el-form ref="form" :model="form" label-width="80px">\n        <el-form-item label="\u6d3b\u52a8\u540d\u79f0">\n            <el-input v-model="form.name"></el-input>\n        </el-form-item>\n        <el-form-item label="\u6d3b\u52a8\u533a\u57df">\n            <el-select v-model="form.region" placeholder="\u8bf7\u9009\u62e9\u6d3b\u52a8\u533a\u57df">\n                <el-option label="\u533a\u57df\u4e00" value="shanghai"></el-option>\n                <el-option label="\u533a\u57df\u4e8c" value="beijing"></el-option>\n            </el-select>\n        </el-form-item>\n        <el-form-item label="\u6d3b\u52a8\u65f6\u95f4">\n            <el-col :span="11">\n                <el-date-picker type="date" placeholder="\u9009\u62e9\u65e5\u671f" v-model="form.date1"\n                                style="width: 100%;"></el-date-picker>\n            </el-col>\n            <el-col class="line" :span="2">-</el-col>\n            <el-col :span="11">\n                <el-time-picker type="fixed-time" placeholder="\u9009\u62e9\u65f6\u95f4" v-model="form.date2"\n                                style="width: 100%;"></el-time-picker>\n            </el-col>\n        </el-form-item>\n        <el-form-item label="\u5373\u65f6\u914d\u9001">\n            <el-switch v-model="form.delivery"></el-switch>\n        </el-form-item>\n        <el-form-item label="\u6d3b\u52a8\u6027\u8d28">\n            <el-checkbox-group v-model="form.type">\n                <el-checkbox label="\u7f8e\u98df/\u9910\u5385\u7ebf\u4e0a\u6d3b\u52a8" name="type"></el-checkbox>\n                <el-checkbox label="\u5730\u63a8\u6d3b\u52a8" name="type"></el-checkbox>\n                <el-checkbox label="\u7ebf\u4e0b\u4e3b\u9898\u6d3b\u52a8" name="type"></el-checkbox>\n                <el-checkbox label="\u5355\u7eaf\u54c1\u724c\u66dd\u5149" name="type"></el-checkbox>\n            </el-checkbox-group>\n        </el-form-item>\n        <el-form-item label="\u7279\u6b8a\u8d44\u6e90">\n            <el-radio-group v-model="form.resource">\n                <el-radio label="\u7ebf\u4e0a\u54c1\u724c\u5546\u8d5e\u52a9"></el-radio>\n                <el-radio label="\u7ebf\u4e0b\u573a\u5730\u514d\u8d39"></el-radio>\n            </el-radio-group>\n        </el-form-item>\n        <el-form-item label="\u6d3b\u52a8\u5f62\u5f0f">\n            <el-input type="textarea" v-model="form.desc"></el-input>\n        </el-form-item>\n        <el-form-item>\n            <el-button type="primary" @click="onSubmit">\u7acb\u5373\u521b\u5efa</el-button>\n            <el-button>\u53d6\u6d88</el-button>\n        </el-form-item>\n    </el-form>\n</div>\n\n<script>\n    /**var form =  {\n    data() {\n      return {\n        form: {\n          name: \'\',\n          region: \'\',\n          date1: \'\',\n          date2: \'\',\n          delivery: false,\n          type: [],\n          resource: \'\',\n          desc: \'\'\n        }\n      }\n    },\n    methods: {\n      onSubmit() {\n        console.log(\'submit!\');\n\n      }\n    }\n  }\n     var form = Vue.extend(form)\n     new form().$mount(\'#form\')***/\n</script>\n<script>\n    //csrf\u9a8c\u8bc1\n    axios.interceptors.request.use((config) => {\n        config.headers[\'X-Requested-With\'] = \'XMLHttpRequest\';\n        let regex = /.*csrftoken=([^;.]*).*$/; // \u7528\u4e8e\u4ececookie\u4e2d\u5339\u914d csrftoken\u503c\n        config.headers[\'X-CSRFToken\'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];\n        return config\n    });\n\n    let vm = new Vue({\n        el: \'#form\',\n        data: {\n            form: {\n                name: \'111\',\n                region: \'\',\n                date1: \'\',\n                date2: \'\',\n                delivery: false,\n                type: [],\n                resource: \'\',\n                desc: \'\'\n            },\n\n\n        },\n        methods: {\n            onSubmit() {\n                console.log(\'submit!\')\n\n                /**axios.post(\'')
        __M_writer(unicode(SITE_URL))
        __M_writer(u"db_connection_manage/vue_add/',this.form,{emulateHTTP: true}).then(function (res) {\n                    console.log(this.form)\n                });**/\n\n                axios({\n                    method: 'post',\n                    url: '")
        __M_writer(unicode(SITE_URL))
        __M_writer(u"db_connection_manage/vue_add/',\n                    data: this.form,\n\n                }).then((res)=>{\n\n                }).catch();\n\n\n                /**this.$http.post('")
        __M_writer(unicode(SITE_URL))
        __M_writer(u"db_connection_manage/vue_add/',this.form,{emulateHTTP: true}).then(function () {\n                    console.log(this.form)\n                });**/\n\n                /**Vue.http({\n                    url:'")
        __M_writer(unicode(SITE_URL))
        __M_writer(u"db_connection_manage/vue_add/',\n                    data:{id:1},\n                    dataType:'json',\n                    type:'post',\n                    emulateHTTP:true,\n                    success:function (res) {\n                        console.log(res)\n                    }\n                })**/\n\n                /***$.ajax({\n                    type:'post',\n                    url:'")
        __M_writer(unicode(SITE_URL))
        __M_writer(u'db_connection_manage/vue_add/\',\n                    data:this.form,\n                    success:function (res) {\n                        alert("jquery")\n                    }\n                });**/\n            }\n        }\n    });\n\n\n</script>\n</body>\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"16": 0, "23": 1, "24": 4, "25": 4, "26": 6, "27": 6, "28": 8, "29": 8, "30": 10, "31": 10, "32": 12, "33": 12, "34": 13, "35": 13, "36": 14, "37": 14, "38": 122, "39": 122, "40": 128, "41": 128, "42": 136, "43": 136, "44": 141, "45": 141, "46": 153, "47": 153, "53": 47}, "uri": "/db_connection_manage/vue_test_add.html", "filename": "/Users/zhanglibing/vagrant/django18/LanhuSaas/framework/templates/db_connection_manage/vue_test_add.html"}
__M_END_METADATA
"""
