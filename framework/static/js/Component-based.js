function job_monitor(job_params){
    selector_id='job_'+job_params.id
    var status=job_params.status
    if(status==0){
        $('#'+selector_id).append($('<div class="unexecuted" style="color: grey;"><h1>作业未执行</h1><i class="el-icon-error" style="color: grey;font-size: 30px;margin-top: 20px;"></i></div>'))
    }else if(status==1){
        $('#'+selector_id).append($('<div class="success" style="color: green;display: none"><h1>作业执行成功</h1><i class="el-icon-success" style="color: green;font-size: 30px;margin-top: 20px;"></i></div>'))
    }else if(status==2){
        $('#'+selector_id).append($('<div class="loading" style="color: orange;"><h1>正在执行</h1><i class="el-icon-loading" style="color: orange;font-size: 30px;margin-top: 20px;"></i></div>'))
    }else if(status==-1){
        $('#'+selector_id).append($('<div class="error" style="color: red;"><h1>作业执行失败</h1><i class="el-icon-error" style="color: red;font-size: 30px;margin-top: 20px;"></i></div>'))
    }
    $('#'+selector_id).css('height',job_params.height);
    $('#'+selector_id).css('width',job_params.width);
}
function chart_monitor(item_id,chart_type,height,width) {
    new_res=[]
    var barX=[]
    var barCount=[]
    var person_count=''
    var chartdata=[]
    $.post("/monitorScene/get_chart_data/"+item_id,function (res) {
        res=res.message
       for(r in res){
           if(isNotANumber(res[r].values[0])){
               new_res[1]=res[r]
           }else{
                new_res[0]=res[r]
           }
       }
       console.log(new_res)
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
        show_chart(barX,barCount,person_count,chartdata,chart_type,height,width)
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

function show_chart(barX,barCount,person_count,chartData,chart_type,height,width) {
        console.log(chartData)
        if (chart_type == "饼图") {
            myChart = echarts.init(document.getElementById('maintenancePie'), 'macarons');
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

            var myChart = echarts.init(document.getElementById('maintenancePie'), 'macarons');
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
            myChart = echarts.init(document.getElementById('maintenancePie'), 'macarons');
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
        $('#maintenanceIndex').find("canvas").css('height',height);
        $('#maintenanceIndex').find("canvas").css('width',width)
}