$(function () {
    var site_url = $('#siteUrl').val();
    //csrf验证
    axios.interceptors.request.use((config) => {
        config.headers['X-Requested-With'] = 'XMLHttpRequest';
        let regex = /.*csrftoken=([^;.]*).*$/; // 用于从cookie中匹配 csrftoken值
        config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
        return config
    });


    var ve = new Vue({
        el: '#main',
        data: {
            menusearch: '',//搜索框的值
            page_count: 0,
            currentPage: 1, //当前页
            isAdd: 1,
            tableData: [],
            editMuenu: [],
            dataCk: [],
            checkedKeys: [],
            getchekedKeys: [],
            addmuenus: {
                mname: '',
                url: '',
                pcode: 0,
                mImg: '',
            },
            pcodes: [
                {
                    label: "无",
                    value: 0
                },{
                    label: "首页概览",
                    value: 4
                },{
                    label: "监控项管理",
                    value: 5
                },{
                    label: "场景管理",
                    value: 6
                },{
                    label: "场景展示",
                    value: 1
                },
                {
                    label: "看板系统配置",
                    value: 2
                },
                {
                    label: "历史和报表",
                    value: 3
                },
            ],
            mImgs: [],
            rules: {
                mname: [
                    {required: true, message: '请输入连接名称', trigger: 'blur'},
                    {min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur'},

                ],
                url: [
                    {required: true, message: '请输入url地址', trigger: 'blur'},
                    {message: '请输入正确的IP地址', trigger: 'blur'},
                ],
                pcode: [
                    {required: true, message: '请选择父级菜单', trigger: 'blur'},
                ], mImg: [
                    {required: true, message: '请选择父级菜单', trigger: 'blur'},
                ],
            },


        },
        methods: {
            //搜索
            select_table() {
                ve.current_change(1)
            },
            current_change(value) {
                axios({
                    method: 'post',
                    url: site_url + 'db_connection/selecthor2/',
                    data: {
                        search: this.menusearch,
                        page: value,
                        limit: 5,
                    }
                }).then((res) => {
                    ve.tableData = res.data.items;
                    ve.page_count = res.data.pages;
                    this.currentPage = value;
                    if (value > res.data.pages) {
                        this.currentPage = res.data.pages;
                    }
                })
            },
            get_header_data() {
                axios.get(site_url + '/market_day/get_header/').then(function (res) {
                })
            },
            show() {
                this.isAdd = 2
            },

            //获取所有角色对应菜单
            get_roleAmuenus() {
                axios.post(site_url + 'db_connection/get_roleAmuenus/').then((res) => {
                    ve.dataCk = res.data.message
                });
                axios.post(site_url + 'db_connection/checked_menu/').then((re) => {
                    ve.checkedKeys = re.data.message
                });
                this.isAdd = 4
            },

            hide() {
                this.isAdd = 1;
                ve.current_change(ve.currentPage)
            },

            rowClass({row, rowIndex}) {
                return 'background:#F7F7F7'
            },

            //获取选中节点
            checked(e, dataCk) {
                this.checkedKeys = dataCk.checkedNodes;
                ve.getchekedKeys = this.checkedKeys;
            },

            //保存节点
            savemnus() {
                if (ve.getchekedKeys == '') {
                    ve.getchekedKeys = ve.checkedKeys;
                }
                axios.post(site_url + 'db_connection/savemnus/', ve.getchekedKeys).then((res) => {
                    console.log(res);
                    if (res.data.message == 1) {
                        alert('请进行修改');
                    } else {
                        ve.hide();
                    }
                })
            },


            //保存菜单
            savemuenu(formName) {
                this.$refs[formName].validate((valid) => {
                    if (!valid) {
                        alert('验证不通过');
                        return false;
                    } else {
                        axios.post(
                            site_url + 'db_connection/addmuenus/', this.addmuenus
                        ).then(function (res) {
                            if (ve.currentPage < res.data.results['page_count']) {
                                ve.currentPage = res.data.results['page_count'];
                                ve.hide();
                            }
                        });
                    }
                });
            },


            //去修改
            showe(row) {
                this.isAdd = 3;
                if(row.pcode>6){
                    row.pcode=0
                }
                this.editMuenu = row;
            },

            //修改
            edit_muenu(formName) {
                this.$refs[formName].validate((valid) => {
                    if (!valid) {
                        alert('验证不通过');
                        return false;
                    } else {
                        axios.post(
                            site_url + 'db_connection/edit_muenu/', this.editMuenu
                        ).then(function (res) {
                            if (res.data.code == 0) {
                                ve.hide();
                            }
                        })
                    }
                })
            },


            //删除
            delete_muenu(id, index, data) {
                this.$confirm('此操作将永久删除该菜单, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                    center: true
                }).then(() => {
                    this.$message({
                            type: 'success',
                            message: '删除成功!',
                        },
                        axios.post(
                            site_url + 'db_connection/delete_muenu/' + id + '/'
                        ).then((res) => {
                            if (res.data.code == 0) {
                                this.$message('删除成功');
                                data.splice(index, 1);
                                ve.hide();
                            }
                        }),
                    );
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                });
            },
            append_mImgs() {
                axios.post(
                    site_url + 'db_connection/get_all_mImgs/'
                ).then((res) => {
                    ve.mImgs=res.data.message
                })
            }
        }
    });
    ve.select_table();
    ve.append_mImgs();
    ve.get_header_data();
});