var ve = null;
var site_url = null;
$(function(){
    site_url = $('#siteUrl').val();
    //csrf验证
    axios.interceptors.request.use((config) => {
        config.headers['X-Requested-With'] = 'XMLHttpRequest';
        let regex = /.*csrftoken=([^;.]*).*$/; // 用于从cookie中匹配 csrftoken值
        config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
        return config
    });
    ve = new Vue({
        el: '#main',
        data: {
            search:'',//搜索框的值
            page_count:200,
            page:1, //当前页
            isAdd: 1,
            tableData: [],
            editDataBase:[],
            addconn: {
                connname:'',
                type:'',
                ip: '',
                port: '',
                username:'',
                password:'',
                databasename:'',
            },
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
            current_change1(value) {
                ve.page = value;
                ve.conn()
            },
            show() {
                this.addconn = {}
                this.isAdd = 2
            },
            hide() {
                this.isAdd=1
                ve.conn()
            },
            rowClass({row, rowIndex}) {
                return 'background:#F7F7F7'
            },
            //搜索
            select_table() {
                axios({
                    method: 'post',
                    url: site_url+'db_connection/selecthor/',
                    data: {
                        search:this.search,
                        page:ve.page,
                        limit:5,
                    }
                }).then((res) => {
                    //没有数据也不能异常啊
                    if(res.data.items && res.data.items.length > 0){
                        ve.tableData = res.data.items
                        ve.page_count = res.data.pages;
                    }else{
                        ve.tableData = [];
                        ve.page_count = 0;
                    }
                })
            },
            //查询所有
            conn(){
                 axios({
                    method: 'post',
                    url: site_url+'db_connection/selecthor/',
                    data:{
                        search:"",
                        page:ve.page,
                        limit:5,
                    }
                }).then((res) => {
                    //没有数据也不能异常啊
                    if(res.data.items && res.data.items.length > 0){
                        ve.tableData = res.data.items
                        ve.page_count = res.data.pages;
                    }else{
                        ve.tableData = [];
                        ve.page_count = 0;
                    }
                })
            },
            //保存
            saveconn(formName){
               this.$refs[formName].validate((valid) => {
                    if (!valid) {
                        alert('验证不通过');
                        return false;
                    }else {
                        this.addconn.password = Base64.encode(this.addconn.password)
                        axios.post(
                            site_url+'db_connection/saveconn/',this.addconn
                        ).then(function (res) {
                            console.log(res);
                            if(res.data.code == 0){
                                ve.hide()
                            }
                        });
                    }
                });
            },
            //去修改
            showe(row){
                this.isAdd = 3
                this.editDataBase=row
            },

            //修改
            editConn(formName){
                this.$refs[formName].validate((valid) => {
                    if (!valid) {
                        alert('验证不通过');
                        return false;
                    }else {
                        axios.post(site_url+'db_connection/editconn/',this.editDataBase)
                        .then((res)=>{
                            if(res.data.message != null){
                                this.isAdd = 1
                                ve.conn()
                            }
                        })
                    }
                })
            },
            //删除
            deleteDataBase(id,index,data){
                this.$confirm('此操作将永久删除该数据库链接配置, 是否继续?', '提示', {
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
                        site_url+'db_connection/deleteconn/'+id+'/'
                    ).then((res) => {
                       if(res.data.message==0){
                           this.$message('删除成功')
                           data.splice(index,1)
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
            //数据库连接测试
            testConn(formName){
                console.log(this.addconn)
                this.$refs[formName].validate((valid) => {
                    if (!valid) {
                        alert('验证不通过');
                        return false;
                    }else {
                        this.addconn.password = Base64.encode(this.addconn.password);
                        axios.post(site_url+'db_connection/testConn/',this.addconn)
                            .then((res)=>{
                            if(res.data.code == 0){
                                 alert("数据库连接成功")
                            }else{
                                alert("数据库连接失败")
                            }
                            this.addconn.password = Base64.decode(this.addconn.password)
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
                        this.editDataBase.password = Base64.encode(this.editDataBase.password);
                        axios.post(site_url+'db_connection/testConn/',this.editDataBase)
                            .then((res)=>{
                        if(res.data.code == 0){
                             alert("数据库连接成功")
                        }else{
                            alert("数据库连接失败")
                        }
                    })
                    }
                })

            },
            //jlq-2019-05-23-add-编辑密码框的值发生改变时
            changePass(){
               // alert('jlq');
                this.editDataBase.password = Base64.encode(this.editDataBase.password)
            }
        }
    });
    ve.conn()
})
