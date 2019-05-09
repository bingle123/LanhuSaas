var vm = null;
var site_url = null;
$(function(){
    site_url = $('#siteUrl').val();
    axios.interceptors.request.use((config) => {
        config.headers['X-Requested-With'] = 'XMLHttpRequest';
        let regex = /.*csrftoken=([^;.]*).*$/; // 用于从cookie中匹配 csrftoken值
        config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
        return config
    });
    vm = new Vue({
        el: '.content',
        data: {
            page_count: 100,                             //总页码数
            page: 1,                                   //分页页码数
            dialogFormVisible: false,                   //新增岗位人员模态框是否显示
            dialogFormVisible2: false,                  //编辑岗位模态框是否显示
            dialogFormVisible3: false,                  //新增岗位模态框是否显示
            form: {
                pos_name: '',
            }, rules: {
                pos_name: [{
                    required: true,
                    message: '不能为空，请输入岗位名称',
                    trigger: 'blur'
                }, {
                    pattern: /^[A-Za-z0-9\u4e00-\u9fa5]+$/,
                    message: '请不要输入特殊字符', trigger: 'blur'
                }, {
                    max: 50,
                    message: '长度必须在 50个字符',
                }]
            },
            users: [],
            form2: {
                tempjobname: '',
            },
            rules2: {
                tempjobname: [{
                    required: true,
                    message: '不能为空，请输入岗位名称',
                    trigger: 'blur'
                }, {
                    pattern: /^[A-Za-z0-9\u4e00-\u9fa5]+$/,
                    message: '请不要输入特殊字符', trigger: 'blur'
                }, {
                    max: 50,
                    message: '长度在 50个字符',
                }]
            },
            tempid: '',
            form1: '',
            jobname: '',
            username: '',
            search: '',
            value1: '',
            value12: '',
            positiontable: [],
            data2: '',
            value2: '',
            filterText: '',
            data3: [],
            defaultProps: {
                children: 'children',
                label: 'label'
            },
        },
        methods: {
            handleDialogClose(){
                vm. ref()
            },
            get_tree() {
                axios({
                    method: 'post',
                    url: site_url + 'position/get_tree/',
                }).then(function (res) {
                    vm.data3 = res.data.message;
                })
            },
            ref() {
                vm.dialogFormVisible = false;
                vm.users = [];
                vm.select_all_user();
            },
            current_change1(value) {
                vm.page = value;
                axios({
                    method: 'post',
                    url: site_url + 'position/select_pos/',
                    data: {
                        search: this.search,
                        page: vm.page,
                        limit: 10
                    },
                }).then((res) => {
                    if(res.data.message.length == 0){
                        vm.page_count=1
                        vm.positiontable = []
                    }else{
                        vm.positiontable = res.data.message;
                        vm.page_count = res.data.message[0].page_count;
                    }
                })
            },
            synchronize() {  //与蓝鲸用户同步
                axios({
                    method: 'post',
                    url: site_url + 'position/synchronize/',
                })
            },
            show() {
                //显示首页
                axios({
                    method: 'post',
                    url: site_url + 'position/show/',
                    data: {
                        page: vm.page,
                        limit: 10
                    },
                }).then(function (res) {
                    vm.positiontable = res.data.message;
                    vm.page_count = res.data.message[0].page_count;
                })
            },
            deletePosition(row) {                                                  //删除一条记录
                this.$confirm('此操作将永久删除该文件, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                    center: true
                }).then(() => {
                    axios({
                        method: 'post',
                        url: site_url + 'position/delete/',
                        data: {
                            id: row,
                        }
                    }).then((res) => {
                        if(res.data.result){
                            this.$message({
                            type: 'success',
                            message: '删除成功!',})
                        }
                        else{
                            this.$message({
                            type: 'false',
                            message: '删除失败!请先移除该岗位的所有人员！',})
                        }
                        vm.page = 1;
                        vm.show();
                    })
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                });
            },
            select_pos() {
                vm.page = 1                                             //查询岗位
                if (this.search.trim() == '') {
                    vm.show()
                }
                axios({
                    method: 'post',
                    url: site_url + 'position/select_pos/',
                    data: {
                        search: this.search,
                        page: this.page,
                        limit: 10
                    },
                }).then((res) => {
                    if(res.data.message.length == 0){
                        vm.page_count=1
                        vm.positiontable = []
                    }else{
                        vm.positiontable = res.data.message;
                        vm.page_count = res.data.message[0].page_count;
                    }
                })
            },
            add_pos(formName) {                                              //增加岗位
                this.$refs[formName].validate((valid) => {
                    if (!valid) {
                        return false;
                    } else {
                        axios({
                            method: 'post',
                            url: site_url + 'position/add_pos/',
                            data: this.form,
                        }).then((res) => {
                            if(res.data.result){
                                this.$message({
                                type: 'success',
                                message: '新增岗位成功!',})
                                vm.dialogFormVisible3 = false;
                                window.location.href = site_url + "position/position"
                            }else{
                                this.$message({
                                type: 'false',
                                message: '新增岗位失败!岗位已经存在',})
                            }

                        })
                    }
                });
            },
            edit_posname(row) {                                     //显示弹框，传值到edit_pos
                vm.dialogFormVisible2 = true;
                vm.tempid = row.id;
                vm.form2.tempjobname = row.pos_name;
            },
            edit_pos(formName) {                                            //修改岗位名
                this.$refs[formName].validate((valid) => {
                    if (!valid) {
                        return false;
                    } else {
                        axios({
                            method: "post",
                            url: site_url + 'position/edit_pos/',
                            data: {
                                id: this.tempid,
                                pos_name: this.form2.tempjobname,
                            }
                        }).then((res) => {
                            if(res.data.result){
                                this.$message({
                                type: 'success',
                                message: '编辑成功!',})
                                vm.dialogFormVisible2 = false
                                window.location.href = site_url + "position/position"
                            }else{
                                this.$message({
                                type: 'false',
                                message: '编辑失败!请先检查后在进行修改',})
                            }
                        })
                    }
                });
            },
            show_pos(row) {                                      //显示弹框和穿梭框，传值到add_person
                vm.dialogFormVisible = true;
                vm.jobname = row.pos_name;
                vm.id = row.id;
                var x = row.user_name;
                x.forEach((x, index) => {
                    vm.users.push(x)
                })
                const data = [];
                var people = this.users;
                const pinyin = this.users;
                people.forEach((people, index) => {
                    data.push({
                        <!--label: people,-->
                        pinyin: pinyin[index],
                        key: people,
                    });
                });
                this.data2 = data;
                this.value2 = x;
            },
            add_person(row) {
                axios({
                    method: 'post',
                    url: site_url + 'position/add_person/',
                    data: {
                        value2: vm.value2,
                        id: this.id,
                        jobname: this.jobname,
                        data2: vm.data2,
                    },
                }).then((res) => {
                    vm.dialogFormVisible = false
                    window.location.href = site_url + "position/position"
                })
            },
            select_all_user() {                                                      //调接口查询所有用户
                axios({
                    method: 'post',
                    url: site_url + 'position/get_user/',
                }).then((res) => {
                    for (var i = 0; i < res.data.message.length; i++) {
                        this.users.push(res.data.message[i])
                    }
                })
            },
            filterMethod(query, item) {
                return item.pinyin.indexOf(query) > -1;
            },
            filterNode(value, data) {
                if (!value) return true;
                return data.label.indexOf(value) !== -1;
            }
        },
        watch: {
            filterText(val) {
                this.$refs.tree2.filter(val);
            }
        }
    });
    vm.synchronize();
    vm.show();
    vm.select_all_user();
    vm.get_tree();
})

