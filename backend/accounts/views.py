from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('nickname')
            messages.success(request, f'Hisob yaratildi! Endi kirishingiz mumkin.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from posts.models import Post, Reply


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