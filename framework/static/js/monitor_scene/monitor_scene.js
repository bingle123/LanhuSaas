var vm = null;
var site_url = "";
$(function () {
    //csrf验证
    axios.interceptors.request.use((config) => {
        config.headers['X-Requested-With'] = 'XMLHttpRequest';
        let regex = /.*csrftoken=([^;.]*).*$/; // 用于从cookie中匹配 csrftoken值
        config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
        return config
    });
    vm = new Vue({
        el: '.content',
        data: {
            //场景编排数据为空提示信息标志
            scene_empty_data_display:false,
            //场景编排搜索框是否可见
            scene_basic_search_display: false,
            //场景编排基本监控项的检索条件
            basic_search: '',
            scene_font_color: '#AAAAAA',
            page_count: 1,//分页总页数
            page: 1,                                   //分页页码数
            start_time: '8:00',
            end_time: '16:00',
            falg: false,
            selectvalue: '',
            search: '',//搜索框的值
            isAdd: 1,
            line_flag: 0,
            canvas_flag: 0,
            lines: [],
            pre_id: 0,
            areas: [],
            imgUrl: './static/1.png',
            chartData: {
                columns: ['日期', '下单用户'],
                rows: [
                    {'日期': '1/1', '下单用户': 1093},
                    {'日期': '1/2', '下单用户': 3230},
                    {'日期': '1/3', '下单用户': 2623},
                    {'日期': '1/4', '下单用户': 1423},
                    {'日期': '1/5', '下单用户': 3492},
                    {'日期': '1/6', '下单用户': 4293}
                ]
            },
            value9: [4, 5],
            textarea: '',
            currentPage1: 5,
            currentPage2: 5,
            currentPage3: 5,
            currentPage4: 4,
            tableData: [],
            pos: [],//岗位
            scene: {                            //场景管理
                scene_name: '', //场景名称
                scene_startTime: '',
                pos_name: '',
                scene_endTime: '',
                area: 1,
            },
            scene1: {                            //场景管理
                scene_name: '', //场景名称
                scene_startTime: '',
                pos_name: '',
                scene_endTime: '',
                area: 1,
            },
            scene_edit: {                       //编辑页面中的
                id: '',
                scene_name: '', //场景名称
                pos_name: '',//岗位
                scene_startTime: '',
                scene_endTime: '',
                area: 1,
                scene_content: '',
            },
            rules: {
                scene_name: [
                    {required: true, message: '请输入场景名称', trigger: 'blur'}
                ],
                pos_name: [
                    {required: true, message: '请选择岗位', trigger: 'change'}
                ],
                scene_startTime: [
                    {type: 'string', required: true, message: '请选择开始时间', trigger: 'change'}
                ],
                scene_endTime: [
                    {type: 'string', required: true, message: '请选择结束时间', trigger: 'change'}
                ]
            },
            result_list: [],                 //保存场景与其对应监控项信息
            result_list_edit: [],            //获取场景及其监控项信息
            base_page_count: 0,              //初始化总页数
            chart_page_count: 0,              //初始化总页数
            job_page_count: 0,              //初始化总页数
            flow_page_count: 0,              //初始化总页数
            monitor_type: 0,              //判断是那种监控项
            page1: 1,              //初始化默认页码
            limit: 4,              //限制每页显示条数
            base_monitor: [],              //基本监控项的信息列表
            chart_monitor: [],              //图表监控项的信息列表
            job_monitor: [],              //作业监控项的信息列表
            flow_monitor: [],              //流程监控项的信息列表
            drigging_id: 1,      //画布拖动元素id
            show_num: 0,         //关闭场景编辑页面时返回上一步
            monitor_data: [],        //接受监控项的具体数据
            scale: 1,            //比例
            multiple: 0,         //限制比例的参数
            bl_search:true, //判断是否为搜索
        },
        methods: {
            //场景编排模糊检索
            scene_search: function(type, value){
                //每次检索时，默认不显示数据空的提示信息，在获取内容时再根据数据长度是否显示提示
                vm.scene_empty_data_display = false;
                if('basic' == type){
                    const loading = this.popup_loading();
                    var data = {
                        'type' : 'basic',
                        'condition': vm.basic_search,
                        'page' : value,
                        'limit' : '4'
                    };
                    axios({
                        method: 'post',
                        url: site_url + 'monitor_scene/monitor_scene_fuzzy_search/',
                        data: data
                    }).then(function (res) {
                        loading.close();
                        vm.base_monitor = res.data.results.base_list;
                        if(0 == vm.base_monitor.length){
                            vm.base_page_count = 0;
                            vm.scene_empty_data_display = true;
                        }else{
                            vm.base_page_count = res.data.results.base_list[0].page_count;
                        }
                    }).catch(function (e) {
                        loading.close();
                        vm.$message.error('监控项信息检索失败！');
                    });
                }
            },
            //显示加载中..背景
            popup_loading: function(){
                return this.$loading({
                    lock: true,
                    text: '正在拼命加载中...',
                    spinner: 'el-icon-loading',
                    background: 'rgba(0, 0, 0, 0.7)'
                });
            },
            //变更场景颜色
            change_scene_color: function(){
                $('.monitor_content').css('color', vm.scene_font_color);
                //$('.Drigging').css('border-color', vm.scene_font_color);
            },
            sizeStrFun: function () {
                //菜单 放大 缩小
                var html = "<span onclick='vm.changeSizeFun(this,1)'>放大</span>" +
                    "<span onclick='vm.changeSizeFun(this,2)'>缩小</span>";
                return html;
            },
            changeSizeFun(obj, type) {
                //放大的功能
                var dto = $(obj).parent().parent();
                var num = dto.css("transform");
                if (num == undefined
                    || num == "none") {
                    num = 1;
                } else {
                    var str = dto.attr("style");
                    var arrStr = str.split("transform");
                    var str1 = arrStr[1].substring(arrStr[1].indexOf("(") + 1, arrStr[1].indexOf(")"));
                    num = parseFloat(str1);
                }
                var numTotal = parseFloat(num) + 0.1;//原来基本上放大
                if (type == 2) {//原来基本上缩小
                    numTotal = parseFloat(num) - 0.1;
                }
                if (numTotal >= 0.1) {
                    dto.css("transform", "scale(" + numTotal + ")");
                }
            },
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        const loading = this.popup_loading();
                        // 新增场景
                        if (formName == 'scene') {
                            axios({
                                method: 'post',
                                url: site_url + 'monitor_scene/addSence/',
                                data: {
                                    data: vm.scene,
                                    monitor_data: vm.result_list
                                }
                            }).then(function (res) {
                                loading.close();
                                if(res.data.scene_name){
                                    vm.$alert("场景名称"+"'"+res.data.scene_name+"'"+"已经存在，请修改场景名称进入编排功能",'错误')
                                    return false;
                                }
                                /*
                                //上传当前场景字体颜色设置
                                var color_info = {
                                    'scene_id' : res.data.scene_id,
                                    'type' : 'add',
                                    'scene_color' : vm.scene_font_color
                                };
                                axios({
                                    method: 'post',
                                    url: site_url + 'monitor_scene/scene_color_save/',
                                    data: color_info
                                }).then(function (res) {
                                    loading.close();
                                    //上传场景颜色后，场景颜色恢复默认值
                                    vm.scene_font_color = '#AAAAAA';
                                }).catch(function (e) {
                                    loading.close();
                                    //上传场景颜色失败后，场景颜色恢复默认值
                                    vm.scene_font_color = '#AAAAAA';
                                    vm.$message.error('场景颜色上传失败！');
                                });*/
                                vm.isAdd = 1;
                                vm.select_table();
                                 //打开场景编辑器
                                window.open(site_url+"monitor_scene/edit_flow_graph/");
                            }).catch(function (e) {
                                loading.close();
                                vm.$message.error('获取数据失败！');
                            });
                        } else if (formName == 'scene_edit') {
                            //上传当前场景字体颜色设置
                            var color_info = {
                                'scene_id' : vm.scene_edit['id'],
                                'type' : 'edit',
                                'scene_color' : vm.scene_font_color
                            };
                            axios({
                                method: 'post',
                                url: site_url + 'monitor_scene/editSence/',
                                data: {
                                    data: vm.scene_edit,
                                    monitor_data: vm.result_list
                                }
                            }).then(function (res) {
                                //jlq-2019-05-29-add-修改场景名称不重复
                                loading.close();
                                if(res.data.scene_name){
                                    vm.$alert("场景名称"+"'"+res.data.scene_name+"'"+"已经存在，请修改场景名称进入编排功能",'错误')
                                    return false;
                                }
                                if(res.data.result == "success"){
                                    vm.$alert("场景修改成功！","提示")
                                }
                                axios({
                                    method: 'post',
                                    url: site_url + 'monitor_scene/scene_color_save/',
                                    data: color_info
                                }).then(function (res) {
                                    loading.close();
                                }).catch(function (e) {
                                    loading.close();
                                    vm.$message.error('场景颜色上传失败！');
                                });
                                vm.isAdd = 1;
                                vm.select_table()
                            }).catch(function (e) {
                                loading.close();
                                vm.$message.error('获取数据失败！');
                            });
                        }
                        $('.monitor_content').html('');
                    } else {
                        console.log('提交失败!!');
                        return false;
                    }
                });

            },
            get_all_area() {
                axios({
                    method: 'get',
                    url: site_url + 'market_day/get_all_area',
                }).then(function (res) {
                    res = res.data.message
                    vm.areas = []
                    for (var i = 0; i < res.length; i++) {
                        var label = res[i].country + "(" + res[i].timezone + ")"
                        temp = {
                            'area': label,
                            'value': res[i].id
                        }
                        vm.areas.push(temp)
                    }
                }).catch(function (e) {
                    vm.$message.error('获取数据失败！');
                });
            },
            //初始加载数据
            current_change(value) {
                vm.bl_search =false
                vm.page = value;
                vm.paging()
            },
            paging() {
                if(vm.bl_search){
                    vm.page = 1
                }
                vm.bl_search = true
                axios({
                    method: 'post',
                    url: site_url + 'monitor_scene/paging/',
                    data: {
                        page: vm.page,
                        search:vm.search,
                        limit: 10
                    },
                }).then(function (res) {
                    //这里要注意，初始化是没有数据的
                    if(res.data.message && res.data.message.length > 0){
                        vm.tableData = res.data.message;
                        vm.page_count = res.data.message[0].page_count;
                    }else{
                        vm.tableData = res.data.message;
                        vm.page_count = 0;
                    }
                }).catch(function (e) {
                    vm.$message.error('获取数据失败！');
                });
            },
            rowclass({row, rowIndex}) {
                return 'background:#F7F7F7'
            },
            handleSizeChange(val) {
                console.log('每页' + val + '条')
            },
            handleCurrentChange(val) {
                console.log('当前页: ' + val + '')
            },
            //新增场景
            monitor_sence_add() {
                this.isAdd = 2;
                vm.sen_position()
                vm.scene = vm.scene1
                setTimeout(function () {
                    vm.Time()
                }, 100)
            },
            //场景修改
            monitor_sence_edit(row) {
                vm.scene_edit.id = row.id
                vm.scene_edit.scene_name = row.scene_name
                vm.scene_edit.scene_startTime = row.scene_startTime
                vm.scene_edit.scene_endTime = row.scene_endTime
                vm.scene_edit.pos_name = row.pos_name
                vm.scene_edit.area = row.scene_area
                vm.scene_edit.scene_content = row.scene_content
                this.isAdd = 3

                vm.sen_position()
                vm.monitore_edit_start(row.id)

                /*
                axios({
                    method: 'post',
                    url: site_url + 'monitor_scene/scene_color_get/',
                    data: row.id
                }).then((res) => {
                    vm.scene_font_color = res.data.color;
                }).catch(function (e) {
                    vm.$message.error('获取场景颜色设置失败！');
                });
                setTimeout(function () {
                    vm.Time()
                }, 100)*/
            },
            monitore_edit_start(value) {    //获取场景监控项信息
                const loading = this.popup_loading();
                $.ajax({
                    type: "POST",
                    data: JSON.stringify(value),
                    dataType: "JSON",
                    async: true,
                    url: site_url + "monitor_scene/scene_data/",
                    success: function (data) {
                        //防止空场景编辑异常
                        vm.result_list_edit = data.results;
                        vm.result_list = vm.result_list_edit;
                        if(data.results.length > 0){
                            vm.scale = parseFloat(data.results[0].scale);
                        }else{
                            //清空缓存
                            $(".monitor_content").html("");
                            vm.scale = parseFloat(1);
                        }
                        vm.multiple = Math.round((vm.scale - 1) * 10);
                        loading.close();
                    }
                })
            },
            hide: function (type) {
                //取消新增，还原新增录入界面的信息
                if(type == "add"){
                    vm.scene.scene_name = "";
                    vm.scene.area = 1;
                    vm.scene.scene_startTime = '';
                    vm.scene.scene_endTime = '';
                    vm.scene.pos_name = '';
                }
                //取消编辑，还原编辑界面的信息
                if(type == "edit"){
                    vm.scene_edit.scene_name = "";
                    vm.scene_edit.area = 1;
                    vm.scene_edit.scene_startTime = '';
                    vm.scene_edit.scene_endTime = '';
                    vm.scene_edit.pos_name = '';
                    vm.scene_edit.scene_content = '';
                }
                this.isAdd = 1;
                vm.paging();
                vm.canvas_flag = 0;
                $('.monitor_content').html('');
                //每次取消，将缓存的数据清空
                vm.result_list_edit = [];
                //退出场景编辑后，颜色重置
                vm.scene_font_color = '#AAAAAA';
            },
            async goto() {
                //场景名称
                let scene_name = encodeURIComponent(vm.scene_edit.scene_name);
                //场景XML
                let scene_content = encodeURIComponent(vm.scene_edit.scene_content);
                //打开场景编辑器并带上场景id
                window.open(site_url+"monitor_scene/edit_flow_graph/");
            },
            monitor_edit_close() {
                $('.monitor_edit').css('display', 'none');
                vm.isAdd = vm.show_num;
                vm.show_num = 0;
            },
            a() {
                scene_name: ''//场景名称
                scene_startTime:''
                pos_name:''
                scene_endTime:''
            },
            select_table() {
                if (vm.search == "") {
                    vm.paging()
                } else {
                    vm.scene.scene_endTime = $(".back-bar").children().eq(2).html()
                    vm.scene.scene_startTime = $(".back-bar").children().eq(4).html()
                    axios({
                        method: 'post',
                        url: site_url + 'monitor_scene/select_table/',
                        data: vm.search
                    }).then(function (res) {
                        vm.tableData = res.data.message;
                    }).catch(function (e) {
                        vm.$message.error('获取数据失败！');
                    });
                }

            },
            del_scene(row) {
                this.$confirm('此操作将永久删除该监控项, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                    center: true,
                }).then(() => {
                    //删除场景字体颜色信息
                    axios({
                        method: 'post',
                        url: site_url + 'monitor_scene/scene_color_del/',
                        data: row.id
                    }).catch(function (e) {
                        vm.$message.error('场景颜色删除失败！');
                    });
                    axios({
                        method: 'post',
                        url: site_url + 'monitor_scene/del_scene/',
                        data: row.id
                    }).then((res) => {
                        this.$alert("场景删除成功！", "提示");
                        vm.paging();
                    });
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                });
            },
            //js定时调度（每5秒执行一次）
            Time() {
                setInterval(function () {
                    $(".back-bar").children().eq(1).mouseup(function () {
                        var low = -$(".back-bar").children().eq(2).html()
                        a = (Math.floor(low / 60) + 12) + ":" + ((1200 + low) % 60);
                        setTimeout(function () {
                            $(".back-bar").children().eq(2).html(a)
                            $(".back-bar").children().eq(2).show()
                        }, 100)
                    })
                    $(".back-bar").children().eq(3).mouseup(function () {
                        var high = $(".back-bar").children().eq(4).html()
                        b = (Math.floor(high / 60) + 12) + ":" + ((1200 + high) % 60);
                        setTimeout(function () {
                            $(".back-bar").children().eq(4).html(b)
                            $(".back-bar").children().eq(4).show()
                        }, 100)
                    })
                }, 500)
                $('.slider-input').jRange({
                    from: -1440,
                    to: 1440,
                    step: 1,
                    scale: ["-12:00", "00:00", "12:00", "24:00", "+12:00"],
                    format: '%s',
                    width: "300",
                    showLabels: true,
                    isRange: true
                })
            },
            sen_position() {
                axios({
                    method: 'post',
                    url: site_url + 'monitor_scene/pos_name/',
                }).then(function (res) {
                    vm.pos = res.data.message
                }).catch(function (e) {
                    vm.$message.error('获取数据失败！');
                });
            },
            //根据type类型展开具体的监控项，供场景编排使用
            show_monitor_item() {
                axios({
                    method: 'post',
                    url: site_url + 'monitor_scene/scene_show/',
                    data: {
                        limit: vm.limit,
                        type: vm.monitor_type,
                        page: vm.page1
                    },
                }).then((res) => {
                    console.log(res);
                    if (vm.monitor_type == 0) {
                        vm.base_monitor = res.data.results.base_list;
                        vm.chart_monitor = res.data.results.chart_list;
                        vm.job_monitor = res.data.results.job_list;
                        vm.flow_monitor = res.data.results.flow_list;
                        vm.base_page_count = res.data.results.base_list[0].page_count;
                        vm.chart_page_count = res.data.results.chart_list[0].page_count;
                        vm.job_page_count = res.data.results.job_list[0].page_count;
                        vm.flow_page_count = res.data.results.flow_list[0].page_count;
                    } else if (vm.monitor_type == 1) {
                        vm.base_monitor = res.data.results.base_list;
                        vm.base_page_count = res.data.results.base_list[0].page_count;
                    } else if (vm.monitor_type == 2) {
                        vm.chart_monitor = res.data.results.chart_list;
                        vm.chart_page_count = res.data.results.chart_list[0].page_count;
                    } else if (vm.monitor_type == 3) {
                        vm.job_monitor = res.data.results.job_list;
                        vm.job_page_count = res.data.results.job_list[0].page_count;
                    } else if (vm.monitor_type == 4) {
                        vm.flow_monitor = res.data.results.flow_list;
                        vm.flow_page_count = res.data.results.flow_list[0].page_count;
                    }
                }).catch(function (e) {
                    vm.$message.error('获取数据失败！');
                });
            },
            /**
             * 添加基本监控项
             * @param i
             */
            add_base_monitor(i) {
                var item = $('<div class=\"Drigging\" name=\"' + i.id + '\" type=\"basic' + i.id + '\" id=\"' + vm.drigging_id + '\" style=\"transform: scale(' + vm.scale + ')\"></div>');
                $('.monitor_content').append(item);
                //把当前监控项的内容赋值给vm对象，场景编排时，需要将编排的监控项根据展示规则还原成预览的效果
                vm.current_monitor_item = i;
                preview_monitor_item(vm ,"monitor_scene",".monitor_content");
                vm.drigging_id++ ;
                vm.change_scene_color();
                //对箭头及线条去除边框操作
                if(i.monitor_name.indexOf("箭头") != -1 || i.monitor_name.indexOf("线条") != -1){
                    item.css('border-width', 0);
                }else{
                    item.css('background-color', '#FFFFFF');
                    item.css('box-sizing', 'border-box');
                    item.css('padding-left', '16px');
                    item.css('padding-right', '16px');
                }
            },
            add_chart_monitor(i) {
                $('.monitor_content').append('<div class=\"Drigging\" name=\"' + i.id + '\" id=\"' + vm.drigging_id + '\" style=\"height:' + i.height + 'px;position: absolute;width:' + i.width + 'pxtransform: scale(' + vm.scale + ')\"><div id=\"chart' + i.id + '\" style=\"background:beige;height:' + (i.height - 2) + 'px;width:' + (i.width - 2) + 'px\"></div><input class="score_input" type="text" value="0"><div class="right_click"><span class="score">打分</span><span class="delete">删除监控项</span><span class="line">连线</span>' + vm.sizeStrFun() + '</div></div>')
                show_chart(i.id, "", "", i.gather_params, i.height, i.width, vm.drigging_id, i.contents);
                vm.drigging_id++;
            },
            add_job_monitor(i) {
                var job_params = {
                    'id': i.id,
                    'width': i.width,
                    'height': i.height,
                    'status': i.job_status,
                    'contents': i.contents
                }
                $('.monitor_content').append('<div class=\"Drigging\" name=\"' + i.id + '\" type=\"job' + i.id + '\" id=\"' + vm.drigging_id + '\" style=\"transform: scale(' + vm.scale + ')\"></div>')
                job_monitor(job_params)
                vm.drigging_id++;
            },
            add_flow_monitor(i) {
                let jion_id = [{
                    "id": i.jion_id
                }]
                $('.monitor_content').append('<div class=\"Drigging\" name=\"' + i.id + '\" id=\"' + vm.drigging_id + '\" style=\"transform: scale(' + vm.scale + ')\"><div type=\"flow_monitor' + vm.drigging_id + '\"></div></div>')
                flow_monitor(jion_id, vm.drigging_id)
                vm.drigging_id++;
            },
            current_change1(value) {
                vm.page1 = value;
                vm.monitor_type = 1;
                if('' != vm.basic_search){
                    vm.scene_search('basic', vm.page1);
                }else{
                    vm.show_monitor_item();
                }
            },
            current_change2(value) {
                vm.page1 = value;
                vm.monitor_type = 2;
                vm.show_monitor_item();
            },
            current_change3(value) {
                vm.page1 = value;
                vm.monitor_type = 3;
                vm.show_monitor_item();
            },
            current_change4(value) {
                vm.page1 = value;
                vm.monitor_type = 4;
                vm.show_monitor_item();
            },
            monitor_type_switch(value) {
                vm.monitor_type = value;
                vm.page1 = 1;
                vm.show_monitor_item();
                if(1 == vm.monitor_type){
                    vm.scene_basic_search_display = !vm.scene_basic_search_display;
                }
            }
        }
    });

    $('.monitor_type').click(function () {
        $(this).parent().next('div').animate({
            height: 'toggle'
        });
        $(this).parent().next('div').siblings('.monitor_list').animate({
            height: "hide"
        });
    });
    document.oncontextmenu = function () {
        return false;
    };
    document.onclick = function (e) {
        if (e.target.className != 'right_click') {
            $('.right_click').css('display', 'none');
        }
        if (e.target.className != 'score_input') {
            $('.score_input').css('display', 'none');
        }
    };
})
$(function () {
    $('.save').click(function () {
        var len = $('.Drigging').length;
        var order, item_id, x, y, score;
        var scale = 1.0, score = 0.0;
        vm.result_list = [];
        for (var i = 0; i < len; i++) {
            order = $('.Drigging').eq(i).attr('id');
            item_id = $('.Drigging').eq(i).attr('name');
            x = $('.Drigging').eq(i).position().left;
            y = $('.Drigging').eq(i).position().top;
            var style = $('.Drigging').eq(i).attr('style');
            if (style.indexOf('scale') > -1) {
                scale = parseFloat(style.split('scale')[1].substring(style.split('scale')[1].indexOf('(') + 1, style.split('scale')[1].indexOf(')')));
            }
            score = $('.Drigging').eq(i).find('.score_input').val();
            next_item = $('.Drigging').eq(i).data().next_item
            if (next_item == undefined) {
                next_item = 0
            }
            var data = {
                'order': order,
                'item_id': item_id,
                'x': x,
                'y': y,
                'scale': scale,
                'score': score,
                'next_item': next_item
            };
            vm.result_list.push(data);
        }
        vm.canvas_flag = 0;
        vm.lines = [];
    })
});
$(function () {
    site_url = $('#siteUrl').val();
    //flush_canvas();
    //获取节假日
    vm.get_all_area()
    //初始化查询
    vm.paging();
});
