# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1546590187.502
_enable_loop = True
_template_filename = 'E:/LanhuSaas/framework/templates/show_message.html'
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
        __M_writer(u'<html>\r\n<head>\r\n    <meta charset="UTF-8">\r\n    <!-- \u5f00\u53d1\u73af\u5883\u7248\u672c\uff0c\u5305\u542b\u4e86\u6709\u5e2e\u52a9\u7684\u547d\u4ee4\u884c\u8b66\u544a--2.5.51 -->\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/vue.development.js"></script>\r\n    <!-- element UI\u5f15\u5165\u6837\u5f0f -->\r\n    <link rel="stylesheet" href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/element-2.4.11/index.css">\r\n    <!-- element UI\u5f15\u5165\u7ec4\u4ef6\u5e93 -->\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/element-2.4.11/index.js"></script>\r\n    <!--axios.min.js--vue.js\u7684ajax\u652f\u6301-->\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/vue-2.5.21/axios.min.js"></script>\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/jquery/jquery-3.1.1.min.js"></script>\r\n<style>\r\n    .div1{\r\n        width: 1100px;\r\n        height: 1000px;\r\n    }\r\n    .div2{\r\n        width: 1100px;\r\n        height: 800px;\r\n        background-color: whitesmoke;\r\n        position: absolute;\r\n        top: 10px;\r\n        left: 10px;\r\n    }\r\n    input{\r\n        width: 250px;\r\n        height: 30px;\r\n    }\r\n    .center1{\r\n        width: 217px;\r\n        text-align:center;\r\n    }\r\n</style>\r\n</head>\r\n<body>\r\n<div id="app">\r\n  <div class="div1" >\r\n    <div>\r\n        <input type="text" placeholder="\u8bf7\u8f93\u5165\u641c\u7d20\u5185\u5bb9" v-model="contents">\r\n        <el-button type="primary" icon="el-icon-search" v-on:click="aaa">\u641c\u7d22</el-button>\r\n          <el-popover placement="top-start"  width="200" trigger="hover" content="\u65b0\u589e\u4e00\u4e2a\u5355\u5143\u3002">\r\n            <el-button slot="reference">\u65b0\u589e</el-button>\r\n          </el-popover>\r\n    </div>\r\n    <div>\r\n     <el-table :data="sites" border style="width: 100%">\r\n    <el-table-column prop="id" label="\u5e8f\u53f7" sortable width="180">\r\n    </el-table-column>\r\n    <el-table-column prop="unit_name" label="\u5355\u5143\u540d\u79f0" sortable width="180">\r\n    </el-table-column>\r\n    <el-table-column prop="unit_type" label="\u5355\u5143\u7c7b\u578b" sortable width="180">\r\n    </el-table-column>\r\n      <el-table-column prop="editor" label="\u7f16\u8f91\u4eba" sortable width="180">\r\n    </el-table-column>\r\n      <el-table-column prop="edit_time" label="\u4fee\u6539\u65f6\u95f4" sortable width="180">\r\n    </el-table-column>\r\n     <el-table-column label="\u64cd\u4f5c" >\r\n      <template slot-scope="scope">\r\n        <el-button id="button1" type="text" size="small" v-on:click="edit(scope.row.id)" >\u7f16\u8f91</el-button>\r\n        <el-button type="text" v-on:click="edit2(scope.row.id)">\u5220\u9664</el-button>\r\n      </template>\r\n    </el-table-column>\r\n  </el-table>\r\n  <el-pagination background layout="prev, pager, next" :total="1000">\r\n    </el-pagination>\r\n    </div>\r\n  </div>\r\n\r\n<div class="div2" id="div3" >\r\n     <div id="unit_name" style="width: 217px;margin:10px" >\r\n     <div class="center1" >\u6a21\u677f\u540d\u79f0</div>\r\n     <el-input v-model="unit_name" placeholder="\u8bf7\u8f93\u5165\u6a21\u677f\u540d\u79f0"></el-input>\r\n </div>\r\n    <div class="center1" style="margin:10px">\u5b57\u53f7</div>\r\n<el-autocomplete  popper-class="my-autocomplete" v-model="state3" :fetch-suggestions="querySearch" placeholder="\u8bf7\u8f93\u5165\u5185\u5bb9" @select="handleSelect">\r\n  <i class="el-icon-edit el-input__icon" slot="suffix" @click="handleIconClick">\r\n  </i>\r\n  <template slot-scope="{ item }">\r\n    <div class="name">{{ item.value }}</div>\r\n  </template>\r\n</el-autocomplete>\r\n <div id="height1" style="width: 217px;margin:10px">\r\n     <div class="center1">\u9ad8</div>\r\n     <el-input v-model="height1" placeholder="\u8bf7\u8f93\u5165\u9ad8\u5ea6"></el-input>\r\n </div>\r\n\r\n <div id="width1" style="width: 217px;margin:10px" >\r\n     <div class="center1">\u5bbd</div>\r\n     <el-input v-model="width1" placeholder="\u8bf7\u8f93\u5165\u5bbd\u5ea6" ></el-input>\r\n </div>\r\n    <div class="center1" style="margin:10px">\r\n        <el-button type="success" icon="el-icon-check" circle v-on:click="edit1"></el-button>\r\n        <el-button type="danger" icon="el-icon-delete" circle v-on:click="dddd"></el-button>\r\n    </div>\r\n</div>\r\n</div>\r\n</body>\r\n\r\n\r\n\r\n<script>\r\nvar vm = new Vue({\r\n    el:\'#app\',\r\n    data:{\r\n        restaurants: [],\r\n        state3: \'\',\r\n        sites:[],\r\n        contents:\'\',\r\n        height1:\'\',\r\n        width1:\'\',\r\n        unit_name:\'\',\r\n        font_size:\'\',\r\n        unit_id:0,\r\n        message1:\'\',\r\n    },\r\n    methods: {\r\n      querySearch(queryString, cb) {\r\n        var restaurants = this.restaurants;\r\n        var results = queryString ? restaurants.filter(this.createFilter(queryString)) : restaurants;\r\n        // \u8c03\u7528 callback \u8fd4\u56de\u5efa\u8bae\u5217\u8868\u7684\u6570\u636e\r\n        cb(results);\r\n\r\n      },\r\n      createFilter(queryString) {\r\n        return (restaurant) => {\r\n          return (restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);\r\n        };\r\n      },\r\n      loadAll() {\r\n        return [\r\n          { "value": \'8\'},\r\n          { "value": \'10\'},\r\n          { "value": \'12\'},\r\n          { "value": \'14\'},\r\n          { "value": \'16\'},\r\n          { "value": \'18\'},\r\n          { "value": \'20\'},\r\n        ];\r\n      },\r\n      handleSelect(item) {\r\n        this.font_size = item.value;\r\n      },\r\n      handleIconClick(ev) {\r\n      },\r\n      edit2(row) {\r\n          this.$confirm(\'\u6b64\u64cd\u4f5c\u5c06\u6c38\u4e45\u5220\u9664\u8be5\u6587\u4ef6, \u662f\u5426\u7ee7\u7eed?\', \'\u63d0\u793a\', {\r\n              confirmButtonText: \'\u786e\u5b9a\',\r\n              cancelButtonText: \'\u53d6\u6d88\',\r\n              type: \'warning\',\r\n              center: true\r\n          }).then(() => {\r\n              this.$message({\r\n                      type: \'success\',\r\n                      message: \'\u5220\u9664\u6210\u529f!\',\r\n                  },\r\n                  axios({\r\n                      method:\'post\',\r\n                      url:\'')
        __M_writer(unicode(SITE_URL))
        __M_writer(u"test3/',\r\n                      data:{\r\n                        unit_id:row\r\n                      }\r\n              }).then((res)=>{\r\n                  vm.a();\r\n          }),);\r\n          }).catch(() => {\r\n              this.$message({\r\n                  type: 'info',\r\n                  message: '\u5df2\u53d6\u6d88\u5220\u9664'\r\n              });\r\n          });\r\n      },\r\n      a() {\r\n        axios({\r\n            method: 'post',\r\n            url: '")
        __M_writer(unicode(SITE_URL))
        __M_writer(u"test/',\r\n        }).then((res) => {\r\n            vm.sites = res.data.message;\r\n\r\n        })\r\n    },\r\n      aaa() {\r\n        axios({\r\n            method: 'post',\r\n            url: '")
        __M_writer(unicode(SITE_URL))
        __M_writer(u'test1/\',\r\n            data: this.contents,\r\n        }).then((res)=>{\r\n            vm.sites = res.data.message;\r\n\r\n        })\r\n    },\r\n      edit(row){\r\n        var $div = $("#div3");\r\n        $div.toggle(500);\r\n        vm.unit_id = row;\r\n      },\r\n      edit1() {\r\n          axios({\r\n              method:\'post\',\r\n              url:\'')
        __M_writer(unicode(SITE_URL))
        __M_writer(u"test2/',\r\n              data:{\r\n                  height:this.height1,\r\n                  width:this.width1,\r\n                  unit_name:this.unit_name,\r\n                  unit_id:vm.unit_id,\r\n                  font_size:this.font_size,\r\n              }}).then((res)=>{\r\n                  vm.a();\r\n          })\r\n    },\r\n      dddd(){\r\n          vm.edit(0)\r\n      },\r\n      },\r\n    mounted() {\r\n      this.restaurants = this.loadAll();\r\n    },\r\n  });\r\nvm.a();\r\nvm.edit(0);\r\n</script>\r\n\r\n</html>")
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"32": 12, "33": 12, "34": 159, "35": 159, "36": 176, "37": 176, "38": 185, "39": 185, "40": 200, "41": 200, "47": 41, "16": 0, "23": 1, "24": 5, "25": 5, "26": 7, "27": 7, "28": 9, "29": 9, "30": 11, "31": 11}, "uri": "show_message.html", "filename": "E:/LanhuSaas/framework/templates/show_message.html"}
__M_END_METADATA
"""
