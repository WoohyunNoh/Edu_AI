import jwt                                                
import json                 
import requests

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist  

from decouple import config
from .models import User

def permission(func):
    def wrapper(self, request, *args, **kwargs):
        # print(request.headers.get('Authorization', None))
        try:
            access_token = request.headers.get('access-token', None)
            print(access_token)
            payload = jwt.decode(access_token, config('SECRET_KEY'), algorithm='HS256')
            # print(payload)
            user = User.objects.get(email=payload['email'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN' }, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=400)

        return func(self, request, *args, **kwargs)

    return wrapper