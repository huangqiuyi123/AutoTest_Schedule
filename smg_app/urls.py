# -*- coding: utf-8 -*-
# @Time    : 2022/3/25 13:14
# @Author  : HQY
# @FileName: urls.py
# @Software: PyCharm

from django.conf.urls import url
from . import views
# from smg_app.views import Schedule

urlpatterns = [
    url(r'^login/$', views.login),
    url(r'^query_user/$',views.query_user),
    url(r'^add_user/$',views.add_user),
    url(r'^update_user/$',views.update_user),
    url(r'^delete_user/$',views.delete_user)
    # url(r'^query_user/$',Schedule.as_view(),name='query_user')
]




