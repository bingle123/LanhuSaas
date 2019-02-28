//csrf验证
axios.interceptors.request.use((config) => {
    config.headers['X-Requested-With'] = 'XMLHttpRequest';
    let regex = /.*csrftoken=([^;.]*).*$/; // 用于从cookie中匹配 csrftoken值
    config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
    return config
});
var vm = new Vue({
    el: '#app',
    data: {
        myDate: [],
        list: [],
        historyChose: [],
        dateTop: '',
        loading2: true,
        areas: [],
        area:1,
        country:'',
        file_url:'/market_day/get_file/1',
        zones:[],
        zone:'',
        dialogVisible: false
    },
    props: {
        markDate: {
            type: Array,
            default: () => []
        },
        markDateMore: {
            type: Array,
            default: () => []
        },
        textTop: {
            type: Array,
            default: () => ['日', '一', '二', '三', '四', '五', '六']
        },
        sundayStart: {
            type: Boolean,
            default: () => true
        },
        agoDayHide: {
            type: String,
            default: `0`
        },
        futureDayHide: {
            type: String,
            default: `2554387200`
        }
    },
    created() {
        this.intStart();
        this.myDate = new Date();
    },
    methods: {
        loadingfinsh() {
            this.loading2 = false;
        },
        intStart() {
            sundayStart = this.sundayStart;
        },
        setClass(data) {
            let obj = {};
            obj[data.markClassName] = data.markClassName;
            return obj;
        },
        clickDay: function (item, index) {
            var vm=this
            if (item.isMark) {
                vm.$confirm('此操作将删除当前节假日, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    axios({
                        method:'post',
                        url:'/market_day/delone/',
                        data:{
                            'date':item.date,
                            'timezone': vm.zone
                        }
                    }).then(function (resp) {
                        vm.$message({
                            type: 'success',
                            message: '删除成功!'
                        });
                        for (var i = 0; i < vm.markDate.length; i++) {
                            if (vm.markDate[i] == item.date) {
                                vm.markDate.splice(i, 1)
                            }
                        }
                    })
                }).catch(() => {
                    vm.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                })
            } else {
                this.$confirm('此操作将该日修改为节假日, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    axios({
                        method:'post',
                        url:'/market_day/addone/',
                        data:{
                            'date':item.date,
                            'timezone': vm.zone
                        }
                    }).then(function (resp) {
                        vm.$message({
                            type: 'success',
                            message: '添加成功!'
                        });
                        vm.markDate.push(item.date)
                    })
                })
            }
            if (item.otherMonth === 'nowMonth' && !item.dayHide) {
                this.getList(this.myDate, item.date);
            }
            if (item.otherMonth !== 'nowMonth') {
                item.otherMonth === 'preMonth' ?
                    this.PreMonth(item.date) :
                    this.NextMonth(item.date);
            }
        },
        ChoseMonth: function (date, isChosedDay = true) {
            date = dateFormat(date);
            this.myDate = new Date(date);
            this.$emit('changeMonth', dateFormat(this.myDate));
            if (isChosedDay) {
                this.getList(this.myDate, date, isChosedDay);
            } else {
                this.getList(this.myDate);
            }
        },
        PreMonth: function (date, isChosedDay = true) {
            date = dateFormat(date);
            this.myDate = getOtherMonth(this.myDate, 'preMonth');
            this.$emit('changeMonth', dateFormat(this.myDate));
            if (isChosedDay) {
                this.getList(this.myDate, date, isChosedDay);
            } else {
                this.getList(this.myDate);
            }
        },
        NextMonth: function (date, isChosedDay = true) {
            date = dateFormat(date);
            this.myDate = getOtherMonth(this.myDate, 'nextMonth');
            this.$emit('changeMonth', dateFormat(this.myDate));
            if (isChosedDay) {
                this.getList(this.myDate, date, isChosedDay);
            } else {
                this.getList(this.myDate);
            }
        },
        forMatArgs: function () {
            let markDate = this.markDate;
            let markDateMore = this.markDateMore;
            markDate = markDate.map((k) => {
                return dateFormat(k);
            })
            markDateMore = markDateMore.map((k) => {
                k.date = dateFormat(k.date)
                return k;
            })
            return [markDate, markDateMore];
        },
        getList: function (date, chooseDay, isChosedDay = true) {
            const [markDate, markDateMore] = this.forMatArgs();
            this.dateTop = `${date.getFullYear()}年${date.getMonth() + 1}月`;
            let arr = getMonthList(this.myDate);
            for (let i = 0; i < arr.length; i++) {
                let markClassName = '';
                let k = arr[i];
                k.chooseDay = false;
                const nowTime = k.date;
                const t = new Date(nowTime).getTime() / 1000;
                //看每一天的class
                for (const c of markDateMore) {
                    if (c.date === nowTime) {
                        markClassName = c.className || '';
                    }
                }
                //标记选中某些天 设置class
                k.markClassName = markClassName;
                k.isMark = markDate.indexOf(nowTime) > -1;
                //无法选中某天
                k.dayHide = t < this.agoDayHide || t > this.futureDayHide;
                if (k.isToday) {
                    this.$emit('isToday', nowTime);
                }
                let flag = !k.dayHide && k.otherMonth === 'nowMonth';
                if (chooseDay && chooseDay === nowTime && flag) {
                    this.$emit('choseDay', nowTime);
                    this.historyChose.push(nowTime);
                    k.chooseDay = true;
                } else if (
                    this.historyChose[this.historyChose.length - 1] === nowTime && !chooseDay && flag
                ) {
                    k.chooseDay = true;
                }
            }
            this.list = arr;
        },
        addarrs() {
            year = new Date().getFullYear()
            var vm=this
            axios.get('/market_day/get_holiday/'+vm.area).then(function (res) {
                for (var i = 0; i < res.data.message.length; i++) {
                    vm.markDate.push(res.data.message[i])
                }
                vm.loadingfinsh()
            })
        },
        get_header_data(){
            axios.get('/market_day/get_header/').then(function (res) {
            })
        },
        upsuccess() {
            this.$message({
                message: '节假日导入成功!',
                type: 'success'
            })
            vm.markDate=[]
            vm.addarrs()
        },
        get_file_url(){
          return this.file_url
        },
        err() {
            this.$message({
                message: '节假日导入失败!',
                type: 'error'
            })
        }, deleteallday() {
            var vm=this
            this.$confirm('此操作将删除所有节假日, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                axios.post('/market_day/delall/'+vm.area).then(function (resp) {
                    vm.$message({
                        type: 'success',
                        message: '删除成功!'
                    });
                    vm.markDate=[]
                })
            }).catch(() => {
                vm.$message({
                    type: 'info',
                    message: '已取消删除'
                });
            })
        },
        get_all_area(){
            axios({
                method:'get',
                url:'/market_day/get_all_area',
            }).then(function (res) {
                res=res.data.message
                vm.areas=[]
                for (var i=0;i<res.length;i++){
                    var label=res[i].country+"("+res[i].timezone+")"
                    temp={
                        'area':label,
                        'value':res[i].id
                    }
                    vm.areas.push(temp)
                }
            })
        },add_area(){
            axios({
                method: 'post',
                url:'/market_day/add_area',
                data:{
                    'country':vm.country,
                    'timezone':vm.zone
                }
            }).then(function (res) {
                vm.$message({
                    type: 'info',
                    message: '添加地区成功!'
                });
                vm.get_all_area()
            })
        },del_area(){
            this.$confirm('此操作将删除该地区以及所有节假日, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                    axios({
                    method: 'get',
                    url:'/market_day/del_area/'+vm.area,
                }).then(function (res) {
                    vm.$message({
                        type: 'info',
                        message: '删除地区成功!'
                    });
                    window.location.reload()
                })
            }).catch(() => {
                vm.$message({
                    type: 'info',
                    message: '已取消删除'
                });
            })
        },get_all_timezone(){
            axios({
                method:'get',
                url:'/market_day/get_all_timezone'
            }).then(function (res) {
                res=res.data.message
                for (var i=0;i<res.length;i++){
                    temp={
                        'value':res[i],
                        'label':res[i]
                    }
                    vm.zones.push(temp)
                }
            })
        }
    },
    mounted() {
        this.addarrs();
        this.getList(this.myDate);
        this.get_header_data()
        this.get_all_area()
        this.get_all_timezone()
    },
    watch: {
        markDate: {
            handler(val, oldVal) {
                this.getList(this.myDate);
            },
            deep: true
        },
        markDateMore: {
            handler(val, oldVal) {
                this.getList(this.myDate);
            },
            deep: true
        },
        agoDayHide: {
            handler(val, oldVal) {
                this.agoDayHide = parseInt(val);
                this.getList(this.myDate);
            },
            deep: true
        },
        futureDayHide: {
            handler(val, oldVal) {
                this.futureDayHide = parseInt(val);
                this.getList(this.myDate);
            },
            deep: true
        },
        sundayStart: {
            handler(val, oldVal) {
                this.intStart();
                this.getList(this.myDate);
            },
            deep: true
        },
        area:{
            handler(val, oldVal) {
                vm.file_url='/market_day/get_file/'+val
                vm.markDate=[]
                this.addarrs()
            },
            deep: true
        }
    }
});

