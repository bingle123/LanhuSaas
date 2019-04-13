let vm = null;
$(function() {
    axios.interceptors.request.use((config) => {
        config.headers['X-Requested-With'] = 'XMLHttpRequest';
        let regex = /.*csrftoken=([^;.]*).*$/; // 用于从cookie中匹配 csrftoken值
        config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
        return config
    });
    vm = new Vue({
        el: "#main",
        data: {
            imgList: [],
            imgHeight: '' + document.documentElement.clientHeight + 'px',
            start: '09:00',                                                                   //开始时间
            end: '18:00',                                                                   //结束时间
            region1: '1',                                                                 //岗位选择
            position: '1',                                                                  //岗位
            options: [],
        },
        methods: {
            get_pos() {
                axios({
                    method: 'post',
                    url: '/monitor_scene/get_all_pos/',
                }).then((res) => {
                    let json = [];
                    if (res.data.message.length > 0) {
                        for (var i = 0; i < res.data.message.length; i++) {
                            let j = {};
                            j.value = res.data.message[i].id;
                            j.label = res.data.message[i].pos_name;
                            json.push(j);
                        }
                        ;
                        this.options = json;
                    }
                }).catch((res) => {
                    vm.$message.error('获取用户错误')
                })
            },
            async alternate_play_test() {
                var res = await axios({
                    method: 'post',
                    url: '/monitor_scene/alternate_play_test/',
                    data: {
                        'pos_id': vm.position,
                        'start': vm.start,
                        'end': vm.end
                    }
                }).catch(function (e) {
                    vm.$message.error('获取数据失败！');
                });
                vm.imgList = res.data.message;
            },
            scene_change(value1, value2) {
                if (vm.imgList.length == 1) {    //只有一个场景
                    vm.scene_content_change(0);
                    setInterval(function () {
                        vm.scene_content_change(0);   //十秒钟更新一次dom
                    }, 30000)
                }
                if (vm.imgList.length > 1) {  //多于一个场景
                    vm.scene_content_change(value1);
                }

            },
            //更新dom
            scene_content_change(value) {
                let selector = '.scene_content' + value;
                let base_list = vm.imgList[value].scene_content[0].base_list;  //获取当前场景的基本监控项数据
                let chart_list = vm.imgList[value].scene_content[0].chart_list;  //获取当前场景的图标监控项数据
                let job_list = vm.imgList[value].scene_content[0].job_list;  //获取当前场景的作业监控项数据
                let flow_list = vm.imgList[value].scene_content[0].flow_list;  //获取当前场景的流程监控项数据
                $(selector).html('');    //初始化场景
                for (let i = 0; i < base_list.length; i++) {
                    //添加一个div容器，形如<div type="basic1"></div>
                    $(selector).append('<div type=\"basic' + base_list[i].id + '\" style=\"position: absolute;top:' + base_list[i].y + 'px;left:' + base_list[i].x + 'px;transform: scale(' + base_list[i].scale + ')\"></div>');
                    //调用基本监控项的渲染方法,第一个参数对应容器div的type
                    base_monitor_active(base_list[i].id, base_list[i].font_size, base_list[i].height, base_list[i].width, base_list[i].contents);
                }
                for (let i = 0; i < chart_list.length; i++) {
                    //添加一个div容器,形如<div id="1_1"><div id="chart1_1"></div></div>
                    $(selector).append('<div id=\"' + value + '_' + chart_list[i].order + '\" style=\"position: absolute;background:beige;height:' + chart_list[i].height + 'px;width:' + chart_list[i].width + 'px;top:' + chart_list[i].y + 'px;left:' + chart_list[i].x + 'px;transform: scale(' + chart_list[i].scale + ')\"><div id=\"chart' + value + '_' + chart_list[i].order + '\" style=\"background:beige;height:' + chart_list[i].height + 'px;width:' + chart_list[i].width + 'px\"></div><input class="score_input" type="text" value="0"><div class="right_click"><span class="score">打分</span><span class="delete">删除监控项</span></div></div>');
                    //调用图标监控项的渲染方法，最后一个参数对应容器外层div的id
                    show_chart_active(chart_list[i].id, chart_list[i].gather_params, chart_list[i].height, chart_list[i].width, value + '_' + chart_list[i].order);

                }
                for (let i = 0; i < job_list.length; i++) {
                    let job_params = {
                        'id': job_list[i].id,     //监控项id
                        'width': job_list[i].width,
                        'height': job_list[i].height,
                        'status': job_list[i].job_status,   //采集测试的作业状态
                        'contents': job_list[i].contents    //监控项的显示内容参数
                    };
                    //添加一个div容器,形如<div id="job1"></div></div>
                    $(selector).append('<div type=\"job' + job_list[i].id + '\" id=\"' + value + '_' + job_list[i].order + '\" style=\"position: absolute;top:' + job_list[i].y + 'px;left:' + job_list[i].x + 'px;transform: scale(' + job_list[i].scale + ')\"></div>');
                    //调用作业监控项的渲染方法，参数的第一条值对应容器外层div的id
                    job_monitor_active(job_params);
                }
                for (let i = 0; i < flow_list.length; i++) {

                    let jion_id = [{
                        "id": flow_list[i].jion_id
                    }];
                    //添加一个div容器,形如<div><div id="flow1_1"></div></div>
                    $(selector).append('<div class=\"flow_monitor\" type=\"' + flow_list[i].id + '\" style=\"position: absolute;top:' + flow_list[i].y + 'px;left:' + flow_list[i].x + 'px;transform: scale(' + flow_list[i].scale + ')\"><div type=\"flow_monitor' + value + '_' + flow_list[i].order + '\"></div></div>');
                    //调用流程监控项的渲染方法，第一条参数必须为[{}]格式，用来调v3接口，第二条参数对应容器内部div的id
                    flow_monitor(jion_id, value + '_' + flow_list[i].order);
                    setTimeout(function () {
                        axios({
                            method: 'post',
                            url: '/monitor_item/node_state_by_item_id/',
                            data: {
                                'item_id': flow_list[i].id
                            }
                        }).then(function (res) {

                            var len = res.data.message.length
                            for (var j = 0; j <= len - 1; j++) {
                                data_key = res.data.message[j].data_value
                                if (data_key == '1' || data_key == '4') {
                                    $('p:contains(' + res.data.message[j].data_key + ')').parent().siblings('.node-icon').css('background', '#67c23a');
                                } else if (data_key == '0' || data_key == '3') {
                                    $('p:contains(' + res.data.message[j].data_key + ')').parent().siblings('.node-icon').css('background', '#f56c6c')
                                } else if (data_key == '2') {
                                    $('p:contains(' + res.data.message[j].data_key + ')').parent().siblings('.node-icon').css('background', '#f56c6c')
                                    $('p:contains(' + res.data.message[j].data_key + ')').parent().siblings('.node-icon').children().css('position', 'relative')
                                    $('p:contains(' + res.data.message[j].data_key + ')').parents().siblings('.node-icon').children().html('<div class=\"keepOn\"><p>是否继续</p><span class="keepOn_yes">是</span><span class="keepOn_no">否</span></div>')
                                }
                            }
                        }).catch(function (e) {
                            vm.$message.error('获取数据失败！');
                        });
                    }, 1000)


                }
            },
        },
        mounted() {
            //const that = this
            //这里很关键；大部分博客都是这样写的，其实也没有毛病，只不过有时候不起作用；
            window.onresize = () => {
                return (() => {
                    window.imgHeight = document.documentElement.clientHeight - 100;
                    vm.imgHeight = '' + window.imgHeight + 'px';
                })()
            }

        },
        watch: {
            imgHeight(val) {
                if (!this.timer) {
                    this.imgHeight = val;
                    this.timer = true;
                    let that = this;
                    setTimeout(function () {
                        // that.screenWidth = that.$store.state.canvasWidth
                        console.log(that.imgHeight);
                        that.timer = false;
                    }, 400)
                }
            },
        }
    });
    vm.get_pos();
    vm.alternate_play_test();
    var interval = setInterval(function () {
        vm.alternate_play_test();
    }, 10000);
});
$(function () {
    $(document).on("click", ".keepOn_yes", function (e) {
        e.preventDefault();
        var id=$(this).parents('.flow_monitor').attr('type');
        axios({
            method: 'post',
                    url: '/monitor_item/resume_flow/',
                    data: {
                        'item_id': id
                    }
        }).then(function (res) {
            console.log(res);
        });
        $(this).parent().hide();
    });
    $(document).on("click", ".keepOn_no", function (e) {
        e.preventDefault();
        $(this).parent().hide();
    });
    $(document).on("click", ".block", function (e) {
        var elem = document.body;
        if (elem.webkitRequestFullScreen) {
            elem.webkitRequestFullScreen();
        } else if (elem.mozRequestFullScreen) {
            elem.mozRequestFullScreen();
        } else if (elem.requestFullScreen) {
            elem.requestFullscreen();
        } else {
            notice.notice_show("浏览器不支持全屏API或已被禁用", null, null, null, true, true);
        }
    });
});