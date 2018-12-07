import json

from django.shortcuts import render


from blueking.component.shortcuts import get_client_by_request
from common.mymako import render_mako_context, render_json

def show_info(request):
    pass


def run_shell_host(request):
    client = get_client_by_request(request)

    client.set_bk_api_ver('v2')
    if request.method == 'GET':
        return render(request, 'base.html')
    else:
        list = []
        bk_token = request.COOKIES.get ("bk_token")
        req = json.loads(request.body)
        bk_app_code = client.app_code
        bk_app_secret = client.app_secret
        list = req.get("list") #接受前台传来数据
        client.set_bk_api_ver ('v2')
        if list:
            for i in list:
                print list
                param = {
                    "bk_app_code": bk_app_code,
                    "bk_app_secret": bk_app_secret,
                    "bk_token": bk_token,
                    "bk_biz_id": list.bk_biz_id,
                    "script_id": list.script_id,
                    #"script_content": "ZWNobyAkMQ==",
                    #"script_param": "aGVsbG8=",
                    "script_timeout": 1000,
                    "account": list.account,
                    "is_param_sensitive": 0,
                    "script_type": list.script_type,
                    "ip_list": [
                        {
                            "bk_cloud_id": list.bk_cloud_id,
                            "ip": list.ip
                        },
                        {
                            "bk_cloud_id": list.bk_cloud_id,
                            "ip": list.ip
                        }
                    ],
                    "custom_query_id": [
                        "3"
                    ]
                }
            res = client.job.fast_execute_script(param)
            list1 = []
            dic = {
                "bk_biz_name":"name",
                "script_name":"name",
                #前台展示的各项数据
            }
            if res.get('result',False):
                message = res.get('message')
                dic['message'] = message
                list1.append(dic)
            return render_json (
                {
                    "result": True,
                    "message": u"执行脚本成功",
                    "code": 0,
                    "results": list1
                }
            )
