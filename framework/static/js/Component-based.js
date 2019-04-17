
function job_monitor(job_params){
    selector_id='job'+job_params.id
    // var status=job_params.status
    // if(status==0){
        $('[type='+selector_id+']').html($('<div class="unexecuted" style="background: beige;color: grey;"><h1>作业未执行</h1><i class="el-icon-error" style="color: grey;font-size: 30px;margin-top: 20px;"></i></div>'))
    // }else if(status==1){
    //     $('[type='+selector_id+']').html($('<div class="success" style="background: beige;color: green;"><h1>作业执行成功</h1><i class="el-icon-success" style="color: green;font-size: 30px;margin-top: 20px;"></i></div>'))
    // }else if(status==2){
    //     $('[type='+selector_id+']').html($('<div class="loading" style="background: beige;color: orange;"><h1>正在执行</h1><i class="el-icon-loading" style="color: orange;font-size: 30px;margin-top: 20px;"></i></div>'))
    // }else if(status==-1){
    //     $('[type='+selector_id+']').html($('<div class="error" style="background: beige;color: red;"><h1>作业执行失败</h1><i class="el-icon-error" style="color: red;font-size: 30px;margin-top: 20px;"></i></div>'))
    // }
    $('[type='+selector_id+']').append('<input class="score_input" type="text" value="0">');
    $('[type='+selector_id+']').append('<div class="right_click"><span class="score">打分</span><span class="delete">删除监控项</span><span class="line">连线</span>'+vm.sizeStrFun()+'</div>');
    $('[type='+selector_id+']').css('height',job_params.height);
    $('[type='+selector_id+']').css('width',job_params.width);
    $('[type='+selector_id+']').find("*").css('font-size',job_params.font_size);
}

function job_monitor_active(job_params) {
    selector_id='job'+job_params.id
    var status=job_params.status
    if(status==0){
        $('[type='+selector_id+']').html($('<div class="unexecuted" style="background: beige;color: grey;"><h1>作业未执行</h1><i class="el-icon-error" style="color: grey;font-size: 30px;margin-top: 20px;"></i></div>'))
    }else if(status==1){
        $('[type='+selector_id+']').html($('<div class="success" style="background: beige;color: green;"><h1>作业执行成功</h1><i class="el-icon-success" style="color: green;font-size: 30px;margin-top: 20px;"></i></div>'))
    }else if(status==2){
        $('[type='+selector_id+']').html($('<div class="loading" style="background: beige;color: orange;"><h1>正在执行</h1><i class="el-icon-loading" style="color: orange;font-size: 30px;margin-top: 20px;"></i></div>'))
    }else if(status==-1){
        $('[type='+selector_id+']').html($('<div class="error" style="background: beige;color: red;"><h1>作业执行失败</h1><i class="el-icon-error" style="color: red;font-size: 30px;margin-top: 20px;"></i></div>'))
    }
    $('[type='+selector_id+']').append('<input class="score_input" type="text" value="0">');
    $('[type='+selector_id+']').append('<div class="right_click"><span class="score">打分</span><span class="delete">删除监控项</span><span class="line">连线</span>'+vm.sizeStrFun()+'</div>');
    var height=Number(job_params.height)+50;
    $('[type='+selector_id+']').css('height',height+'px');
    $('[type='+selector_id+']').css('width',job_params.width);
    $('[type='+selector_id+']').find("*").css('font-size',job_params.font_size);
}
function show_chart_active(item_id,chart_type,height,width,drigging_id){
    var new_res=[]
    var chartdata=[]
    $.get("/monitor_scene/get_chart_data/"+item_id,function (res) {
        res=res.message
       for(r in res){
           if(isNotANumber(res[r].values[0])){
               new_res[1]=res[r]
           }else{
                new_res[0]=res[r]
           }
       }
       person_count=new_res[0].key
        for(var i=0;i<new_res[0].values.length;i++){
            temp={
                'name':new_res[0].values[i],
                'value':new_res[1].values[i]
            }
            chartdata.push(temp)
        }
        show_chart(item_id,chartdata,person_count,chart_type,height,width,drigging_id,'')
    },dataType='json')
}
function isNotANumber(inputData) {
　　//isNaN(inputData)不能判断空串或一个空格
　　//如果是一个空串或是一个空格，而isNaN是做为数字0进行处理的，而parseInt与parseFloat是返回一个错误消息，这个isNaN检查不严密而导致的。
　　if (parseFloat(inputData).toString() == "NaN") {
　　　　return false;
　　} else {
　　　　return true;
　　}
}

