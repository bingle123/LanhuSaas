# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1544517252.446
_enable_loop = True
_template_filename = 'F:/Users/DeleMing/Desktop/Lanhu/framework/templates/common/select.html'
_template_uri = './common/select.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        APP_ID = context.get('APP_ID', UNDEFINED)
        STATIC_URL = context.get('STATIC_URL', UNDEFINED)
        SITE_URL = context.get('SITE_URL', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'<!DOCTYPE html>\r\n<html lang="en">\r\n<head>\r\n    <meta charset="UTF-8">\r\n    <title>Title</title>\r\n    <!-- Bootstrap css -->\r\n    <link href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'assets/bootstrap-3.3.4/css/bootstrap.css" rel="stylesheet">\r\n    <!--\u84dd\u9cb8\u5e73\u53f0APP \u516c\u7528\u7684\u6837\u5f0f\u6587\u4ef6 -->\r\n    <link href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'css/dataTables.bootstrap.css" rel="stylesheet">\r\n    <link href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'css/jquery-ui.min.css" rel="stylesheet">\r\n    <link href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'css/theme.css" rel="stylesheet">\r\n    <link href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'css/bk_base.css" rel="stylesheet">\r\n    <link href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'css/bk_app_theme.css" rel="stylesheet">\r\n    <link href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'css/ijobs.css" rel="stylesheet">\r\n    <!--JQuery-->\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'js/jquery-1.10.2.min.js"></script>\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'js/jquery-3.1.1.min.js"></script>\r\n    <!--\u5206\u9875CSS\u548cJS-->\r\n    <script src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'js/pageNav.js"></script>\r\n    <link href="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'css/pageNav.css" rel="stylesheet">\r\n    <!-- \u8fd9\u4e2a\u662f\u5168\u5c40\u914d\u7f6e\uff0c\u5982\u679c\u9700\u8981\u5728js\u4e2d\u4f7f\u7528app_id\u548csite_url,\u5219\u8fd9\u4e2ajavascript\u7247\u6bb5\u4e00\u5b9a\u8981\u4fdd\u7559 -->\r\n    <script type="text/javascript">\r\n          var app_id = "')
        __M_writer(unicode(APP_ID))
        __M_writer(u'";\r\n          var site_url = "')
        __M_writer(unicode(SITE_URL))
        __M_writer(u'";\t        // app\u7684url\u524d\u7f00,\u5728ajax\u8c03\u7528\u7684\u65f6\u5019\uff0c\u5e94\u8be5\u52a0\u4e0a\u8be5\u524d\u7f00\r\n          var static_url = "')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'";     // \u9759\u6001\u8d44\u6e90\u524d\u7f00\r\n    </script>\r\n</head>\r\n<body style="background: white;">\r\n\r\n<!--\u670d\u52a1\u5668-->\r\n<div class="container">\r\n    <div class="row">\r\n        <!--\u9009\u62e9\u670d\u52a1\u5668-->\r\n        <div class="col-sm-4 p0 i18scriptLeft">\r\n            <button type="button" class="bk-button bk-primary showModel" data-placement="right" style="min-width: 115px">\r\n                <i class="glyphicon glyphicon-search"></i>&nbsp;\u9009\u62e9\u670d\u52a1\u5668\r\n            </button>\r\n        </div>\r\n        <!--\u9009\u62e9\u670d\u52a1\u5668-->\r\n\r\n        <!--\u9009\u4e2d\u670d\u52a1\u5668\u663e\u793a-->\r\n        <div class="col-sm-12">\r\n            <table class="table table-header-bg mt40 mb0 serverIpResultTable table-bordered table-hover none" style="font-size: 13px!important">\r\n                <thead>\r\n                <tr>\r\n                    <th style="width:180px;">\u5b50\u7f51\u540d\u79f0</th>\r\n                    <th>IP/\u5206\u7ec4</th>\r\n                    <th>\u72b6\u6001</th>\r\n                    <th class="table-header-option-th">\u6240\u6709\u64cd\u4f5c</th>\r\n                </tr>\r\n                </thead>\r\n                <tbody class="displaytbody">\r\n\r\n                </tbody>\r\n            </table>\r\n        </div>\r\n        <!--\u9009\u4e2d\u670d\u52a1\u5668\u663e\u793a-->\r\n    </div>\r\n</div>\r\n<!--\u670d\u52a1\u5668-->\r\n\r\n<!-- Modal \u5f39\u51fa\u7a97-->\r\n<div class="modal fade serverIpModal h1000 in ui-draggable" data-backdrop="false" data-keyboard="false" role="dialog" aria-hidden="false" style="display: none;">\r\n    <div class="modal-dialog w800" role="document">\r\n        <div class="modal-content">\r\n            <div class="modal-loading-wrap none" style="z-index: 9999;position: absolute;left:0;top:0;width:100%;height:100%;text-align:center;vertial-align:middle;">\r\n                <img src="')
        __M_writer(unicode(STATIC_URL))
        __M_writer(u'img/loading_2_36x36.gif" style="margin-left:-18px;position:absolute;top:50%;margin-top:-36px;">\r\n            </div>\r\n            <div class="modal-body" style="min-height:450px;">\r\n                <div class="nav nav-tabs serverIpListtabs w h40 pl20 text-left ui-draggable-handle">\r\n                    <label class="pr5 radio-inline changeIp" style="cursor: pointer;"><input type="radio" name="serverSelect" id="selectone" value="1" checked=""> \u901a\u8fc7IP\u9009\u62e9\u670d\u52a1\u5668</label>\r\n                    <label  class="pr5 radio-inline changeIp" style="cursor: pointer;"><input type="radio" name="serverSelect" id="selecttwo" value="2"> \u914d\u7f6e\u5e73\u53f0</label>\r\n                    <label class="pr5 radio-inline changeIp" style="cursor: pointer;"><input type="radio" name="serverSelect" id="selectthree" value="3"> \u624b\u52a8\u6dfb\u52a0</label>\r\n                    <label id="dynamicGroup" class="pr5 radio-inline changeIp" style="cursor: pointer;"><input type="radio" id="selectfour" name="serverSelect" value="4"> \u52a8\u6001\u5206\u7ec4</label>\r\n\r\n                </div>\r\n\r\n                <div class="tab-content" style="min-height:380px;position: relative;">\r\n                    <!-- start \u901a\u8fc7IP\u9009\u62e9\u670d\u52a1\u5668 -->\r\n                    <div class="ipList-tab-pane ipChoose-tab-pane w p10">\r\n                        <input type="search" class="form-control w filterText" placeholder="\u4e3b\u673a\u540d\u6309Enter\u8fdb\u884c\u8fc7\u6ee4...">\r\n                        <span class="glyphicon glyphicon-search form-control-feedback search-feedback" style="color: #3596e0;font-size: 16px;top: 10px;right: 10px;cursor:pointer;pointer-events:auto !important;"></span>\r\n                        <div id="DataTables_Table_0_wrapper" class="dataTables_wrapper form-inline dt-bootstrap no-footer">\r\n                            <div class="row"><div class="col-sm-6"></div><div class="col-sm-6"></div></div><div class="row"><div class="col-sm-12"><table class="table table-header-bg mt10 w serverIp-result-table-thead table-hover serverIpTable dataTable no-footer" style="margin-bottom: -1px; font-size: 13px !important; width: 748px;" id="DataTables_Table_0" role="grid" aria-describedby="DataTables_Table_0_info">\r\n                            <thead>\r\n                            <tr role="row"><th class="sorting_disabled" rowspan="1" colspan="1" style="width: 13px;"><input type="checkbox" class="selectedAllChecks" title="\u5f53\u524d\u9875"></th><th class="sorting_disabled" rowspan="1" colspan="1" style="width: 101px;">\u5b50\u7f51\u540d\u79f0</th><th class="sorting_disabled" rowspan="1" colspan="1" style="width: 198px;">\u64cd\u4f5c\u7cfb\u7edf</th><th class="sorting_disabled" rowspan="1" colspan="1" style="width: 97px;">IP</th><th class="sorting_disabled" rowspan="1" colspan="1" style="width: 80px;">\u72b6\u6001</th><th class="sorting_disabled" rowspan="1" colspan="1" style="width: 163px;">\u4e3b\u673a\u540d</th></tr>\r\n                            </thead>\r\n                            <tbody class="osbody">\r\n\r\n                            </tbody>\r\n                        </table>\r\n                        </div></div>\r\n                            <div class="row none">\r\n                                <div class="col-sm-5">\r\n                                    <div class="dataTables_info" id="DataTables_Table_0_info" role="status" aria-live="polite">\r\n                                        \u7b2c 1 \u9875 / \u5171 2 \u9875&nbsp;&nbsp;\u6bcf\u9875\u663e\u793a 7 \u6761&nbsp;&nbsp;\u5171 12 \u6761\r\n                                    </div>\r\n                                </div>\r\n                                <div class="col-sm-7">\r\n                                    <div class="dataTables_paginate paging_simple_numbers" id="DataTables_Table_0_paginate">\r\n                                        <ul class="pagination">\r\n                                            <li class="paginate_button previous disabled" id="DataTables_Table_0_previous">\r\n                                                <a href="http://job.blueking.com:8030/?fastExecuteScript&amp;appId=2#" aria-controls="DataTables_Table_0" data-dt-idx="0" tabindex="0">&lt;&lt;</a>\r\n                                            </li>\r\n                                            <li class="paginate_button active">\r\n                                                <a href="http://job.blueking.com:8030/?fastExecuteScript&amp;appId=2#" aria-controls="DataTables_Table_0" data-dt-idx="1" tabindex="0">1</a>\r\n                                            </li>\r\n                                            <li class="paginate_button ">\r\n                                                <a href="http://job.blueking.com:8030/?fastExecuteScript&amp;appId=2#" aria-controls="DataTables_Table_0" data-dt-idx="2" tabindex="0">2</a>\r\n                                            </li>\r\n                                            <li class="paginate_button next" id="DataTables_Table_0_next"><a href="http://job.blueking.com:8030/?fastExecuteScript&amp;appId=2#" aria-controls="DataTables_Table_0" data-dt-idx="3" tabindex="0">&gt;&gt;</a>\r\n                                            </li>\r\n                                        </ul>\r\n                                    </div>\r\n                                </div>\r\n                            </div>\r\n                            <div class="row">\r\n                                <div class="col-sm-5">\r\n                                    <div class="dataTables_info" id="DataTables_Table_0_info" role="status" aria-live="polite">\r\n                                        \u7b2c 1 \u9875 / \u5171 2 \u9875&nbsp;&nbsp;\u6bcf\u9875\u663e\u793a 7 \u6761&nbsp;&nbsp;\u5171 12 \u6761\r\n                                    </div>\r\n                                </div>\r\n                                <div aria-label="Page navigation" class="page-nav-outer" id="PageNavId"></div>\r\n                            </div>\r\n                        </div>\r\n                    </div>\r\n                    <!-- end \u901a\u8fc7IP\u9009\u62e9\u670d\u52a1\u5668 -->\r\n\r\n                    <!-- start \u914d\u7f6e\u5e73\u53f0 -->\r\n                    <div class="ipList-tab-pane configCenter-tab-pane none w p10">\r\n                        <div style="height: 384px; overflow: auto;text-align: left;" class="treeviewDiv">\r\n                            <div class="treeviewByAjax"></div>\r\n                        </div>\r\n                    </div>\r\n                    <!-- end \u914d\u7f6e\u5e73\u53f0 -->\r\n\r\n                    <!-- start \u624b\u52a8\u6dfb\u52a0 -->\r\n                    <div class="ipList-tab-pane manually-tab-pane none w p10">\r\n                        <!-- <textarea class="form-control server-ip-textarea" rows="3" placeholder="\u8bf7\u8f93\u5165IP\uff0c\u4ee5\u201c\u7a7a\u683c\u201d\u6216\u8005\u201c\u56de\u8f66\u201d\u6216\u8005\u201c;\u201d\u5206\u9694"  style="height: 375px"></textarea> -->\r\n                        <div>\r\n                            <label class="control-label">\u5b50\u7f51\u540d\u79f0\uff1a</label>\r\n                            <div class="ijobs-input plat-name-box" style="width:550px;">\r\n\r\n                            </div>\r\n                            <div class="plat-area-box">\r\n\r\n                            </div>\r\n                        </div>\r\n\r\n\r\n                    </div>\r\n                    <!-- end \u624b\u52a8\u6dfb\u52a0 -->\r\n\r\n                    <!-- start \u670d\u52a1\u5668\u96c6 -->\r\n                    <div class="ipList-tab-pane group-tab-pane none w p10">\r\n                        <input type="text" class="form-control w groupfilterText" placeholder="\u901a\u8fc7\u540d\u79f0\u63cf\u8ff0\u8fdb\u884c\u8fc7\u6ee4...">\r\n                        <table class="table table-header-bg mt10 w serverIp-result-table-thead table-hover groupTable" style="margin-bottom: -1px;font-size: 13px">\r\n                            <thead>\r\n                            <tr>\r\n                                <th style="width: 5%">&nbsp;</th>\r\n                                <th style="width: 60%">\u4e1a\u52a1\u540d\u79f0</th>\r\n                                <th style="width: 35%">\u5206\u7ec4\u540d\u79f0</th>\r\n                            </tr>\r\n                            </thead>\r\n                        </table>\r\n                    </div>\r\n                    <!-- end \u670d\u52a1\u5668\u96c6 -->\r\n\r\n                    <!-- start cc\u811a\u672c -->\r\n                    <div class="ipList-tab-pane cc-tab-pane none w p10 tl">\r\n                        <div class="row mb10">\r\n                            <label class="col-sm-2 control-label">CC\u811a\u672c\u5bfc\u5165<span class="red">&nbsp;*</span>\uff1a</label>\r\n                            <div class="col-sm-10">\r\n                                <select class="form-control w cc-name"></select>\r\n                            </div>\r\n                        </div>\r\n\r\n                        <div class="row mb10">\r\n                            <label class="col-sm-2 control-label">\u5165\u53e3\u53c2\u6570\uff1a</label>\r\n                            <div class="col-sm-10">\r\n                                <input class="form-control cc-param" style="float:left;max-width:531px;margin-right:5px;" maxlength="25" placeholder="\u8bf7\u8f93\u5165\u6d4b\u8bd5\u7528\u7684\u811a\u672c\u53c2\u6570\uff0c\u65e0\u5219\u4e0d\u586b">\r\n                                <a href="javascript:void(0)" class="btn btn-success cc-test-btn">\u83b7\u53d6\u7ed3\u679c</a>\r\n                            </div>\r\n                        </div>\r\n\r\n                        <div class="row mb10">\r\n                            <label class="col-sm-2 control-label">\u6d4b\u8bd5\u7ed3\u679c\uff1a</label>\r\n                            <div class="col-sm-10">\r\n                                <textarea class="form-control w cc-test-rs" placeholder="\u8bf7\u70b9\u51fb&#39;\u6d4b\u8bd5\u7ed3\u679c\uff1a&#39;\u6309\u94ae\u8fdb\u884c\u6d4b\u8bd5" style="resize: none;height:300px;"></textarea>\r\n                                <span style="color:red">\u8bf7\u786e\u4fddCC\u811a\u672c\u83b7\u53d6\u7ed3\u679c\u4e2d\u7b2c\u4e00\u884c\u4e00\u5b9a\u8981\u5305\u542bInnerIP\u6216OuterIP\u5b57\u6bb5\uff0c\u5982\u679c\u6ca1\u6709\uff0c\u5219\u5728\u4f5c\u4e1a\u4e2d\u4f7f\u7528\u6b64CC\u811a\u672c\u65f6\u4f1a\u5bfc\u81f4\u5bfc\u5165IP\u5217\u8868\u4e3a\u7a7a</span>\r\n                                <span class="cc-ip-count"></span>\r\n                            </div>\r\n                        </div>\r\n                    </div>\r\n                    <!-- end cc\u811a\u672c -->\r\n\r\n                </div>\r\n            </div>\r\n            <div class="modal-footer">\r\n                <label class="pr10 radio-inline fl"><input type="checkbox" class="selectAll"> \u5168\u9009</label>\r\n                <button type="button" class="bk-button bk-default fl copyIPByPage" data-clipboard-target="">\u590d\u5236\u5df2\u9009IP</button>\r\n                <button type="button" class="bk-button bk-default fl copyAllPageIP" style="margin-left:5px;">\u590d\u5236\u5168\u90e8IP</button>\r\n                <button type="button" class="bk-button btn-primary savebtn" style="min-width:60px;">\u6dfb\u52a0</button>\r\n                <button type="button" class="bk-button bk-default cancelbtn" style="min-width:60px;">\u53d6\u6d88</button>\r\n            </div>\r\n        </div>\r\n    </div>\r\n</div>\r\n<!-- Modal \u5f39\u51fa\u7a97-->\r\n\r\n<!--\u8868\u683c\u6a21\u677f-->\r\n\r\n<template id="tpl">\r\n    <tr role="row" class="odd">\r\n        <td class="1"><input value="#bk_host_innerip#" type="checkbox" class="userChecks select_all_flag"></td>\r\n        <td class="2"><span class="select_all_flag ">#bk_inst_name#</span></td>\r\n        <td class="3"><span title="linux redhat" class="select_all_flag">#bk_os_name#</span></td>\r\n        <td class="4"><span title="192.168.1.201" class="select_all_flag">#bk_host_innerip#</span></td>\r\n        <td class="5"><span class="text-success select_all_flag ">#bk_agent_alive#</span></td>\r\n        <td class="6"><span class="select_all_flag " title="paas-1" >#bk_host_name#</span></td>\r\n    </tr>\r\n</template>\r\n<!--\u8868\u683c\u6a21\u677f-->\r\n\r\n<!--\u70b9\u51fb\u4e8b\u4ef6\u811a\u672c-->\r\n<script>\r\n    //\u524d\u540e\u7aef\u6570\u636e\u4ea4\u4e92\u901a\u7528\u65b9\u6cd5\r\n    function renderTpl(str, cfg) {\r\n        var re = /(#(.+?)#)/g;\r\n\r\n        return str.replace(re, function() {\r\n            var val = cfg[arguments[2]]+\'\';\r\n            if(typeof val == \'undefined\') {\r\n                val = \'\';\r\n            }\r\n            return val;\r\n        });\r\n    };\r\n\r\n    //\u8868\u683c\u5220\u9664\u6570\u636e\r\n    function deltable(obj){\r\n        var res = confirm(\'\u786e\u8ba4\u8981\u5220\u9664\u5417\uff1f\');\r\n        if(res == true)\r\n        {\r\n            $(obj).parents("tr").remove();\r\n        }\r\n    }\r\n\r\n    //\u9875\u9762\u52a0\u8f7d\r\n    $(document).ready(function () {\r\n        $.ajax({\r\n            url: \'')
        __M_writer(unicode(SITE_URL))
        __M_writer(u'test/\',\r\n            type: \'GET\',\r\n            dataType:  \'json\',\r\n            success:function (res) {\r\n                //\u83b7\u53d6\u6570\u636e\u6210\u529f\r\n                if (res.code == 0){\r\n                    var _html = \'\';\r\n                    var list = res.results;\r\n                    var tpl = $(\'#tpl\').html();\r\n                    //alert(tpl)\r\n                    //alert(list.length)\r\n                    if (list.length == 0){\r\n                        alert(\'\u6ca1\u6709\u6570\u636e\');\r\n                    }else {\r\n                        for (var i = 0,len = list.length;i < len;i++){\r\n                            var item = list[i];\r\n                            _html += renderTpl(tpl,item)\r\n                            //alert(item)\r\n                        }\r\n                    }\r\n                    $(\'.serverIpTable tbody\').html(_html);\r\n                }\r\n            }\r\n        });\r\n\r\n    });\r\n\r\n    //\u65b0\u589e\u670d\u52a1\u5668\uff0c\u6253\u5f00\u7a97\u53e3\r\n    $(\'.showModel\').click(function () {\r\n        $(\'.ui-draggable\').css(\'display\', \'block\');\r\n        $(\'.modal-loading-wrap\').removeClass("none");\r\n        $.ajax({\r\n            url: \'')
        __M_writer(unicode(SITE_URL))
        __M_writer(u'test/\',\r\n            type: \'GET\',\r\n            dataType:  \'json\',\r\n            success:function (res) {\r\n                //\u83b7\u53d6\u6570\u636e\u6210\u529f\r\n                if (res.code == 0){\r\n                    var _html = \'\';\r\n                    var list = res.results;\r\n                    var tpl = $(\'#tpl\').html();\r\n                    //alert(tpl)\r\n                    //alert(list.length)\r\n                    if (list.length == 0){\r\n                        alert(\'\u6ca1\u6709\u6570\u636e\');\r\n                    }else {\r\n                        for (var i = 0,len = list.length;i < len;i++){\r\n                            var item = list[i];\r\n                            _html += renderTpl(tpl,item)\r\n                            //alert(item)\r\n                        }\r\n                    }\r\n                    $(\'.serverIpTable tbody\').html(_html);\r\n                    $(\'.modal-loading-wrap\').addClass("none");\r\n                }\r\n            }\r\n        });\r\n    });\r\n\r\n    //\u65b0\u589e\u670d\u52a1\u5668\u53d6\u6d88\u7a97\u53e3\r\n    $(\'.cancelbtn\').click(function () {\r\n        $(\'.modal-loading-wrap\').removeClass("none");\r\n        $.ajax({\r\n            url: \'')
        __M_writer(unicode(SITE_URL))
        __M_writer(u'test/\',\r\n            type: \'GET\',\r\n            dataType:  \'json\',\r\n            success:function (res) {\r\n                //\u83b7\u53d6\u6570\u636e\u6210\u529f\r\n                if (res.code == 0){\r\n                    var _html = \'\';\r\n                    var list = res.results;\r\n                    var tpl = $(\'#tpl\').html();\r\n                    //alert(tpl)\r\n                    //alert(list.length)\r\n                    if (list.length == 0){\r\n                        alert(\'\u6ca1\u6709\u6570\u636e\');\r\n                    }else {\r\n                        for (var i = 0,len = list.length;i < len;i++){\r\n                            var item = list[i];\r\n                            _html += renderTpl(tpl,item)\r\n                            //alert(item)\r\n                        }\r\n                    }\r\n                    $(\'.serverIpTable tbody\').html(_html);\r\n                    $(\'.modal-loading-wrap\').addClass("none");\r\n                }\r\n            }\r\n        });\r\n        $(\'.ui-draggable\').css(\'display\', \'none\');\r\n    });\r\n\r\n    //\u6253\u5f00\u914d\u7f6e\u5e73\u53f0\r\n    $(\'#selecttwo\').click(function () {\r\n        $(\'.ipChoose-tab-pane\').addClass("none");           //\u5173\u95ed\u901a\u8fc7IP\u7b5b\u9009\u670d\u52a1\u5668\r\n        $(\'.configCenter-tab-pane\').addClass("none");       //\u5173\u95ed\u901a\u8fc7\u914d\u7f6e\u5e73\u53f0\u7b5b\u9009\u670d\u52a1\u5668\r\n        $(\'.manually-tab-pane\').addClass("none");           //\u5173\u95ed\u901a\u8fc7\u624b\u52a8\u6dfb\u52a0\r\n        $(\'.group-tab-pane\').addClass("none");              //\u5173\u95ed\u52a8\u6001\u5206\u7ec4\r\n        $(\'.configCenter-tab-pane\').removeClass("none");    //\u6253\u5f00\u914d\u7f6e\u5e73\u53f0\r\n    });\r\n\r\n    //\u901a\u8fc7IP\u7b5b\u9009\u670d\u52a1\u5668\r\n    $(\'#selectone\').click(function () {\r\n        $(\'.ipChoose-tab-pane\').addClass("none");           //\u5173\u95ed\u901a\u8fc7IP\u7b5b\u9009\u670d\u52a1\u5668\r\n        $(\'.configCenter-tab-pane\').addClass("none");       //\u5173\u95ed\u901a\u8fc7\u914d\u7f6e\u5e73\u53f0\u7b5b\u9009\u670d\u52a1\u5668\r\n        $(\'.manually-tab-pane\').addClass("none");           //\u5173\u95ed\u901a\u8fc7\u624b\u52a8\u6dfb\u52a0\r\n        $(\'.group-tab-pane\').addClass("none");              //\u5173\u95ed\u52a8\u6001\u5206\u7ec4\r\n        $(\'.ipChoose-tab-pane\').removeClass("none");        //\u6253\u5f00\u914d\u7f6e\u5e73\u53f0\r\n    });\r\n\r\n    //\u901a\u8fc7\u624b\u52a8\u6dfb\u52a0\r\n    $(\'#selectthree\').click(function () {\r\n        $(\'.ipChoose-tab-pane\').addClass("none");           //\u5173\u95ed\u901a\u8fc7IP\u7b5b\u9009\u670d\u52a1\u5668\r\n        $(\'.configCenter-tab-pane\').addClass("none");       //\u5173\u95ed\u901a\u8fc7\u914d\u7f6e\u5e73\u53f0\u7b5b\u9009\u670d\u52a1\u5668\r\n        $(\'.manually-tab-pane\').addClass("none");           //\u5173\u95ed\u901a\u8fc7\u624b\u52a8\u6dfb\u52a0\r\n        $(\'.group-tab-pane\').addClass("none");              //\u5173\u95ed\u52a8\u6001\u5206\u7ec4\r\n        $(\'.manually-tab-pane\').removeClass("none");        //\u6253\u5f00\u914d\u7f6e\u5e73\u53f0\r\n    });\r\n\r\n    //\u901a\u8fc7IP\u5206\u7ec4\u7b5b\u9009\u670d\u52a1\u5668\r\n    $(\'#selectfour\').click(function () {\r\n        $(\'.ipChoose-tab-pane\').addClass("none");           //\u5173\u95ed\u901a\u8fc7IP\u7b5b\u9009\u670d\u52a1\u5668\r\n        $(\'.configCenter-tab-pane\').addClass("none");       //\u5173\u95ed\u901a\u8fc7\u914d\u7f6e\u5e73\u53f0\u7b5b\u9009\u670d\u52a1\u5668\r\n        $(\'.manually-tab-pane\').addClass("none");           //\u5173\u95ed\u901a\u8fc7\u624b\u52a8\u6dfb\u52a0\r\n        $(\'.group-tab-pane\').addClass("none");              //\u5173\u95ed\u52a8\u6001\u5206\u7ec4\r\n        $(\'.group-tab-pane\').removeClass("none");        //\u6253\u5f00\u914d\u7f6e\u5e73\u53f0\r\n    });\r\n    //\u5168\u9009\u4e0e\u4e0d\u5168\u9009\r\n    $(\'.selectAll\').click(function () {\r\n        if($(this).is(":checked")){\r\n            $(\'.select_all_flag\').prop("checked",true);\r\n        }else {\r\n            $(\'.select_all_flag\').prop("checked", false);\r\n        }\r\n    });\r\n\r\n    //\u663e\u793a\u767b\u8bb0\u8d26\u6237\r\n    $(\'#addUserBut\').click(function () {\r\n        var display = $(\'#regUserDiv\').css(\'display\');  //\u83b7\u53d6\u662f\u5426\u9690\u85cf\r\n        if(display == "none"){\r\n            $(\'#regUserDiv\').css(\'display\', \'block\');$(\'#DataTables_Table_0_wrapper\').css(\'display\',\'block\');\r\n        }else{\r\n            $(\'#regUserDiv\').css(\'display\', \'none\');\r\n        }\r\n    });\r\n\r\n    //\u70b9\u51fb\u4fdd\u5b58\u6309\u94ae\uff0c\u7279\u6548\u548c\u6570\u636e\u8f6c\u79fb\r\n    $(\'.savebtn\').click(function () {\r\n        $(\'.serverIpResultTable\').removeClass("none");\r\n        $(\'.serverIpMode-1\').children("div").removeClass("none");\r\n        $(\'.btnGroup\').removeClass("none");\r\n        $(\'.server-text\').removeClass("none");                      //\u79fb\u9664\u9690\u85cf\u6837\u5f0f\r\n        var ischecked = $(\'.serverIpTable tbody input:checked:checked\');\r\n        for (var i = 0 ;i < ischecked.length;i++){\r\n            var ischeckedflag = ischecked.eq(i).parents("tr");\r\n            var _htmlUrl = "<td>"+"<a class=\'select_all_flag\' href="+"\'javascript:;\'"+" onclick"+"="+"deltable(this)"+">\u5220\u9664</a>"+"</td>";\r\n            ischeckedflag.append(_htmlUrl);\r\n            $(\'.displaytbody\').append(ischeckedflag);\r\n            $(\'.displaytbody .1\').remove();\r\n            $(\'.displaytbody .2\').remove();\r\n            $(\'.displaytbody .6\').remove();\r\n        }\r\n        $(\'.ui-draggable\').css(\'display\', \'none\');\r\n    });\r\n\r\n</script>\r\n\r\n<script type="text/javascript">\r\n    var pageNavObj = null;//\u7528\u4e8e\u50a8\u5b58\u5206\u9875\u5bf9\u8c61\r\n    var pageCount = 30;\r\n    var perPageNum = 3;\r\n    pageNavObj = new PageNavCreate("PageNavId",{\r\n         pageCount:pageCount,\r\n         currentPage:1,\r\n         perPageNum:perPageNum,\r\n    });\r\n    pageNavObj.afterClick(pageNavCallBack);\r\n    function pageNavCallBack(clickPage){\r\n        pageNavObj = new PageNavCreate("PageNavId",{\r\n             pageCount:pageCount,\r\n             currentPage:clickPage,\r\n             perPageNum:perPageNum,\r\n        });\r\n        $(\'.modal-loading-wrap\').removeClass("none");\r\n        $.ajax({\r\n            url:"')
        __M_writer(unicode(SITE_URL))
        __M_writer(u'test/?pageCount="+pageCount+"&clickPage="+clickPage,     ///?pageCount="+pageCount+"&perPageNum"+perPageNum\r\n            type:"GET",\r\n            dataType: "json",\r\n            success:function (res) {\r\n                //\u83b7\u53d6\u6570\u636e\u6210\u529f\r\n\r\n                if (res.code == 0){\r\n                    var _html = \'\';\r\n                    var list = res.results;\r\n                    var tpl = $(\'#tpl\').html();\r\n                    //alert(tpl)\r\n                    //alert(list.length)\r\n                    if (list.length == 0){\r\n                        alert(\'\u6ca1\u6709\u6570\u636e\');\r\n                    }else {\r\n                        for (var i = 0,len = list.length;i < len;i++){\r\n                            var item = list[i];\r\n                            _html += renderTpl(tpl,item)\r\n                            //alert(item)\r\n                        }\r\n                    }\r\n                    $(\'.serverIpTable tbody\').html(_html);\r\n                }\r\n                $(\'.modal-loading-wrap\').addClass("none");\r\n            }\r\n        });\r\n        pageNavObj.afterClick(pageNavCallBack);\r\n    }\r\n</script>\r\n\r\n</body>\r\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"16": 0, "24": 1, "25": 7, "26": 7, "27": 9, "28": 9, "29": 10, "30": 10, "31": 11, "32": 11, "33": 12, "34": 12, "35": 13, "36": 13, "37": 14, "38": 14, "39": 16, "40": 16, "41": 17, "42": 17, "43": 19, "44": 19, "45": 20, "46": 20, "47": 23, "48": 23, "49": 24, "50": 24, "51": 25, "52": 25, "53": 67, "54": 67, "55": 252, "56": 252, "57": 284, "58": 284, "59": 315, "60": 315, "61": 436, "62": 436, "68": 62}, "uri": "./common/select.html", "filename": "F:/Users/DeleMing/Desktop/Lanhu/framework/templates/common/select.html"}
__M_END_METADATA
"""