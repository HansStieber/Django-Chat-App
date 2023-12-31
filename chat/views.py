from django.shortcuts import get_object_or_404, render, redirect
from .models import Chat, Message
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
@login_required(login_url='/login/')
def chatroom(request, chatId):
  currentChat = get_object_or_404(Chat, id=chatId)
  if request.method == 'POST':
    new_message = Message.objects.create(
      text=request.POST['textmessage'],
      chat=currentChat,
      author=request.user,
      )
    serialized_object = serializers.serialize('json', [ new_message, ])
    return JsonResponse(serialized_object[1:-1], safe=False)
  chatMessages = Message.objects.filter(chat__id=chatId)
  return render(request, 'chatroom/chatroom.html', {'messages': chatMessages, 'chatId': chatId, 'currentChat': currentChat})


def login_view(request):
  next = request.GET.get('next') or '/chat/'
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
    user_exists = False
    no_pw_match = False

    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('usernameRegister')
        password = request.POST.get('passwordRegister')
        passwordRepeat = request.POST.get('passwordRepeat')

        if User.objects.filter(username=username).exists():
            user_exists = True
            return render(request, 'register/register.html', {'userExists': user_exists})

        if password == passwordRepeat:
            User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            return redirect('/login/')
        else:
            no_pw_match = True

    return render(request, 'register/register.html', {'userExists': user_exists, 'noPwMatch': no_pw_match})




def user_logout(request):
    logout(request)
    return redirect('/login/')
  
 
@login_required(login_url='/login/')
def chat_overview(request):
    current_user = request.user
    chats = Chat.objects.filter(creator=current_user) | Chat.objects.filter(partners=current_user)
    chats = chats.distinct()
    users = User.objects.exclude(id=current_user.id)
    return render(request, 'chat_overview/chat_overview.html', {'chats': chats, 'users': users})


@login_required(login_url='/login/')
def create_chat(request):
  if request.method == 'POST':
    selected_partner_ids = request.POST.getlist('selected_partners')
    
    if not selected_partner_ids:
        return redirect('chat_overview')

    creator = request.user
    new_chat = Chat.objects.create(creator=creator)
    new_chat.partners.add(creator)

    for partner_id in selected_partner_ids:
        partner = get_user_model().objects.get(pk=partner_id)
        new_chat.partners.add(partner)

    return redirect('chatroom', chatId=new_chat.id)
  return redirect('chat_overview')