function show_chart(item_id,chartData,person_count,chart_type,height,width,drigging_id,content) {
    if(chartData==''){
        chartData=[]
    }
    if(content!=''){
                var obj = JSON.parse(content);
                for(let i=0;i<obj.X.v.length;i++){
                    var obj_1={};
                    obj_1.name=obj.X.v[i];
                    obj_1.value=obj.Y.v[i];
                    chartData.push(obj_1)
                }
                person_count=obj.Y.k
    }
    var barX=[];
    var barCount=[];
    for(var i=0;i<chartData.length;i++){
        barX.push(chartData[i].name)
        barCount.push(chartData[i].value)
    }
        $('#'+drigging_id).css('height',height);
        $('#'+drigging_id).css('width',width);
        if (chart_type == "饼图") {
            myChart = echarts.init(document.getElementById(drigging_id).firstElementChild, 'macarons');
            var legendData = [];
                    for(var i=0;i<chartData.length;i++){
                        legendData.push(chartData[i].name)
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
                                name:person_count,
                                type: 'pie',
                                radius: '50%',
                                center: ['50%', '30%'],
                                data: chartData,
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
                myChart.setOption(option);
        }

        if (chart_type == "柱状图") {
            myChart = echarts.init(document.getElementById(drigging_id).firstElementChild, 'macarons');
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
                        name: person_count,
                        type: 'bar',
                        stack: 'data',
                        data: barCount
                    },
                ]
            };
            myChart.setOption(option);
        }
        if (chart_type == "折线图") {
            myChart = echarts.init(document.getElementById(drigging_id).firstElementChild, 'macarons');
            option = {
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: [person_count]
                },
                calculable: true,
                xAxis: [
                    {
                        type: 'category',
                        boundaryGap: false,
                        data: barX
                    }
                ],
                yAxis: [
                    {
                        type: 'value'
                    }
                ],
                series: [
                    {
                        name: person_count,
                        type: 'line',
                        smooth: true,
                        itemStyle: {normal: {areaStyle: {type: 'default'}}},
                        data: barCount,
                    },
                ]
            };
            myChart.setOption(option);
        }
}
function base_monitor_active(vm_obj, html_obj) {
    var current_monitor_item = vm_obj.current_monitor_item;
    current_monitor_item.dimension_data = JSON.parse(current_monitor_item.dimension);
    if(current_monitor_item.source_type == 0){
         current_monitor_item.interface_type = "log";
    }
    if(current_monitor_item.source_type == 1){
         current_monitor_item.interface_type = "measures";
    }
    current_monitor_item.show_rule_type = current_monitor_item.display_type;
    current_monitor_item.measures = current_monitor_item.target_name;
    //名字不一样，后台用的measures_name数据库字段是measure_name
    current_monitor_item.measures_name = current_monitor_item.measure_name
    //这里变成字符串，因为后台是用字符串判断的
    current_monitor_item.show_rule_type = current_monitor_item.show_rule_type+"";
    //根据监控项的采集时间段，在后台判断是否需要调用一体化平台接口获取监控数据
    // 这里是异步处理,后台执行监控采集迁移入库
    $.ajax({
        type: "POST",
        data : JSON.stringify(current_monitor_item),
        dataType: "JSON",
        async: true,
        url: "/monitor_scene/is_monitor_item_collect/",
        success: function(data) {
        }
    });
    //取得当前的监控项信息
    current_monitor_item = vm_obj.current_monitor_item;
    var selector_id='basic'+current_monitor_item.id;
    var drigging_id = vm_obj.drigging_id;
    var content_json = content_to_json(current_monitor_item.contents);
    var display_rule = current_monitor_item.display_rule
    var selector = null;
    //从采集表获取监控项的采集数据
    $.get("/monitor_scene/get_basic_data/"+current_monitor_item.id, function (res) {
        for (i in res) {
            key = i
        }
        //将采集结果转换为json,这里的key固定为“measures”
        //原因是这里只取度量值，不考虑历史垃圾数据
        var gather_base_test_data = JSON.parse(res["measures"]);
        var bgcolor = null;
        let scene_show = function (split_char) {
            for (let i = 0; i < gather_base_test_data.length; i++) {
                let selector = '.div' + drigging_id + i;
                let data_org = [];
                let data_key = [];
                let data_value = [];
                for (k in gather_base_test_data[i]) {
                    if(gather_base_test_data[i][k].toString().indexOf(split_char)>-1){
                        //保留颜色信息
                        if("#" == split_char){
                            bgcolor = gather_base_test_data[i][k].split(split_char)[1];
                        }
                    }
                    //颜色展示可以没有值
                    if (!isEmptyObject(content_json)) {
                        for (x in content_json) {
                            if (x == k) {
                                data_org.push(k)
                                data_key.push(content_json[x]);
                                data_value.push(gather_base_test_data[i][k]);
                            }
                        }
                    } else {
                        //展示内容为空，只放度量值
                        if (gather_base_test_data[i][k].toString().indexOf(split_char) > -1) {
                            data_org.push(k);
                            data_key.push(k);
                            data_value.push(gather_base_test_data[i][k]);
                        }
                    }
                }
                $('[type=' + selector_id + ']').append('<div class="div' + drigging_id + i + '"></div>');
                for (let j = 0; j < data_key.length; j++) {
                    if (data_org[j] == current_monitor_item.target_name + '_' + current_monitor_item.measure_name) {
                        var data_value_str = data_value[j].toString();
                        if (data_value_str.indexOf(split_char) > -1) {
                            //颜色展示可以没有值
                            if (!isEmptyObject(content_json)) {
                                if ("%" == split_char) {
                                    $(selector).append('<p>' + data_key[j] + ':' + data_value[j] + '</p>');
                                } else {
                                    $(selector).append('<p>' + data_key[j] + ':' + data_value[j].split(split_char)[0] + '</p>');
                                }
                            } else {
                                $(selector).append('<p >&nbsp;</p>');
                                if ("@" == split_char) {
                                    $(selector).append('<p >' + data_value[j].split(split_char)[1] + '</p>');
                                }
                            }
                        } else {
                            $('#base_test_text').html('');
                            vm.$message.error('采集规则配置出错！');
                            return
                        }
                    } else {
                        $(selector).append('<p>' + data_key[j] + ':' + data_value[j] + '</p>');
                    }
                }
            }
        }
        //按百分比展示
        if (current_monitor_item.display_type == 0) {
            scene_show("%");
        }
        //按颜色展示
        if (current_monitor_item.display_type == 1) {
            scene_show("#");
            $('[type=' + selector_id + ']').css("background", "#" + bgcolor);
        }
        //其它展示类型
        if (current_monitor_item.display_type == 2) {
            scene_show("@");
        }
        vm_obj.font_size = current_monitor_item.font_size;
        vm_obj.height = current_monitor_item.height;
        vm_obj.width = current_monitor_item.width;
        //字体大小变更操作
        collection_base_size(vm_obj,'[type='+selector_id+']');
        //高宽变更操作
        collection_base_height_change(vm_obj,'[type='+selector_id+']');
        collection_base_width_change(vm_obj,'[type='+selector_id+']');
    })
}
function base_monitor(item_id,font_size,height,width,content) {
    selector_id='basic'+item_id
    var circle1='<div id="status" style="display: inline-block;margin-left:5px;width:16px;height:16px;background-color:lawngreen;border-radius:50%;-moz-border-radius:50%;-webkit-border-radius:50%;"></div>'
    var circle4='<div id="status" style="display: inline-block;margin-left:5px;width:16px;height:16px;background-color:red;border-radius:50%;-moz-border-radius:50%;-webkit-border-radius:50%;"></div>'
    var circle3='<div id="status" style="display: inline-block;margin-left:5px;width:16px;height:16px;background-color:grey;border-radius:50%;-moz-border-radius:50%;-webkit-border-radius:50%;"></div>'
    var circle2='<div id="status" style="display: inline-block;margin-left:5px;width:16px;height:16px;background-color:darkgreen;border-radius:50%;-moz-border-radius:50%;-webkit-border-radius:50%;"></div>'
    var asd='<div class="display: inline-block;">'
        $('[type='+selector_id+']').html("");
        $('[type='+selector_id+']').append("<div>"+content +"</div>");
        $('[type='+selector_id+']').append('<input class="score_input" type="text" value="0">');
        $('[type='+selector_id+']').append('<div class="right_click"><span class="score">打分</span><span class="delete">删除监控项</span><span class="line">连线</span>'+vm.sizeStrFun()+'</div>');
        $('[type='+selector_id+']').css('height',height+'px');
        $('[type='+selector_id+']').css('width',width+'px');
        // if(content.indexOf("#") > -1 && content.indexOf('@') == -1){
        //     var temp1 = content.split("#");
        //     var temp2=[];
        //     var temp3=[];
        //     var temp4=[];
        //     var str=[];
        //     for(var i=1;i<temp1.length;i=i+2){
        //         temp2.push(temp1[i]);
        //     }
        //     for(var i=0;i<temp2.length;i++){
        //         temp3.push(temp2[i].split("="))
        //     }
        //     for(var i=0;i<temp3.length;i++){
        //         temp4.push(temp3[i][1])
        //     }
        //     for(i=0;i<temp2.length;i++){
        //         str[i]='#'+temp2[i]+'#'
        //     }
        //     $('[type='+selector_id+']').html("")
        //      for (var i = 0, j = 0; i < temp1.length; i = i + 2, j++) {
        //          if(j<temp4.length){
        //              $('[type='+selector_id+']').append("<div>" + temp1[i] + temp4[j]+ "</div>");
        //          }
        //          else{
        //               $('[type='+selector_id+']').append("<div>" + temp1[i]+ "</div>");
        //          }
        //      }
        //   }
        if(content.indexOf('@') > -1 && content.indexOf("#") == -1){
            var icon1 = content.split("@");
            var icon2=[];
            var icon3=[];
            var icon4=[-2];
            var icon=[];
            for(var i=1;i<icon1.length;i=i+2){
                icon2.push(icon1[i]);
            }
            for(var i=0;i<icon2.length;i++){
                icon3.push(icon2[i].split("="));
            }
            for(var i=0;i<icon3.length;i++){
                icon4.pop();
                icon4.push(icon3[i][1]);
            }
            $('[type='+selector_id+']').html("")
            $('[type='+selector_id+']').append('<input class="score_input" type="text" value="0">');
            $('[type='+selector_id+']').append('<div class="right_click"><span class="score">打分</span><span class="delete">删除监控项</span><span class="line">连线</span>'+vm.sizeStrFun()+'</div>');
            $('[type='+selector_id+']').append(asd);
            if(icon4 ){
                icon4.push("-2")
             }
            if (icon4[0] == 1) {
                 $('[type='+selector_id+']').append(circle1);
             }
             if (icon4[0] == 2) {
                 $('[type='+selector_id+']').append(circle2);
             }
             if (icon4[0] == 0) {
                 // $('[type='+selector_id+']').append(circle4);
             }
             if (icon4[0] == -1 || icon4 == -2) {
                 $('[type='+selector_id+']').append(circle3);
             }
         }
        if(content.indexOf("#") > -1 && content.indexOf('@') > -1) {
            var temp1 = content.split("#");
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
                temp4.push(temp3[i][1])
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
            icon4 = icon3[1]
            $('[type='+selector_id+']').html("")
            $('[type='+selector_id+']').append('<input class="score_input" type="text" value="0">');
            $('[type='+selector_id+']').append('<div class="right_click"><span class="score">打分</span><span class="delete">删除监控项</span><span class="line">连线</span>'+vm.sizeStrFun()+'</div>');
            for (var i = 0, j = 0; i < temp1.length; i = i + 2, j++) {
                if (i == flag2) {
                    $('[type='+selector_id+']').append(asd);
                    if (icon4 == 1) {
                        $('[type='+selector_id+']').append("<div style='display: inline-block'>"+icon1[0]+"</div>")
                        $('[type='+selector_id+']').append(circle1);
                    }
                    if (icon4 == 2) {
                        $('[type='+selector_id+']').append("<div style='display: inline-block'>"+icon1[0]+"</div>")
                        $('[type='+selector_id+']').append(circle2);
                    }
                    if (icon4 == 0) {
                        $('[type='+selector_id+']').append("<div style='display: inline-block'>"+icon1[0]+"</div>")
                        $('[type='+selector_id+']').append(circle4);
                    }
                    if (icon4 == -1 || icon4 == -2) {
                        $('[type='+selector_id+']').append("<div style='display: inline-block'>"+icon1[0]+"</div>")
                        $('[type='+selector_id+']').append(circle3);
                    }
                } else {
                    $('[type='+selector_id+']').append("<div>" + temp1[i] + temp4[j] + "</div>");
                }
            }
            $('[type='+selector_id+']').find("*").css("font-size",font_size)
            $('[type='+selector_id+']').css('height',height);
            $('[type='+selector_id+']').css('width',width);
        }

}

