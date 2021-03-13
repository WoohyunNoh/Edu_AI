import os
import shutil

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from django.http import HttpResponse
from django.http import JsonResponse

from .image_training import *
from .models import Project
from accounts.models import User
from accounts.serializers import UserSerializer
from .serializers import ProjectSerializer

from .forms import UploadFileForm
import json


# Create your views here.
# http://www.semusa.org/blog/8f82b881-3aed-44b2-a8d6-de8721880f36/
@csrf_exempt
def engine(request):
    data = {}
    if request.method == 'POST':

        # 폴더 존재 유무 확인
        def isFolder(directory):
            if not os.path.exists(directory):
                return False
            else:
                return True

        name = request.POST.get("name").split(',')
        pk = request.POST.get("id")
        print(name)
        # print(pk)

        # try:
        #     key = Project.objects.latest('id').id+ 1
        # except e:
        #     key=1
        # path = os.path.join(os.getcwd(), 'static','model',str(pk),str(key))
        # path = '/static/model/'+str(pk)+'/'+str(key)
        # print(path)
        user = User.objects.get(id=pk)
        print("user", user)
        user_serial = UserSerializer(user).data
        print("serial", user_serial)

        a = User(id=pk, name=user_serial['name'], email=user_serial['email'])

        model_instance = Project(user=user)
        model_instance.save()
        key = model_instance.pk
        model_instance.name = "project" + str(key)
        model_instance.save()
        for className in name:
            flist = request.FILES.getlist(className)
            directory = os.path.join(os.getcwd(), 'static', 'image', str(pk), str(key), className)

            index = 1
            # 폴더 없으면 폴더 생성
            if not isFolder(directory):
                os.makedirs(directory)

            for f in flist:
                ext = os.path.splitext(f.name)[1]
                print(ext)
                if not ext:
                    ext = '.jpg'
                tmp = open(os.path.join(directory, str(index) + ext), 'wb+')
                for chunk in f.chunks():
                    tmp.write(chunk)
                index += 1
        # train(name)
        data["key"] = key
        data["status"] = "success"
        return JsonResponse(data)
    data["key"] = None
    data["status"] = "fail"
    return JsonResponse(data)


@csrf_exempt
def training(request):
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    if request.method == 'POST':
        try:
            pk = data['pk']
            key = data['key']
            params = dict()
            params['epoch'] = data['epoch']
            params['batch'] = data['batch']
            params['rate'] = data['rate']
            params['pk'] = pk
            params['key'] = key
            project = Project.objects.filter(id=pk)
            res = serializers.serialize('json', project)
            image_base_dir = os.path.join(os.getcwd(), 'static', 'image')
            image_dir = os.path.join(image_base_dir, str(pk), str(key))
            class_names = [dI for dI in os.listdir(image_dir) if os.path.isdir(os.path.join(image_dir, dI))]
            train(class_names, params)
            return HttpResponse("success")
        except Exception as e:
            print(e)
            return HttpResponse("fail")
        # res = ProjectSerializer(project, many=True)
