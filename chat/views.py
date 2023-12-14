from django.shortcuts import get_object_or_404, render
from .models import Chat, Message

# Create your views here.
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
