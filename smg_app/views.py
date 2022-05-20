import datetime

import pymysql,json
import logging
from django.views import View
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core import serializers
from smg_app import models
from schedule.settings import DATABASES



# Create your views here.
# 添加用户处理函数
#
# def add_user():
#
#     conn = MySQLdb.connect(host='127.0.0.1',user='root',password='niki123456',db='schedule',charset='utf8')
#     with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
#         cursor.execute("INSERT INTO smg_app_user (login_name,password,nickname,role,status)"
#                        "VALUES (%s,%s,%s,%s,%s) % (login_name,password,nickname,role,status]")
#         conn.commit()
#         print("操作成功")


def logger():
    # 日志打印函数
    log = logging.getLogger(__name__)
    return log

def database():
    # 数据库连接
    # db = pymysql.connect(host='127.0.0.1', user='root', password='niki123456', db='schedule', charset='utf8')
    # 获取数据库信息
    host = DATABASES["default"].get("HOST")
    user = DATABASES["default"].get("USER")
    password = DATABASES["default"].get("PASSWORD")
    name = DATABASES["default"].get("NAME")
    db = pymysql.connect(host=host, user=user, password=password, db=name, charset='utf8')
    # 发起请求时候确保服务器与数据库保持连接
    db.ping(reconnect=True)
    return db

def get_data(request):
    # 获取请求body，并转化成json格式
    log = logger()
    data_str = request.body.decode()
    # log.debug(type(data_str))
    data = json.loads(data_str)
    # log.debug(data)
    return data

def login(request):
    """
    用户登录接口
    :param request:
    :return:
    """
    log = logger()
    if request.method == "POST":
        body = get_data(request)
        name = body["login_name"]
        psw = body["password"]
        condition = models.User.objects.filter(login_name=name)
        if condition:
            if condition[0].password == psw:
                ser = serializers.serialize('json', queryset=condition, ensure_ascii=False)
                result = {"code": "200","msg": "登录成功~","data":json.loads(ser)}  # 登录成功返回该用户信息
            else:
                result = {"code": "500","msg": "密码错误，请检查！"}
        else:
            result = {"code": "500","msg": "登录名不存在，请检查！"}
    else:
        result = {"code": "500","msg": "请求方法错误，请检查！"}
    return JsonResponse(result, content_type="application/json", safe=False)


def query_user(request):
    """
    用户查询接口
    :param request:登录名称精确/模糊查询
    :return:序列化结果集
    """
    log = logger()
    # 连接数据库
    db = database()
    # 创建游标
    cursor = db.cursor()
    if request.method == "POST":
        # 获取请求参数
        data = get_data(request)
        # 获取value值
        login_name = data["login_name"]
        sql = "select * from smg_app_user where login_name = '%s'" % login_name
        log.debug(sql)
        # 普通的%用两个%（%%）转义表示
        # sql = "select * from smg_app_user where login_name like '%%%s%%'" % login_name

        try:
            # 执行sql
            cursor.execute(sql)
            db.commit()
            res = cursor.fetchall()
            log.debug(res)
            if len(res) != 0:
                # objects.all()--获取user表中所有的数据,objects.filter(login_name=login_name)--指定条件返回数据
                # queryset = models.User.objects.all()
                queryset = models.User.objects.filter(login_name=login_name)
                # 序列化方法转成json格式,ensure_ascii=False 转换成中文
                ser = serializers.serialize('json',queryset=queryset,ensure_ascii=False)
                result = {"code": "200","msg": "查询成功~","data": json.loads(ser)}
            else:
                # 如果查询结果为空，则返回所有数据
                queryset = models.User.objects.all()
                # 序列化方法转成json格式,ensure_ascii=False 转换成中文
                ser = serializers.serialize('json', queryset=queryset, ensure_ascii=False)
                result = {"code": "200","msg": "查询成功~","data": json.loads(ser)}
        except pymysql.Error as e:
            # 发生错误回滚
            db.rollback()
            result = {"code": "500","error": e,"msg": "执行错误，请检查！"}

    else:
        result = {"code": "500","msg": "请求方法错误，请检查！"}
    return JsonResponse(result,content_type="application/json",safe=False)
    # return HttpResponse(result,content_type="application/json")