function getDaysInOneMonth(date) {
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const d = new Date(year, month, 0);
    return d.getDate();
}

// 向前空几个
function getMonthweek(date) {
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const dateFirstOne = new Date(year + '/' + month + '/1');
    return this.sundayStart ?
        dateFirstOne.getDay() == 0 ? 7 : dateFirstOne.getDay() :
        dateFirstOne.getDay() == 0 ? 6 : dateFirstOne.getDay() - 1;
}

/**
 * 获取当前日期上个月或者下个月
 */
function getOtherMonth(date, str = 'nextMonth') {
    const timeArray = this.dateFormat(date).split('/');
    const year = timeArray[0];
    const month = timeArray[1];
    const day = timeArray[2];
    let year2 = year;
    let month2;
    if (str === 'nextMonth') {
        month2 = parseInt(month) + 1;
        if (month2 == 13) {
            year2 = parseInt(year2) + 1;
            month2 = 1;
        }
    } else {
        month2 = parseInt(month) - 1;
        if (month2 == 0) {
            year2 = parseInt(year2) - 1;
            month2 = 12;
        }
    }
    let day2 = day;
    const days2 = new Date(year2, month2, 0).getDate();
    if (day2 > days2) {
        day2 = days2;
    }
    if (month2 < 10) {
        month2 = '0' + month2;
    }
    if (day2 < 10) {
        day2 = '0' + day2;
    }
    const t2 = year2 + '/' + month2 + '/' + day2;
    return new Date(t2);
}

