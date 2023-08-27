from django.shortcuts import render
from django.shortcuts import render

# Create your views here.
import json
import os.path
import pprint
import time
import uuid
import platform

import jwt
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
import re
from datetime import datetime, timedelta
from django.template import loader
from jose import JWTError
from jwt import ExpiredSignatureError

from summer_backend import settings
from summer_backend.settings import SECRET_KEY, EMAIL_HOST_USER
from user.authentication import validate_all, validate_login
from user.cos_utils import get_cos_client, Label, Category, SubLabel
from user.models import User
from team.models import Team, Member, Project
from django.utils import timezone

from user.views import upload_cover_method


# Create your views here.
@validate_login
def create_team(request):
    if request.method == 'POST':
        user = request.user
        team_name = request.POST.get("team_name")
        description = request.POST.get('description')
        team = Team.objects.create(name=team_name, user=user)
        cover = request.FILES.get('cover')
        if description:
            team.description = description
        if cover:
            res, cover_url, content = upload_cover_method(cover, user.id, 'team_cover')
            if res == -2:
                return JsonResponse({'errno': 1, 'msg': "图片格式不合法"})
            elif res == 1:
                return JsonResponse({'errno': 1, 'msg': content})
            else:
                team.cover_url = cover_url
        team.save()
        member = Member.objects.create(role='CR', user=user, team=team)
        return JsonResponse({'errno': 0, 'msg': "创建团队成功"})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方法错误"})


@validate_login
def update_team(request, team_id):  # 修改团队描述 上传头像
    if request.method == 'POST':
        user = request.user
        description = request.POST.get('description')
        team_name = request.POST.get('team_name')
        cover = request.FILES.get('cover')
        team_list = Team.objects.filter(id=team_id)
        if not team_list.exists():
            return JsonResponse({'errno': 1, 'msg': "该团队不存在"})
        team = team_list[0]
        if not team.user == user:
            return JsonResponse({'errno': 1, 'msg': "用户权限不足"})
        if team_name:
            team.name = team_name
        if description:
            team.description = description
        if cover:
            res, cover_url, content = upload_cover_method(cover, team.id, 'team_cover')
            if res == -2:
                return JsonResponse({'errno': 1, 'msg': "图片格式不合法"})
            elif res == 1:
                return JsonResponse({'errno': 1, 'msg': content})
            else:
                team.cover_url = cover_url
        team.save()
        return JsonResponse({'errno': 0, 'msg': "修改信息成功"})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方法错误！"})


# 邀请好友
@validate_login
def get_invitation(request):
    if request.method != 'GET':
        return JsonResponse({'errno': 1, 'msg': "请求方法错误"})
    user = request.user
    team_id = request.GET.get("team_id")
    team_list = Team.objects.filter(id=team_id)
    if not team_list.exists():
        return JsonResponse({'errno': 1, 'msg': "该团队不存在"})
    team = team_list[0]
    member_list = Member.objects.filter(user=user, team=team)
    if not member_list.exists():
        return JsonResponse({'errno': 1, 'msg': "当前用户不属于该团队"})
    member = member_list[0]
    if member.role == 'MB':
        return JsonResponse({'errno': 1, 'msg': "用户权限不足"})
    invitation = team.invitation
    if not invitation:
        payload = {"team_id": team_id}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        # if platform.system()=='linux':
        invitation = "http://www.aamofe.top/api/team/open_invitation/" + token + '/'
        # else :
        #     invitation = "http://127.0.0.1/api/team/accept_invitation/" + token+'/'
        team.invitation = invitation
        team.save()
    return JsonResponse({'errno': 1, 'msg': "链接已生成", 'invatation': invitation})
@validate_all
def redi(request):
    token1 = request.META.get('HTTP_Authorization'.upper())
    if not token1:
        return redirect('http://www.aamofe.top/')
    payload = jwt.decode(token1, SECRET_KEY, algorithms=['HS256'])
    token1 = token1.replace('Bearer ', '')
    try:
        jwt_token = jwt.decode(token1, settings.SECRET_KEY, options={'verify_signature': False})
        try:
            user = User.objects.get(id=jwt_token.get('id'), isActive=True)
            user_id = user.id
        except User.DoesNotExist:
            title = '用户不存在'
            content = '请先注册'
    except ExpiredSignatureError:
        title = '登录已过期'
        content = '请重新登录'
    except JWTError:
        title = '用户身份错误'
        content = '请重新登录'
    request.user=user
    return JsonResponse({'title':title,"user_id":user.id,"content":content})

