'''
Created on 01-Sep-2016

@author: jatinbhola6
'''
from django.conf.urls import url
from . import views
app_name='MnCapp'
urlpatterns=[
             url(r'^$',views.index,name='index'),
             url(r'^signin/$',views.SignInView.as_view(),name='signin'),
             url(r'^signup/$',views.SignUpView.as_view(),name='signup'),
             url(r'^success/$',views.SuccessView.as_view(),name='success'),
             url(r'^logout/$', views.log_out, name='logout'),
             url(r'^writememo/$',views.MemoView.as_view(),name='write_memo'),
             url(r'^getMemo/$',views.getMemo,name='getMemo'),
             url(r'^test/$',views.test,name="test")
]