function font_size(id,value) {
     $("#"+id+"").find('*').css("font-size", value)
     $("#"+id+"").find('*').css("height", value)
     $("#"+id+"").find('*').css("width", value)
}
function flow_monitor(value1,value2){
                var selector_id='flow'+value2;
                var selector_type='flow_monitor'+value2
                var selector_canvas='canvas'+value2
                var selector_template='template'+value2
                var location ='';
                var line='';
                var template_list={};
                var constants='';
                var cc=" <div id=\"flow_canvas\" style=\"text-align:center;background-color: whitesmoke;\">\n" +
                            "                                <div id=\""+selector_id+"\" class=\"clearfix workflow-box\" style=\"width: 100%;position: relative;\">\n" +
                            "\n" +
                            "                                        <div class=\"workflow-canvas\" style=\"margin-left: 0px;padding-left: 0px\">\n" +
                            "                                            <!-- 画布模板 start -->\n" +
                            "                                            <div class=\"jtk-content\">\n" +
                            "                                                <div class=\"jtk-demo-canvas canvas-wide jtk-surface jtk-surface-nopan\"\n" +
                            "                                                     id=\""+selector_canvas+"\" style=\"width: 585px;height: 420px;\">\n" +
                            "                                                    <!-- 流程 -->\n" +
                            "                                                </div>\n" +
                            "                                            </div>\n" +
                            "                                            <!-- 画布模板 end -->\n" +
                            "\n" +
                            "                                        </div>\n" +
                            "\n" +
                            "    <!-- template 模板-->\n" +
                            "                                        <div class=\"jtk-delete jtk-none \">删除节点</div>\n" +
                            "                                        <div id=\""+selector_template+"\" class=\"jtk-none\">\n" +
                            "                                            <div class=\"jtk-window jtk-node workfolw-node start-node\" id=\"{charts}\"\n" +
                            "                                                 data-type=\"EmptyEndEvent\">\n" +
                            "                                                <div class=\"node-wrapper\">\n" +
                            "                                                    <div class=\"node-icon-start\">\n" +
                            "                                                        <i class=\"bk-icon icon-star-shape\"></i>\n" +
                            "                                                    </div>\n" +
                            "                                                </div>\n" +
                            "                                            </div>\n" +
                            "                                             <div class=\"jtk-window jtk-node workfolw-node start-node\" id=\"{charts}\"\n" +
                            "                                                  data-type=\"EmptyStartEvent\">\n" +
                            "                                                <div class=\"node-wrapper\">\n" +
                            "                                                    <div class=\"node-icon-start\">\n" +
                            "                                                        <i class=\"bk-icon icon-star-shape\"></i>\n" +
                            "                                                    </div>\n" +
                            "                                                </div>\n" +
                            "                                            </div>\n" +
                            "                                            <div class=\"jtk-window jtk-node workfolw-node database-node\" id=\"{charts}\"\n" +
                            "                                                 data-type=\"ServiceActivity\">\n" +
                            "                                                <div class=\"node-wrapper\">\n" +
                            "                                                    <div class=\"node-content\" style=\"position: relative\">\n" +
                            "                                                        <div class=\"start_time\" style=\"position: absolute;width: 70px;height: 20px;top: -26px;left: 0px;\"></div>\n" +
                            "                                                        <div class=\"end_time\" style=\"position: absolute;width: 70px;height: 20px;top: -26px;right: 0px;\"></div>\n" +
                            "                                                        <p class=\"node-title\"></p>\n" +
                            "                                                    </div>\n" +
                            "                                                    <div class=\"node-icon\">\n" +
                            "                                                        <i class=\"bk-icon icon-data\"></i>\n" +
                            "                                                    </div>\n" +
                            "                                                </div>\n" +
                            "                                            </div>\n" +
                            "\n" +
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
                            "                                    </div>\n" +
                            "                            </div>";
                        $('[type='+selector_type+']').html(cc);
                        $('[type='+selector_type+']').append('<input class="score_input" type="text" value="0">');
                        $('[type='+selector_type+']').append('<div class="right_click"><span class="score">打分</span><span class="delete">删除监控项</span><span class="line">连线</span>'+vm.sizeStrFun()+'</div>');
                axios({
                    method:'post',
                    url:'/monitor_item/flow_change/',
                    data: {
                        template_id:value1
                    }
                }).then(function (res) {
                    {
                        location = res.data.activities
                        line = res.data.flows
                        for(var i=0;i<line.length;i++){
                           line[i].source.id =line[i].source.id+value2
                           line[i].target.id =line[i].target.id+value2
                        }
                        for(var i=0;i<location.length;i++){
                           location[i]['id'] = location[i]['id']+value2
                        }
                        //显示流程单元中的预览图
                        $('#'+selector_id).dataflow({
                            el: '.tool', //流程拖动源
                            canvas: '#'+selector_canvas, //画布
                            arrowWidth: 8,
                            arrowHeight: 10,
                            template: '#'+selector_template,
                            data:
                                {
                                    "line": line, "location": location

                                }
                        });
                    }
                })

            }

