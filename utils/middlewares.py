# from rest_framework import request
from functools import wraps

from django.http import request, JsonResponse
from requests import Response
from rest_framework import status

from travel_dj.settings import G
from utils.jwt_util import verify_jwt


def my_middleware(get_response):

    def get_userinfo(request):
        """获取用户信息"""

        # 获取请求头中的token
        auth = request.META.get('HTTP_AUTHORIZATION')
        # print(auth)
        # input('等待》》》》》》》》》》》》》》》》')
        G["user_id"] = None     # 如果未登录， userid=None
        G["is_refresh"] = None       # 设置是否刷新token
        if auth and auth.startswith('Bearer '):
            # "提取token 0-6 被Bearer和空格占用 取下标7以后的所有字符"
            token = auth[7:]
            # 校验token

            data = verify_jwt(token)

            if data:    # 校验成功
                G["user_id"] = data.get('user_id')   # 如果已登录，  userid=2
                G["is_refresh"] = data.get('is_refresh')



        response = get_response(request)
        return response

    return get_userinfo



def login_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        # 如果用户已登录，正常访问

        if G["user_id"] and not G["is_refresh"]:
            return f(*args, **kwargs)
        else:
            return JsonResponse({'message': 'Invalid Token', 'data': None})

    return wrapper
