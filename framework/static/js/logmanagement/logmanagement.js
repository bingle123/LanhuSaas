let vm = new Vue({
        el: '.content',
        data: {
            page_count: 1,                             //总页码数
            page: 1,                                   //分页页码数
            Operatelog:[],
            search: '',                                 //搜索框
        },
        methods: {
           show() {
               //显示
                axios({
                    method: 'post',
                    url: '/logmanagement/show_all/',
                    data: {
                        page: vm.page,
                        limit: 10
                    },
                }).then(function (res) {
                    vm.Operatelog = res.data.message;
                    vm.page_count = res.data.message[0].page_count;
                })
            },
           current_change(value){
               vm.page = value;
                axios({
                    method: 'post',
                    url: '/logmanagement/select_log/',
                    data: {
                        search: this.search,
                        page: vm.page,
                        limit: 10
                    },
                }).then((res) => {
                    vm.Operatelog = res.data.message;
                    vm.page_count = res.data.message[0].page_count;
                })
            },
           select_log(){
               vm.page = 1                                             //查询
                if (this.search.trim() == '') {
                    vm.show()
                }
                axios({
                    method: 'post',
                    url: '/logmanagement/select_log/',
                    data: {
                        search: this.search,
                        page: this.page,
                        limit: 10
                    },
                }).then((res) => {

                    if(res.data.message.length == 0){
                        vm.Operatelog = []
                        vm.page_count = 1
                    }else{
                        vm.Operatelog = res.data.message;
                        vm.page_count = res.data.message[0].page_count;
                    }

                })
           }

        }
    });
    vm.show();