/**
 * 基本监控项预览与编排展示预览组件（监控项与场景编排通用）
 * @param vm_obj
 * @param preview_type 预览类型
 * @param html_obj
 */
function preview_monitor_item(vm_obj, preview_type,html_obj){
    var current_monitor_item = null;
    //最终预览结果
    var preview_result = function(html_obj){
        if("monitor_item" == preview_type){
            //预览内容变更操作(根据“展示规则”和“显示内容”显示预览效果)
            collection_content_change(vm_obj,html_obj);
        }else{
            vm_obj.font_size = current_monitor_item.font_size;
            vm_obj.height = current_monitor_item.height;
            vm_obj.width = current_monitor_item.width;
        }
        //字体大小变更操作
        collection_base_size(vm_obj,html_obj);
        //高宽变更操作
        collection_base_height_change(vm_obj,html_obj);
        collection_base_width_change(vm_obj,html_obj);
    }
    //监控项预览
    if("monitor_item" == preview_type){
        var gather_base_test_data=vm_obj.gather_test_data;
        //判断是否为新增或修改的初始状态
        if(vm_obj.base_monitor_edit_test_init || vm_obj.base_monitor_add_test_init){
            var content='';
            for(var x in gather_base_test_data[0]){           //遍历列表的第i个对象
                content+='"'+x+'":"'+x+'"@\n';
            }
            if('0' == vm_obj.add_pamas && vm_obj.base_monitor_add_test_init){
                vm_obj.base.contents = content;
                vm_obj.base_monitor_add_test_init = false;
            }else if('1' == vm_obj.add_pamas && vm_obj.base_monitor_edit_test_init){
                vm_obj.base_monitor_edit_test_init = false;
            }
            vm_obj.base_monitor_show_cache = content;
        }
        //清空预览区域
        $(html_obj).html('');
        //展示监控项的私有方法
        let monitor_show = function(split_char){
            for(let i=0;i<gather_base_test_data.length;i++){
                let selector='.div'+i;
                let data_key=[];
                let data_value=[];
                for(k in gather_base_test_data[i]){
                    data_key.push(k);
                    data_value.push(gather_base_test_data[i][k]);
                }
                //border: 1px solid #000;
                $(html_obj).append('<div class="div'+i+'" style=""></div>');
                for(let j=0;j<data_key.length;j++){
                    if(data_key[j]==vm_obj.base.measures+'_'+vm_obj.base.measures_name){
                        var data_value_str=data_value[j].toString();
                        if(data_value_str.indexOf(split_char)>-1){
                            var str = data_value_str.split(split_char);
                            if("#" == split_char){
                               $(selector).css('background-color', split_char + str[1]);
                            }
                            if("@" == split_char){
                                str[0] = str[0] + str[1];
                                selected_measure = str[1];
                                $(selector).append('<p id="other_fixed_show" style="display: none">'+selected_measure+'</p>');
                            }
                            if("%" == split_char){
                                $(selector).append('<p class="display" type="'+data_key[j]+'">'+data_key[j]+':'+data_value[j]+ '</p>');
                            }else{
                                $(selector).append('<p class="display" type="'+data_key[j]+'">'+data_key[j]+':'+str[0]+'</p>');
                            }
                        }else {
                            $(html_obj).html('');
                            vm_obj.$message.error('展示规则参数配置出错！');
                            return
                        }
                    }else {
                        $(selector).append('<p class="display" type="'+data_key[j]+'">'+data_key[j]+':'+data_value[j]+'</p>');
                    }
                }
                //当显示内容为空的情况下
                if("@" == split_char && '' == vm_obj.base['contents'].replace(/^\s+|\s+$/g,"")){
                    $('#other_fixed_show').show();
                }
            }
        }
        //按百分比展示，采集数据时，后台已经做了初步数据分析带上了百分比
        if(vm_obj.base.show_rule_type == 0){
            monitor_show("%");
        }
        // 按颜色展示
        if(vm_obj.base.show_rule_type == 1){
            monitor_show("#");
        }
        //其它展示方式
        if(vm_obj.base.show_rule_type==2){
            monitor_show("@");
        }
        //已获取到指标数据预览区加载图标取消
        vm_obj.preview_loading = false;
        preview_result(html_obj);
        vm_obj.gather_data_test_flag = true;
    }
    //场景编排监控项展示
    if("monitor_scene" == preview_type){
        //取得当前的监控项信息
        current_monitor_item = vm_obj.current_monitor_item;
        var selector_id='basic'+current_monitor_item.item_id;
        var drigging_id = vm_obj.drigging_id;
        var content_json = content_to_json(current_monitor_item.contents);
        var display_rule = current_monitor_item.display_rule
        var selector = null;
        //从采集表获取监控项的采集数据
        $.get("/monitor_scene/get_basic_data/"+current_monitor_item.item_id, function (res){
            for(i in res){
                key=i
            }
            //将采集结果转换为json,这里的key固定为“measures”
            //原因是这里只取度量值，不考虑历史垃圾数据
            var gather_base_test_data=JSON.parse(res["measures"]);
            //场景播放不需要右键菜单
            if(!vm_obj.play){
                $('[type='+selector_id+']').html("");                  //清空dom
                $('[type='+selector_id+']').append('<input class="score_input" type="text" value="0">');
                $('[type='+selector_id+']').append('<div class="right_click"><span class="score">打分</span><span class="delete">删除监控项</span><span class="line">连线</span>'+vm.sizeStrFun()+'</div>');
            }
            var bgcolor = null;
            let scene_show = function(split_char){
                 for(let i=0;i<gather_base_test_data.length;i++){
                    let selector='.div'+drigging_id+i;
                    let data_org = [];
                    let data_key=[];
                    let data_value=[];
                    for(k in gather_base_test_data[i]){
                        if(gather_base_test_data[i][k].toString().indexOf(split_char)>-1){
                            //保留颜色信息
                            if("#" == split_char){
                                bgcolor = gather_base_test_data[i][k].split(split_char)[1];
                            }
                        }
                        //颜色展示可以没有值
                        if(!isEmptyObject(content_json)){
                            for(x in content_json){
                                if(x == k){
                                    data_org.push(k)
                                    data_key.push(content_json[x]);
                                    data_value.push(gather_base_test_data[i][k]);
                                }
                            }
                        }else{
                            //展示内容为空，只放度量值
                            if(gather_base_test_data[i][k].toString().indexOf(split_char)>-1){
                                data_org.push(k);
                                data_key.push(k);
                                data_value.push(gather_base_test_data[i][k]);
                            }
                        }
                    }
                    $('[type='+selector_id+']').append('<div class="div'+drigging_id+i+'"></div>');
                    for(let j=0;j<data_key.length;j++){
                        if(data_org[j]==current_monitor_item.target_name+'_'+current_monitor_item.measure_name){
                            var data_value_str=data_value[j].toString();
                            if(data_value_str.indexOf(split_char)>-1){
                                //颜色展示可以没有值
                                if(!isEmptyObject(content_json)){
                                    if("%" == split_char){
                                       $(selector).append('<p>'+data_key[j]+':'+data_value[j]+'</p>');
                                    }else{
                                        $(selector).append('<p>'+data_key[j]+':'+data_value[j].split(split_char)[0]+'</p>');
                                    }
                                }else{
                                    $(selector).append('<p >&nbsp;</p>');
                                    if("@" == split_char){
                                        $(selector).append('<p >'+data_value[j].split(split_char)[1]+'</p>');
                                    }
                                }
                            }else {
                                $('#base_test_text').html('');
                                vm.$message.error('采集规则配置出错！');
                                return
                            }
                        }else {
                            $(selector).append('<p>'+data_key[j]+':'+data_value[j]+'</p>');
                        }
                    }
                }
            }
            //按百分比展示
            if(current_monitor_item.display_type ==0){
                scene_show("%");
            }
            //按颜色展示
            if(current_monitor_item.display_type == 1){
                scene_show("#");
                $('[type='+selector_id+']').css("background","#"+bgcolor);
            }
            //其它展示类型
            if(current_monitor_item.display_type==2){
               scene_show("@");
            }
            preview_result('[type='+selector_id+']');
        }).catch(function (e) {
                vm.$message.error('采集失败！');
                $('[type='+selector_id+']').html('');
        });
    }
}

