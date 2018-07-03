from django.shortcuts import render, HttpResponse, redirect
import re
from  rbac.models import *
from rbac.service.perssions import *


# Create your views here.



class Per(object):
    def __init__(self, actions, userid):
        self.actions = actions
        self.userid = userid

    def add(self):
        return "add" in self.actions

    def delete(self):
        return "delete" in self.actions

    def edit(self):
        return "edit" in self.actions

    def list(self):
        return "list" in self.actions

    def user(self):
        user = User.objects.filter(id=self.userid).first()
        return user


# 用户
def users(request):
    user_list = User.objects.all()

    per = Per(request.actions, request.session.get("user_id"))

    return render(request, "users.html", locals())


def add_user(request):
    print('--------------------------->add_user')
    return HttpResponse("add user....")


def del_user(request, id):
    print('------------------------>del_user')
    return HttpResponse("del" + id)


# 角色
def roles(request):
    role_list = Role.objects.all()

    per = Per(request.actions, request.session.get("user_id"))

    return render(request, "roles.html", locals())


def add_roles(request):
    return HttpResponse("add roles....")


# 登陆
def login(request):
    if request.method == "POST":

        user = request.POST.get("user")
        pwd = request.POST.get("pwd")

        user = User.objects.filter(name=user, pwd=pwd).first()

        if user:
            ############################### 在session中注册用户ID######################
            request.session["user_id"] = user.pk
            ############################### 在session注册权限列表######################

            # 查询当前登陆用户的所有权限

            initial_session(user, request)

            return redirect('/user/')

    return render(request, "index_login.html")


def logout(request):
    del request.session["user_id"]
    return redirect('/login/')
