from django.shortcuts import get_object_or_404, render, redirect
from .models import Chat, Message
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
@login_required(login_url='/login/')
def index(request, chatId):
  currentChat = get_object_or_404(Chat, id=chatId)
  if request.method == 'POST':
    new_message = Message.objects.create(
      text=request.POST['textmessage'],
      chat=currentChat,
      author=request.user,
      receiver=request.user, 
      )
    serialized_object = serializers.serialize('json', [ new_message, ])
    return JsonResponse(serialized_object[1:-1], safe=False)
  chatMessages = Message.objects.filter(chat__id=chatId)
  return render(request, 'chat/index.html', {'messages': chatMessages, 'chatId': chatId})


def login_view(request):
  next = request.GET.get('next') or '/select_chatpartner/'
  if request.method == 'POST':
    user = authenticate(
      username=request.POST.get('usernameLogin'),
      password=request.POST.get('passwordLogin')
      ) 
    if user:
      login(request, user)
      return redirect(request.POST.get('next'))
    else:
      return render(request, 'auth/login.html', {'wrongPassword': True})
  return render(request, 'auth/login.html', {'next': next})


def register_view(request):
  if request.method == 'POST':
      first_name = request.POST.get('firstname')
      last_name = request.POST.get('lastname')
      username = request.POST.get('usernameRegister')
      password = request.POST.get('passwordRegister')
      passwordRepeat = request.POST.get('passwordRepeat')
      if password == passwordRepeat:
        User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        return redirect('/login/')
      else:
        return render(request, 'register/register.html', {'noPwMatch': True})
  return render(request, 'register/register.html')


def user_logout(request):
    logout(request)
    return redirect('/login/')
  
 
@login_required(login_url='/login/') 
def select_chat(request):
  chats = Chat.objects.all()
  return render(request, 'select_chatpartner/select.html', {'chats': chats})


@login_required(login_url='/login/')
def create_chat(request):
    creator = request.user
    partner = get_user_model().objects.get(pk=request.POST.get('partner_id'))  # Beispiel für den Partner

    new_chat = Chat.objects.create(
        creator=creator,
        partner=partner
    )
    return redirect('chat_index', chatId=new_chat.id)