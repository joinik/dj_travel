




# register_converter(UsernameConverter, 'user')
# register_converter(PhoneConverter, 'phone')
from django.urls import path

from apps.users.views import UserAuthorizeView, UserInfoView

urlpatterns = [
    # # 注册用户
    # path('register/', RegisterView.as_view()),
    # # 用户登录验证 自定义类
    path('authorizations/', UserAuthorizeView.as_view()),
    #
    # # # 刷新token
    # # path('refresh/', refresh_jwt_token),
    # # 用户个人信息
    path('user', UserInfoView.as_view()),


]