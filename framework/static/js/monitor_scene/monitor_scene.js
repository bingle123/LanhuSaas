var vm = null;
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
            page_count: 100,//分页总页数
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
                        url: '/monitor_scene/monitor_scene_fuzzy_search/',
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
                        if (formName == 'scene') {
                            axios({
                                method: 'post',
                                url: '/monitor_scene/addSence/',
                                data: {
                                    data: vm.scene,
                                    monitor_data: vm.result_list
                                }
                            }).then(function (res) {
                                //上传当前场景字体颜色设置
                                var color_info = {
                                    'scene_id' : res.data.scene_id,
                                    'type' : 'add',
                                    'scene_color' : vm.scene_font_color
                                };
                                axios({
                                    method: 'post',
                                    url: '/monitor_scene/scene_color_save/',
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
                                });
                                vm.isAdd = 1;
                                vm.select_table();
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
                                url: '/monitor_scene/editSence/',
                                data: {
                                    data: vm.scene_edit,
                                    monitor_data: vm.result_list
                                }
                            }).then(function (res) {
                                axios({
                                    method: 'post',
                                    url: '/monitor_scene/scene_color_save/',
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
                    url: '/market_day/get_all_area',
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
                vm.page = value;
                vm.paging()
            },
            paging() {
                axios({
                    method: 'post',
                    url: '/monitor_scene/paging/',
                    data: {
                        page: vm.page,
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
                this.isAdd = 3
                vm.sen_position()
                vm.monitore_edit_start(row.id)
                axios({
                    method: 'post',
                    url: '/monitor_scene/scene_color_get/',
                    data: row.id
                }).then((res) => {
                    vm.scene_font_color = res.data.color;
                }).catch(function (e) {
                    vm.$message.error('获取场景颜色设置失败！');
                });
                setTimeout(function () {
                    vm.Time()
                }, 100)
            },
            monitore_edit_start(value) {    //获取场景监控项信息
                axios({
                    method: 'post',
                    url: '/monitor_scene/scene_data/',
                    data: value,
                }).then(function (res) {
                    console.log(res)
                    vm.result_list_edit = res.data.results;
                    vm.result_list = vm.result_list_edit;
                    vm.scale = parseFloat(res.data.results[0].scale);
                    vm.multiple = Math.round((vm.scale - 1) * 10);
                }).catch(function (e) {
                    vm.$message.error('获取数据失败！');
                });
            },
            hide: function () {
                this.isAdd = 1;
                vm.paging();
                vm.canvas_flag = 0;
                $('.monitor_content').html('');
                //退出场景编辑后，颜色重置
                vm.scene_font_color = '#AAAAAA';
            },
            async goto(type) {
                //新增
                if("1" == type){
                    //新增每次清空编排面板
                    $('.monitor_content').html() == '';
                    vm.result_list_edit = [];
                }
                vm.canvas_flag = 1;
                if ($('.monitor_content').html() == '') {//场景编排内容块无元素
                    $(".monitor_content").append('<canvas id="line_canvas" style="position: absolute;"></canvas>');
                    $('.monitor_edit').css('display', 'block');
                    vm.show_num = vm.isAdd;
                    vm.isAdd = 0;
                    let result_list_edit = vm.result_list_edit;
                    if(result_list_edit){
                        for (var i = 0; i < result_list_edit.length; i++) {
                            if (result_list_edit[i].next_item != 0) {
                                line = {
                                    'pid': result_list_edit[i].item_id,
                                    'nid': result_list_edit[i].next_item
                                }
                                vm.lines.push(line)
                            }
                        }
                    }
                    let max = 0;
                    let index = 0;
                    for (var i = 0; i < result_list_edit.length; i++) {
                        if (max < result_list_edit[i].order) {  //场景监控项拖拽元素唯一
                            max = result_list_edit[i].order;
                        }
                        //监控项类型1和5都为基本监控项
                        //1为原始基本监控项，5为一体化平台基本监控项
                        if (result_list_edit[i].monitor_type === 1 || result_list_edit[i].monitor_type === 5) {
                            let res = await axios({
                                method: 'post',
                                url: '/monitor_scene/monitor_scene_show/',
                                data: result_list_edit[i].item_id,
                            }).catch(function (e) {
                                vm.$message.error('获取数据失败！');
                            });
                            vm.monitor_data = res.data.results;
                            var item = $('<div class=\"Drigging\" name=\"' + result_list_edit[i].item_id + '\" type=\"basic' + result_list_edit[i].item_id + '\" id=\"' + result_list_edit[i].order + '\" style=\"top:' + result_list_edit[i].y + 'px;left:' + result_list_edit[i].x + 'px;transform: scale(' + result_list_edit[i].scale + ')\"></div>');
                            $('.monitor_content').append(item);
                            vm.current_monitor_item = vm.monitor_data[0];
                            preview_monitor_item(vm ,"monitor_scene",".monitor_content");
                            vm.drigging_id++ ;
                            id_value = parseInt(result_list_edit[i].item_id);
                            if(9000 <= id_value && id_value <= 10000){
                                item.css('border-width',0);
                            }else{
                                item.css('background-color', '#FFFFFF');
                                item.css('box-sizing', 'border-box');
                                item.css('padding-left', '16px');
                                item.css('padding-right', '16px');
                            }
                        }
                        if (result_list_edit[i].monitor_type === 2) {
                            let res = await axios({
                                method: 'post',
                                url: '/monitor_scene/monitor_scene_show/',
                                data: result_list_edit[i].item_id,
                            }).catch(function (e) {
                                vm.$message.error('获取数据失败！');
                            });
                            vm.monitor_data = res.data.results;
                            var txt = '<div class=\"Drigging\" name=\"' + result_list_edit[i].item_id + '\" id=\"' + result_list_edit[i].order + '\" style=\"background:beige;height:' + vm.monitor_data[0].height + 'px;width:' + vm.monitor_data[0].width + 'px;top:' + result_list_edit[i].y + 'px;left:' + result_list_edit[i].x + 'px;transform: scale(' + result_list_edit[i].scale + ')\"><div id=\"chart' + result_list_edit[i].order + '\" style=\"background:beige;height:' + (vm.monitor_data[0].height - 2) + 'px;width:' + (vm.monitor_data[0].width - 2) + 'px\"></div><input class="score_input" type="text" value="0"><div class="right_click"><span class="score">打分</span><span class="delete">删除监控项</span><span class="line">连线</span>' + vm.sizeStrFun() + '</div></div>';
                            $('.monitor_content').append();
                            show_chart(vm.monitor_data[0].id, "", "", vm.monitor_data[0].gather_params, vm.monitor_data[0].height, vm.monitor_data[0].width, result_list_edit[i].order, vm.monitor_data[0].contents);
                        }
                        if (result_list_edit[i].monitor_type === 3) {
                            let res = await axios({
                                method: 'post',
                                url: '/monitor_scene/monitor_scene_show/',
                                data: result_list_edit[i].item_id,
                            }).catch(function (e) {
                                vm.$message.error('获取数据失败！');
                            });
                            vm.monitor_data = res.data.results;
                            let job_params = vm.monitor_data[0];
                            $('.monitor_content').append('<div class=\"Drigging\" name=\"' + result_list_edit[i].item_id + '\" type=\"job' + result_list_edit[i].item_id + '\" id=\"' + result_list_edit[i].order + '\" style=\"top:' + result_list_edit[i].y + 'px;left:' + result_list_edit[i].x + 'px;transform: scale(' + result_list_edit[i].scale + ')\"></div>');
                            job_monitor(job_params);
                        }
                        if (result_list_edit[i].monitor_type === 4) {
                            let res = await axios({
                                method: 'post',
                                url: '/monitor_scene/monitor_scene_show/',
                                data: result_list_edit[i].item_id,
                            }).catch(function (e) {
                                vm.$message.error('获取数据失败！');
                            });
                            vm.monitor_data = res.data.results;
                            let jion_id = [{
                                "id": vm.monitor_data[0].jion_id
                            }];
                            $('.monitor_content').append('<div class=\"Drigging\" name=\"' + result_list_edit[i].item_id + '\" id=\"' + result_list_edit[i].order + '\" style=\"top:' + result_list_edit[i].y + 'px;left:' + result_list_edit[i].x + 'px;transform: scale(' + result_list_edit[i].scale + ')\"><div type=\"flow_monitor' + result_list_edit[i].order + '\"></div></div>');
                            flow_monitor(jion_id, result_list_edit[i].order);
                        }
                    }
                    vm.drigging_id = max + 1;
                    //调整场景的字体颜色
                    vm.change_scene_color();
                } else {
                    $('.monitor_edit').css('display', 'block');
                    vm.show_num = vm.isAdd;
                    vm.isAdd = 0;
                }
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
                        url: '/monitor_scene/select_table/',
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
                        url: '/monitor_scene/scene_color_del/',
                        data: row.id
                    }).catch(function (e) {
                        vm.$message.error('场景颜色删除失败！');
                    });
                    axios({
                        method: 'post',
                        url: '/monitor_scene/del_scene/',
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
                    url: '/monitor_scene/pos_name/',
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
                    url: '/monitor_scene/scene_show/',
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
    vm.get_all_area()
    vm.paging();
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
    var obox = $('.monitor_content');
    var selector = '';
    var flag = false;
    var x, y;
    var offsetLeft, offsetTop;
    $(document).on("mouseover", ".Drigging", function () {
        $(this).css('cursor', 'pointer');//当鼠标移动到拖拽目标上的时候，将鼠标的样式设置为移动(move)
    });
    $(document).on("mousedown", ".Drigging", function (e) {
        var e = window.event || e;
        selector = '#' + this.id;
        flag = true;//当鼠标在移动元素按下的时候将flag设定为true
        x = e.clientX;//获取鼠标在当前窗口的相对偏移位置的Left值并赋值给x
        y = e.clientY;//获取鼠在当前窗口的相对偏移位置的Top值并赋值给y
        offsetLeft = $(selector).position().left;
        offsetTop = $(selector).position().top;
        w = $(selector).width();
        h = $(selector).height();
        $(this).css({"cursor": "pointer", "z-index": "500"});
        $(this).siblings().css({"z-index": "0"});
    });
    $(document).on("mouseup", "html", function () {
        flag = false;//当鼠标在移动元素起来的时候将flag设定为false
    });
    $(document).on("mousedown", ".Drigging", function (e) {//监控项右击显示打分输入框
        if (e.button == 2) {
            e.preventDefault();
            var x = e.offsetX + 10;
            var y = e.offsetY + 10;
            $(this).find('.right_click').css({
                left: x,
                top: y,
                display: 'block'
            });
            $(this).find('.right_click').off();
            $(this).find('.score').on('click', function (e) {
                e.stopPropagation();
                $(selector + ' .score_input').css('display', 'block');
                $('.right_click').css('display', 'none');
            })
            $(this).find('.delete').on('click', function (e) {
                e.stopPropagation();
                $(this).parent().parent().remove();
                //找出连线并删除
                id = $(this).parent().parent()[0].attributes.name.value
                for (var i = 0; i < vm.lines.length; i++) {
                    if (vm.lines[i].pid == id || vm.lines[i].nid == id) {
                        vm.lines.splice(i, 1)
                    }
                }
                $(this).data().next_item = 0;
                vm.line_flag = 0
            })
            $(this).find('.line').on('click', function (e) {
                e.stopPropagation();
                add_line($(this).parent().parent()[0]);
            });
        }
    });
    $(document).on("blur", ".score_input", function () {//打分输入框失去焦点隐藏
        $('.score_input').css('display', 'none');
    });

    $(document).mousemove(function (e) {
        if (!flag)//如果flag为false则返回
            return;//当flag为true的时候执行下面的代码
        e.preventDefault();
        var e = window.event || e;
        var _x = e.clientX - x + offsetLeft + ($(selector).width() / vm.scale) * (vm.scale - 1) / 2;
        //event.clientX得到鼠标相对于客户端正文区域的偏移
        //然后减去offsetX即得到当前推拽元素相对于当前窗口的X值
        //（减去鼠标刚开始拖动的时候在当前窗口的偏移X）
        var _y = e.clientY - y + offsetTop + ($(selector).height() / vm.scale) * (vm.scale - 1) / 2;
        //event.clientY得到鼠标相对于客户端正文区域的偏移
        //然后减去offsetX即得到当前推拽元素相对于当前窗口的Y值
        //（减去鼠标刚开始拖动的时候在当前窗口的偏移Y）
        if (_x < 0) {
            _x = 0 + ($(selector).width() / vm.scale) * (vm.scale - 1) / 2;
        }
        if (_y < 0) {
            _y = 0 + ($(selector).height() / vm.scale) * (vm.scale - 1) / 2;
        }
        if (_x > obox.width() - $(selector).width()) {
            //_x=obox.width()-$(selector).width();
            _x = obox.width() - (($(selector).width() / vm.scale) * (vm.scale - 1) / 2 + ($(selector).width() / vm.scale));
        }
        if (_y > obox.height() - $(selector).height()) {
            //_y=obox.height()-$(selector).height();
            _y = obox.height() - (($(selector).height() / vm.scale) * (vm.scale - 1) / 2 + ($(selector).height() / vm.scale));
        }
        $(selector).css("left", _x);
        $(selector).css("top", _y);
        $(selector).css('cursor', 'pointer');
        var t = $(selector).position().top;
        var r = $(selector).position().left + $(selector).width();
        var b = $(selector).position().top + $(selector).height();
        var l = $(selector).position().left;
        for (var i = 0; i < $(selector).siblings().length; i++) {
            var t1 = $(selector).siblings().eq(i).position().top;
            var r1 = $(selector).siblings().eq(i).position().left + $(selector).siblings().eq(i).width();
            var b1 = $(selector).siblings().eq(i).position().top + $(selector).siblings().eq(i).height();
            var l1 = $(selector).siblings().eq(i).position().left;
            if (Math.abs(t - b1) < 10) {
                $(selector).css("top", b1 + ($(selector).height() / vm.scale) * (vm.scale - 1) / 2);
            }
            if (Math.abs(l - r1) < 10) {
                $(selector).css("left", r1 + ($(selector).width() / vm.scale) * (vm.scale - 1) / 2);
            }
            if (Math.abs(b - t1) < 10) {
                $(selector).css("top", t1 - $(selector).height() / vm.scale - ($(selector).height() / vm.scale) * (vm.scale - 1) / 2);
            }
            if (Math.abs(r - l1) < 10) {
                $(selector).css("left", l1 - $(selector).width() / vm.scale - ($(selector).width() / vm.scale) * (vm.scale - 1) / 2);
            }
        }
    });
    $('.el-icon-circle-plus-outline').click(function () {
        if (vm.multiple < 4) {
            // vm.scale = vm.scale + 0.1;
            // $('.monitor_content').find('.Drigging').css('transform', 'scale(' + vm.scale + ')');
            var dris = $('.monitor_content').find('.Drigging')
            for (var i = 0; i < dris.length; i++) {
                var style = dris[i].style.transform;
                var scale = parseFloat(style.replace("scale", "").replace("(", "").replace(")", "")) + 0.1;
                dris[i].style.transform = 'scale(' + scale + ')';
            }
            vm.multiple++;
        } else {
            return
        }
    });
    $('.el-icon-remove-outline').click(function () {
        if (vm.multiple > -4) {
            // vm.scale = vm.scale - 0.1;
            // $('.monitor_content').find('.Drigging').css('transform', 'scale(' + vm.scale + ')');
            var dris = $('.monitor_content').find('.Drigging')
            for (var i = 0; i < dris.length; i++) {
                var style = dris[i].style.transform;
                var scale = parseFloat(style.replace("scale", "").replace("(", "").replace(")", "")) - 0.1;
                if (scale >= 0.1) {
                    dris[i].style.transform = 'scale(' + scale + ')';
                }
            }
            vm.multiple--;
        } else {
            return
        }
    });

    function draw_line() {
        //让canvas append后才能执行此方法
        if (vm.canvas_flag == 1) {
            var c = document.getElementById("line_canvas");
            c.width = 1298.7;
            c.height = 600
            ctx = c.getContext("2d");
            for (var i = 0; i < vm.lines.length; i++) {
                var pid = vm.lines[i].pid;
                var nid = vm.lines[i].nid;
                var PY = $("[name='" + pid + "']").position().top;
                var PX = $("[name='" + pid + "']").position().left;
                var NY = $("[name='" + nid + "']").position().top;
                var NX = $("[name='" + nid + "']").position().left
                var pcx = $("[name='" + pid + "']")[0].clientWidth
                var pcy = $("[name='" + pid + "']")[0].clientHeight
                var ncx = $("[name='" + nid + "']")[0].clientWidth
                var ncy = $("[name='" + nid + "']")[0].clientHeight
                var arrow_length = 12
                var arrow_angle = 60
                var up = arrow_length * (Math.sin(arrow_angle * Math.PI / 180))
                var left = arrow_length * (Math.cos(arrow_angle * Math.PI / 180))
                //将线条的渲染分为四种情况
                if (PY > NY && (PX < NX + ncx) && (PX + pcx > NX)) { //上边
                    var pre_x = pcx / 2 + PX;
                    var pre_y = PY;
                    var now_x = NX + ncx / 2
                    var now_y = NY + ncy
                    var a_x = now_x - up
                    var b_x = now_x + up
                    var a_y = now_y + left
                    var b_y = now_y + left
                } else if ((PY + pcy) < NY && (PX < NX + ncx) && (PX + pcx > NX)) { //下边
                    var pre_x = pcx / 2 + PX;
                    var pre_y = PY + pcy;
                    var now_x = NX + ncx / 2
                    var now_y = NY
                    var a_x = now_x - up
                    var b_x = now_x + up
                    var a_y = now_y - left
                    var b_y = now_y - left
                } else if ((PX + pcx) < NX) { //右边
                    var pre_x = pcx + PX;
                    var pre_y = pcy / 2 + PY;
                    var now_x = NX
                    var now_y = ncy / 2 + NY
                    var a_x = now_x - left
                    var b_x = now_x - left
                    var a_y = now_y + up
                    var b_y = now_y - up
                } else if ((PX + pcx) > NX) { //左边
                    var pre_x = PX;
                    var pre_y = pcy / 2 + PY;
                    var now_x = NX + ncx
                    var now_y = ncy / 2 + NY
                    var a_x = now_x + left
                    var b_x = now_x + left
                    var a_y = now_y + up
                    var b_y = now_y - up
                }
                ctx.beginPath()
                ctx.moveTo(pre_x, pre_y);
                ctx.lineTo(now_x, now_y);
                ctx.lineWidth = 3
                ctx.strokeStyle = "grey"
                ctx.stroke();
                ctx.closePath()
                ctx.beginPath()
                ctx.moveTo(now_x, now_y)
                ctx.lineTo(a_x, a_y)
                ctx.lineTo(b_x, b_y)
                ctx.lineTo(now_x, now_y)
                ctx.strokeStyle = "grey";
                ctx.fillStyle = "grey";
                ctx.fill()
                ctx.stroke()
                ctx.closePath()
            }
        }
    }

    function add_line(item_info) {
        if (vm.line_flag == 0) {
            vm.line_flag = 1;
            id = item_info.id
            vm.pre_id = $('#' + id).attr('name')
        } else {
            id = item_info.id
            var name = $('#' + id).attr('name')
            if (name != vm.pre_id) {
                $("[name='" + vm.pre_id + "']").data().next_item = $('#' + id).attr('name')
                line = {
                    'pid': vm.pre_id,
                    'nid': $('#' + id).attr('name')
                }
                vm.lines.push(line)
            }
            vm.line_flag = 0;
            vm.pre_id = 0;
        }
    }

    function flush_canvas() {
        setInterval(draw_line, 200);
    }

    flush_canvas();
});
setInterval(function () {
    //flow1_js_start
    $('#save2').click(function () {
        // 获取全部数据
        var data = $('#flow1').data('dataflow').getAllData();
        var name = data.location[0];
        $('#result2').val(JSON.stringify(data));
    });
    // 清空画布
    $('#resetCanvas').click(function () {
        $('#flow1').data('dataflow').resetCanvas();
    });
    //flow1_js_end
    // $('.node-wrapper').click(function () {
    //
    //     $(this).find(".node-title").attr('contenteditable','plaintext-only');
    // })
    //节点抽屉
    $('.tool-title').click(function () {
        $(this).next('.tool-list').animate({
            height: 'toggle'
        });
        $(this).parent().siblings().children('.tool-list').animate({
            height: "hide"
        });
    });
}, 1)