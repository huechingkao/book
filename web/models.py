# -*- coding: utf8 -*-
from django.db import models

class Book(models.Model):
    # 書名
    title = models.CharField(max_length=255, verbose_name='書名')
    # 作者
    author = models.CharField(max_length=255, verbose_name='作者')
    # 日期
    publication_date = models.DateTimeField(auto_now_add=True)
    
class Reader(models.Model):
    # 姓名
    realname = models.CharField(max_length=255, verbose_name='姓名')
    # 連絡電話
    phone = models.CharField(max_length=255, verbose_name='電話')
    
# 流通紀錄
class Circulation(models.Model):
    # 書籍
    book_id = models.IntegerField(default=0)
    # 借閱人
    reader_id = models.IntegerField(default=0)
    # 借出日期
    date_checkout = models.DateTimeField(blank=False)
    # 歸還日期, 若為 null 表示尚未歸還
    date_return = models.DateTimeField(null=True)