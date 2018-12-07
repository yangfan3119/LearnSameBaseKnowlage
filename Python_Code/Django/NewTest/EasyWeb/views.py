from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse
from EasyWeb import models
from dwebsocket.decorators import accept_websocket, require_websocket

from MyRaspSock.RaspClientManage import RaspOp


Testlist = [{'name': 'good', 'password': 'python'}, {'name': 'learning', 'password': 'django'}]
DeviceRequest = None


def RaspDevAdd(d1, d2, d3, d4):
    # print(da,DeviceRequest)
    if DeviceRequest is not None:
        da = '%s %s %s %s' % (d1, d2, d3, d4)
        DeviceRequest.websocket.send(da.encode())


DeviceSk = RaspOp()
# DeviceSk.RaspSingIn(RaspDevAdd)


def index(request):
    # Hello World 显示
    # return HttpResponse("Hello World!!")
    # 第一次测试，输出显示本地数据
    # if request.method =="POST":
    #     name = request.POST.get('name',None)
    #     password = request.POST.get('password',None)
    #
    #     print('name Set:*', type(name),'**',str(name).strip(),'*',len(str(name)))
    #     if(TxtJudge(name) and TxtJudge(password)):
    #         # print('print Get:*',type(name),'**',password,'*')
    #         Testlist.append({'name':name,'password':password})
    #
    # return render(request,'NamePassTable.html',{'form':Testlist})
    # return render(request, "HelloShow.html",)
    # 第三次测试加入数据库
    if request.method == "POST":
        name = request.POST.get('name', None)
        password = request.POST.get('password', None)

        if TxtJudge(name) and TxtJudge(password):
            models.UserInfo.objects.create(user=name, pwd=password)
    user_list = models.UserInfo.objects.all()
    print(user_list)
    return render(request, 'NamePassTable.html', {'form': user_list})


def TxtJudge(tt):
    if tt is None:
        return False
    if str(tt).__len__() > 0:
        return True
    return False


def raspView(request):
    return render(request, 'RaspTest.html')


@require_websocket
def rasp(request):
    message = request.websocket.wait()
    request.websocket.send(message)


def WebSkView(request):
    return render(request, 'RaspCommSendClose.html')


@accept_websocket
def WebSk(request):
    if not request.is_websocket():
        try:
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'RaspCommSendClose.html')
    else:
        for message in request.websocket:
            print('WebSk:', message)
            if message == b'ConnSucc':
                request.websocket.send(str('请发送数据！').encode())
            else:
                request.websocket.send(message)


@accept_websocket
def NewWebSk(request):
    global DeviceRequest
    if not request.is_websocket():
        try:
            message = request.GET['message']
            return HttpResponse(message)
        except Exception as e:
            print('Error X:', str(e))
            return render(request, 'RaspCommSendClose.html')
    else:
        try:
            for message in request.websocket:
                print('WebSk:', message)
                if message is None:
                    return

                if message == b'ConnSucc':
                    request.websocket.send(str('请发送数据！').encode())
                    DeviceRequest = request
                    # print(request,DeviceRequest,type(request),type(request.websocket))
                    DeviceSk.GetLotCount()
                elif message == b'Disconnect':
                    print('Disconnect socket!')
                    DeviceSk.StopGetCount()
                    DeviceRequest = None
                else:
                    request.websocket.send(message)
        except Exception as e:
            print('WebSocket Error:', str(e))
    print("NewRaspSk End!")