@validate_all
def open_invitation(request, token):
    title = ''
    content = ''
    user_id = ''
    team_id = ''
    # 下面是用户的信息
    print(request.META)
    print(111)
    pprint.pprint(request.META)
    # 下面是team_id的信息
    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    team_id = payload.get('team_id')
    team_list = Team.objects.filter(id=team_id)
    if not team_list.exists():
        title = '链接不正确'
        content = "记得要个新链接"
    else:
        team = team_list[0]
        team_id = team.id
        title = "邀请你加入团队 " + team.name
        content = '点击下方链接'
    context = {'title': title, 'content': content, "team_id": team_id, 'user_id': user_id}
    return render(request, "invite.html", context)


@validate_all
def accept_invitation(request):

    team_id = request.POST.get('team_id')
    user_id = request.POST.get('user_id')
    if team is None:
        team=3
    if user_id is None:
        user_id=3
    team = Team.objects.get(id=team_id)
    user = User.objects.get(id=user_id)
    member = Member.objects.filter(user=user, team=team)
    if member.exists():
        return JsonResponse({'errno': 0, 'msg': "您已加入该团队"})
    member = Member.objects.create(user=user, team=team)
    return JsonResponse({'errno': 0, 'msg': "加入成功"})
@validate_login
# def all_teams(request):
#     if request.method != 'GET':
#         print(2)
#         return JsonResponse({'errno': 1, 'msg': "请求方法错误"})
#     print(3)
    
#     # user = request.user
#     user_id=request.GET.get("user_id")
#     print('user_id : ',user_id)
#     try:
#         user=User.objects.get(id=user_id)
#     except User.DoesNotExist:
#         return JsonResponse({'errno': 1, 'msg': "用户id不存在"})
#     member_list = Member.objects.filter(user=user)
#     print(4)
#     teams = []
#     for member in member_list:
#         team_info = member.team.to_dict()
#         team_info['role'] = member.role
#         teams.append(team_info)
#     # pprint.pprint(teams)
#     return JsonResponse({'errno': 0, 'msg': "获取团队", 'teams': teams})
# 获取所有团队
@validate_login
def all_teams(request):
    print(1)
    if request.method != 'GET':
        print(2)
        return JsonResponse({'errno': 1, 'msg': "请求方法错误"})
    print(3)
    user = request.user
    print('user_id : ',user.id)
    try:
        user=User.objects.get(id=user.id,isActive=True)
    except User.DoesNotExist:
        return JsonResponse({'errno': 1, 'msg': "用户id不存在"})
    member_list = Member.objects.filter(user=user)
    print(4)
    teams = []
    for member in member_list:
        team_info = member.team.to_dict()
        team_info['role'] = member.role
        teams.append(team_info)
    pprint.pprint(teams)
    return JsonResponse({'errno': 0, 'msg': "获取团队", 'teams': teams})


@validate_login
def all_members(request):
    if request.method != 'GET':
        return JsonResponse({'errno': 1, 'msg': "请求方法错误"})
    user = request.user
    team_id = request.GET.get("team_id")
    try:
        team=Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return JsonResponse({'errno': 1, 'msg': "团队不存在"})
    member_list = Member.objects.filter(user=user, team=team)
    if not member_list.exists():
        return JsonResponse({'errno': 1, 'msg': "当前用户不属于该团队"})
    members = []
    member_list = Member.objects.filter(team=team,role="CR")
    for member in member_list:
        user_info = member.user.to_dict()
        user_info['role'] = member.role
        members.append(user_info)
    member_list = Member.objects.filter(team=team,role="MG")
    for member in member_list:
        user_info = member.user.to_dict()
        user_info['role'] = member.role
        members.append(user_info)
    member_list = Member.objects.filter(team=team,role="MB")
    for member in member_list:
        user_info = member.user.to_dict()
        user_info['role'] = member.role
        members.append(user_info)
    return JsonResponse({'errno': 0, 'msg': "获取成员", 'members': members})


@validate_login
def update_permisson(request, team_id):
    if request.method != 'POST':
        return JsonResponse({'errno': 1, 'msg': "请求方法错误"})
    choice = request.POST.get('choice')  # MG MB DE
    user_id = request.POST.get('user_id')
    editor = request.user
    team_list = Team.objects.filter(id=team_id)
    if not team_list.exists():
        return JsonResponse({'errno': 1, 'msg': "该团队不存在"})
    team = team_list[0]
    member_list = Member.objects.filter(user=editor, team=team)
    if not member_list.exists():
        return JsonResponse({'errno': 1, 'msg': "当前用户不属于该团队"})
    medtor = member_list[0]
    try:
        edited = User.objects.filter(id=user_id)[0]
    except User.DoesNotExist:
        return JsonResponse({'errno': 1, 'msg': "该用户不存在"})
    member_list = Member.objects.filter(user=edited, team=team)
    if not member_list.exists():
        return JsonResponse({'errno': 1, 'msg': "该用户不属于该团队"})
    medted = member_list[0]
    if edited.id == editor.id:
        return JsonResponse({'errno': 1, 'msg': "无法修改自身权限"})
    if medtor.role == 'MB' or (medtor.role == 'MG' and medted.role == 'CR'):
        return JsonResponse({'errno': 1, 'msg': "用户权限不足"})
    if choice == medted.role:
        return JsonResponse({'errno': 1, 'msg': "身份未发生改变"})
    elif choice == 'DE':
        medted.delete()
    elif choice == 'MG' or choice == 'MB':
        medted.role = choice
        medted.save()
    else:
        return JsonResponse({'errno': 1, 'msg': "操作错误"})
    return JsonResponse({'errno': 0, 'msg': "操作成功"})


