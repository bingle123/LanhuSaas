$(function(){
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
            connsearch:'',//搜索框的值
            page_count:0,//总页码
            currentPage:1, //当前页
            isAdd: 1,       //当前状态：列表/添加/修改/删除
            tableData: [],//表单展示
            editDataBase:{},
            addconn: {},//新增数据库连接
            rules: {
                connname: [
                    { required: true, message: '请输入连接名称', trigger: 'blur' },
                    { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' },

              ],
                ip: [
                    { required: true, message: '请输入ip地址', trigger: 'blur' },
                    {pattern: /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/,message:'请输入正确的IP地址',trigger: 'blur' }
              ],
                port: [
                    { required: true, message: '请输入端口号', trigger: 'blur' },
                    {pattern:/^([0-9]|[1-9]\d{1,3}|[1-5]\d{4}|6[0-4]\d{4}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$/,message:'请输入正确端口号',trigger: 'blur' }
              ],
                databasename: [
                { required: true, message: '请输入数据库名称', trigger: 'blur' },
                { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
              ],
                type: [
                { required: true, message: '请选择数据库类型', trigger: 'blur' },
              ],
                username: [
                    { required: true, message: '请输入用户名', trigger: 'blur' },
                    { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
              ],
                password: [
                    { required: true, message: '请输入密码', trigger: 'blur' },
                    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
              ]
            },


        },
        methods: {
            //点击搜索按钮，跳转到第一页
            select_table() {
                ve.current_change(1)
            },
            //点击页码，翻页
            current_change(value) {
                axios({
                    method: 'post',
                    url: site_url + 'db_connection/selecthor/',
                    data: {
                        search:this.connsearch,
                        page:value,
                        limit:5,
                    }
                }).then((res) => {
                    ve.tableData = res.data.items;
                    ve.page_count = res.data.pages;
                    this.currentPage = value;
                    if(value > res.data.pages){
                        this.currentPage = res.data.pages;
                    }
                })
                },

            show() {
                this.isAdd = 2
            },
            get_header_data(){
            axios.get(site_url + '/market_day/get_header/').then(function (res) {
               console.log(res)
            })
            },
            hide() {
                this.isAdd=1;
                ve.current_change(ve.currentPage)
            },

            rowClass({row, rowIndex}) {
                return 'background:#F7F7F7'
            },

            //保存
            saveconn(formName){
               this.$refs[formName].validate((valid) => {
                    if (!valid) {
                        alert('验证不通过');
                        return false;
                    }else {
                        axios.post(
                        site_url + 'db_connection/saveconn/', this.addconn
                    ).then(function (res) {
                        if(ve.currentPage < res.data.results['page_count']){
                            ve.currentPage = res.data.results['page_count'];
                            ve.hide()
                        }
                    });
                    }
                });
            },


            //去修改
            showe(row){
                this.isAdd = 3;
                this.editDataBase=row
            },

            //修改
            editConn(formName){
                this.$refs[formName].validate((valid) => {
                    if (!valid) {
                        alert('验证不通过');
                        return false;
                    }else {
                        axios.post(
                            site_url + 'db_connection/editconn/',this.editDataBase
                        ).then(((res)=>{
                            console.log(res)
                            ve.hide()

                    }))
                    }
                })
            },


            //删除
            deleteDataBase(id,index,data){
            this.$confirm('此操作将永久删除该数据, 是否继续?', '提示', {
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
                   site_url + 'db_connection/deleteconn/'+id+'/'
               ).then((res) => {
                   if(res.data.message==0){
                       this.$message('删除成功');
                       data.splice(index,1);
                       ve.hide()

                   }
                    })
                    ,
                );
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消删除'
                });
            });
        },

            //数据库连接测试
            testConn(formName){
                console.log(this.addconn);
                this.$refs[formName].validate((valid) => {
                    if (!valid) {
                        alert('验证不通过');
                        return false;
                    }else {
                        axios.post(site_url + 'db_connection/testConn/',this.addconn)
                            .then((res)=>{
                        if(res.data.code == 0){
                             alert("数据库连接成功");
                        }else{
                            alert("数据库连接失败");
                        }
                    })
                    }
                })

            },

            //测试2
            textconn2(formName){
                this.$refs[formName].validate((valid) => {
                    if (!valid) {
                        alert('验证不通过');
                        return false;
                    }else {
                        axios.post(site_url + 'db_connection/testConn/',this.editDataBase)
                            .then((res)=>{
                        if(res.data.code == 0){
                             alert("数据库连接成功");
                        }else{
                            alert("数据库连接失败");
                        }
                    })
                    }
                })

            },
        }
    });
    ve.current_change(1);
    ve.get_header_data();
});