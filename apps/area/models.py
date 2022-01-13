from django.db import models

# Create your models here.

from django.db import models




class Area(models.Model):
    """省市区"""
    name = models.CharField(max_length=20, verbose_name='名称')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True, verbose_name='上级行政区划')
    city_code = models.CharField(max_length=12, verbose_name="地区编码")
    city_level = models.IntegerField(verbose_name='地区级别')

    class Meta:
        db_table = 'tab_citys'
        verbose_name = '省市区'
        verbose_name_plural = '省市区'

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'parent': self.parent.name if self.parent else self.parent,
            'subs': self.subs,
            'city_level': self.city_level
        }