/**
 * 设置预览区域的展示内容(根据“展示规则”和“显示内容”显示预览效果)
 * @param vm_obj
 * @param html_obj
 */
function collection_content_change(vm_obj,html_obj){
    //转json
    var content_json = content_to_json(vm_obj.base.contents);
    $(html_obj).find('.display').hide();       //隐藏预览区域的dom
    for(x in content_json){                             //遍历json
        $(html_obj).find('[type='+x+']').show();   //显示内容存在的key会在预览区域显示
        let len=$(html_obj+" p").length;
        for(let i=0;i<len;i++){
            let dom_type=$(html_obj+" p").eq(i).attr('type');//获取dom的type
            let value1=$(html_obj+" p").eq(i).text().split(':')[0];//获取dom的text ：前面的内容
            if(x==dom_type){//显示内容的key等于dom的type
                let text=$(html_obj+" p").eq(i).text();
                $(html_obj+" p").eq(i).html(text.replace(value1,content_json[x]));//将dom的text ：前面的内容替换成显示内容的value
                var content = $(html_obj+" p").eq(i).html();
            }
        }
    }
}

/**
 * 设置预览区域字体
 * @param vm_obj
 * @param html_obj
 */
function collection_base_size(vm_obj,html_obj){
    var font_size = null;
    if(!vm_obj.base){
        font_size = vm_obj.font_size;
    }else{
        font_size = vm_obj.base.font_size;
    }
    $(html_obj).css('font-size', font_size)
}

/**
 * 设置预览区域高度
 * @param vm_obj
 * @param html_obj
 */
function collection_base_height_change(vm_obj,html_obj){
    var heigth = null
    if(vm_obj.base){
        heigth = vm_obj.base.height;
        $(html_obj).children().css('height', heigth);
    }else {
        heigth = vm_obj.height;
        $(html_obj).css('height', heigth);
    }
}
/**
 * 设置预览区域宽度
 * @param vm_obj
 * @param html_obj
 */
function collection_base_width_change(vm_obj,html_obj){
    var width = null
    if(vm_obj.base){
        width = vm_obj.base.width;
        $(html_obj).children().css('width', width);
    }else {
        width = vm_obj.width;
        $(html_obj).css('width', width);
    }
}
//判断空对象
function isEmptyObject(obj){
   for(var key in obj){
       return false
   };
   return true
}
//将显示内容转换为json
function content_to_json(content){
    var content_str = content.substring(0,content.lastIndexOf('@')); //去@符号
    var content_obj = '{'+content_str.replace(/@\n/g,',')+'}';      //加{}
    var content_json = JSON.parse(content_obj);           //转json
    return content_json;
}
