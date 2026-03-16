from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth import logout, login
from posts.models import Post, Reply
import hashlib
import hmac
import time
from django.conf import settings
from accounts.models import User

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Hisob yaratildi! Endi kirishingiz mumkin.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def profile_view(request):
    # Foydalanuvchining o'z postlari
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    # Uning postlariga kelgan javoblar
    replies_to_my_posts = Reply.objects.filter(post__author=request.user).exclude(author=request.user)

    return render(request, 'accounts/profile.html', {
        'user_posts': user_posts,
        'replies_to_my_posts': replies_to_my_posts,
    })

def logout_view(request):
    logout(request)
    return redirect('login')

def telegram_login_callback(request):
    """
    Telegram Login Widget orqali kelgan ma'lumotlarni tekshiradi va
    foydalanuvchini tizimga kiritib yuboradi.
    """
    url_params = request.GET.dict()
    
    if not url_params or 'hash' not in url_params:
        messages.error(request, "Telegram orqali kirishda xatolik yuz berdi.")
        return redirect('login')

    received_hash = url_params.pop('hash')
    
    # Ma'lumotlarni alifbo tartibida saralaymiz
    data_check_arr = []
    for key, value in sorted(url_params.items()):
        data_check_arr.append(f'{key}={value}')
    
    data_check_string = '\n'.join(data_check_arr)
    
    # Bot token yordamida secret key yaratamiz
    bot_token = settings.SOCIALACCOUNT_PROVIDERS['telegram']['APP']['secret']
    secret_key = hashlib.sha256(bot_token.encode('utf-8')).digest()
    
    # Yaratilgan secret key va ma'lumotlar satri yordamida hash hisoblaymiz
    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # Hashlarni solishtiramiz
    if calculated_hash != received_hash:
        messages.error(request, "Telegram ma'lumotlari tasdiqlanmadi (Hash xato).")
        return redirect('login')
        
    # Vaqtni tekshiramiz (eski so'rovlarni o'tkazib yubormaslik uchun)
    if time.time() - int(url_params.get('auth_date', 0)) > 86400:
        messages.error(request, "Telegram sessiyasi eskirgan. Qaytadan urinib ko'ring.")
        return redirect('login')
        
    # Foydalanuvchi ma'lumotlarini ajratib olamiz
    telegram_id = url_params.get('id')
    first_name = url_params.get('first_name', '')
    last_name = url_params.get('last_name', '')
    username = url_params.get('username', f'tg_user_{telegram_id}')
    
    # Baza dan qidiramiz yoki yaratamiz
    # CustomUser (accounts.User) da 'username' yo'q, email ishlatamiz
    email = f"{telegram_id}@telegram.local"
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
            'nickname': username,
        }
    )
    
    # Foydalanuvchini tizimga kiritamiz
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    
    return redirect('home')