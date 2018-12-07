from django.shortcuts import render
from django.shortcuts import HttpResponse
from EasyWeb.views import DeviceSk


# Create your views here.



def HtmlShow(request):
    return HttpResponse('Hello World!')

def IndexShow(request):
    return render(request,'WebSock_B1.html')