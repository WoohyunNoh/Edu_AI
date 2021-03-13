from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse


from decouple import config

from .models import User
from .forms import LoginForm, CustomUserChangeForm, CustomUserCreationForm
from .serializers import UserSerializer
# from .utils import permission

import requests
import json
import jwt

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser



@csrf_exempt
def signup(request):
    print('회원가입 진입')
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    if request.method == 'POST':
        form = CustomUserCreationForm(data=data)
        print(form)
        if form.is_valid():
            user = form.save()
            # UserPrivacy(user=user).save()
            print(user)
            data = {}
            data['result'] = 'success'
            return JsonResponse(data)
    else:
        form = CustomUserCreationForm()
    data = {}
    data['error'] = form.errors.as_json()
    return JsonResponse(data)


@csrf_exempt
def check_email(request):
    data = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        email = data['email']
        print(email)
        data = {}
        #이메일 중복
        if User.objects.filter(email=email).exists():
            data["result"] = True
            return JsonResponse(data)
        #중복 X
        else:
            data["result"] = False
            return JsonResponse(data)

@csrf_exempt
def login(request):
    # print("login 진입")
    # print(request.body)
    data = json.loads(request.body.decode('utf-8'))
    # print(data)

    if request.method == 'GET':
        return HttpResponse("GET또다제")

    if request.method == 'POST':
        form = LoginForm(data=data)

        if form.is_valid():
            email = data["email"]
            password = data["password"]
            print("email: ", email, "password: ",password)
            user = authenticate(email=email, password=password)
            print(user)
            if user is not None:
                if user.is_active:
                    token = jwt.encode({"email": email}, config(
                        'SECRET_KEY'), algorithm="HS256")
                    token = token.decode("utf-8")
                    # print(token)
                    data = {}
                    data["token"] = token
                    data["user_pk"] = user.pk
                    return JsonResponse(data)
            else:
                data = {}
                data['error'] = "존재하지 않는 회원입니다."
        else:
            data = {}
            data['error'] = "아이디, 비밀번호를 확인해주세요."
    return JsonResponse(data)


def logout(request):
    pass

def get_all_profile(request):
    users = User.objects.all()
    users_serial = UserSerializer(users, many=True)

    return JsonResponse(users_serial.data, safe=False)

#유저 정보 token
@csrf_exempt
def getInfo(request):
    if request.method == 'POST':
        try:
            access_token = request.headers.get('access-token', None)
            print(access_token)
            payload = jwt.decode(access_token, config('SECRET_KEY'), algorithm='HS256')
            # print(payload)
            user = User.objects.get(email=payload['email'])
            # request.user = user
            a = UserSerializer(user)
            print(a.data)
            return JsonResponse(a.data, safe =False)
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN' }, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=400)


# class ProfileView(View):
#     @permission
#     def get(self, request, user_pk):
#         print('profile 진입')
#         user = get_object_or_404(User, pk=user_pk)
#         user_serial = UserSerializer(user)
#         print(user_serial.data)
#         # user_privacy = get_object_or_404(UserPrivacy, user=user)
#         # user_privacy_serial = UserPrivacySerializer(user_privacy)
#         # print(user_privacy_serial.data)

#         data = {}

#         for key, val in user_serial.data.items():
#             data[key] = val
#         # for key, val in user_privacy_serial.data.items():
#         #     data['privacy'][key] = val
#         return JsonResponse(data)

#     @permission
#     def post(self, request, user_pk):
#         # print('프로필 수정 진입')
#         data = json.loads(request.body.decode('utf-8'))
#         # print(data)
#         form = CustomUserChangeForm(data=data, instance=request.user)
#         if form.is_valid():
#             user = form.save()
#             # print(user)
#             data = {}
#             user_serial = UserSerializer(user)
#             for key, val in user_serial.data.items():
#                 data[key] = val
#             data['result'] = 'success'
#             return JsonResponse(data)
#         else:
#             form = CustomUserCreationForm(instance=request.user)
#         data = {}
#         data['error'] = "입력값을 확인해주세요."
#         return JsonResponse(data)



