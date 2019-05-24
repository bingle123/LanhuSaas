var vm = null;
var site_url = "";
//csrf验证
axios.interceptors.request.use((config) => {
    config.headers['X-Requested-With'] = 'XMLHttpRequest';
    let regex = /.*csrftoken=([^;.]*).*$/; // 用于从cookie中匹配 csrftoken值
    config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
    return config
});
$(function(){
    site_url = $('#siteUrl').val();
    //自定义校验规则
    //基本监控项高度大小范围校验
    const height_range_check = (rule, value, callback) => {
        var reg = /^[0-9]*$/;
        if (!reg.test(value)) {
            return callback(new Error('高度值必须是一个数字'));
        }
        var height = parseInt(value);
        if (0 > height || 480 < height) {
            return callback(new Error('高度值范围在0-480'));
        }
        return callback();
    };

    const width_range_check = (rule, value, callback) => {
        var reg = /^[0-9]*$/;
        if (!reg.test(value)) {
            return callback(new Error('宽度值必须是一个数字'));
        }
        var height = parseInt(value);
        if (0 > height || 422 < height) {
            return callback(new Error('宽度值范围在0-422'));
        }
        return callback();
    };

    vm = new Vue({
        el: '#app',
        data: {
            //预览加载变量
            preview_loading: false,
            //基本监控项（修改后）显示内容缓存，显示所有指标
            base_monitor_show_cache: '',
            //颜色采集规则注释
            color_rules_comments: false,
            //其他采集规则注释
            other_rules_comments: false,
            //基本监控项（修改后）添加的情况下是否为第一次加载数据的标记
            base_monitor_add_init: true,
            //基本监控项（修改后）编辑的情况下是否为第一次加载数据标记
            base_monitor_edit_init: true,
            //基本监控项（修改后）添加后是否为第一次采集测试的标记
            base_monitor_add_test_init: true,
            //基本监控项（修改后）修改后是否为第一次采集测试的标记
            base_monitor_edit_test_init: true,
            //基本监控项上传数据
            base_monitor_upload_data: {},
            //采集测试数据缓存变量
            gather_test_data: null,
            //采集测试数据标记位，默认为null，采集数据成功置true，采集失败置false
            gather_data_test_flag: null,
            database_show: true,
            file_show: false,
            interface_show: false,
            loading: false,
            message: '',                                           //弹框提示信息
            constants: '',
            unit_id1: 0,
            location: '',
            line: '',
            old_html: '',
            msg1: '',
            sql_id: '',
            template_list: {
                name: '',
                id: ''
            },
            add_pamas: 0,                                        //新增编辑判断
            font_size_range: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40],   //字体大小
            job2: [],                                   //作业模板
            flow2: [],                                  //流程模板
            activities_node_name: [],                    //节点名称
            activities_node_time: {                      //节点时间
                start_time: '',                      //开始时间
                end_time: '',                        //结束时间
            },
            page_count: 100,                            //总页码数
            page: 1,                                    //分页页码数
            sites: [],                                  //table内容
            sites1: [],
            contents: '',                               //搜索输入框内容
            checked1: false,                           //作业启动选框
            checked2: false,                           //流程启动选框
            disabled1: false,
            disabled2: false,                            //基本单元
            //disabled3: false,                            //图表单元
            //disabled4: false,                            //作业单元
            //disabled5: false,                            //流程单元
            disabled6: false,
            isShow:false,
            areas: [],
            area: 1,
            caiji1: 'block',
            caiji2: 'none',
            monitor_name: '',                             //单元名称
            unit_id: 0,                                   //单元id
            centerDialogVisible: false,                  //弹窗状态
            sql1: 'block',
            file1: 'none',
            interface1: 'none',
            sql_file_interface: 3,
            server_url: '',
            file_param: '',
            param1: '',
            param2: '',
            zuoye: 'none',
            liucheng: 'none',
            basic_show_content: "",
            fields: [],                                  //字段选择数组
            result_data: {},                            //传递新增数据
            monitor_type: 'first',                     //单元类型
            basic: {                                   //基本单元
                monitor_name: '',                      //单元名称
                monitor_type: '',                      //单元类型
                font_size: '20',                         //字号
                height: '20',                            //高度
                width: '0',                             //宽度
                start_time: '',                        //开始时间
                end_time: '',                          //结束时间
                period: '10',                            //采集周期
                params: '',                            //监控参数
                status: '',                            //监控状态
                contents: '',                          //显示内容
                gather_rule: '',                       //采集规则
                gather_params: 'sql',                  //采集参数
                monitor_area: '',                             //日历地区
                score: '1',                                //分值
            },
            base: {
                //基本单元
                dimension_data: [],//维度名称
                measures_name: '',//指标名称
                measures: '',       //指标集
                interface_type: '',//接口类型
                show_rule_type: '',//展示规则
                monitor_name: '',                      //单元名称
                monitor_type: '',                      //单元类型
                font_size: '20',                         //字号
                height: '480',                            //高度
                width: '422',                             //宽度
                start_time: '',                        //开始时间
                end_time: '',                          //结束时间
                period: '10',                            //采集周期
                params: '',                            //监控参数
                status: '',                            //监控状态
                contents: '',                          //显示内容
                gather_rule: '',                       //采集规则
                gather_params: 'sql',                  //采集参数
                monitor_area: '',                             //日历地区
                score: ''                                //分值
            },             //基本单元
            rules1: {
                font_size: [
                    {required: true, message: '请选择字号', trigger: 'change'}
                ],
                height: [
                    {required: true, message: '请输入高度', trigger: 'blur'}
                ],
                width: [
                    {required: true, message: '请输入宽度', trigger: 'blur'}
                ],
                contents: [
                    {required: true, message: '请输入内容', trigger: 'blur'}
                ],
                period: [
                    {required: true, message: '请输入采集周期(以秒为单位)', trigger: 'blur'}
                ],
                score: [
                    {required: true, message: '请输入分值', trigger: 'blur'}
                ]
            },                              //校验规则
            chart: {                                //图表单元
                monitor_name: '',                    //单元名称
                monitor_type: '',                    //单元类型
                font_size: '20',                       //字号
                height: '380',                          //高度
                width: '580',                            //宽度
                start_time: '',                      //开始时间
                end_time: '',                        //结束时间
                period: '10',                          //采集周期
                status: '',                          //监控状态
                contents: '',                        //显示内容
                gather_rule: '',                     //采集规则
                gather_params: '',                   //节点
                params: '',                         //监控参数
                monitor_area: ''                             //日历地区
            },             //图表单元
            rules2: {
                font_size: [
                    {required: true, message: '请选择字号', trigger: 'change'}
                ],
                height: [
                    {required: true, message: '请输入高度', trigger: 'blur'}
                ],
                width: [
                    {required: true, message: '请输入宽度', trigger: 'blur'}
                ],
                contents: [
                    {required: true, message: '请输入内容', trigger: 'blur'}
                ],
                gather_params: [
                    {required: true, message: '请选择图片类型', trigger: 'change'}
                ],
                period: [
                    {required: true, message: '请输入采集周期(以秒为单位)', trigger: 'blur'}
                ],
            },                              //校验规则
            job: {                                   //作业单元
                monitor_name: '',                    //单元名称
                monitor_type: '',                    //单元类型
                font_size: '20',                       //字号
                height: '120',                          //高度
                width: '200',                            //宽度
                start_time: '',                      //开始时间
                end_time: '',                        //结束时间
                period: '10',                          //采集周期
                status: '',                          //监控状态
                contents: '',                        //显示内容
                gather_rule: '',                     //NODE_KEY
                gather_params: '',                   //作业模板
                params: '',                         //执行服务器
                monitor_area: ''                             //日历地区
            },                //作业单元
            rules3: {
                font_size: [
                    {required: true, message: '请选择字号', trigger: 'change'}
                ],
                height: [
                    {required: true, message: '请输入高度', trigger: 'blur'}
                ],
                width: [
                    {required: true, message: '请输入宽度', trigger: 'blur'}
                ],
                contents: [
                    {required: true, message: '请输入内容', trigger: 'blur'}
                ],
                gather_params: [
                    {required: true, message: '请选择作业模板', trigger: 'change'}
                ],
                period: [
                    {required: true, message: '请输入采集周期(以秒为单位)', trigger: 'blur'}
                ],
            },                              //校验规则
            flow: {                                     //流程单元
                monitor_name: '',                    //单元名称
                monitor_type: '',                    //单元类型
                font_size: '20',                       //字号
                height: '20',                          //高度
                width: '0',                            //宽度
                start_time: '',                      //开始时间
                end_time: '',                        //结束时间
                period: '10',                          //采集周期
                params: '',                         //监控参数
                status: '',                          //监控状态
                contents: '',                        //显示内容
                gather_rule: '',                     //采集规则
                gather_params: '',                   //流程模板
                node_name: '',
                monitor_area: ''                             //日历地区
            },              //流程单元
            rules4: {
                font_size: [
                    {required: true, message: '请选择字号', trigger: 'change'}
                ],
                height: [
                    {required: true, message: '请输入高度', trigger: 'blur'}
                ],
                width: [
                    {required: true, message: '请输入宽度', trigger: 'blur'}
                ],
                gather_rule: [
                    {required: true, message: '请选择流程模板', trigger: 'change'}
                ],
                period: [
                    {required: true, message: '请输入采集周期(以秒为单位)', trigger: 'blur'}
                ]
            },//基本监控项（修改后）的校验规则
            basicMonitorRules: {
                font_size: [
                    {required: true, message: '请选择字号', trigger: 'change'}
                ],
                height: [
                    {required: true, message: '请填写高度', trigger: 'blur'},
                    {validator: height_range_check, trigger: 'blur'}
                ],
                width: [
                    {required: true, message: '请填写宽度', trigger: 'blur'},
                    {validator: width_range_check, trigger: 'blur'}
                ],
                interface_type: [
                    {required: true, message: '请选择来源类型', trigger: 'change'}
                ],
                measures: [
                    {required: true, message: '请选择来源名称', trigger: 'change'}
                ],
                measures_name: [
                    {required: true, message: '请选择度量值', trigger: 'change'}
                ],
                show_rule_type: [
                    {required: true, message: '请选择展示规则', trigger: 'change'}
                ],
                gather_rule: [
                    {required: true, message: '请填写数据采集规则', trigger: 'change'}
                ],
                start_time: [
                    {required: true, message: '请选择采集开始时间', trigger: 'change'}
                ],
                end_time: [
                    {required: true, message: '请选择采集结束时间', trigger: 'change'}
                ],
                period: [
                    {required: true, message: '请填写采集周期', trigger: 'blur'}
                ],
                dimension_data: {
                    dimension_name: [
                        {required: true, message: '请选择维度名称', trigger: 'change'}
                    ],
                    dimension_value: [
                        {required: true, message: '请填写维度值', trigger: 'blur'}
                    ]
                },
                score: [
                    {required: true, message: '请输入分值', trigger: 'change'}
                ]
            },
            //校验规则
            basic1: {                                //基本单元
                monitor_name: '',                    //单元名称
                monitor_type: '',                    //单元类型
                font_size: '20',                       //字号
                height: '20',                          //高度
                width: '0',                            //宽度
                start_time: '',                      //开始时间
                end_time: '',                        //结束时间
                period: '10',                          //采集周期
                params: '',                         //监控参数
                status: '',                          //监控状态
                contents: '',                        //显示内容
                gather_rule: '',                     //采集规则
                gather_params: 'sql',                   //采集参数
                monitor_area: ''                             //日历地区
            },
            chart1: {                                //图表单元
                monitor_name: '',                    //单元名称
                monitor_type: '',                    //单元类型
                font_size: '20',                       //字号
                height: '380',                          //高度
                width: '580',                            //宽度
                start_time: '',                      //开始时间
                end_time: '',                        //结束时间
                period: '10',                          //采集周期
                status: '',                          //监控状态
                contents: '',                        //显示内容
                gather_rule: '',                     //采集规则
                gather_params: '',                   //节点
                params: '',                          //监控参数
                monitor_area: ''                             //日历地区
            },
            job1: {                                   //作业单元
                monitor_name: '',                    //单元名称
                monitor_type: '',                    //单元类型
                font_size: '20',                       //字号
                height: '20',                          //高度
                width: '0',                            //宽度
                start_time: '',                      //开始时间
                end_time: '',                        //结束时间
                period: '10',                          //采集周期
                status: '',                          //监控状态
                contents: '',                        //显示内容
                gather_rule: '',                     //NODE_KEY
                gather_params: '',                   //作业模板
                params: '',                         //执行服务器
                monitor_area: ''                             //日历地区
            },
            flow7: {                                //流程单元
                monitor_name: '',                    //单元名称
                monitor_type: '',                    //单元类型
                font_size: '20',                       //字号
                height: '20',                          //高度
                width: '0',                            //宽度
                start_time: '',                      //开始时间
                end_time: '',                        //结束时间
                period: '',                          //采集周期
                params: '10',                         //监控参数
                status: '',                          //监控状态
                contents: '',                        //显示内容
                gather_rule: '',                     //采集规则
                gather_params: '',                   //流程模板
                monitor_area: ''                             //日历地区
            },
            myChart: null,
            chart_content: '',
            chartData: '',
            person_count: '',
            measures: '',
            measures_name: '',
            iqube_name: [],
            //度量值列表
            metric_list: [],
            //维度名称列表
            dimension_list: [],
            gather_list: [],
            gather_base_test_data: [],
            /*dimension_data:[{
                dimension_name:'ip',
                dimension_value:'192.168.1.153'
            }],*/


        },
        methods: {
            //显示加载中..背景
            popup_loading: function(){
                return this.$loading({
                    lock: true,
                    text: '正在拼命加载中...',
                    spinner: 'el-icon-loading',
                    background: 'rgba(0, 0, 0, 0.7)'
                });
            },
            //获取采集测试的结果，同步调用
            get_gather_test() {
                $.ajax({
                    type: "POST",
                    data: JSON.stringify(vm.base),
                    dataType: "JSON",
                    async: false,
                    url: site_url+"iqube_interface/gather_base_test/",
                    success: function (data) {
                        if (0 != data.code) {
                            vm.$alert("采集测试未通过，请校正接口调用参数或稍后重试！", "错误");
                            return;
                        }
                        //采集测试的数据缓存到gather_data_test_data变量中
                        console.log(data.results)
                        vm.gather_test_data = data.results;
                    },
                    error: function (error) {
                        vm.$alert("采集测试未通过，请校正接口调用参数或稍后重试！", "错误");
                        return;
                    }
                });
            },
            //基本监控项（修改后）显示内容变更时调用的预览变更方法
            content_modified_change() {
                this.base_monitor_other_fixed_status();
                this.content_change();
            },
            //基本监控项显示方式为其他且显示内容为空时显示的单位
            base_monitor_other_fixed_status() {
                if (vm.base.show_rule_type == 2) {
                    if ('' == vm.base['contents'].replace(/^\s+|\s+$/g, "")) {
                        $('#other_fixed_show').show();
                    } else {
                        $('#other_fixed_show').hide();
                    }
                }
            },
            //基本监控项修改后显示内容重置方法
            base_monitor_show_reset() {
                //base['contents']使用缓存的所有指标值显示内容替换
                this.base['contents'] = this.base_monitor_show_cache;
                //如果显示方式为其他，且显示内容为空，移除为空时显示的当前单位
                this.base_monitor_other_fixed_status();
                //更替显示内容
                this.content_change();
            },
            //基本监控项修改后颜色和其他选项提示信息添加方法
            add_comments() {
                if ('1' == this.base.show_rule_type) {
                    this.color_rules_comments = true;
                    this.other_rules_comments = false;
                } else if ('2' == this.base.show_rule_type) {
                    this.color_rules_comments = false;
                    this.other_rules_comments = true;
                } else {
                    this.color_rules_comments = false;
                    this.other_rules_comments = false;
                }

            },
            //监控项数据处理，用于编辑状态下回显数据
            monitor_edit_data_process(row) {
                //如果监控项类型为基本基本监控单元（修改后）
                if ('five' == vm.monitor_type) {
                    //基本监控项采集类型初始化
                    this.sql_file_interface = row.gather_params;
                    //切换基本监控项的数据来源类型展示不同的内容
                    this.base_gather_source_change(vm.sql_file_interface);
                    if (vm.sql_file_interface == 'interface') {
                        vm.sql_file_interface = 9;
                        if (row.dimension != null) {
                            vm.base['dimension_data'] = JSON.parse(row.dimension);
                        } else {
                            vm.base['dimension_data'] = [];
                        }
                        if (0 == row.source_type) {
                            this.change_source_type('log');
                            this.base['interface_type'] = 'log';
                        } else if (1 == row.source_type) {
                            this.change_source_type('measures');
                            this.base['interface_type'] = 'measures';
                        } else {
                            this.base['interface_type'] = null;
                        }
                        vm.base['measures_name'] = row.measure_name;
                        vm.base['measures'] = row.target_name;
                        //下拉框不识别number类型的数据，需要转化为字符串供下拉框回显
                        vm.base['show_rule_type'] = row.display_type.toString();
                        //展示类型为颜色时显示提示信息
                        if ('1' == vm.base['show_rule_type']) {
                            this.color_rules_comments = true;
                            this.other_rules_comments = false;
                        } else if ('2' == vm.base['show_rule_type']) {
                            this.other_rules_comments = true;
                            this.color_rules_comments = false;
                        }
                        vm.base['monitor_name'] = vm.monitor_name;
                        vm.base['monitor_type'] = vm.monitor_type;
                        vm.base['font_size'] = row.font_size;
                        vm.base['height'] = row.height;
                        vm.base['width'] = row.width;
                        vm.base['start_time'] = row.start_time;
                        vm.base['end_time'] = row.end_time;
                        vm.base['period'] = row.period;
                        vm.base['params'] = row.params;
                        vm.base['status'] = row.status;
                        vm.base['contents'] = row.contents;
                        vm.base['gather_rule'] = row.gather_rule;
                        vm.base['gather_params'] = row.gather_params;
                        vm.base['monitor_area'] = vm.area;
                        vm.base['score'] = row.score;
                    } else {
                        alert('暂未实现！');
                    }
                }
            },
            //数据添加后缓存数据清空操作
            monitor_cache_clean() {
                //基本监控项（修改后）的清空操作
                if ('five' == vm.monitor_type) {
                    this.base['dimension_data'] = [];
                    this.base['measures_name'] = '';
                    this.base['measures'] = '';
                    this.base['interface_type'] = '';
                    this.base['show_rule_type'] = '';
                    //清空数据后默认为基本监控类型（修改后）
                    this.base['monitor_type'] = 5;
                    this.base['font_size'] = '20';
                    this.base['height'] = '480';
                    this.base['width'] = '422';
                    this.base['start_time'] = '';
                    this.base['end_time'] = '';
                    this.base['period'] = '10';
                    this.base['params'] = '';
                    this.base['status'] = '';
                    this.base['contents'] = '';
                    this.base['gather_rule'] = '';
                    //采集参数默认为interface
                    this.base['gather_params'] = 'interface';
                    this.base['monitor_area'] = '';
                }
                //采集测试标志位置空
                vm.gather_data_test_flag = null;
                //采集测试缓存数据清空
                this.gather_test_data = null;
                //采集测试的预览框清空
                $('#base_test_text').html('');
                //提示信息状态标志位置false
                this.color_rules_comments = false;
                this.other_rules_comments = false;
                //如果是基本监控项（修改后）的修改窗口被关闭基本监控项编辑初始化状态重置为true
                if (1 == vm.add_pamas) {
                    this.base_monitor_edit_init = true;
                    this.base_monitor_edit_test_init = true;
                } else if (0 == vm.add_pamas) {
                    this.base_monitor_add_init = true;
                    this.base_monitor_add_test_init = true;
                }
                //缓存的当前所有指标的显示内容清空
                vm.base_monitor_show_cache = '';
            },
            //基本监控项（修改后）的数据来源切换
            base_gather_source_change(source_type) {
                if ('sql' == source_type || '3' == source_type) {
                    //显示数据库表单
                    this.database_show = true;
                    this.file_show = false;
                    this.interface_show = false;
                } else if ('interface' == source_type || '9' == source_type) {
                    //显示关闭文件和数据库的显示，显示接口表单
                    this.database_show = false;
                    this.file_show = false;
                    this.interface_show = true;
                } else if ('file' == source_type || '6' == source_type) {
                    //显示文件表单
                    this.database_show = false;
                    this.file_show = true;
                    this.interface_show = false;
                } else {
                    console.log('基本监控项数据来源类型错误： ' + source_type);
                }
            },
            //将监控项类型的编码转换成中文的名称，前台转换
            format_monitor_type(row, column) {
                if (row.monitor_type === 1) {
                    return "基本监控项"
                } else if (row.monitor_type === 2) {
                    return "图表监控项"
                } else if (row.monitor_type === 3) {
                    return "作业监控项"
                } else if (row.monitor_type === 4) {
                    return "流程监控项"
                } else if (row.monitor_type === 5) {
                    return "基本监控项（一体化平台）"
                }
            },
            //基本监控项的数据处理方法
            base_monitor_data_process() {
                //数据整合与处理
                this.base_monitor_upload_data['jion_id'] = null;
                if ('log' == this.base['interface_type']) {
                    this.base_monitor_upload_data['source_type'] = 0;
                } else if ('measures' == this.base['interface_type']) {
                    this.base_monitor_upload_data['source_type'] = 1;
                } else {
                    this.base_monitor_upload_data['source_type'] = null;
                }
                //base对象被其他功能所使用，因此不能删除其属性用于上传数据，另外定义一个新的变量缓存并上传
                this.base_monitor_upload_data['target_name'] = this.base['measures'];
                this.base_monitor_upload_data['measure_name'] = this.base['measures_name'];
                if (null == this.base['dimension_data'] || 0 === this.base['dimension_data'].length) {
                    this.base_monitor_upload_data['dimension'] = null;
                } else {
                    this.base_monitor_upload_data['dimension'] = JSON.stringify(this.base['dimension_data']);
                }
                this.base_monitor_upload_data['display_type'] = this.base['show_rule_type'];
                this.base_monitor_upload_data['display_rule'] = this.base['gather_rule'];
                this.base_monitor_upload_data['gather_rule'] = this.base['gather_rule'];
                this.base_monitor_upload_data['gather_params'] = this.base['gather_params'];
                this.base_monitor_upload_data['params'] = this.base['params'];
                this.base_monitor_upload_data['width'] = this.base['width'];
                this.base_monitor_upload_data['height'] = this.base['height'];
                this.base_monitor_upload_data['font_size'] = this.base['font_size'];
                this.base_monitor_upload_data['period'] = this.base['period'];
                this.base_monitor_upload_data['start_time'] = this.base['start_time'];
                this.base_monitor_upload_data['end_time'] = this.base['end_time'];
                this.base_monitor_upload_data['contents'] = this.base['contents'];
                this.base_monitor_upload_data['score'] = this.base['score'];
                this.result_data = this.base_monitor_upload_data;
                //由于调用采集测试接口需要以下参数,因此在此统一删除数据库表不存在的字段,避免监控项添加时报错
                /*delete this.base['dimension_data'];
                delete this.base['interface_type'];
                delete this.base['measures'];
                delete this.base['measures_name'];
                delete this.base['show_rule_type'];*/
            },
            //采集测试的数据保存方法
            gather_data_test_save(item_id, type) {
                axios({
                    method: 'post',
                    url: site_url+'gather_data/gather_data_save',
                    data: {
                        'measures': this.gather_test_data,
                        'item_id': item_id,
                        'type': type
                    }
                }).then((res) => {
                    console.log('采集测试数据保存成功');
                }).catch((error) => {
                    vm.$alert("采集测试数据保存失败！", "错误");
                });
            },
            //监控项数据编辑后的保存方法
            monitor_data_save(unit_id, flow) {
                //unit_id大于0的情况为编辑后的数据上传
                if (unit_id > 0) {
                    axios({
                        method: 'post',
                        url: site_url+'monitor_item/edit/',
                        data: {
                            'flow': flow,
                            data: vm.result_data,
                            monitor_type: vm.monitor_type,
                            monitor_name: vm.monitor_name,
                            unit_id: vm.unit_id,
                            monitor_area: vm.area
                        }
                    }).then((res) => {
                        if (res['data']['code'] == 1) {
                            this.$alert("保存失败!", "错误");
                            vm.centerDialogVisible = true;
                        } else {
                            //数据库监控项编辑，重新采集数据并入库采集表
                            if(vm.monitor_type == "first") {
                                axios({
                                    method: 'post',
                                    url: site_url+'monitor_item/basic_test/',
                                    data: {
                                        id: vm.unit_id,
                                        params: vm.server_url,
                                        gather_rule: vm.basic.gather_rule,
                                        gather_params: vm.basic.gather_params,
                                        score:vm.basic.score
                                    },
                                }).then(function (res) {});
                            }
                            //一体化的监控项，调用采集逻辑
                            if(vm.monitor_type == "five") {
                                //保存采集测试的数据到服务器
                                vm.gather_data_test_save(vm.unit_id, 'edit');
                            }
                            //保存成功，清空预览区域
                            vm.clear_review();
                            this.$alert("保存成功!", "提示");
                            vm.centerDialogVisible = false;
                        }
                        vm.show();
                    }).catch((error) => {
                        this.$alert("修改保存出错！", "错误")
                    });
                }
                //unit_id等于0的情况下为添加后的数据上传
                else if (unit_id == 0) {
                    const loading = this.popup_loading();
                    axios({
                        method: 'post',
                        url: site_url+'monitor_item/add/',
                        data: {
                            'flow': flow,
                            data: vm.result_data,
                            monitor_type: vm.monitor_type,
                            monitor_name: vm.monitor_name,
                            monitor_area: vm.area
                        }
                    }).then((res) => {
                        loading.close();
                        if (res['data']['code'] == 1) {
                            this.$alert("新增保存失败!", "错误");
                            vm.centerDialogVisible = true;
                        } else {
                            if(vm.monitor_type == "first") {
                                axios({
                                    method: 'post',
                                    url: site_url+'monitor_item/basic_test/',
                                    data: {
                                        id: res.data['item_id'],
                                        params: vm.server_url,
                                        gather_rule: vm.basic.gather_rule,
                                        gather_params: vm.basic.gather_params,
                                        score: vm.basic.score
                                    },
                                }).then(function (res) {
                                });
                            }
                            if(vm.monitor_type == "five"){
                                //保存采集测试的数据到服务器
                                vm.gather_data_test_save(res.data['item_id'], 'add');
                            }
                            //保存成功，清空预览区域
                            vm.clear_review();
                            this.$alert("保存成功!");
                            vm.centerDialogVisible = false
                        }
                        vm.show()
                    }).catch((error) => {
                        this.$alert('新增保存失败!', "错误");
                    });
                } else {
                    vm.centerDialogVisible = true;
                    if (vm.add_pamas == 0) {
                        vm.unit_id = 0
                    } else {
                        vm.unit_id = vm.unit_id1
                    }
                }
            },
            add_dimension() {
                vm.$set(vm.base.dimension_data, vm.base.dimension_data.length, {
                    dimension_name: '',
                    dimension_value: ''
                });
            },
            delete_dimension(index) {
                vm.base.dimension_data.splice(index, 1);
            },
            basic_size() {
                $("#text2").find("*").css("font-size", this.basic.font_size)
            },
            //基本监控项修改后的字体大小变更
            base_size() {
                collection_base_size(vm, '#base_test_text')
            },
            basic_height() {
                $('#text2').css('height', this.basic.height)
            },
            basic_width() {
                $("#text2").css("width", this.basic.width)
            },
            get_header_data() {
                axios.get(site_url+'market_day/get_header/').then(function (res) {
                })
            },
            get_all_area() {
                axios({
                    method: 'get',
                    url: site_url+'market_day/get_all_area',
                }).then(function (res) {
                    res = res.data.message
                    console.log(res)
                    vm.areas = []
                    for (var i = 0; i < res.length; i++) {
                        var label = res[i].country + "(" + res[i].timezone + ")"
                        temp = {
                            'area': label,
                            'value': res[i].id
                        }
                        vm.areas.push(temp)
                    }
                })
            },
            sycontent() {
                //当显示内容为空的情况下
                if ("@" == split_char && '' == vm.basic.contents.replace(/^\s+|\s+$/g, "")) {
                    $('#text2').show();
                }
                var content = vm.basic.contents
                var content_str = content.substring(0, content.lastIndexOf('@')); //去@符号
                var content_obj = '{' + content_str.replace(/@\n/g, ',') + '}';      //加{}
                var content_json = JSON.parse(content_obj);
                var html_obj = "#text2"
                $(html_obj).find('.display').hide();       //隐藏预览区域的dom
                for (x in content_json) {                             //遍历json
                    $(html_obj).find('[type=' + x + ']').show();   //显示内容存在的key会在预览区域显示
                    let len = $(html_obj + " p").length;
                    for (let i = 0; i < len; i++) {
                        let dom_type = $(html_obj + " p").eq(i).attr('type');//获取dom的type
                        let value1 = $(html_obj + " p").eq(i).text().split(':')[0];//获取dom的text ：前面的内容
                        if (x == dom_type) {//显示内容的key等于dom的type
                            let text = $(html_obj + " p").eq(i).text();
                            $(html_obj + " p").eq(i).html(text.replace(value1, content_json[x]));//将dom的text ：前面的内容替换成显示内容的value
                            var content = $(html_obj + " p").eq(i).html();
                        }
                    }
                }
            },
            basic_review(res) {//基本监控项预览
                let tempcontents2 = vm.basic.contents
                $("#text2").append("<div class=\"newline\" style=\"font-size:" + vm.basic.font_size + "px;\">" + tempcontents2 + "</div>")
                if (vm.basic.contents.indexOf("#") > -1 && vm.basic.contents.indexOf('@') == -1) {
                    var temp1 = tempcontents2.split("#");
                    var temp2 = [];
                    var temp3 = [];
                    var temp4 = [];
                    for (var i = 1; i < temp1.length; i = i + 2) {
                        temp2.push(temp1[i]);
                    }
                    for (var i = 0; i < temp2.length; i++) {
                        temp3.push(temp2[i].split("="))
                    }
                    for (var i = 0; i < temp3.length; i++) {
                        temp4.push(temp3[i][0])
                    }
                    vm.clear_review();
                    for (var i = 0, j = 0; i < temp1.length; i = i + 2, j++) {
                        if (j < temp4.length) {
                            if(res.data.message[0][temp4[j]]){
                                $("#text2").append("<div class=\"newline\" style=\"font-size:" + vm.basic.font_size + "px;\">" + temp1[i] + res.data.message[0][temp4[j]] + "</div>");
                            }else{
                                $("#text2").append("<div class=\"newline\" style=\"font-size:" + vm.basic.font_size + "px;\">" + temp1[i] +  temp3[j][1] + "</div>");
                            }
                        } else {
                            $("#text2").append("<div class=\"newline\" style=\"font-size:" + vm.basic.font_size + "px;\">" + temp1[i] + "</div>");
                        }
                    }
                }
                if (vm.basic.contents.indexOf('@') > -1 && vm.basic.contents.indexOf("#") == -1) {
                    var icon1 = tempcontents2.split("@");
                    var icon2 = [];
                    var icon3 = [];
                    var icon4 = '';
                    if (res.data.message[0]['DB_CONNECTION']) {
                        icon4 = res.data.message[0]['DB_CONNECTION'];
                    }
                    if (res.data.message[0]['URL_CONNECTION']) {
                        icon4 = res.data.message[0]['URL_CONNECTION'];
                    }
                    if (res.data.message[0]['FILE_EXIST']) {
                        icon4 = res.data.message[0]['FILE_EXIST'];
                    }
                    vm.clear_review();
                    $("#text2").append("<div class = \"asd\" style=\"font-size:" + vm.basic.font_size + "px;\">" + icon1[0] + "</div>");
                    if (icon4 == 1) {
                        $("#text2").append("<div class=\"circle1\"></div>");
                    }
                    if (icon4 == 2) {
                        $("#text2").append("<div class=\"circle2\"></div>");
                    }
                    if (icon4 == 0) {
                        $("#text2").append("<div class=\"circle3\"></div>");
                    }
                    if (icon4 == -1 || icon4 == -2) {
                        $("#text2").append("<div class=\"circle4\"></div>");
                    }
                }
                if (vm.basic.contents.indexOf("#") > -1 && vm.basic.contents.indexOf('@') > -1) {
                    var temp1 = tempcontents2.split("#");
                    var temp2 = [];
                    var temp3 = [];
                    var temp4 = [];
                    for (var i = 1; i < temp1.length; i = i + 2) {
                        temp2.push(temp1[i]);
                    }
                    for (var i = 0; i < temp2.length; i++) {
                        temp3.push(temp2[i].split("="))
                    }
                    for (var i = 0; i < temp3.length; i++) {
                        temp4.push(temp3[i][0])
                    }
                    var icon1 = [];
                    var icon2 = [];
                    var icon3 = [];
                    var icon4 = '';
                    var flag2 = 0;
                    for (var i = 0; i < temp1.length; i = i + 2) {
                        if (temp1[i].indexOf("@") > -1) {
                            icon1 = temp1[i].split("@")
                            flag2 = i
                            for (var k = 0; k < icon1.length; k++) {
                                icon2.push(icon1[k])
                            }
                        }
                    }
                    icon3 = icon2[1].split("=")
                    if (res.data.message[0]['DB_CONNECTION']) {
                        icon4 = res.data.message[0]['DB_CONNECTION'];
                    }
                    if (res.data.message[0]['URL_CONNECTION']) {
                        icon4 = res.data.message[0]['URL_CONNECTION'];
                    }
                    if (res.data.message[0]['FILE_EXIST']) {
                        icon4 = res.data.message[0]['FILE_EXIST'];
                    }
                    vm.clear_review();
                    for (var i = 0, j = 0; i < temp1.length; i = i + 2, j++) {
                        //flag2 标记sql语句是否正常
                        if (i == flag2) {
                            $("#text2").append("<div class = \"asd\" style=\"font-size:" + vm.basic.font_size + "px;\">" + icon1[0] + "</div>");
                            if (icon4 == 1) {
                                $("#text2").append("<div class=\"circle1\"></div>");
                            }else
                            if (icon4 == 2) {
                                $("#text2").append("<div class=\"circle2\"></div>");
                            }else
                            if (icon4 == 0) {
                                $("#text2").append("<div class=\"circle3\"></div>");
                            }else {
                                $("#text2").append("<div class=\"circle4\"></div>");
                            }
                        } else {
                            if(res.data.message[0][temp4[j]]){
                                $("#text2").append("<div class=\"newline\" style=\"font-size:" + vm.basic.font_size + "px;\">" + temp1[i] + res.data.message[0][temp4[j]] + "</div>");
                            }else{
                                $("#text2").append("<div class=\"newline\" style=\"font-size:" + vm.basic.font_size + "px;\">" + temp1[i] + temp3[j][1] + "</div>");
                            }
                        }
                    }
                }
            },
            basic_test() {
                let params = '';
                //数据库监控项
                if (vm.sql_file_interface == 3) {
                    //第一步校验
                    if(vm.server_url == ""){
                        vm.message = '请选择数据库连接!';
                        this.$alert(vm.message, "错误");
                        vm.unit_id = -1;
                        return false;
                    }
                    if(vm.basic.contents == ""){
                        vm.message = '请录入显示类容!';
                        this.$alert(vm.message, "错误");
                        vm.unit_id = -1;
                        return false;
                    }
                    if(vm.basic.gather_rule == ""){
                        vm.message = '请录入数据采集规则!';
                        this.$alert(vm.message, "错误");
                        vm.unit_id = -1;
                        return false;
                    }
                    params = vm.server_url
                }
                if (vm.sql_file_interface == 6 || vm.sql_file_interface == 9) {
                    params = vm.server_url + '#' + vm.file_param
                }
                const loading = this.popup_loading();
                axios({
                    method: 'post',
                    url: site_url+'monitor_item/basic_test/',
                    data: {
                        id: vm.unit_id,
                        params: params,
                        gather_rule: vm.basic.gather_rule,
                        gather_params: vm.basic.gather_params,
                        score:vm.basic.score
                    },
                }).then(function (res) {
                    loading.close();
                    vm.basic_review(res)
                });
            },
            // 保存
            pefFrom() {
                //彭英杰 20190520 strat
                vm.loading_tool = true;
                var basic = $("#tab-first[aria-selected='true']");
                var chart = $("#tab-second[aria-selected='true']");
                var job = $("#tab-third[aria-selected='true']");
                var flow = $("#tab-fourth[aria-selected='true']");
                var base = $("#tab-five[aria-selected='true']");
                if (basic.length>0) {
                    vm.submitForm('basic')
                } else if (chart.length>0) {
                    vm.submitForm('chart')
                } else if (job.length>0) {
                    vm.submitForm('job')
                } else if (flow.length>0) {
                    vm.submitForm('flow')
                } else if (base.length>0) {
                    vm.submitForm('base')
                }
                //彭英杰 20190520 end
            },
            current_change1(value) {
                vm.page = value;

                vm.select2();
            },
            //保存按钮
            submitForm(formName) {
                if(vm.isShow == false){
                    this.$refs[formName].validate((valid) => {
                        if (valid) {
                            vm.edit1()
                        } else {
                            console.log('error submit!!');
                            return false;
                        }
                    });
                 }
            },
            delete_unit(row) {
                this.$confirm('此操作将永久删除该监控项, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                    center: true
                }).then(() => {
                    this.$message({
                            type: 'success',
                            message: '删除成功!',
                        },
                        axios({
                            method: 'post',
                            url: site_url+'monitor_item/delete/',
                            data: {
                                unit_id: row.id,
                                monitor_name: row.monitor_name,
                                monitor_type: row.monitor_type,
                            }
                        }).then((res) => {
                            vm.page = 1;
                            vm.show()

                        }),);
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                });
            },
            show() {
                axios({
                    method: 'post',
                    url: site_url+'monitor_item/show/',
                    data: {
                        page: vm.page,
                        limit: 10
                    },
                }).then(function (res) {
                    vm.sites = res.data.results.res_list;
                    vm.page_count = res.data.results.res_list[0].page_count;
                    //vm.job2 = res.data.results.job;
                    //vm.flow2 = res.data.results.flow;
                })
                    vm.showAPI();
            },
            showAPI() {
                 setTimeout(function(){
                       axios({
                            method: 'post',
                            url: site_url+'monitor_item/showAPI/',
                            data: {
                                page: vm.page,
                                limit: 10
                            },
                        }).then(function (res) {
                            vm.job2 = res.data.results.job;
                            vm.flow2 = res.data.results.flow;
                        })
                        },1000);
            },
            select1(){
                vm.centerDialogVisible = false;
                vm.page = 1;
                if (vm.contents === "") {
                    vm.show()
                }else {
                    vm.select2();
                }
            },
            select2() {
                    axios({
                        method: 'post',
                        url: site_url+'monitor_item/select/',
                        data: {
                            data: this.contents,
                            page: vm.page,
                            limit: 10
                        }
                    }).then((res) => {
                        if (res.data.results.length == 0) {
                            vm.sites = [];
                            vm.page_count = 1
                        } else {
                            vm.sites = res.data.results;
                            vm.page_count = res.data.results[0].page_count;
                        }
                    }).catch(function (e) {
                        vm.$message.error('获取数据失败！');
                    });
            },
            //编辑单元
            edit_unit(row) {
                this.get_db_connections();
                vm.add_pamas = 1;
                vm.centerDialogVisible = true;
                //默认编辑下显示基本监控项取消
                //初始化不可用
                vm.disabled2 = true;
                vm.disabled3 = true;
                vm.disabled6 = true;
                //-----------------------------
                //vm.disabled4 = true;
                //vm.disabled5 = true;
                //-----------------------------
                vm.unit_id = row.id;
                vm.monitor_name = row.monitor_name;
                //原始基本监控项
                if (row.monitor_type === 1) {
                    vm.disabled2 = false;
                    vm.monitor_type = 'first';
                    vm.basic.font_size = row.font_size;
                    vm.basic.height = row.height;
                    vm.basic.width = row.width;
                    vm.basic.start_time = row.start_time;
                    vm.basic.end_time = row.end_time;
                    vm.basic.period = row.period;
                    vm.sql_file_interface = row.gather_params;
                    vm.file_param = row.file_param;
                    vm.basic.start_time = row.start_time;
                    vm.basic.end_time = row.end_time;
                    vm.basic.gather_rule = row.gather_rule;
                    vm.basic.contents = row.contents;
                    vm.basic.status = row.status;
                    vm.basic.score = row.score;
                    vm.basic.measure_name = row.measure_name;
                    vm.basic.display_type = row.display_type;
                    vm.basic.display_rule = row.display_rule;
                    vm.area = row.monitor_area;
                    if (vm.sql_file_interface === 'sql') {
                        vm.sql_file_interface = 3;
                        axios({
                            method: 'post',
                            url: site_url+'db_connection/get_conname/',
                            data: row.params,
                        }).then((res) => {
                            if(res['data']['result']){
                                vm.sql_id = res['data']['results']['id'];
                                vm.server_url = vm.sql_id;
                                vm.basic_size();
                                vm.basic_height();
                                vm.basic_width();
                                //当监控项的监控状态为0，表示不自动采集数据
                                //预览前清空预览
                                vm.clear_review();
                                if(row.status === "1"){
                                    vm.basic_test();
                                }else{
                                    //这里暂不需要实现
                                    //预览取历史数据
                                }
                            }else{
                                vm.clear_review();
                                vm.$alert('获取数据库连接配置失败！',"错误");
                            }
                        }).catch(function (e) {
                            vm.clear_review();
                            vm.$alert('获取数据库连接配置失败！',"错误");
                        });
                        vm.sql1 = 'block';
                        vm.file1 = 'none';
                        vm.interface1 = 'none';
                        vm.basic.gather_params = 'sql'
                    }
                    if (vm.sql_file_interface === 'file') {
                        vm.sql_file_interface = 6;
                        arr = row.params.split("#");
                        vm.server_url = arr[0];
                        vm.file_param = arr[1];
                        vm.typeid = '2';
                        vm.sql1 = 'none';
                        vm.file1 = 'block';
                        vm.interface1 = 'none';
                        vm.basic.gather_params = 'file';
                        vm.basic_size();
                        vm.basic_height();
                        vm.basic_width();
                        vm.sycontent();
                        if(row.status === "1"){
                            vm.basic_test();
                        }
                    }
                    if (vm.sql_file_interface === 'interface') {
                        vm.sql_file_interface = 9;
                        arr = row.params.split("#");
                        vm.server_url = arr[0];
                        vm.file_param = arr[1];
                        vm.typeid = '3';
                        vm.sql1 = 'none';
                        vm.file1 = 'none';
                        vm.interface1 = 'block';
                        vm.basic.gather_params = 'interface';
                        vm.basic_size();
                        vm.basic_height();
                        vm.basic_width();
                        vm.sycontent();
                        if(row.status === "1"){
                            vm.basic_test();
                        }
                    }

                }
                //图表监控项
                if (row.monitor_type === 2) {
                    vm.disabled3 = false;
                    vm.monitor_type = 'second';
                    vm.chart.font_size = row.font_size;
                    vm.chart.height = row.height;
                    vm.chart.width = row.width;
                    vm.chart.start_time = row.start_time;
                    vm.chart.end_time = row.end_time;
                    vm.chart.period = row.period;
                    vm.chart.gather_params = row.gather_params;
                    vm.chart.contents = row.contents;
                    vm.chart.start_time = row.start_time;
                    vm.chart.end_time = row.end_time;
                    vm.chart.gather_rule = row.gather_rule;
                    vm.chart.status = row.status;
                    vm.area = row.monitor_area;
                    axios({
                        method: 'post',
                        url: site_url+'db_connection/get_conname/',
                        data: row.params,
                    }).then((res) => {
                        vm.chart.params = res['data']['results']['connname'];
                        vm.show_content();
                    }).catch(function (e) {
                        vm.$message.error('获取数据库失败！');
                    });
                }
                //作业监控项
                /*
                if (row.monitor_type === 3) {
                    vm.disabled4 = false;
                    vm.monitor_type = 'third';
                    vm.job.font_size = row.font_size;
                    vm.job.height = row.height;
                    vm.job.width = row.width;
                    vm.change_job_fontSize();
                    vm.change_job_height();
                    vm.change_job_width();
                    vm.job.start_time = row.start_time;
                    vm.job.end_time = row.end_time;
                    vm.job.period = row.period;
                    vm.job.contents = row.contents;
                    vm.job.gather_rule = row.gather_rule;
                    vm.job.gather_params = row.gather_params;
                    vm.job.params = row.params;
                    vm.job.status = row.status;
                    vm.area = row.monitor_area;
                }*/
                //流程监控项
                /*
                if (row.monitor_type === 4) {
                    vm.disabled5 = false;
                    vm.monitor_type = 'fourth';
                    console.log(row)
                    vm.flow.font_size = row.font_size;
                    vm.flow.height = row.height;
                    vm.flow.width = row.width;
                    vm.flow.start_time = row.start_time;
                    vm.flow.end_time = row.end_time;
                    vm.flow.period = row.period;
                    vm.flow.status = row.status;
                    vm.flow.jion_id = row.jion_id;
                    vm.flow.period = row.period;
                    vm.flow.node_name = row.gather_params;
                    vm.flow.gather_rule = {
                        'name': row.gather_rule,
                        'id': row.jion_id
                    };
                    vm.area = row.monitor_area;
                    var id1 = row.jion_id
                    var id = [{
                        'id': id1
                    }]
                    vm.flow_change(id)
                }*/
                //基本监控项（一体化）
                if (row.monitor_type === 5) {
                    vm.disabled6 = false;
                    //监控项类型设置
                    this.monitor_type = 'five';
                    //处理监控项的数据用于修改时的数据回显
                    this.monitor_edit_data_process(row);
                    // 执行采集测试
                     if(row.status === "1"){
                         this.base_cell_test();
                     }
                }
            },
            //保存数据处理
            edit1() {
                var node_time = {};
                var flow = {};
                if (vm.monitor_name == '') {
                    vm.message = '监控项名称不能为空!';
                    this.$alert(vm.message, "错误");
                    vm.unit_id = -1;
                    return false;
                }
                //基本监控项（数据库监控项）
                if (vm.monitor_type == 'first') {
                    vm.result_data = vm.basic;
                    //当前只有数据库连接，就直接赋值连接的编号
                    vm.basic.params = vm.server_url
                    vm.basic.monitor_name = vm.monitor_name;
                    vm.basic.monitor_type = vm.monitor_type;
                    if (vm.server_url == '') {
                        vm.unit_id = -1;
                        vm.message = '请选择数据库连接！'
                        this.$alert(vm.message, "错误");
                        return false;
                    }
                    if (vm.basic.gather_rule == '') {
                        vm.unit_id = -1;
                        vm.message = '请输入数据采集规则!'
                        this.$alert(vm.message, "错误");
                        return false;
                    }
                    if (vm.basic.start_time == '') {
                        vm.unit_id = -1;
                        vm.message = '请选择开始时间!'
                        this.$alert(vm.message, "错误");
                        return false;
                    }
                    if (vm.basic.end_time == '') {
                        vm.unit_id = -1;
                        vm.message = '请选择结束时间!'
                        this.$alert(vm.message, "错误");
                        return false;
                    }
                    //上传数据至服务器保存
                    vm.monitor_data_save(vm.unit_id, flow);
                } else if (vm.monitor_type == 'second') {
                    vm.result_data = vm.chart;
                    vm.chart.monitor_name = vm.monitor_name;
                    vm.chart.monitor_type = vm.monitor_type;
                    if (vm.chart.params == '') {
                        vm.unit_id = -1;
                        vm.message = '请选择数据库!'
                    }
                    if (vm.chart.gather_rule == '') {
                        vm.unit_id = -1;
                        vm.message = '请输入采集规则!'
                    }
                    if (vm.chart.start_time == '') {
                        vm.unit_id = -1;
                        vm.message = '请选择开始时间!'
                    }
                    if (vm.chart.end_time == '') {
                        vm.unit_id = -1;
                        vm.message = '请选择结束时间!'
                    }
                    //上传数据至服务器保存
                    vm.monitor_data_save(vm.unit_id, flow);
                } else if (vm.monitor_type == 'third') {
                    vm.result_data = vm.job;
                    vm.job.monitor_name = vm.monitor_name;
                    vm.job.monitor_type = vm.monitor_type;
                    if (vm.job.gather_rule == '') {
                        vm.unit_id = -1;
                        vm.message = '请选择作业模板!'
                    }
                    var reg = /^(?:(?:2[0-4][0-9]\.)|(?:25[0-5]\.)|(?:1[0-9][0-9]\.)|(?:[1-9][0-9]\.)|(?:[0-9]\.)){3}(?:(?:2[0-4][0-9])|(?:25[0-5])|(?:1[0-9][0-9])|(?:[1-9][0-9])|(?:[0-9]))$/;
                    var re = new RegExp(reg);
                    if (vm.job.params == null || vm.job.params == '') {
                        vm.unit_id = -1;
                        vm.message = "IP不可为空!";
                    }
                    if (!re.test(vm.job.params)) {
                        vm.unit_id = -1;
                        vm.message = "请填写有效的IP地址!";
                    }
                    if (vm.job.start_time == '') {
                        vm.unit_id = -1;
                        vm.message = '请选择开始时间!'
                    }
                    if (vm.job.end_time == '') {
                        vm.unit_id = -1;
                        vm.message = '请选择结束时间!'
                    }
                    //上传数据至服务器保存
                    vm.monitor_data_save(vm.unit_id, flow);
                } else if (vm.monitor_type == 'fourth') {
                    vm.result_data = vm.flow;
                    vm.flow.monitor_name = vm.monitor_name;
                    vm.flow.monitor_type = vm.monitor_type;
                    if (vm.flow.gather_rule == '') {
                        vm.unit_id = -1;
                        vm.message = '请选择流程模板!'
                    }
                    var node_times = [];
                    for (var i = 4; i <= vm.location.length - 1; i++) {
                        node_time.node_id = vm.location[i].id ,
                            node_time.starttime = $('#' + vm.location[i].id + '').find('.start_time').text(),
                            node_time.endtime = $('#' + vm.location[i].id + '').find('.end_time').text()
                        node_time.node_name = $('#' + vm.location[i].id + '').find('.node-title').text()
                        if (node_time.starttime == "") {
                            vm.unit_id = -1;
                            vm.message = '请配置每个节点的开始时间';
                        } else if (node_time.endtime == "") {
                            vm.unit_id = -1;
                            vm.message = '请配置每个节点的结束时间';
                        }
                    }
                    node_times.push(node_time);
                    flow.node_times = node_times;
                    flow.monitor_name = vm.monitor_name;
                    flow.monitor_type = vm.monitor_type;
                    console.log(vm.flow.gather_rule);
                    flow.jion_id = vm.flow.gather_rule[0].id;
                    flow.font_size = vm.flow.font_size;
                    flow.height = vm.flow.height;
                    flow.width = vm.flow.width;
                    flow.period = vm.flow.period;
                    flow.constants = vm.constants;
                    //上传数据至服务器保存
                    vm.monitor_data_save(vm.unit_id, flow);
                    //修改后的基本监控项的数据上传处理
                } else if (vm.monitor_type == 'five') {
                    //判断是否已经进行采集测试
                    if (null != this.gather_data_test_flag && false == this.gather_data_test_flag) {
                        vm.message ="采集测试未通过，请校正接口调用参数或稍后重试！\", \"错误\""
                        // this.$alert("采集测试未通过，请校正接口调用参数或稍后重试！", "错误");
                        vm.gather_data_test_flag = null;
                    } else if (null == this.gather_data_test_flag) {
                        //获取采集测试数据，调用同步服务
                        vm.get_gather_test();
                        //基本监控项的数据处理
                        vm.base_monitor_data_process();
                        //上传监控项数据至服务器保存
                        vm.monitor_data_save(vm.unit_id, flow);
                    } else {
                        //基本监控项的数据处理
                        vm.base_monitor_data_process();
                        //上传监控项数据至服务器保存
                        vm.monitor_data_save(vm.unit_id, flow);
                    }
                }
            },
            flow_change(value) {
                vm.node_name(value)
                vm.location = ''
                vm.line = ''
                axios({
                    method: 'post',
                    url: site_url+'monitor_item/flow_change/',
                    data: {
                        template_id: value
                    }
                }).then(function (res) {
                    {
                        vm.template_list.id = res.data.template_id[0].id
                        vm.template_list.name = res.data.template_id[0].name
                        vm.constants = res.data.constants
                        var aa = "  <div id=\"flow1\" class=\"clearfix workflow-box\" style=\"width:1000px;position: relative;\">\n" +
                            "\n" +
                            "                                        <div class=\"workflow-canvas\" style=\"margin-left: 0px;padding-left: 0px\">\n" +
                            "                                            <!-- 画布模板 start -->\n" +
                            "                                            <div class=\"jtk-content\">\n" +
                            "                                                <div class=\"jtk-demo-canvas canvas-wide jtk-surface jtk-surface-nopan\"\n" +
                            "                                                     id=\"canvas\" style=\"height:500px\">\n" +
                            "                                                    <!-- 流程 -->\n" +
                            "                                                </div>\n" +
                            "                                            </div>\n" +
                            "                                            <!-- 画布模板 end -->\n" +
                            "\n" +
                            "                                        </div>\n" +
                            "\n" +
                            "                                    <!-- template 模板-->\n" +
                            "                                        <div class=\"jtk-delete jtk-none \">删除节点</div>\n" +
                            "                                        <div id=\"template\" class=\"jtk-none\">\n" +
                            "                                            <div class=\"jtk-window jtk-node workfolw-node start-node\" id=\"{charts}\" data-type=\"EmptyEndEvent\">\n" +
                            "                                               <div class=\"node-wrapper\">\n" +
                            "                                                    <img src=\"${STATIC_URL}img/canvas/endpoint.png\" style=\"top: 5px;left: 20px;position: absolute;\">\n" +
                            "                                                </div>\n" +
                            "                                            </div>\n" +
                            "                                             <div class=\"jtk-window jtk-node workfolw-node start-node\" id=\"{charts}\" data-type=\"EmptyStartEvent\">\n" +
                            "                                                <div class=\"node-wrapper\">\n" +
                            "                                                    <img src=\"${STATIC_URL}img/canvas/Start.png\" style=\"top: 5px;left: 20px;position: absolute;\">\n" +
                            "                                                </div>\n" +
                            "                                            </div>\n" +
                            "                                            <div class=\"jtk-window jtk-node workfolw-node database-node\" id=\"{charts}\" data-type=\"ServiceActivity\">\n" +
                            "                                                <div class=\"node-wrapper\">\n" +
                            "                                                    <div class=\"node-content\" style=\"position: relative\">\n" +
                            "                                                        <div class=\"start_time\"\n" +
                            "                                                             style=\"position: absolute;width: 70px;height: 20px;top: -26px;left: 0px;\"></div>\n" +
                            "                                                        <div class=\"end_time\"\n" +
                            "                                                             style=\"position: absolute;width: 70px;height: 20px;top: -26px;right: 0px;\"></div>\n" +
                            "                                                        <p class=\"node-title\" style=\" overflow: hidden;text-overflow:ellipsis;white-space: nowrap;\"></p>\n" +
                            "                                                    </div>\n" +
                            "                                                    <div class=\"node-icon\" style=\"top: 26px;width: 100%;height: 100%;\">\n" +
                            "                                                        <span class=\"title\" style=\"top: -14px;height: 100%;position: relative;color: #F4FFF9;\"></span>\n" +
                            "                                                    </div>\n" +
                            "                                                </div>\n" +
                            "                                            </div>\n" +
                            "                                           <div class=\"jtk-window jtk-node workfolw-node start-node\" id=\"{charts}\" data-type=\"ConvergeGateway\">\n" +
                            "                                                 <div class=\"node-wrapper\">\n" +
                            "                                                    <img src=\"${STATIC_URL}img/canvas/convergegateway.png\">\n" +
                            "                                                </div>\n" +
                            "                                            </div>\n" +
                            "                                            <div class=\"jtk-window jtk-node workfolw-node start-node\" id=\"{charts}\" data-type=\"ParallelGateway\">\n" +
                            "                                                <div class=\"node-wrapper\">\n" +
                            "                                                    <img src=\"${STATIC_URL}img/canvas/ParallelGateway.png\">\n" +
                            "                                                </div>\n" +
                            "                                            </div>\n" +
                            "                                            <div class=\"jtk-window jtk-node workfolw-node cog-node\" id=\"{charts}\"\n" +
                            "                                                 data-type=\"dataCog\">\n" +
                            "                                                <div class=\"node-wrapper\">\n" +
                            "                                                    <div class=\"node-content\">\n" +
                            "                                                        <p class=\"node-title\"></p>\n" +
                            "                                                    </div>\n" +
                            "                                                    <div class=\"node-icon\">\n" +
                            "                                                        <i class=\"bk-icon icon-cog\"></i>\n" +
                            "                                                    </div>\n" +
                            "                                                </div>\n" +
                            "                                            </div>\n" +
                            "\n" +
                            "                                            <div class=\"jtk-window jtk-node workfolw-node filter-node\" id=\"{charts}\"\n" +
                            "                                                 data-type=\"dataFilter\">\n" +
                            "                                                <div class=\"node-wrapper\">\n" +
                            "                                                    <div class=\"node-content\">\n" +
                            "                                                        <p class=\"node-title\"></p>\n" +
                            "                                                    </div>\n" +
                            "                                                    <div class=\"node-icon\">\n" +
                            "                                                        <i class=\"bk-icon icon-circle\"></i>\n" +
                            "                                                    </div>\n" +
                            "                                                </div>\n" +
                            "                                            </div>\n" +
                            "                                        </div>\n" +
                            "                                    </div>"
                        $('#flow_canvas').html(aa)
                        vm.location = res.data.activities
                        vm.line = res.data.flows
                        //显示流程单元中的预览图
                        $('#flow1').dataflow({
                            el: '.tool', //流程拖动源
                            canvas: '#canvas', //画布
                            arrowWidth: 8,
                            arrowHeight: 10,
                            template: '#template',
                            data:
                                {
                                    "line": vm.line, "location": vm.location
                                }
                        });
                        let old_html = $('#canvas').html()
                        $('#canvas').html('<div style="transform: scale(0.65)">' + old_html + '</div>')
                    }
                }).catch(function (e) {
                    vm.$message.error('获取数据失败！');
                });
            },
            node_name(value) {
                axios({
                    method: 'post',
                    url: site_url+'monitor_item/node_name/',
                    data: {
                        'id': value
                    }
                }).then(function (res) {
                    vm.activities_node_name = res.data.activities
                }).catch(function (e) {
                    vm.$message.error('获取数据失败！');
                });
            },
            Rendering_start_time() {
                $('p:contains(' + vm.flow.node_name + ')').parent().find('.start_time').text(vm.activities_node_time.start_time)
            },
            Rendering_end_time() {
                $('p:contains(' + vm.flow.node_name + ')').parent().find('.end_time').text(vm.activities_node_time.end_time)
            },
            canvas_new() {
                if (vm.liucheng == 'block') {
                    var node_id = ''
                    var start_time = ''
                    var end_time = ''
                    var node_times = []
                    for (var i = 2; i <= vm.location.length - 1; i++) {
                        var node_time = {}
                        node_time.node_id = vm.location[i].id ,
                            node_time.starttime = $('#' + vm.location[i].id + '').find('.start_time').text(),
                            node_time.endtime = $('#' + vm.location[i].id + '').find('.end_time').text()
                        node_time.node_name = $('#' + vm.location[i].id + '').find('.node-title').text()
                        node_times.push(node_time)
                    }
                    var period = $('#period').val()
                    var template_list = vm.template_list
                    axios({
                        method: 'post',
                        url: site_url+'monitor_item/start_flow_task/',
                        data: {
                            'period': period,
                            'template_list': template_list,
                            'node_times': node_times,
                            'monitor_name': vm.monitor_name,
                            'monitor_type': vm.monitor_type,
                            'constants': vm.constants
                        }
                    }).then(function (res) {
                        setInterval(function () {
                            axios({
                                method: 'post',
                                url: site_url+'monitor_item/node_state/',
                                data: {
                                    'item_id': res.data
                                }
                            }).then(function (res) {
                                len = res.data.message.length
                                for (var i = 0; i <= len - 1; i++) {
                                    data_key = res.data.message[i].data_value
                                    if (data_key == '1' || data_key == '4') {
                                        $('p:contains(' + res.data.message[i].data_key + ')').parent().siblings('.node-icon').css('background', '#67c23a')
                                    } else if (data_key == '0' || data_key == '2' || data_key == '3') {
                                        $('p:contains(' + res.data.message[i].data_key + ')').parent().siblings('.node-icon').css('background', '#f56c6c')
                                    }
                                }
                            }).catch(function (e) {
                                vm.$message.error('获取数据失败！');
                            });
                        }, 13000)
                    }).catch(function (e) {
                        vm.$message.error('获取数据失败！');
                    });
                } else if (vm.liucheng == 'none') {
                    var period = $('#period').val()
                    var template_list = vm.template_list
                    axios({
                        method: 'post',
                        url: site_url+'monitor_item/flow_gather_test/',
                        data: {}
                    }).then(function () {
                    }).catch(function (e) {
                        vm.$message.error('获取数据失败！');
                    });
                }
            },
            clear_review(){
                $("#text2").html("");
                $("#base_test_text").html("");
            },
            add_unit(row) {   //新增监控项
                {
                    if (vm.add_pamas == 1) {
                        vm.Initialization()
                    }
                    // 初始化清空预览
                    vm.clear_review();
                    vm.add_pamas = 0;
                    vm.monitor_name = '';
                    //取消默认添加时展示基本监控项
                    vm.disabled2 = false;
                    vm.disabled3 = false;
                    //vm.disabled4 = false;
                    //vm.disabled5 = false;
                    vm.disabled6 = false;
                    //vm.monitor_type = 'first';
                    //默认添加时展示基本监控项（修改后）
                    //监控项类型设置
                    this.monitor_type = 'five';
                    //数据来源选项默认切换为接口
                    this.sql_file_interface = 9;
                    //采集参数gather_params默认置为interface
                    this.base['gather_params'] = 'interface';
                    //切换基本监控项的数据来源类型展示不同的内容，默认切换为接口
                    this.base_gather_source_change('interface');
                    //--------------------------
                    vm.unit_id = row;
                    vm.centerDialogVisible = true;
                    //取消原有基本监控项时默认加载数据库连接信息
                    this.get_db_connections();
                }
            },
            del() {
                vm.edit(0)
            },
            change1(value) {
                if (value == 3) {
                    vm.sql1 = 'block';
                    vm.file1 = 'none';
                    vm.interface1 = 'none';
                    vm.server_url = '';
                    vm.file_param = '';
                    vm.basic.gather_rule = '';
                    vm.basic.gather_params = 'sql';
                    //修改后的基本监控项的采集类型设置
                    vm.base.gather_params = 'sql';
                    //----------------------------
                } else if (value == 6) {
                    vm.typeid = '2';
                    vm.sql1 = 'none';
                    vm.file1 = 'block';
                    vm.interface1 = 'none';
                    vm.server_url = '';
                    vm.file_param = '';
                    vm.basic.gather_rule = '';
                    vm.basic.gather_params = 'file';
                    //修改后的基本监控项的采集类型设置
                    vm.base.gather_params = 'file';
                    //----------------------------
                } else if (value == 9) {
                    vm.typeid = '3';
                    vm.sql1 = 'none';
                    vm.file1 = 'none';
                    vm.interface1 = 'block';
                    vm.server_url = '';
                    vm.file_param = '';
                    vm.basic.gather_rule = '';
                    vm.basic.gather_params = 'interface';
                    //修改后的基本监控项的采集类型设置
                    vm.base.gather_params = 'interface';
                    //----------------------------
                }
            },
            change2(value) {
                if (value == 1) {
                    vm.zuoye = 'block';
                } else {
                    vm.zuoye = 'none';
                }
            },
            change3(value) {
                if (value == 1) {
                    vm.liucheng = 'block';
                } else {
                    vm.liucheng = 'none';
                }
            },
            change4() {
                if (vm.basic.score > 100) {
                    vm.basic.score = 100
                } else if (vm.base.score > 100) {
                    vm.base.score = 100
                }
            },
            change_job_fontSize() {       //修改作业单元中预览字体
                $('#job_text').find("*").css('font-size', this.job.font_size);
            },
            change_job_height() {       //修改作业单元中预览高度
                $('#job_text').css('height', this.job.height);
            },
            change_job_width() {       //修改作业单元中预览宽度
                $('#job_text').css('width', this.job.width);
            },
            change_job_contents() {       //作业单元显示内容
                let contents = vm.job.contents;
                let job_status = contents.split('@')[1].split('=')[1];
                let item_id = 'item_id'
                var job_params = {
                    'id': item_id,
                    'width': vm.job.width,
                    'height': vm.job.height,
                    'status': job_status,
                };
                $('#job_text').html('');
                $('#job_text').append('<div type=\"job' + item_id + '\" style=\"margin:0 auto;\"></div>');
                job_monitor_active(job_params);
            },
            job_test() {
                vm.disabled1 = true;
                setTimeout(function () {
                    vm.disabled1 = false;
                }, 3000);
                var job_params1 = {
                    'id': 'item_id',
                    'width': vm.job.width,
                    'height': vm.job.height,
                    'status': 2,
                };
                $('#job_text').html('');
                $('#job_text').append('<div type=\"jobitem_id\" style=\"margin:0 auto;\"></div>');
                job_monitor_active(job_params1);
                axios({
                    url: site_url+'monitor_item/job_test/',
                    method: 'post',
                    data: {
                        'gather_params': vm.job.gather_params,
                        'job_id': vm.job.gather_rule,
                        'params': vm.job.params,
                    },
                }).then((res) => {
                    let status = res['data']['result'];
                    let job_status = 0;
                    switch (status) {
                        case true:
                            job_status = 1;
                            console.log(1)
                            break;
                        case false:
                            job_status = -1;
                            console.log(-1)
                            break;
                        default:
                            job_status = 2;
                            console.log(2)
                    }
                    let item_id = 'item_id'
                    var job_params = {
                        'id': item_id,
                        'width': vm.job.width,
                        'height': vm.job.height,
                        'status': job_status,
                    };
                    $('#job_text').html('');
                    $('#job_text').append('<div type=\"job' + item_id + '\" style=\"margin:0 auto;\"></div>');
                    job_monitor_active(job_params);
                }).catch(function (e) {
                    vm.$message.error('获取数据失败！');
                });
            },
            rowclass({row, rowIndex}) {
                return 'background:#F7F7F7'
            },
            font_size() {        //修改流程单元中的表字体
                $("#canvas").find('*').css("font-size", this.flow.font_size)
            },
            flow_height() {      //修改流程单元中的高
                $("#canvas").find('*').css("height", this.flow.height)
            },
            flow_width() {       //修改流程单元中的宽
                $("#canvas").find('*').css("width", this.flow.height)
            },
            get_db_connections() {
                axios({
                    url: site_url+'db_connection/get_all_db_connection/',
                    method: 'post',
                }).then((res) => {
                    let json = [];
                    if (res.data.results.length > 0) {
                        for (let i = 0; i < res.data.results.length; i++) {
                            let j = {};
                            j.value = res.data.results[i].id;
                            j.label = res.data.results[i].connname;
                            json.push(j);
                        }
                        ;
                        this.sites1 = json;
                    }
                }).catch(function (e) {
                    vm.$message.error('获取数据失败！');
                });
            },
            //初始化
            Initialization() {
                Object.assign(vm.basic, {});
                Object.assign(vm.basic, vm.basic1);
                Object.assign(vm.job, {});
                Object.assign(vm.job, vm.job1);
                Object.assign(vm.flow, {});
                Object.assign(vm.flow, vm.flow7);
                Object.assign(vm.chart, {});
                Object.assign(vm.chart, vm.chart1);
                vm.server_url = '';
                vm.file_param = '';
                vm.sql_file_interface = 3
            },
            //显示图标
            show_chart() {
                if (this.myChart != null && this.myChart != "" && this.myChart != undefined) {
                    this.myChart.dispose();
                }
                if (vm.chart.gather_params == "饼图") {
                    this.myChart = echarts.init(document.getElementById('maintenancePie'), 'macarons');
                    let legendData = [];
                    for (let i = 0; i < vm.chartData.length; i++) {
                        this.$set(legendData, i, vm.chartData[i].name);
                    }
                    option = {
                        tooltip: {
                            trigger: 'item',
                            formatter: "{a} <br/>{b} : {c} ({d}%)"
                        },
                        legend: {
                            type: 'scroll',
                            orient: 'vertical',
                            right: 10,
                            bottom: 50,
                            data: legendData
                        },
                        series: [
                            {
                                name: vm.person_count,
                                type: 'pie',
                                radius: '50%',
                                center: ['50%', '30%'],
                                data: vm.chartData,
                                itemStyle: {
                                    emphasis: {
                                        shadowBlur: 10,
                                        shadowOffsetX: 0,
                                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                                    }
                                },
                                avoidLabelOverlap: false,
                                label: {
                                    normal: {
                                        show: true,
                                        position: 'inside',
                                        formatter: '{c}'
                                    }
                                },
                                labelLine: {
                                    normal: {
                                        show: false
                                    },
                                    emphasis: {
                                        show: true
                                    }
                                }
                            }
                        ]
                    };
                    this.myChart.setOption(option);
                }
                if (vm.chart.gather_params == "柱状图") {
                    this.myChart = echarts.init(document.getElementById('maintenancePie'), 'macarons');
                    let barX = [];
                    let barCount = [];
                    for (var i = 0; i < vm.chartData.length; i++) {
                        this.$set(barX, i, vm.chartData[i].name);
                        this.$set(barCount, i, vm.chartData[i].value);
                    }
                    option = {
                        tooltip: {
                            trigger: 'axis',
                            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                                type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                            }
                        },
                        barWidth: 15,
                        legend: {
                            data: ['已执行'],
                            bottom: 10,
                            right: 30
                        },
                        grid: {
                            left: '3%',
                            right: '4%',
                            top: 10,
                            containLabel: true
                        },
                        xAxis: {
                            type: 'category',
                            data: barX
                        },
                        yAxis: {
                            type: 'value'
                        },
                        series: [
                            {
                                name: vm.person_count,
                                type: 'bar',
                                data: barCount
                            },
                        ]
                    };
                    this.myChart.setOption(option);
                }
                if (vm.chart.gather_params == "折线图") {
                    this.myChart = echarts.init(document.getElementById('maintenancePie'), 'macarons');
                    let lineX = [];
                    let lineCount = [];
                    for (var i = 0; i < vm.chartData.length; i++) {
                        this.$set(lineX, i, vm.chartData[i].name);
                        this.$set(lineCount, i, vm.chartData[i].value);
                    }
                    option = {
                        tooltip: {
                            trigger: 'axis'
                        },
                        legend: {
                            data: [vm.person_count]
                        },
                        calculable: true,
                        xAxis: [
                            {
                                type: 'category',
                                boundaryGap: false,
                                data: lineX
                            }
                        ],
                        yAxis: [
                            {
                                type: 'value'
                            }
                        ],
                        series: [
                            {
                                name: vm.person_count,
                                type: 'line',
                                smooth: true,
                                itemStyle: {normal: {areaStyle: {type: 'default'}}},
                                data: lineCount
                            },
                        ]
                    };
                    this.myChart.setOption(option);
                }
                vm.echart_height();
                vm.echart_width();
            },
            show_content() {
                let content = vm.chart.contents;
                let obj = JSON.parse(content);
                let echartData = [];
                for (let i = 0; i < obj.X.v.length; i++) {
                    let obj_1 = {};
                    obj_1.name = obj.X.v[i];
                    obj_1.value = obj.Y.v[i];
                    this.$set(echartData, i, obj_1);
                }
                vm.chartData = echartData;
                vm.show_chart();
                vm.echart_height();
                vm.echart_width();
            },
            chart_get_test() {
                //20190508 彭英杰 处理图表显示 start
                var tab = $("div[role='tablist']");
                if (tab.length > 0) { //判断是否存在
                    var ar_tab = tab.find("div[aria-selected='true']");
                    if (ar_tab.length > 0) {//判断是否选择
                        var id = ar_tab[0].id;
                        if (id == "tab-second") {//为图表监控项
                            //pane-second
                            // maintenancePie 展示页面
                            //required
                            //vm.chart.gather_rule
                            if (vm.chart.gather_rule != "") {
                                $("#pane-second maintenancePie").load(vm.chart.gather_rule)
                            }
                            return;
                        }
                    }
                }

                //20190508 彭英杰 处理图表显示 end
                axios({
                    url: site_url+'monitor_item/chart_get_test/',
                    method: 'post',
                    data: {
                        database_id: vm.chart.params,
                        sql: vm.chart.gather_rule,
                    },
                }).then((res) => {
                    if (res.data.result) {
                        this.$message({
                            message: '数据采集成功，请选择图表类型进行查看！',
                            type: 'success',
                            center: true
                        })
                    } else {
                        this.$message({
                            message: '数据采集失败，请检查数据配置或采集规则！',
                            type: 'warning',
                            center: true
                        })
                    }
                    vm.chartData = res.data.results;
                    vm.person_count = res.data.column_name_list[0];
                    vm.show_chart();
                    vm.echart_height();
                    vm.echart_width();
                }).catch(function (e) {
                    vm.$message.error('获取数据失败！');
                });
            },
            echart_height() {
                $('#maintenanceIndex').find("canvas").css('height', vm.chart.height);
            },
            echart_width() {
                $('#maintenanceIndex').find("canvas").css('width', vm.chart.width)
            },
            base_height_change() {
                collection_base_height_change(vm, '#base_test_text');
            },
            base_width_change() {
                collection_base_width_change(vm, '#base_test_text');
            },
            switch_change(value) {
                axios({
                    method: 'post',
                    url: site_url+'monitor_item/change_status/',
                    data: {
                        flag: value.status,
                        id: value.id,
                        monitor_name: value.monitor_name
                    },
                }).then((res) => {
                    if (res.data.code == 1) {
                        alert(res.data.message)
                    }
                }).catch(function (e) {
                    vm.$message.error('获取数据失败！');
                });
            },
            //获取指标集
            get_gather_info(value) {
                this.base.measures = '';
                this.base.measures_name = '';
                vm.iqube_name = [];
                //日志监控项模拟数据,目前一体化平台没有数据
                if ("get_log_type/" == value) {
                    var temp_json = {'label': 'zy-shangpin-initial', 'value': 'zy-shangpin-initial'};
                    vm.iqube_name.push(temp_json)
                } else {
                    vm.loading = true;
                    axios({
                        url: site_url+'iqube_interface/' + value,
                    }).then((res) => {
                        vm.gather_list = res.data.results;
                        for (let i = 0; i < res.data.results.length; i++) {
                            // 第一个
                            for (let j in res.data.results[i]) {
                                temp_json = {'label': j, 'value': j};
                                vm.iqube_name.push(temp_json)
                            }
                        }
                        //在第一次编辑的情况下，根据当前来源名称加载对应的候选度量值
                        if ('1' == vm.add_pamas && vm.loading == true) {
                            this.change_measures(vm.base['measures']);
                        }
                        vm.loading = false;
                    }).catch((res) => {
                        console.error("获取指标集失败" + res);
                        vm.loading = false;
                    });
                }
            },
            //获取指标名称
            change_measures(value) {
                //base_monitor_edit_init默认为true代表处于点击编辑后的数据初始化后的状态，
                //这种情况下不会清除其初始化好的度量值。如果不是数据初始化后的状态，
                // 而是通过手动点击来源名称下拉框的形式调用此函数，
                // 将会清空其度量值，避免在改变来源名称之后还是原来的度量值名称，
                // 导致度量值候选项中末尾出现暂无数据的BUG
                if (null != vm.base['measures_name'] || vm.base['measures_name'] != '') {
                    if (!this.base_monitor_edit_init || !this.base_monitor_add_init) {
                        vm.base['measures_name'] = '';
                    }
                }
                //日志监控项模拟数据
                if (this.base.interface_type == 'log') {
                    vm.metric_list = {0: 'system-init'};
                }
                //如果是点击编辑后的数据初始化时触发的此函数，base_monitor_edit_init标记
                //置为false，在下次触发change_measures函数时将清空度量值
                if (this.base_monitor_edit_init) {
                    if ('1' == vm.add_pamas) {
                        this.base_monitor_edit_init = false;
                    } else if ('0' == vm.add_pamas) {
                        this.base_monitor_add_init = false;
                    } else {
                        console.log('触发类型不是添加/修改！')
                    }
                }
                for (let i in vm.gather_list) {
                    for (let key in vm.gather_list[i]) {
                        if (key === value) {
                            vm.metric_list = vm.gather_list[i][key]['metric_list']
                            vm.dimension_list = vm.gather_list[i][key]['dimension_list']
                        }
                    }
                }
                console.log(vm.dimension_list);
            },
            //切换来源类型
            change_source_type(value) {
                if (value == 'log') {
                    vm.get_gather_info('get_log_type/')
                } else {
                    vm.get_gather_info('get_measures_type/')
                }
            },
            //一体化监控项采集测试校验（必填校验）
            collection_test_validate(){
                if(vm.base.interface_type == ""){
                    vm.$alert("请选择数据来源类型","提示");
                    return false;
                }else
                if(vm.base.measures == ""){//来源名称
                    vm.$alert("请选择数据来源名称","提示");
                    return false;
                }else
                if(vm.base.measures_name == ""){//度量值
                    vm.$alert("请选择数度量值","提示");
                    return false;
                }else
                if(vm.base.show_rule_type == ""){//展示规则
                    vm.$alert("请选择数展示规则","提示");
                    return false;
                }else if(vm.base.gather_rule == ""){//采集规则
                    vm.$alert("请录入采集规则","提示");
                    return false;
                }else if(vm.base.show_rule_type == "0"){//选百分比校验
                    if(vm.base.gather_rule != "" && vm.base.gather_rule !="100" && vm.base.gather_rule !="1000"){
                        vm.$alert("百分比采集规则的值只能是'100'或'1000'","提示");
                        return false;
                    }
                }else if(vm.base.show_rule_type == "1" || vm.base.show_rule_type == "2"){//选颜色和其它校验
                    var filter=/^\r|\n\r|\n$/;
                    if(filter.test(vm.base.gather_rule)){
                        vm.$alert("采集规则中不能包含有空行","提示");
                        return false;
                    }
                }
                return true;
            },
            //采集测试方法
            base_cell_test() {
                if(vm.collection_test_validate()){
                    //同步获取采集数据
                    vm.get_gather_test();
                    //预览采集，调用预览组件
                    preview_monitor_item(vm, 'monitor_item', "#base_test_text");
                    base_monitor_show_reset();
                }
            },
            change_data_sources(value) {
                if (value == 9) {
                    //接口类型
                    vm.file_show = false;
                    vm.interface_show = true;
                    vm.database_show = false;
                    vm.change1(9);
                } else if (value == 6) {
                    //文件
                    vm.file_show = true;
                    vm.interface_show = false;
                    vm.database_show = false;
                    vm.change1(6);
                } else if (value == 3) {
                    //数据库
                    vm.change1(3);
                    vm.file_show = false;
                    vm.interface_show = false;
                    vm.database_show = true;
                }
            },
            // 预览类容编辑
            // 采集表中保存的是实际调用一体化平台的返回的结果，在场景编排中再根据展示规则还原预览效果
            content_change() {
                collection_content_change(vm, "#base_test_text")
            },
            //jlq-2019-05-16-add
            //监控项名称不重复
            monitorName(){
                axios({
                    method: 'post',
                    url: site_url+'monitor_item/verify_name_only/',
                    data:{
                        name:vm.monitor_name,
                        id:vm.unit_id
                    }
                }).then(function (res) {
                    //flag=res.message
                    //alert(res);
                    console.log(res);
                    if(res.data.message == false){
                      //  alert('111');
                       // new Error('监控项名称不能重复')
                       //vm.message = '监控项名称不能重复';
                      // this.$alert(vm.message, "错误");
                        vm.isShow = true;
                    }else{
                        vm.isShow = false;
                    }
                }).catch(function (e) {
                    vm.$message.error('获取数据失败！');
                });
            }

        },
        mounted() {
            this.get_header_data()
            this.get_all_area()
        },
        watch: {
            'basic.gather_rule': function (oldval, newval) {//展示内容探测狗
                fs = oldval.split('@')
                vm.fields = []
                for (var i = 1; i < fs.length; i += 2) {
                    vm.fields.push(fs[i].split("=")[0])
                }
            },
            "monitor_type":function(value){//tab页切换探测狗
               if(value == "first"){
                   //vm.change1(3);
                   vm.sql_file_interface = 3
               }
               if(value == "five"){
                   //vm.change_data_sources(9);
                   vm.sql_file_interface = 9
               }
            }
        }
    });
    vm.show();
    setInterval(function () {
        $('input[type=number]').keypress(function (e) {
            if (!String.fromCharCode(e.keyCode).match(/[0-9\.]/)) {
                return false;
            }
        });
    }, 1)
})