@validate_login
def create_project(request, team_id):
    if request.method != 'POST':
        return JsonResponse({'errno': 1, 'msg': "请求方法错误"})
    user = request.user
    project_name = request.POST.get('project_name')
    if not project_name:
        return JsonResponse({'errno': 1, 'msg': "请输入项目名称"})
    team_list = Team.objects.filter(id=team_id)
    if not team_list.exists():
        return JsonResponse({'errno': 1, 'msg': "该团队不存在"})
    team = team_list[0]
    project = Project.objects.create(name=project_name, team=team)
    return JsonResponse({'errno': 1, 'msg': "项目创建成功"})


@validate_login
def update_project(request, project_id):
    if request.method != 'POST':
        return JsonResponse({'errno': 1, 'msg': "请求方法错误"})
    try:
        project = Project.objects.filter(id=project_id)[0]
    except Project.DoesNotExist:
        return JsonResponse({'errno': 1, 'msg': "项目不存在"})
    user = request.user
    member_list = Member.objects.filter(user=user, team=project.team)
    if not member_list.exists():
        return JsonResponse({'errno': 1, 'msg': "当前用户不属于该团队"})
    project.is_deleted ^= True
    project.save()
    return JsonResponse({'errno': 0, 'msg': "项目删除成功"})


@validate_login
def rename_project(request, project_id):
    if request.method != 'POST':
        return JsonResponse({'errno': 1, 'msg': "请求方法错误"})
    try:
        project = Project.objects.filter(id=project_id)[0]
    except Project.DoesNotExist:
        return JsonResponse({'errno': 1, 'msg': "项目不存在"})
    user = request.user
    new_name = request.POST.get("new_name")
    member_list = Member.objects.filter(user=user, team=project.team)
    if not member_list.exists():
        return JsonResponse({'errno': 1, 'msg': "当前用户不属于该团队"})
    project.name = new_name
    project.save()
    return JsonResponse({'errno': 0, 'msg': "项目删除成功"})

def checkout_team(request):
    if request.method == 'POST':
        user=request.user
        team_id=request.POST.get('team_id')
        team_list = Team.objects.filter(id=team_id)
        if not team_list.exists():
            return JsonResponse({'errno': 1, 'msg': "该团队不存在"})
        team = team_list[0]
        member_list = Member.objects.filter(user=user, team=team)
        if not member_list.exists():
            return JsonResponse({'errno': 1, 'msg': "当前用户不属于该团队"})
        member = member_list[0]
        user.current_team_id=team.id
        user.save()
        team_info={'user_id': user.id,'current_team':user.team.id,}
        return JsonResponse({ 'data':team_info, 'errno': 0, 'msg': "登录成功"})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方法错误！"})
def quit_team(request,team_id):
    if request.method != 'POST':
        return JsonResponse({'errno': 1, 'msg': "请求方法错误"})
    
@validate_all
def get_current_team(request):
    if request.method != 'GET':
        return JsonResponse({'errno': 1, 'msg': "请求方法错误"})
    user_id=request.GET.get('user_id')
    try:
        user=User.objects.get(id=user_id)
    except:
        return JsonResponse({'errno': 1, 'msg': "用户不存在"})
    return JsonResponse({'errno': 0,'team_id':user.current_team_id, 'msg': "请求成功"})
    user=request.user
@validate_login
def all_projects(request):
    if request.method != 'GET':
        return JsonResponse({'errno': 1, 'msg': "请求方法错误"})
    user=request.user
    try:
        team=Team.objects.get(id=user.current_team_id)
    except Team.DoesNotExist:
        team=Team.objects.get(user=user,name='个人空间')
        user.current_team_id=team.id
        user.save()
    projects=Project.objects.filter(team=team,is_deleted=False)
    project_list=[]
    for p in projects:
        project_list.append(p.to_dict())
    return JsonResponse({'errno': 0, 'msg': "获取团队所有项目成功",'projects':project_list})