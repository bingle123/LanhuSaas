var vue = null;
$(function(){
    var site_url = $('#siteUrl').val();
    //csrf验证
    axios.interceptors.request.use((config) => {
        config.headers['X-Requested-With'] = 'XMLHttpRequest';
        let regex = /.*csrftoken=([^;.]*).*$/; // 用于从cookie中匹配 csrftoken值
        config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
        return config
    });
    //接收人校验
    const receiversCheck = (rule, value, callback) => {
        //通知接收人填写为空的情况
        if(null == vue.customProcessNode.seq || 0 == vue.customProcessNode.receivers.length){
            callback(new Error('请输入通知接收人'));
        //通知接收人长度超过2000的情况
        }else if(2000 < vue.customProcessNode.receivers.length){
            return callback('通知接收人内容长度在1~2000之间');
        //通知接收人填写符合校验的情况
        }else{
            return callback();
        }
    };
    //节点顺序校验
    const seqCheck = (rule, value, callback) => {
        //未填写任何节点顺序的情况
        if(null == vue.customProcessNode.seq || 0 == vue.customProcessNode.seq.length){
            callback(new Error('请输入节点顺序'));
        //校验节点顺序填写是否符合规则
        }else if(!/^[1-9][0-9]{0,1}$/.test(vue.customProcessNode.seq)){
            return callback(new Error('节点值在1~99之间'));
        //判断节点顺序是否被重复定义
        }else{
            $.each(vue.customProcessTableData, function(k, v){
                if(vue.customProcessNode.seq == v.seq){
                    if(null == vue.customProcessNodeInitSeq){
                        return callback(new Error('该节点顺序已被定义'));
                    }else if(vue.customProcessNodeInitSeq != vue.customProcessNode.seq){
                        return callback(new Error('该节点顺序已被定义'));
                    }
                }
            });
            return callback();
        }
    };
    vue = new Vue({
        el: '#customProcess',
        data: {
            //检索条件
            customProcessSearch: '',
            //步骤条偏移值，用于居中显示步骤条
            customProcessStepOffset: 0,
            //每多少个元素生成一个新的步骤条
            customProcessStepLimit: 3,
            //当前用户名称
            currentUser: null,
            //节点列表信息共有多少页
            customProcessPageCount: 0,
            //节点列表当前处于第几页
            currentPage: 1,
            //用于列表显示的节点信息
            customProcessTableListData: [],
            //蓝鲸平台用户列表信息
            bkUsers: {},
            //步骤条默认高度
            customProcessHeight: '1000',
            //发送通知按钮属性控制
            customProcessNotifyButtonType: 'primary',
            customProcessNotifyButtonText: '发送通知',
            customProcessNotifyButtonDisabled: false,
            //节点列表模态框是否显示
            addDialogVisible: false,
            //发送通知的模态框是否显示
            customProcessSendMsgDialogVisible: false,
            //添加节点的table当前状态，list=列表显示,add=添加节点,edit=编辑节点
            customProcessTableStatus: 'list',
            //当前流程中节点总数，直接计算processDataList的长度获得
            customProcessStepSum: -1,
            //流程是否已经开始执行，应该根据数据库中的信息来判断
            customProcessStatus: false,
            //当前是否有流程节点标记位
            customProcessHasNode: false,
            //通知接收人信息
            customProcessReceivers: '',
            //通知内容信息
            customProcessNoticeContent: '',
            //当前节点信息，用于修改节点信息的提交
            customProcessNode: {
                /*node_name: null,
                send_content: null,
                seq: null,
                receivers: null*/
            },
            //临时变量，用于保存节点的顺序信息
            customProcessNodeInitSeq: null,
            //节点的列表信息
            customProcessTableData: [],
            //校验规则定义
            rules: {
                node_name: [
                    { required: true, message: '请输入节点名称', trigger: 'blur' },
                    { min: 1, max: 50, message: '节点名称长度在1~50之间', trigger: 'blur' }
                ],
                send_content: [
                    { required: true, message: '请输入通知内容', trigger: 'blur' },
                    { min: 1, max: 1000, message: '通知内容长度在1~1000之间', trigger: 'blur' }
                ],
                seq: [
                    { validator: seqCheck, trigger: 'blur' }
                ],
                receivers: [
                    { validator: receiversCheck, trigger: 'blur' }
                ]
            }
        },
        methods:{
            //获取当前用户名
            customProcessCurrUser: function(){
                axios({
                    method: 'post',
                    url: site_url + 'position/get_active_user',
                }).then((res) => {
                    this.currentUser=res.data.message
                }).catch((res) => {
                    var msg = '当前用户信息获取失败！';
                    this.alertRulePopupErrorMessage(msg + res);
                });
            },
            //根据条件检索节点
            customProcessSearchByNodeName: function(){
                this.customProcessPageChange(1);
            },
            //分页显示方法
            customProcessPageChange: function(page) {
                const loading = this.customProcessPopupLoading();
                var data = {
                    page: page,
                    limit: 5,
                    condition: this.customProcessSearch
                };
                axios({
                    method: 'post',
                    url: site_url + 'custom_process/select_nodes_pagination',
                    data: data
                }).then((res) => {
                    loading.close();
                    //当前页节点信息
                    this.customProcessTableListData = res.data.items;
                    //节点信息总页数
                    this.customProcessPageCount = res.data.pages;
                    this.currentPage = page;
                    //当前页数大于服务端分页总数的情况，获取服务端最后一页的数据，并调整当前页为服务端页面的最大值
                    if(page > res.data.pages){
                        this.currentPage = res.data.pages;
                    }
                }).catch((res) => {
                    loading.close();
                    var msg = '节点信息加载失败！';
                    this.alertRulePopupErrorMessage(msg + res);
                });
            },
            //Date()对象转yyyy-MM-dd HH:mm:ss函数
            formatDateTime: function (date) {
                var y = date.getFullYear();
                var m = date.getMonth() + 1;
                m = m < 10 ? ('0' + m) : m;
                var d = date.getDate();
                d = d < 10 ? ('0' + d) : d;
                var h = date.getHours();
                h=h < 10 ? ('0' + h) : h;
                var minute = date.getMinutes();
                minute = minute < 10 ? ('0' + minute) : minute;
                var seconds = date.getSeconds();
                seconds = seconds < 10 ? ('0' + seconds) : seconds;
                return y + '-' + m + '-' + d+' '+h+':'+minute+':'+seconds;
            },
            //发送通知
            customProcessSendNotification: function(){
                //发送通知的按钮状态变更
                this.customProcessNotifyButtonText = '正在发送...';
                this.customProcessNotifyButtonType = 'info';
                this.customProcessNotifyButtonDisabled = true;
                var url = site_url + 'custom_process/send_notification';
                var nofityData = {
                    'receivers': this.customProcessReceivers,
                    'content': this.customProcessNoticeContent
                };
                axios({
                    method: 'post',
                    url: url,
                    data: nofityData
                }).then((res) =>{
                    //通知发送完毕后，按钮复原，供下一次发送通知使用
                    this.customProcessSendMsgDialogVisible = false;
                    this.customProcessNotifyButtonText = '发送通知';
                    this.customProcessNotifyButtonType = 'primary';
                    this.customProcessNotifyButtonDisabled = false;
                    //通知发送没有存在错误的情况
                    if('ok' == res.data.message){
                        var msg = res.data.info;
                        this.customProcessPopupSuccessMessage(msg);
                    }else{
                    //通知发送过程中存在错误的情况
                        var msg = '通知发送失败！' + res.data.info;
                        this.customProcessPopupErrorMessage(msg);
                    }
                }).catch((res) => {
                    //请求发送通知过程中出现错误
                    this.customProcessSendMsgDialogVisible = false;
                    this.customProcessNotifyButtonText = '发送通知';
                    this.customProcessNotifyButtonType = 'primary';
                    this.customProcessNotifyButtonDisabled = false;
                    var msg = '通知发送失败！' + res;
                    this.customProcessPopupErrorMessage(msg);
                });
            },
            //弹出加载界面
            customProcessPopupLoading: function() {
                //返回加载标记，供外部关闭
                return this.$loading({
                    lock: true,
                    text: '正在拼命加载中...',
                    spinner: 'el-icon-loading',
                    background: 'rgba(0, 0, 0, 0.7)'
                });
            },
            //弹出数据加载错误的警告信息
            customProcessPopupErrorMessage: function(msg) {
                this.$notify.error({
                  title: '错误',
                  message: msg
                });
            },
            //弹出成功的信息
            customProcessPopupSuccessMessage: function(msg) {
                this.$notify({
                  title: '成功',
                  message: msg,
                  type: 'success'
                });
            },
            //发送通知
            customProcessConfirmNode: function(index, id, curr) {
                const loading = this.customProcessPopupLoading();
                //上传当前节点已执行状态
                var url = site_url + 'custom_process/update_node_status';
                //执行时间取当前时间
                var execTime = this.formatDateTime(new Date());
                //当前执行人取当前用户的名称
                var execPerson = this.currentUser;
                //定义当前节点正在执行的节点状态信息，后续上传至服务器保存
                var statusData = {};
                statusData.node_id = id;
                statusData.is_done = 'y';
                statusData.do_time = execTime;
                statusData.do_person = execPerson;
                axios({
                    method: 'post',
                    url: url,
                    data: statusData
                }).then((res) =>{
                    if('ok' == res.data.message){
                        loading.close();
                    }else{
                        var msg = '节点信息上传失败！';
                        this.customProcessPopupErrorMessage(msg);
                    }
                }).catch((res) => {
                    var msg = '节点信息上传失败！';
                    this.customProcessPopupErrorMessage(msg);
                });
                var customProcessExecPerson = '<div>执行人：'+ execPerson +'</div>';
                var customProcessExecTime = '<div>' + execTime + '</div>';
                var customProcessExecStatus = '执行状态：执行完毕！<i class="el-icon-check"></i>';
                var temp = $(curr).parent().find('.execute_status');
                temp.html(customProcessExecPerson + customProcessExecTime + customProcessExecStatus);
                $(curr).remove();
                this.customProcessSendMessage(index);
            },
            //发送短信通知
            customProcessSendMessage: function(nodeOrder) {
                var step_index = parseInt(nodeOrder / this.customProcessStepLimit);
                var item_index = parseInt(nodeOrder % this.customProcessStepLimit);
                this.customProcessReceivers = this.customProcessTableData[step_index][item_index].receivers;
                this.customProcessNoticeContent = this.customProcessTableData[step_index][item_index].send_content;
                this.customProcessSendMsgDialogVisible = true;
            },
            //短信通知关闭前的确认
            customProcessHandleClose: function() {
                this.$confirm('确定不发送短信通知吗？').then(_ => {
                    this.customProcessSendMsgDialogVisible = false;
                }).catch(_ => {

                });
            },
            //切换添加节点的界面
            customProcessAddNode: function() {
                this.customProcessTableStatus = 'add';
            },
            //切换列出所有节点的界面
            customProcessListNode: function() {
                this.customProcessNode = {};
                this.customProcessSearch = '';
                this.customProcessTableStatus = 'list';
            },
            //切换修改节点信息的界面
            customProcessEditNode: function(id) {
                const loading = this.customProcessPopupLoading();
                var url = site_url + 'custom_process/select_node';
                var editData = {};
                editData.id = id;
                axios({
                    method: 'post',
                    url: url,
                    data: editData,
                }).then((res) =>{
                    loading.close();
                    this.customProcessNode = res.data.message[0];
                    //保存该节点的初始顺序，用于后续修改节点是节点顺序是否重复的判断
                    this.customProcessNodeInitSeq = this.customProcessNode.seq;
                    //切换修改节点的时候使用逗号切割发送人信息，使select组件能识别选中默认值，并切换列表展示为编辑状态
                    this.customProcessNode.receivers = this.customProcessNode.receivers.split(',');
                    this.customProcessTableStatus = 'edit';
                }).catch((res) => {
                    loading.close();
                    var msg = '请求节点数据失败！';
                    this.customProcessPopupErrorMessage(msg);
                });
            },
            //增加/修改流程节点
            defineOrChangeProcess: function() {
                //流程正在使用的情况
                /*if(this.customProcessStatus){
                    this.$confirm('当前流程正在使用中, 强制修改将会导致执行状态信息丢失，是否继续?', '提示', {
                      confirmButtonText: '确定',
                      cancelButtonText: '取消',
                      type: 'warning',
                      center: true
                    }).then(() => {
                        //点击确定时，清除所有节点的状态信息
                        var url = site_url + 'custom_process/clear_execute_status';
                        const loading = this.customProcessPopupLoading();
                        axios({
                            method: 'post',
                            url: url
                        }).then((res) =>{
                            if('ok' == res.data.message){
                                this.customProcessPageChange(1);
                                this.addDialogVisible = true;
                                this.customProcessSelectAllNodes()
                            }else{
                                var msg = '修改过程通知失败！';
                                this.customProcessPopupErrorMessage(msg);
                            }
                            loading.close();
                        }).catch((res) => {
                            loading.close();
                            var msg = '修改过程通知失败！';
                            this.customProcessPopupErrorMessage(msg);
                        });
                    }).catch(() => {
                        this.$message({
                            type: 'info',
                            message: '取消修改过程通知'
                        });
                    });
                //流程未在使用的情况下，可以直接进行节点信息的修改
                }else{
                    this.customProcessPageChange(1);
                    this.addDialogVisible = true;
                }*/
                this.customProcessPageChange(1);
                this.addDialogVisible = true;
            },
            //从数据库中删除节点信息
            customProcessDeleteNode: function(id) {
                this.$confirm('此操作将删除该节点, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                    center: true
                }).then(() => {
                    const loading = this.customProcessPopupLoading();
                    var url = site_url + 'custom_process/del_node';
                    var delData = {};
                    delData.id = id;
                    axios({
                        method: 'post',
                        url: url,
                        data: delData,
                    }).then((res) =>{
                        loading.close();
                        if('ok' == res.data.message){
                            //重新加载当前页的节点信息,渲染流程节点
                            this.customProcessPageChange(this.currentPage);
                            this.customProcessSelectAllNodes();
                            this.customProcessListNode();
                            this.$message({
                                type: 'success',
                                message: '删除节点成功!'
                            });
                        }else{
                            var msg = '请求删除节点数据失败！';
                            this.customProcessPopupErrorMessage(msg);
                        }
                    }).catch((res) => {
                        loading.close();
                        var msg = '请求删除节点数据失败！';
                        this.customProcessPopupErrorMessage(msg);
                    });
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '取消节点删除'
                    });
                });
            },
            get_header_data(){
            axios.get(site_url + 'market_day/get_header/').then(function (res) {
               console.log(res)
            })
             },
            //添加节点信息到数据库中
            customProcessSaveNodeInfo: function(formName) {
                this.$refs[formName].validate((valid) => {
                    if (!valid) {
                        this.$message({
                            type: 'error',
                            message: '请仔细检查表单项!'
                        });
                        return false;
                    }else {
                        const loading = this.customProcessPopupLoading();
                        var url = site_url + 'custom_process/add_node';
                        //下拉框选中的通知接收者信息是以数组形式保存的，需要转换为,间隔的字符串形式上传至服务器
                        if(1 != this.customProcessNode.receivers.length){
                            this.customProcessNode.receivers = this.customProcessNode.receivers.join(',');
                        }else{
                            this.customProcessNode.receivers = this.customProcessNode.receivers[0];
                        }
                        //清除临时保存的节点顺序信息
                        this.customProcessNodeInitSeq = null;
                        var data = {};
                        data['node'] = this.customProcessNode;
                        //指定当前操作类型是添加还是修改，上传服务器，根据类型做不同的处理
                        if('edit' == this.customProcessTableStatus){
                            data['method'] = 'edit';
                        }
                        else if('add' == this.customProcessTableStatus){
                            data['method'] = 'add';
                        }
                        axios({
                            method: 'post',
                            url: url,
                            data: data,
                        }).then((res) =>{
                            loading.close();
                            if('ok' == res.data.message){
                                //重新获取所有节点的信息,渲染流程节点
                                this.customProcessSelectAllNodes();
                                //如果是编辑节点信息，编辑完成后回到原来的那一页
                                if('edit' == this.customProcessTableStatus){
                                    this.customProcessPageChange(this.currentPage);
                                }
                                //如果是添加节点信息，添加完成后将会跳转到最后一页
                                else if('add' == this.customProcessTableStatus){
                                    this.customProcessPageChange(res.data.total_pages);
                                }
                                //显示节点信息的列表
                                this.customProcessListNode();
                            }else{
                                var msg = '请求添加/修改节点数据失败！';
                                this.customProcessPopupErrorMessage(msg);
                            }
                        }).catch((res) => {
                            loading.close();
                            var msg = '请求添加/修改节点数据失败！';
                            this.customProcessPopupErrorMessage(msg);
                        });
                    }
                });
            },

            //删除当前流程
            customProcessDelete: function() {
                var alertMessage = null;
                if(!this.customProcessStatus){
                    alertMessage = '确认删除当前过程通知吗？';
                }else{
                    alertMessage = '当前流程正在使用，是否强制删除？';
                }
                this.$confirm(alertMessage, '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                    center: true
                }).then(() => {
                    const loading = this.customProcessPopupLoading();
                    //数据库删除所有节点信息
                    var url = site_url + 'custom_process/truncate_node';
                    axios({
                        method: 'post',
                        url: url
                    }).then((res) =>{
                        if('ok' == res.data.message){
                            loading.close();
                            //步骤条总节点的值置0
                            this.customProcessStepSum = 0;
                            //是否包含节点信息置false
                            this.customProcessHasNode = false;
                            //节点执行状态：未开始执行
                            this.customProcessStatus = false;
                            //列表信息置空
                            this.customProcessTableData = [];
                            this.$message({
                                type: 'success',
                                message: '流程已被删除！'
                            });
                        }else{
                            var msg = '请求删除节点数据失败！';
                            this.customProcessPopupErrorMessage(msg);
                        }
                    }).catch((res) => {
                        var msg = '请求删除节点数据失败！';
                        this.customProcessPopupErrorMessage(msg);
                    });
                }).catch(() => {
                        this.$message({
                        type: 'info',
                        message: '取消流程删除操作'
                    });
                });
            },
            //从后台数据库获取所有节点信息
            customProcessSelectAllNodes: function() {
                const loading = this.customProcessPopupLoading();
                this.customProcessTableData = null;
                var url = site_url + 'custom_process/select_all_nodes';
                //limit参数为每隔多少条分配一个数组，有多少个数组就会生成多少个步骤条
                var params = {
                    limit: this.customProcessStepLimit
                };
                axios({
                    method: 'post',
                    url: url,
                    data: params
                }).then((res) =>{
                    this.customProcessTableData = res.data.nodes;
                    this.customProcessStepSum = res.data.count;
                    //计算偏移值，使步骤条居中
                    if(this.customProcessTableData.length > 4){
                        this.customProcessStepOffset = 0;
                    }else{
                        this.customProcessStepOffset = (24 - this.customProcessTableData.length * 6) / 2 + 1;
                    }
                    //根据节点数量计算步骤条的高度
                    //var stepsHeight = params['limit'] * 200;
                    //$('.customProcessStepsHeight').css('height',stepsHeight + 'px');
                    if(0 != this.customProcessStepSum) {
                        this.$nextTick(() => {
                            this.customProcessRenderNodeStatus();
                        });
                        this.customProcessHasNode = true;
                    }
                    loading.close();
                }).catch((res) => {
                    loading.close();
                    var msg = '节点数据信息加载错误！';
                    this.customProcessPopupErrorMessage(msg);
                });
            },
            //
            //获取所有设置通知方式的蓝鲸用户
            loadBkUsers: function(){
                const loading = this.customProcessPopupLoading();
                var url = site_url + 'custom_process/select_all_bkusers';
                axios({
                    method: 'post',
                    url: url
                }).then((res) =>{
                    this.bkUsers = res.data.message;
                    loading.close();
                }).catch((res) => {
                    loading.close();
                    var msg = '蓝鲸用户信息加载失败！' + res;
                    this.customProcessPopupErrorMessage(msg);
                });
            },
            //渲染节点的状态信息
            customProcessRenderNodeStatus: function(){
                var customMainProcesses = $('.customMainProcess').children();
                var total_index = null;
                $.each(vue.customProcessTableData, function(step_index, steps){
                    $.each(steps, function(item_index, items){
                        total_index = (step_index * vue.customProcessStepLimit) + item_index;
                       //设置已经执行的步骤的状态信息
                        if('y' == items.status.is_done){
                            var execTime =  items.status.do_time;
                            var execPerson = items.status.do_person;
                            var customProcessExecPerson = '<div>执行人：'+ execPerson +'</div>';
                            var customProcessExecTime = '<div>' + execTime + '</div>';
                            var customProcessExecStatus = '<div>执行状态：执行完毕！<i class="el-icon-check"></i></div>';
                            var selectedProcess =  customMainProcesses.eq(total_index);
                            selectedProcess.find('.el-step__description')
                                .html(customProcessExecPerson + customProcessExecTime + customProcessExecStatus);
                        }else{
                        //还未执行的步骤
                            var customProcessExecStatus = '<div class="execute_status">执行状态：未开始执行<i class="el-icon-close"></i></div>';
                            var selectedProcess =  customMainProcesses.eq(total_index);
                            var click = ' onclick="vue.customProcessConfirmNode('+ total_index + ',' + items.id + ', this)"';
                            var nextButton = '<button type="button" class="el-button el-button--success el-button--small" '+ click +'><span>确认</span></button>';
                            selectedProcess.find('.el-step__description')
                                .html(customProcessExecStatus);
                            selectedProcess.find('.el-step__main').append(nextButton);
                        }
                    });
                });
            }
        },
        watch: {
            //监听流程节点总数，如果总数发生变化，重新获取所有节点的状态信息，由于初始默认节点数是0
            //因此在页面加载完成节点总数会发生变化，从而在页面加载完成后自动加载所有节点的状态信息
            customProcessStepSum: function(val, oldVal) {
                if(-1 == oldVal){
                    this.$nextTick(() => {
                        /*var customMainProcesses = $('#customMainProcess').children();
                        $.each(this.customProcessTableData, function(index, elem){
                            //设置正在执行的步骤的状态信息
                            if(index == vue.customProcessStep){
                                var execTime =  vue.customProcessTableData[index].status.do_time;
                                var execPerson = vue.customProcessTableData[index].status.do_person;
                                var customProcessExecPerson = '<div>执行人：'+ execPerson +'</div>';
                                var customProcessExecTime = '<div>' + execTime + '</div>';
                                var customProcessExecStatus = '<div id="customProcessExecStatus">执行状态：正在执行...<i class="el-icon-loading"></i></div>';
                                var nextButton = '<button id="customProcessNextButton" type="button" class="el-button el-button--success el-button--small" onclick="vue.customProcessConfirmNode()"><span>下一步</span></button>';
                                var selectedProcess =  customMainProcesses.eq(index);
                                selectedProcess.find('.el-step__description')
                                    .html(customProcessExecPerson + customProcessExecTime + customProcessExecStatus);
                                selectedProcess.find('.el-step__main').append(nextButton);
                            //已执行的步骤状态信息
                            }else if(index < vue.customProcessStep){
                                var execTime =  vue.customProcessTableData[index].status.do_time;
                                var execPerson = vue.customProcessTableData[index].status.do_person;
                                var customProcessExecPerson = '<div>执行人：'+ execPerson +'</div>';
                                var customProcessExecTime = '<div>' + execTime + '</div>';
                                var customProcessExecStatus = '执行状态：执行完毕！<i class="el-icon-check"></i>';
                                var selectedProcess =  customMainProcesses.eq(index);
                                selectedProcess.find('.el-step__description')
                                    .html(customProcessExecPerson + customProcessExecTime + customProcessExecStatus);
                            }else{
                            //还未执行的步骤直接返回
                                return false;
                            }
                        });*/
                        //this.customProcessRenderNodeStatus();
                    });
                }
            }
        },
        mounted(){
            //在页面加载完成后获取所有的流程节点
            this.customProcessSelectAllNodes();
            //在页面加载完成后加载所有的蓝鲸用户数据，用于在填写发送通知信息时指定用户
            this.loadBkUsers();
            //获取当前用户信息
            this.customProcessCurrUser();
            //this.get_header_data();
        }
    });
});