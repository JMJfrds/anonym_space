from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message
from django.contrib.auth import get_user_model
from posts.models import Reply
from datetime import date

User = get_user_model()


@login_required
def chat_dashboard(request, user_id=None):
    # 1. Barcha foydalanuvchilar (suhbatdoshlar ro'yxati uchun)
    all_users = User.objects.exclude(id=request.user.id)

    recipient = None
    messages = []

    # 2. Agar suhbatdosh tanlangan bo'lsa
    if user_id:
        recipient = get_object_or_404(User, id=user_id)

        # XABAR YUBORISH (POST so'rovi shu yerda ishlaydi)
        if request.method == 'POST':
            text = request.POST.get('text')
            # Bugun javob yozganini tekshirish (ixtiyoriy, lekin siz so'ragan shart)
            has_replied = Reply.objects.filter(author=request.user, created_at__date=date.today()).exists()

            if text and has_replied:
                Message.objects.create(
                    sender=request.user,
                    receiver=recipient,
                    text=text
                )
                # Xabar ketgandan keyin sahifani yangilab, xabarni ko'rsatamiz
                return redirect('chat_room', user_id=user_id)
            elif text and not has_replied:
                messages.error(request, "Bugun biron bir postga javob yozmaguningizcha chatdan foydalana olmaysiz!")

        # Xabarlar tarixini olish
        messages = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=recipient)) |
            (Q(sender=recipient) & Q(receiver=request.user))
        ).order_by('created_at')

    # Bugun javob yozganlik holati
    has_replied_today = Reply.objects.filter(author=request.user, created_at__date=date.today()).exists()

    if recipient:
        # Menga kelgan xabarlarni o'qildi deb belgilash
        Message.objects.filter(sender=recipient, receiver=request.user, is_read=False).update(is_read=True)


    return render(request, 'chat/chat_main.html', {
        'all_users': all_users,
        'recipient': recipient,
        'chat_messages': messages,
        'has_replied_today': has_replied_today
    })
