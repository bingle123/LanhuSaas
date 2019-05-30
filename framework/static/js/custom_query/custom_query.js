let site_url = null;
let vue = null;
$(function(){
    //csrf验证
    axios.interceptors.request.use((config) => {
        config.headers['X-Requested-With'] = 'XMLHttpRequest';
        let regex = /.*csrftoken=([^;.]*).*$/; // 用于从cookie中匹配 csrftoken值
        config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
        return config
    });
    site_url = $('#siteUrl').val();
    vue = new Vue({
        el: '#customQueryManage',
        data: {
            dialogVisible1: false,
            dialogVisible2: false,
            dialogVisible3: false,
            dialogVisible4: false,
            customQueryDatabase: [],
            tableData: [],
            //灵活得到结果集的列名
            fileds: [],
            //echart对象
            myChart: '',
            //得到列长，美化展示
            TableLength: 0,
            //echart数据
            chartData: [],
            person_count: '',
            //如果更新了sql语句没有检查，不允许保存
            add_flag: true,
            customQueryShowType: [
                '列表',
                '折线图',
                '柱状图',
                '饼图',
            ],
            currentPage: 1,
            //当前自定义查询列表状态：list列表,edit修改,add添加
            customQueryTableStatus: 'list',
            //当前自定义查询Table所使用的数据集
            customQueryTableData: null,
            //当前正在添加或修改的自定义查询的保存对象
            customQueryData: {},
            //自定义查询的名称搜索
            queryNameSearch: '',
            //当前有多少页
            queryCount: 0,
        },
        methods: {
            //sql测试
            sql_test() {
                var data = {
                    'conn_id': this.customQueryData.conn_id,
                    'sql': this.customQueryData.query_sql
                };
                axios({
                    url: site_url+'custom_query/sql_test',
                    method: 'post',
                    data: data
                }).then((res) => {
                    console.log(res)
                    if (res.data.result == 'error') {
                        this.$message.warning("您输入SQL语句有误!请检查")
                    } else {
                        res = res.data.data
                        vue.add_flag = true
                        vue.fileds = []
                        for (key in res[0]) {
                            vue.fileds.push(key)
                        }
                        vue.TableLength = 1200 / vue.fileds.length
                        if (vue.customQueryData.show_type == '列表') {
                            vue.dialogVisible1 = true
                            vue.tableData = res
                        } else {
                            if (vue.fileds.length > 2) {
                                this.$message.warning("目前图表功能只支持二维，请修改SQL语句！")
                            } else {
                                vue.chartData = []
                                var name = ""
                                var value = ""
                                vue.dialogVisible2 = true
                                for (var i = 0; i < res.length; i++) {
                                    for (var j = 0; j < vue.fileds.length; j++) {
                                        if (!(parseFloat(res[i][vue.fileds[j]]).toString() == "NaN")&&res[i][vue.fileds[j]]<10000000){
                                            value = vue.fileds[j]
                                        } else {
                                            name = vue.fileds[j]
                                        }
                                    }
                                    vue.person_count = name
                                    temp = {
                                        'name': res[i][name],
                                        'value': res[i][value]
                                    }
                                    vue.chartData.push(temp)
                                }
                            }
                        }
                    }
                });
            },
            //定制查询的展示function
            customQueryShow(row) {
                var data = {
                    'conn_id': row.conn_id,
                    'sql': row.query_sql
                };
                axios({
                    url: site_url+'custom_query/sql_test',
                    method: 'post',
                    data: data
                }).then((res) => {
                    if (res.data.result == 'error') {
                        this.$message.warning("您输入SQL语句有误!请检查")
                    } else {
                        res = res.data.data
                        vue.add_flag = true
                        vue.fileds = []
                        for (key in res[0]) {
                            vue.fileds.push(key)
                        }
                        vue.TableLength = 1200 / vue.fileds.length
                        if (row.show_type == '列表') {
                            vue.dialogVisible3 = true
                            vue.tableData = res
                        } else {
                            vue.customQueryData.show_type=row.show_type
                            if (vue.fileds.length > 2) {
                                this.$message.warning("目前图表功能只支持二维，请修改SQL语句！")
                            } else {
                                vue.chartData = []
                                var name = ""
                                var value = ""
                                vue.dialogVisible4 = true
                                for (var i = 0; i < res.length; i++) {
                                    for (var j = 0; j < vue.fileds.length; j++) {
                                        if (!(parseFloat(res[i][vue.fileds[j]]).toString() == "NaN")&&res[i][vue.fileds[j]]<10000000) {
                                            value = vue.fileds[j]
                                        } else {
                                            name = vue.fileds[j]
                                        }
                                    }
                                    vue.person_count = name
                                    temp = {
                                        'name': res[i][name],
                                        'value': res[i][value]
                                    }
                                    vue.chartData.push(temp)
                                }
                            }
                        }
                    }
                });
            },
            isNotANumber(inputData) {
                console.log(inputData)
                //isNaN(inputData)不能判断空串或一个空格
                //如果是一个空串或是一个空格，而isNaN是做为数字0进行处理的，而parseInt与parseFloat是返回一个错误消息，这个isNaN检查不严密而导致的。
                if (parseFloat(inputData).toString() == "NaN") {
                    return false;
                } else {
                    return true;
                }
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
                        this.customQueryDatabase = json;
                        console.log(this.customQueryDatabase);
                    }

                }).catch((res) => {
                    console.log('获取数据库连接错误')
                })
            },
            //弹出错误信息
            customQueryPopupErrorMessage: function (msg) {
                this.$notify.error({
                    title: '错误',
                    message: msg
                });
            }
            ,
            //显示加载中..
            customQueryPopupLoading: function () {
                //返回加载标记，供外部关闭
                return this.$loading({
                    lock: true,
                    text: '正在拼命加载中...',
                    spinner: 'el-icon-loading',
                    background: 'rgba(0, 0, 0, 0.7)'
                });
            },
            //自定义查询搜索方法
            customQuerySearch: function () {
                this.customQueryPageChange(1);
            },
            //自定义查询添加页面
            customQueryAdd: function () {
                this.customQueryTableStatus = 'add';
            },
            //自定义查询数据分页获取
            customQueryPageChange: function (page) {
                const loading = this.customQueryPopupLoading();
                var data = {
                    search: this.queryNameSearch,
                    page: page,
                    limit: 5
                };
                axios({
                    method: 'post',
                    url: site_url+'custom_query/select_queries_pagination',
                    data: data
                }).then((res) => {
                    loading.close();
                    this.customQueryTableData = res.data.items;
                    this.queryCount = res.data.pages;
                    this.currentPage = page;
                    if (page > res.data.pages) {
                        this.currentPage = res.data.pages;
                    }
                }).catch((res) => {
                    loading.close();
                    var msg = '自定义查询信息加载失败！';
                    this.customQueryPopupErrorMessage(msg + res);
                });
            },
            //自定义查询编辑
            customQueryEdit: function (id) {
                const loading = this.customQueryPopupLoading();
                var url = site_url+'custom_query/select_query';
                var editData = {};
                editData.id = id;
                axios({
                    method: 'post',
                    url: url,
                    data: editData,
                }).then((res) => {
                    loading.close();
                    this.customQueryData = res.data;
                    this.customQueryTableStatus = 'edit';
                }).catch((res) => {
                    loading.close();
                    var msg = '获取自定义查询数据失败！' + res;
                    this.customQueryPopupErrorMessage(msg);
                });
            },
            //自定义查询删除
            customQueryDelete: function (id) {
                const loading = this.customQueryPopupLoading();
                this.$confirm('确认删除自定义查询信息吗?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                    center: true
                }).then(() => {
                    var url = site_url+'custom_query/del_query';
                    var delData = {};
                    delData.id = id;
                    axios({
                        method: 'post',
                        url: url,
                        data: delData,
                    }).then((res) => {
                        loading.close();
                        if ('ok' == res.data.message) {
                            this.customQueryPageChange(this.currentPage);
                            this.$message({
                                type: 'success',
                                message: '删除自定义查询成功!'
                            });
                        } else {
                            var msg = '请求删除自定义查询失败！';
                            this.customQueryPopupErrorMessage(msg + res.data.message);
                        }
                    }).catch((res) => {
                        loading.close();
                        var msg = '请求删除自定义查询失败！';
                        this.customQueryPopupErrorMessage(msg + res);
                    });
                }).catch(() => {
                    loading.close();
                    this.$message({
                        type: 'info',
                        message: '取消自定义查询删除'
                    });
                });
            },
            //保存自定义查询
            customQuerySave: function (formName) {
                if (!vue.add_flag) {
                    this.$message({
                        type: 'warning',
                        message: '请先验证sql再保存!'
                    });
                } else {
                    const loading = this.customQueryPopupLoading();
                    var url = site_url+'custom_query/add_query';
                    axios({
                        method: 'post',
                        url: url,
                        data: this.customQueryData,
                    }).then((res) => {
                        loading.close();
                        if ('ok' == res.data.message) {
                            if (this.customQueryTableStatus == 'edit') {
                                this.customQueryPageChange(this.currentPage);
                            } else if (this.customQueryTableStatus == 'add') {
                                this.customQueryPageChange(res.data.total_pages);
                            }
                            this.customQueryList();
                        } else {
                            var msg = '请求添加/修改自定义查询失败！';
                            this.customQueryPopupErrorMessage(msg + res);
                        }
                    }).catch((res) => {
                        loading.close();
                        var msg = '请求添加/修改自定义查询失败！';
                        this.customQueryPopupErrorMessage(msg + res);
                    });
                }
            },
            //显示自定义查询清单
            customQueryList: function () {
                this.customQueryData = {};
                this.customQueryTableStatus = 'list';
            },
            //Data对象根据表达式转字符串
            dataToString: function (fmt, date) {
                var o = {
                    "M+": date.getMonth() + 1,                 //月份
                    "d+": date.getDate(),                    //日
                    "h+": date.getHours(),                   //小时
                    "m+": date.getMinutes(),                 //分
                    "s+": date.getSeconds(),                 //秒
                    "q+": Math.floor((date.getMonth() + 3) / 3), //季度
                    "S": date.getMilliseconds()             //毫秒
                };
                if (/(y+)/.test(fmt))
                    fmt = fmt.replace(RegExp.$1, (date.getFullYear() + "").substr(4 - RegExp.$1.length));
                for (var k in o)
                    if (new RegExp("(" + k + ")").test(fmt))
                        fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
                return fmt;
            },
            show_chart() {
                var chartData = vue.chartData
                var person_count = vue.person_count
                var chart_type = vue.customQueryData.show_type
                if (this.myChart != null && this.myChart != "" && this.myChart != undefined) {
                    this.myChart.dispose();
                }
                console.log(chartData)
                if (chart_type == "饼图") {
                    this.myChart = echarts.init(document.getElementById('show2'), 'macarons');
                    var legendData = [];
                    for (var i = 0; i < chartData.length; i++) {
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
                                name: person_count,
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
                    this.myChart.setOption(option);
                }
                if (chart_type == "柱状图") {
                    myChart = echarts.init(document.getElementById('show2'), 'macarons');
                    let barX = [];
                    let barCount = [];
                    for (var i = 0; i < chartData.length; i++) {
                        this.$set(barX, i, chartData[i].name);
                        this.$set(barCount, i, chartData[i].value);
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
                    myChart = echarts.init(document.getElementById('show2'), 'macarons');
                    let lineX = [];
                    let lineCount = [];
                    for (var i = 0; i < chartData.length; i++) {
                        this.$set(lineX, i, chartData[i].name);
                        this.$set(lineCount, i, chartData[i].value);
                    }
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
                                name: person_count,
                                type: 'line',
                                smooth: true,
                                itemStyle: {normal: {areaStyle: {type: 'default'}}},
                                data: lineCount,
                            },
                        ]
                    };
                    myChart.setOption(option);
                }
            },
            isNotANumber(inputData) {
                //isNaN(inputData)不能判断空串或一个空格
                //如果是一个空串或是一个空格，而isNaN是做为数字0进行处理的，而parseInt与parseFloat是返回一个错误消息，这个isNaN检查不严密而导致的。
                if (parseFloat(inputData).toString() == "NaN") {
                    return false;
                } else {
                    return true;
                }
            }
        },
        mounted() {
            //this.loadAlertRuleInfo();
            this.get_db_connections();
            this.customQueryPageChange(1);
        }
    })
})