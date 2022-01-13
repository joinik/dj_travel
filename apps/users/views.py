from datetime import datetime

import re
from django.db import transaction
from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import User, UserProfile
from travel_dj.settings import G
from utils.jwt_util import _generate_tokens
from utils.middlewares import login_required


class UserAuthorizeView(APIView):

    def post(self,request):
        rest_dict = request.data
        mobile = rest_dict.get("mobile")
        sms_code = rest_dict.get("code")

        # 判断是否勾选同意协议
        if rest_dict.get("allow") != 'true':
            return Response({'message': 'Invalid allow', 'data': None}, status=status.HTTP_400_BAD_REQUEST)
        # 判断手机号是否合法
        if not re.match(r'^1[345789]\d{9}$', mobile):
            return Response({'message': 'Invalid mobile', 'data': None}, status=status.HTTP_400_BAD_REQUEST)

        # 3. 短信验证码
        redis_cli = get_redis_connection("verify_codes")
        redis_sms_code = redis_cli.get("sms_%s" % mobile)

        # 3.2判断是否过有效期
        # if redis_sms_code is None:
        #     return Response({'message': "短信验证码过期", 'data': None}, status=status.HTTP_400_BAD_REQUEST)

        # 3.3用户发过来的对比 redis_image_code是二进制 需要decode
        # if redis_sms_code.decode().lower() != sms_code.lower():
        #     return Response({'message': "短信验证码输入错误", 'data': None}, status=status.HTTP_400_BAD_REQUEST)


        # 显式的开启一个事务
        with transaction.atomic():
            # 暴力回滚
            try:
                # 创建事务保存点
                save_id = transaction.savepoint()
                # 查询数据库
                user = User.objects.filter(mobile=mobile).first()

                if user:
                    # 如果存在，返回 更新登录时间
                    user.last_login = datetime.now()

                else:
                    # 数据库存入数据
                    user = User(mobile=mobile, name=mobile, last_login = datetime.now())
                    user.save()
                    user_profile = UserProfile.objects.create(user_id=user.id)
                    # print(user_profile.id)
                    # input('等待')
            except Exception as e:
                print(e)
                print('数据库失败------->>>')
                # 回滚到保存点
                transaction.savepoint_rollback(save_id)

                return Response({"message": "register fail"}, status=status.HTTP_400_BAD_REQUEST)

            # 用户存储成功成功，显式的提交一次事务
            transaction.savepoint_commit(save_id)

        # 生成 token， refresh_token = _generratetokens(user.id)
        token, refresh_token = _generate_tokens(user.id)

        return Response({"message": "OK", "data": {'token': token, 'refresh_token': refresh_token}}, status=status.HTTP_201_CREATED)

    def put(self, request):
        if G["is_refresh"]:
            token, refresh_token = _generate_tokens(G["user_id"], False)
            return Response({'token': token}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': "Invalid refreshToken", 'data': None}, status=status.HTTP_403_FORBIDDEN)





class UserInfoView(APIView):
    """个人信息"""
    @login_required
    def get(self,request):

        user_id = G.get('user_id')
        user = User.objects.filter(id=user_id).first()
        return Response({"message": "OK", "data": user.to_dict()})



