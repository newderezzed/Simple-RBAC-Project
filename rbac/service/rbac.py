import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect

class ValidePermission(MiddlewareMixin):

    def process_request(self,request):

        print('--------------------->中间件')

        # 当前访问路径

        current_path = request.path_info

        # 检查是否属于白名单

        valid_url_list = ["/login/","/logout/","/reg/","/admin/.*"]

        for valid_url in valid_url_list:

            ret = re.match(valid_url,current_path)

            if ret:
                return None

        # 检验是否登陆

        user_id = request.session.get("user_id")

        if not user_id:
            return redirect("/login/")

        # 校验权限

        # new
        permission_dict = request.session.get("permission_dict")

        for item in permission_dict.values():
            urls = item['urls']
            for reg in urls:
                reg = "^%s$" % reg
                ret = re.match(reg, current_path)
                if ret:
                    request.actions = item['actions']
                    print('中间件成功通过！！！！')
                    return None

        return HttpResponse("没有访问权限！")



'''
permission_list = request.session.get("permission_list",[])

flag = False

for permission in permission_list:

    permission = "^%s$" % permission

    ret = re.match(permission,current_path)

    if ret:
        flag = True
        break

if not flag:
    return HttpResponse("没有访问权限！")
return None
'''