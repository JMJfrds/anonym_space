from .models import Message

def unread_messages_count(request):
    if request.user.is_authenticated:
        # Foydalanuvchiga kelgan, lekin hali o'qilmagan (is_read=False) xabarlar soni
        count = Message.objects.filter(receiver=request.user, is_read=False).count()
        return {'unread_count': count}
    return {'unread_count': 0}