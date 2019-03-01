axios.interceptors.request.use((config) => {
        config.headers['X-Requested-With'] = 'XMLHttpRequest';
        let regex = /.*csrftoken=([^;.]*).*$/; // 用于从cookie中匹配 csrftoken值
        config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
        return config
    });
function job_monitor(job_params){
    console.log(job_params);
    selector_id='job'+job_params.job_id
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
    $('[type='+selector_id+']').css('height',job_params.height);
    $('[type='+selector_id+']').css('width',job_params.width);
    $('[type='+selector_id+']').find("*").css('font-size',job_params.font_size);
}
function chart_monitor(item_id,chart_type,height,width,drigging_id) {
    new_res=[]
    var barX=[]
    var barCount=[]
    var person_count=''
    var chartdata=[]
    $.get("/monitorScene/get_chart_data/"+item_id,function (res) {
        res=res.message
       for(r in res){
           if(isNotANumber(res[r].values[0])){
               new_res[1]=res[r]
           }else{
                new_res[0]=res[r]
           }
       }
        barX=new_res[0].values
        barCount=new_res[1].values
        person_count=new_res[1].key
        for(var i=0;i<new_res[0].values.length;i++){
            temp={
                'name':new_res[0].values[i],
                'value':new_res[1].values[i]
            }
            chartdata.push(temp)
        }
        console.log(chartdata)
        show_chart(item_id,barX,barCount,person_count,chartdata,chart_type,height,width,drigging_id)
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

function show_chart(item_id,barX,barCount,person_count,chartData,chart_type,height,width,drigging_id) {
        if (this.myChart != null && this.myChart != "" && this.myChart != undefined) {
                this.myChart.dispose();
            }
        if (chart_type == "饼图") {
            myChart = echarts.init(document.getElementById(item_id), 'macarons');
            console.log(myChart)
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
                    data: barX
                },
                series: [
                    {
                        name: person_count,
                        type: 'pie',
                        radius: '50%',
                        center: ['80%', '30%'],
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
                                show: true
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

            var myChart = echarts.init(document.getElementById(item_id), 'macarons');
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
            console.log(barCount)
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
function base_monitor(item_id,font_size,height,width) {
    $.get("/monitorScene/get_basic_data/"+item_id,function (res){
        console.log(res)
        var selector_id='basic'+item_id
        var cricle='<div id="status" style="display: inline-block;margin-left:5px;width:16px;height:16px;background-color:lawngreen;border-radius:50%;-moz-border-radius:50%;-webkit-border-radius:50%;"></div>'
        var content=''
        for(key in res){
            if(key=='DB_CONNECTION'){
                content+='<div>'+'数据库连接状态:'+cricle+'</div>'
            }else{
                 content+='<div>'+key+':'+res[key]+'</div>'
            }
        }
        console.log(content)
        $('[type='+selector_id+']').html(content)
        $('[type='+selector_id+']').css({
        'text-align':'center',
        'width': '100%',
        'height': '40%',
    })
    $('[type='+selector_id+']').find("*").css("font-size",font_size)
    $('[type='+selector_id+']').css('height',height);
    $('[type='+selector_id+']').css('width',width);
    },dataType='json')
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
                var flow_canvas = "flow_canvas"+value2
                var jtk_content="jtk-content"+value2
                var charts = "charts"+value2
                var jtk_surface_nopan="jtk-surface-nopan"+value2
                var workflow_canvas="workflow-canvas"+value2
                var jtk_surface="jtk-surface"+value2
                var workflow_box="workflow-box"+value2
                var location ='';
                var line='';
                var template_list={};
                var constants='';
                var cc=" <div id=\""+flow_canvas+"\" style=\"text-align:center;width: 300px;height: 200px;background-color: whitesmoke;\">\n" +
                            "                                <div id=\""+selector_id+"\" class=\"clearfix "+workflow_box+"\" style=\"width: 100%;position: relative;\">\n" +
                            "\n" +
                            "                                        <div class=\""+workflow_canvas+"\" style=\"margin-left: 0px;padding-left: 0px\">\n" +
                            "                                            <!-- 画布模板 start -->\n" +
                            "                                            <div class=\""+jtk_content+"\">\n" +
                            "                                                <div class=\"jtk-demo-canvas canvas-wide "+jtk_surface+" "+jtk_surface_nopan+"\"\n" +
                            "                                                     id=\""+selector_canvas+"\" style=\"height:500px\">\n" +
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
                            "                                            <div class=\"jtk-window jtk-node workfolw-node start-node\" id=\"{"+charts+"}\"\n" +
                            "                                                 data-type=\"EmptyEndEvent\">\n" +
                            "                                                <div class=\"node-wrapper\">\n" +
                            "                                                    <div class=\"node-icon-start\">\n" +
                            "                                                        <i class=\"bk-icon icon-star-shape\"></i>\n" +
                            "                                                    </div>\n" +
                            "                                                </div>\n" +
                            "                                            </div>\n" +
                            "                                             <div class=\"jtk-window jtk-node workfolw-node start-node\" id=\"{"+charts+"}\"\n" +
                            "                                                  data-type=\"EmptyStartEvent\">\n" +
                            "                                                <div class=\"node-wrapper\">\n" +
                            "                                                    <div class=\"node-icon-start\">\n" +
                            "                                                        <i class=\"bk-icon icon-star-shape\"></i>\n" +
                            "                                                    </div>\n" +
                            "                                                </div>\n" +
                            "                                            </div>\n" +
                            "                                            <div class=\"jtk-window jtk-node workfolw-node database-node\" id=\"{"+charts+"}\"\n" +
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
                axios({
                    method:'post',
                    url:'/monitor/flow_change/',
                    data: {
                        template_id:value1
                    }
                }).then(function (res) {
                    {

                        location = res.data.activities
                        line = res.data.flows
                        console.log(line[0]['source']['id'])
                        for(var i=0;i<line.length;i++){
                           line[i].source.id =line[i].source.id+value2
                           line[i].target.id =line[i].target.id+value2
                        }
                        console.log(line)
                        for(var i=0;i<location.length;i++){
                           location[i]['id'] = location[i]['id']+""+value2+""
                        }
                        //显示流程单元中的预览图
                        console.log(location)
                        console.log(line)
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