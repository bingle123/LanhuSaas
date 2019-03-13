axios.interceptors.request.use((config) => {
        config.headers['X-Requested-With'] = 'XMLHttpRequest';
        let regex = /.*csrftoken=([^;.]*).*$/; // 用于从cookie中匹配 csrftoken值
        config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
        return config
    });
function job_monitor(job_params){
    console.log(job_params);
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
    $('[type='+selector_id+']').append('<div class="right_click"><span class="score">打分</span><span class="delete">删除监控项</span></div>');
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
    $('[type='+selector_id+']').append('<div class="right_click"><span class="score">打分</span><span class="delete">删除监控项</span></div>');
    var height=Number(job_params.height)+50;
    console.log(height)
    $('[type='+selector_id+']').css('height',height+'px');
    $('[type='+selector_id+']').css('width',job_params.width);
    $('[type='+selector_id+']').find("*").css('font-size',job_params.font_size);
}
function show_chart_active(item_id,chart_type,height,width,drigging_id){
    var new_res=[]
    var chartdata=[]
    $.get("/monitor_scene/get_chart_data/"+item_id,function (res) {
        res=res.message
        console.log(res)
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
            console.log(barCount,barX,chartData)
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
function base_monitor_active(item_id,font_size,height,width,content) {
        var contents=content.split('#')
        var count=(contents.length-1)/2
        var con=[]
        for(var i=0;i<count;i++){
            var temp={
                'key':contents[(i*2)],
                'value':contents[(i*2+1)].split("=")[0]
            }
            con.push(temp)
        }
        console.log(con)
     $.get("/monitor_scene/get_basic_data/"+item_id,function (res){
        var selector_id='basic'+item_id
        var cricle='<div id="status" style="display: inline-block;margin-left:5px;width:16px;height:16px;background-color:lawngreen;border-radius:50%;-moz-border-radius:50%;-webkit-border-radius:50%;"></div>'
         var content=''
        for(key in res){
            if(key!='DB_CONNECTION'&&key!='URL_CONNECTION'&&key!='FILE_EXIST'){
                for(var i=0;i<con.length;i++){
                    if(con[i].value==key){
                         content+='<div>'+con[i].key+':'+res[key]+'</div>'
                    }
                }
            }
        }
        var status=1
        for(key in res){
            if(key=='DB_CONNECTION'){
                status=res[key]
                content+='<div>'+'行情数据库连接状态:'+cricle+'</div>'
            }else if(key=='URL_CONNECTION'){
                    status=res[key]
                 content+='<div>'+'行情接口状态:'+cricle+'</div>'
            }else if(key=='FILE_EXIST'){
                    status=res[key]
                 content+='<div>'+'深圳行情文件状态:'+cricle+'</div>'
            }
        }
        $('[type='+selector_id+']').html(content)
        $('[type='+selector_id+']').css({
        'text-align':'center'
    })
        if(status==2){
            $("#status").css('background-color','darkgreen')
        }else if(status==-1){
            $("#status").css('background-color','red')
        }else if(status==0){
            $("#status").css('background-color','grey')
        }
    $('[type='+selector_id+']').find("*").css("font-size",font_size)
    $('[type='+selector_id+']').css('height',height);
    $('[type='+selector_id+']').css('width',width);
    },dataType='json')
}
function base_monitor(item_id,font_size,height,width,content) {
    selector_id='basic'+item_id
    console.log(content)
    var circle1='<div id="status" style="display: inline-block;margin-left:5px;width:16px;height:16px;background-color:lawngreen;border-radius:50%;-moz-border-radius:50%;-webkit-border-radius:50%;"></div>'
    var circle4='<div id="status" style="display: inline-block;margin-left:5px;width:16px;height:16px;background-color:red;border-radius:50%;-moz-border-radius:50%;-webkit-border-radius:50%;"></div>'
    var circle3='<div id="status" style="display: inline-block;margin-left:5px;width:16px;height:16px;background-color:grey;border-radius:50%;-moz-border-radius:50%;-webkit-border-radius:50%;"></div>'
    var circle2='<div id="status" style="display: inline-block;margin-left:5px;width:16px;height:16px;background-color:darkgreen;border-radius:50%;-moz-border-radius:50%;-webkit-border-radius:50%;"></div>'
    var asd='<div class="display: inline-block;">'
        $('[type='+selector_id+']').html("");
        $('[type='+selector_id+']').append("<div>"+content +"</div>");
        $('[type='+selector_id+']').append('<input class="score_input" type="text" value="0">');
        $('[type='+selector_id+']').append('<div class="right_click"><span class="score">打分</span><span class="delete">删除监控项</span></div>');
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
            console.log(icon1)
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
            $('[type='+selector_id+']').append('<div class="right_click"><span class="score">打分</span><span class="delete">删除监控项</span></div>');
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
            $('[type='+selector_id+']').append('<div class="right_click"><span class="score">打分</span><span class="delete">删除监控项</span></div>');
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
                        $('[type='+selector_type+']').append('<div class="right_click"><span class="score">打分</span><span class="delete">删除监控项</span></div>');
                axios({
                    method:'post',
                    url:'/monitor_item/flow_change/',
                    data: {
                        template_id:value1
                    }
                }).then(function (res) {
                    {
                        console.log(res);
                        location = res.data.activities
                        line = res.data.flows
                        console.log(line[0]['source']['id'])
                        for(var i=0;i<line.length;i++){
                           line[i].source.id =line[i].source.id+value2
                           line[i].target.id =line[i].target.id+value2
                        }
                        console.log(line)
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