// 上个月末尾的一些日期
function getLeftArr(date) {
    const arr = [];
    const leftNum = this.getMonthweek(date);
    const num = this.getDaysInOneMonth(this.getOtherMonth(date, 'preMonth')) - leftNum + 1;
    const preDate = this.getOtherMonth(date, 'preMonth');
    // 上个月多少开始
    for (let i = 0; i < leftNum; i++) {
        const nowTime = preDate.getFullYear() + '/' + (preDate.getMonth() + 1) + '/' + (num + i);
        arr.push({
            id: num + i,
            date: nowTime,
            isToday: false,
            otherMonth: 'preMonth',
        });
    }
    return arr;
}

// 下个月末尾的一些日期
function getRightArr(date) {
    const arr = [];
    const nextDate = this.getOtherMonth(date, 'nextMonth');
    const leftLength = this.getDaysInOneMonth(date) + this.getMonthweek(date);
    const _length = 7 - leftLength % 7;
    for (let i = 0; i < _length; i++) {
        const nowTime = nextDate.getFullYear() + '/' + (nextDate.getMonth() + 1) + '/' + (i + 1);
        arr.push({
            id: i + 1,
            date: nowTime,
            isToday: false,
            otherMonth: 'nextMonth',
        });
    }
    return arr;
}

// format日期
function dateFormat(date) {
    date = typeof date === 'string' ? new Date(date.replace(/\-/g, '/')) : date;
    return date.getFullYear() + '/' + (date.getMonth() + 1) + '/' +
        date.getDate();
}

// 获取某月的列表不包括上月和下月
function getMonthListNoOther(date) {
    const arr = [];
    const num = this.getDaysInOneMonth(date);
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const toDay = this.dateFormat(new Date());
    for (let i = 0; i < num; i++) {
        const nowTime = year + '/' + month + '/' + (i + 1);
        arr.push({
            id: i + 1,
            date: nowTime,
            isToday: toDay === nowTime,
            otherMonth: 'nowMonth',
        });
    }
    return arr;
}

// 获取某月的列表 用于渲染
function getMonthList(date) {
    return [...this.getLeftArr(date), ...this.getMonthListNoOther(date), ...this.getRightArr(date)];
}
