from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key=True,unique=True,verbose_name='用户id')
    login_name = models.CharField(max_length=50,db_index = True,verbose_name='登录名')
    password = models.CharField(max_length=6,verbose_name='密码')
    nickname = models.CharField(max_length=30,verbose_name='昵称')
    role = models.IntegerField(default=2,verbose_name='用户角色，0是超级管理，1是普通管理员，2是普通用户')
    status = models.IntegerField(default=1,verbose_name='用户状态，0是停用，1是启用')
    add_time = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')



class schedule_management(models.Model):
    schedule_id = models.AutoField(primary_key=True,unique=True,verbose_name='日程id')
    title = models.CharField(max_length=100,db_index = True,verbose_name='日程标题')
    content = models.CharField(max_length=1000,verbose_name='日程内容')
    date = models.DateField(auto_now=True,verbose_name='日程内容')
    is_delete = models.IntegerField(default=1,verbose_name='用户状态，0为删除，1为正常')
    add_time = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')











