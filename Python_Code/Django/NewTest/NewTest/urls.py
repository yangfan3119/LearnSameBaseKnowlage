"""NewTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from EasyWeb import views as Hello_v
from SockWeb import views as Sock_v
from TestBlog import views as Blog_v
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^index/',views.index),
    url(r'^$',Hello_v.index),

    url(r'^raspView/',Hello_v.raspView),
    url(r'^raspConn/',Hello_v.rasp),

    url(r'^WebSkView/',Hello_v.WebSkView),
    url(r'^WebSk/',Hello_v.WebSk),
    url(r'^NewWebSk/',Hello_v.NewWebSk),

    url(r'^TestBlog/',Blog_v.BlogShowInHtml),

    url(r'^Sk_b1/',Sock_v.HtmlShow),
    url(r'^Sk_b2/',Sock_v.IndexShow),
]
