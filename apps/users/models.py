from datetime import datetime

from django.db import models

# Create your models here.
from utils.myModels import BaseModel


class User(models.Model):
    # id = models.IntegerField(primary_key=True, verbose_name='用户ID')
    name = models.CharField(max_length=20, unique=True, verbose_name='昵称')
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    profile_photo = models.CharField(max_length=256, verbose_name='用户头像')
    last_login = models.DateTimeField(default=datetime.now, verbose_name='最后登录的时间')
    ctime = models.DateTimeField(auto_now_add=True, verbose_name='注册的时间')
    introduction = models.CharField(max_length=128, verbose_name='简介')
    last_address_id = models.ForeignKey('area.Area', related_name='users', on_delete=models.SET_NULL,
                                        null=True, verbose_name='上一次的位置')
    status = models.IntegerField(default=1, verbose_name='状态，是否可用，0-不可用，1-可用')
    business = models.IntegerField(default=0, verbose_name='商家，是否可用，0-不可用，1-可用')
    default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True,
                                        on_delete=models.SET_NULL, verbose_name='默认地址')
    dianzan_num = models.IntegerField(default=0, verbose_name='获赞总数')
    travel_note_num = models.IntegerField(default=0, verbose_name='游记总数')
    dianliang_area_num = models.IntegerField(default=0, verbose_name='点亮地区数')
    is_admin = models.BooleanField(default=False, verbose_name='是否为管理员')


    class Meta:
        db_table = 'tb_users'
        verbose_name = '用戶'
        verbose_name_plural = verbose_name

    def to_dict(self):
        """模型转字典, 用于序列化处理"""
        return {
            'id': self.id,
            'name': self.name,
            'photo': self.profile_photo,
            'intro': self.introduction,
            'dianzan_count': self.dianzan_num,
            'travel_note_count': self.travel_note_num,
            'dianliang_area_count': self.dianliang_area_num,
            'business': self.business,
        }


class UserProfile(models.Model):
    user = models.ForeignKey("User", null=False, on_delete=models.CASCADE, verbose_name='用户ID')
    sex_choice = ((0, '男'), (1, '女'))
    sex = models.SmallIntegerField(choices=sex_choice, default=0, verbose_name='性别')
    age = models.IntegerField(verbose_name='年龄',default=0)
    email = models.CharField(max_length=20, verbose_name='邮箱')
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

    class Meta:
        db_table = 'tb_users_profile'
        verbose_name = '用戶资料表'
        verbose_name_plural = verbose_name

    def to_dict(self):
        return {
            'name': self.user.name,
            'gender': self.sex,
            'age': self.age,
            'email': self.email,
        }

class Address(BaseModel):
    """用户地址"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    province = models.ForeignKey('area.Area', on_delete=models.PROTECT, related_name='province_addresses',
                                 verbose_name='省')
    city = models.ForeignKey('area.Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('area.Area', on_delete=models.PROTECT, related_name='district_addresses',
                                 verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='地址')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']




