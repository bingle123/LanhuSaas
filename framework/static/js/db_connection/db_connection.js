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
            connection_test:false,
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
                if(!ve.test_connection("add")){
                    alert('测试连接没有通过，不能保存');
                    return false;
                }
               this.$refs[formName].validate((valid) => {
                    if (!valid) {
                        alert('验证不通过');
                        return false;
                    }else {
                        axios.post(
                            site_url+'db_connection/saveconn/',this.addconn
                        ).then(function (res) {
                            if(res.data.code == 0){
                                alert("新增连接测试成功");
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
                if(!ve.test_connection("edit")){
                    alert('测试连接没有通过，不能保存');
                    return false;
                }
                this.$refs[formName].validate((valid) => {
                    if (!valid) {
                        alert('验证不通过');
                        return false;
                    }else {
                        axios.post(site_url+'db_connection/editconn/',this.editDataBase)
                        .then((res)=>{
                            if(res.data.message != null){
                                alert("修改连接配置成功");
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
                //console.log(this.addconn)
                this.$refs[formName].validate((valid) => {
                    if (!valid) {
                        alert('验证不通过');
                        return false;
                    }else {
                        if(ve.test_connection("add")){
                            alert("连接测试通过");
                        }else {
                            alert("连接测试没有通过");
                        }
                    }
                })
            },
            test_connection(type){//连接测试
                let result = false;
                let data = {};
                if(type == "add"){
                    data = JSON.stringify(this.addconn);
                }
                if(type == "edit"){
                    data = JSON.stringify(this.editDataBase);
                }
                //同步连接测试校验
                $.ajax({
                    type: "POST",
                    data: data,
                    dataType: "JSON",
                    async: false,
                    url: site_url+"db_connection/testConn/",
                    success: function (res) {
                        if(res.code == 0){
                            result = true;
                            return result;
                        }else{
                            return result;
                        }
                    },
                    error: function (error) {
                        return result;
                    }
                });
                return result;
            },
            //测试2
            textconn2(formName){
                this.$refs[formName].validate((valid) => {
                    if (!valid) {
                        alert('验证不通过');
                        return false;
                    }else {
                        if(ve.test_connection("edit")){
                            alert("连接测试通过");
                        }else {
                            alert("连接测试没有通过");
                        }
                    }
                })
            },
        }
    });
    ve.conn()
})
