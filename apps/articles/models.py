from django.db import models

# Create your models here.
from utils.myModels import BaseModel


class Category(BaseModel):
    """文章分类"""

    # id = models.IntegerField(db.Integer, primary_key=True)  # 分类编号
    name = models.CharField(max_length=64, null=False)  # 分类名
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_category'
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']






class Article(BaseModel):
    """文章基本信息表"""

    ARTICLE_STATUS_CHOICES =(
        (1, "DRAFT"),       # 草稿
        (2,"UNREVIEWED"),   # 待审核
        (3,"APPROVED"),     # 审核通过
        (4,"FAILED"),       # 审核失败
        (5,"DELETED"),      # 已删除
        (6,"BANNED"),       # 封禁
    )



    title = models.CharField(max_length=128, verbose_name='文章标题')
    cover = models.TextField(verbose_name='封面')
    status = models.SmallIntegerField(choices=ARTICLE_STATUS_CHOICES, default=1, verbose_name='文章状态')
    reason = models.CharField(max_length=256, verbose_name='未通过原因')
    comment_count = models.IntegerField(default=0, verbose_name='评论数')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    dislike_count = models.IntegerField(default=0, verbose_name='点踩数')
    author = models.ForeignKey("users.User", related_name='articles', on_delete=models.CASCADE, null=False, verbose_name='用户ID')
    area = models.ForeignKey("area.Area", related_name='articles', on_delete=models.CASCADE, null=False, verbose_name='地区ID')
    category = models.ForeignKey("Category", related_name='articles', on_delete=models.CASCADE, null=False, verbose_name='分类ID')


    class Meta:
        db_table = 'tb_article'
        verbose_name = '文章基本信息表'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']

    def to_dict(self):
        """
        定义一个方法，用来将将对象中的部分属性，转换为字典
        :return: 一个字典
        """
        ret = {
            "id": self.id,
            "title": self.title,
            "cover": self.cover,
            "status": self.status,
            "reason": self.reason,
            "area": self.area.name,
            "create_time": self.create_time,
            "update_time": self.update_time,
            "comment_count": self.comment_count,
            "like_count": self.like_count,
            "dislike_count": self.dislike_count,
            "category": self.category.name,
            "author": self.author.name,
        }
        return ret


    def __str__(self):
        return self.title


class ArticleContent(models.Model):
    """
    文章内容表
    """
    __tablename__ = 'article_content'

    article = models.ForeignKey("Article", null=False, on_delete=models.CASCADE, verbose_name='文章ID')
    content = models.TextField(verbose_name='帖文内容')

    class Meta:
        db_table = 'tb_aticle_content'
        verbose_name = '文章内容表'
        verbose_name_plural = verbose_name





class Comment(BaseModel):
    content = models.CharField(max_length=256, verbose_name='评论内容')
    user = models.ForeignKey("users.User", null=True, on_delete=models.CASCADE, verbose_name='用户id')
    article = models.ForeignKey("Article", null=True, on_delete=models.CASCADE, verbose_name='文章id')
    comment_parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name='comment_subs', null=True, blank=True, verbose_name='父评论')
    reply_count = models.IntegerField(default=0, verbose_name='回复数')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')


    class Meta:
        db_table = 'tb_aticle_comment'
        verbose_name = '文章评论表'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']




class LikeComment(models.Model):
    """点赞表"""
    user = models.ForeignKey("users.User", null=True, on_delete=models.CASCADE, verbose_name='用户id')
    article = models.ForeignKey("Article", null=True, on_delete=models.CASCADE, verbose_name='文章id')
    article_comment = models.ForeignKey("Comment", null=True, on_delete=models.CASCADE, verbose_name='评论id')

    class Meta:
        db_table = 'tb_like_comment'
        verbose_name = '文章评论表'
        verbose_name_plural = verbose_name


class DislikeComment(models.Model):
    """点踩表"""
    user = models.ForeignKey("users.User", null=True, on_delete=models.CASCADE, verbose_name='用户id')
    article = models.ForeignKey("Article", null=True, on_delete=models.CASCADE, verbose_name='文章id')
    article_comment = models.ForeignKey("Comment", null=True, on_delete=models.CASCADE, verbose_name='评论id')

    class Meta:
        db_table = 'tb_dislike_comment'
        verbose_name = '文章评论表'
        verbose_name_plural = verbose_name
