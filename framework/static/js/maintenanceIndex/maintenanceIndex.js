var maintenanceObj = {};

maintenanceObj.pie = function(){

    var myChart = echarts.init(document.getElementById('maintenancePie'), 'macarons');

    var seriesData = [{
        name: '已执行',
        value: 30
    },{
        name: '正执行',
        value: 11
    },{
        name: '执行出错',
        value: 26
    },{
        name: '未执行',
        value: 33
    }];
    var legendData = ['已执行', '正执行', '执行出错', '未执行'];
    option = {
        tooltip : {
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
        series : [
            {
                name: '执行状态',
                type: 'pie',
                radius : '50%',
                center: ['50%', '30%'],
                data: seriesData,
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
};

maintenanceObj.bar = function(){

    var myChart = echarts.init(document.getElementById('maintenanceBar'), 'macarons');

    option = {
        tooltip : {
            trigger: 'axis',
            axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        barWidth: 15,
        legend: {
            data: ['已执行', '正执行','执行出错','未执行'],
            bottom: 10,
            right: 30
        },
        grid: {
            left: '3%',
            right: '4%',
            top: 10,
            containLabel: true
        },
        xAxis:  {
            type: 'category',
            data: ['6:00','7:00','8:00','9:00','10:00','11:00','12:00',
                '13:00', '14:00', '15:00', '16:00', '17:00', '18:00',
                '19:00', '20:00', '21:00', '22:00', '23:00', '24:00',
                '1:00', '2:00', '3:00', '4:00', '5:00', '6:00']
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name: '已执行',
                type: 'bar',
                stack: 'data',
                data: [0, 2, 4, 6, 8,
                    10, 0, 2, 4, 6,
                    8, 10, 0, 2, 4,
                    6, 8, 10, 0, 2,
                    4, 6, 8, 10, 0]
            },
            {
                name: '正执行',
                type: 'bar',
                stack: 'data',
                data: [2, 1, 2, 6, 4,
                    2, 1, 2, 6, 4,
                    2, 1, 2, 6, 4,
                    2, 1, 2, 6, 4,
                    2, 1, 2, 6, 4]
            },
            {
                name: '执行出错',
                type: 'bar',
                stack: 'data',
                data: [2, 4, 6, 10, 12,
                    2, 4, 6, 10, 12,
                    2, 4, 6, 10, 12,
                    2, 4, 6, 10, 12,
                    2, 4, 6, 10, 12]
            },
            {
                name: '未执行',
                type: 'bar',
                stack: 'data',
                data: [6, 2, 8, 4, 10,
                    6, 2, 8, 4, 10,
                    6, 2, 8, 4, 10,
                    6, 2, 8, 4, 10,
                    6, 2, 8, 4, 10]
            }
        ]
    };
    myChart.setOption(option);
};

maintenanceObj.verticalBar = function(){
    var doneContent = $('.maintenanceVerticalDone').find('.el-step__main').find('.el-step__title');
    var unexecContent = $('.maintenanceVerticalUnexec').find('.el-step__main').find('.el-step__title');
    //遍历垂直步骤条，分别添加当前步骤描述内容
    doneContent.each(function(index, elem){
        var doneText = $(elem).html();
        doneText += '&nbsp;&nbsp;&nbsp;&nbsp;<span class="maintenanceVerticalBarDesc">已执行场景展示</span>';
        $(elem).html(doneText);
    });
    unexecContent.each(function(index, elem){
        var unexecText = $(elem).html();
        unexecText += '&nbsp;&nbsp;&nbsp;&nbsp;<span class="maintenanceVerticalBarDesc">待执行场景展示</span>';
        $(elem).html(unexecText);
    });
};

$(function(){
    //echars饼状图初始化
    //maintenanceObj.pie();
    //echars条形图初始化
    //maintenanceObj.bar();
    //已执行场景与待执行场景的步骤条描述设置
    //maintenanceObj.verticalBar();
});