def add_user(request):
    """
    新增用户接口
    先查询，结果有值则返回查询结果，无值直接新增用户
    """
    log = logger()
    # 连接数据库
    db = database()
    # 创建游标
    cursor = db.cursor()
    if request.method == "POST":
        # 获取请求参数
        data = get_data(request)
        # 获取value值
        id = data["user_id"]
        name = data["login_name"]
        psw = data["password"]
        nick_name = data["nickname"]
        # sql = "select * from smg_app_user where login_name like '%s'" % login_name
        # 普通的%用两个%（%%）转义表示
        query_sql = "select * from smg_app_user where login_name = '%s'" % name
        insert_sql = "INSERT INTO smg_app_user (login_name,password,nickname) \
                VALUES ('%s','%s','%s')" % (name, psw, nick_name)
        if models.User.objects.filter(user_id=id):
            try:
                cursor.execute(query_sql)
                db.commit()
                res = cursor.fetchall()
                if len(res) == 0:
                    if name == "" or psw =="" or nick_name =="":
                        result = {"code": "200", "msg": "必填信息不能为空，请检查！"}
                    else:
                        try:
                            # 执行sql
                            cursor.execute(insert_sql)
                            db.commit()
                            queryset = models.User.objects.filter(login_name=name)
                            # 序列化方法转成json格式,ensure_ascii=False 转换成中文
                            ser = serializers.serialize('json', queryset=queryset, ensure_ascii=False)
                            result = {"code": "200", "msg": "添加用户成功~","data":json.loads(ser)}
                        except pymysql.Error as e:
                            # 发生错误回滚
                            db.rollback()
                            result = {"code": "500","error": e, "msg": "添加用户失败!"}
                else:
                    result = {"code": "500","msg": "该用户名已存在，请换一个试试吧~"}
            except pymysql.Error as e:
                db.rollback()
                result = {"code": "500","msg": e}
        else:
            result = {"code": "500", "msg": "操作用户不存在，请检查！"}
    else:
        result = {"code": "500","msg": "请求方法错误，请检查！"}

    return JsonResponse(result,content_type="application/json",safe=False)
    # return HttpResponse(result,content_type="application/json")

def update_user(request):
    """
    更新用户信息接口
    """
    # 连接数据库
    db = database()
    # 创建游标
    cursor = db.cursor()
    if request.method == "POST":
        # 获取请求参数
        data = get_data(request)
        # 获取value值
        id = data["user_id"]
        name = data["login_name"]
        psw = data["password"]
        nick_name = data["nickname"]
        # 普通的%用两个%（%%）转义表示
        update_sql = "update smg_app_user set login_name = '%s', password = '%s',nickname='%s' where user_id = %s"\
                 % (name, psw, nick_name, id)
        if models.User.objects.filter(user_id=id):
            try:
                cursor.execute(update_sql)
                db.commit()
                result = {"code": "200", "msg": "更新用户信息成功~"}

            except pymysql.Error as e:
                db.rollback()
                result = {"code": "500", "msg": e}
        else:
            result = {"code": "500", "msg": "操作用户不存在，请检查！"}
    else:
        result = {"code": "500", "msg": "更新用户信息失败，请检查！"}

    return JsonResponse(result,content_type="application/json",safe=False)

def delete_user(request):
    """
    删除用户信息接口
    """
    # 连接数据库
    db = database()
    # 创建游标
    cursor = db.cursor()
    if request.method == "POST":
        # 获取请求参数
        data = get_data(request)
        # 获取value值
        id = data["user_id"]
        name = data["login_name"]
        # 普通的%用两个%（%%）转义表示
        delete_sql = "delete from smg_app_user where login_name = '%s'" % name
        if models.User.objects.filter(user_id=id):
            if models.User.objects.filter(login_name=name):
                try:
                    cursor.execute(delete_sql)
                    db.commit()
                    result = {"code": "200","msg": "删除用户成功~"}
                except pymysql.Error as e:
                    db.rollback()
                    result = {"code": "500","msg": e}
            else:
                result = {"code": "500", "msg": "用户信息不存在，请检查~"}
        else:
            result = {"code": "500","msg": "操作用户不存在，请检查~"}
    else:
        result = {"code": "500","msg": "删除用户失败，请检查！"}

    return JsonResponse(result,content_type="application/json",safe=False)





# def add_user(request):
#     """先查询，结果有值则返回查询结果，无值直接新增用户"""
#     log = logger()
#     # 连接数据库
#     db = database()
#     # 创建游标
#     cursor = db.cursor()
#     # 获取请求参数
#     data = get_data(request)
#     # 获取value值
#     name = data["login_name"]
#     psw = data["password"]
#     nick_name = data["nickname"]
#     query = query_user(request)
#     # sql = "select * from smg_app_user where login_name like '%s'" % login_name
#     # 普通的%用两个%（%%）转义表示
#     # query_sql = "select * from smg_app_user where login_name = '%s'" % name
#     insert_sql = "INSERT INTO smg_app_user (login_name,password,nickname) \
#             VALUES ('%s','%s','%s')" % (name,psw,nick_name)
#     if isinstance(query,tuple):
#         try:
#             # 执行sql
#             cursor.execute(insert_sql)
#             db.commit()
#             result = "添加用户成功"
#         except pymysql.Error as e:
#             # 发生错误回滚
#             db.rollback()
#             result = (e, "添加用户失败")
#     else:
#         result = query
#
#     return JsonResponse(result,content_type="application/json",safe=False)
#     # return HttpResponse(result,content_type="application/json")application












