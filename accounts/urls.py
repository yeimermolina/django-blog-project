from django.conf.urls import url
from django.contrib import admin

from .views import (
	login_view,
	logout_view,
	register_view,
	) 

urlpatterns = [
    url(r'^login/$', login_view, name= "login"),
    url(r'^logout/$', login_view, name= "logout"),
    url(r'^register/$', register_view, name= "register"),
    # url(r'^(?P<id>\d+)/delete/$', comment_delete, name = "delete"),
]
