from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Chat, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url='/login/')
def index(request):
  chatId = 4
  myChat = get_object_or_404(Chat, id=chatId)
  if request.method == 'POST':
    Message.objects.create(
      text=request.POST['textmessage'],
      chat=myChat,
      author=request.user,
      receiver=request.user, 
      )
  chatMessages = Message.objects.filter(chat__id=chatId)
  return render(request, 'chat/index.html', {'messages': chatMessages})


def login_view(request):
  if request.method == 'POST':
    user = authenticate(
      username=request.POST.get('username'),
      password=request.POST.get('password')
      )
    if user:
      login(request, user)
      return HttpResponseRedirect('/chat/')
    else:
      return render(request, 'auth/login.html', {'wrongPassword': True})
  return render(request, 'auth/login.html')


def register_view(request):
  if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')
      passwordRepeat = request.POST.get('passwordRepeat')
      if password == passwordRepeat:
        User.objects.create_user(username=username, password=password)
        return HttpResponseRedirect('/login/')
      else:
        return render(request, 'register/register.html', {'noPwMatch': True})
  return render(request, 'register/register.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')