from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response

from apps.users.models import User


class UsernameCountView(APIView):
    """用户查询接口"""

    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return Response({"count": count, 'code': "0", "errmag": "ok"})

