from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Post, Reply

from django.contrib.auth import get_user_model
User = get_user_model()


# Asosiy sahifa
class PostListView(ListView):
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'posts'
    ordering = ['-is_pinned', '-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Oxirgi 5 ta ro'yxatdan o'tgan foydalanuvchi
        context['recent_users'] = User.objects.exclude(id=self.request.user.id).order_by('-id')[:5]
        return context


# Post tafsilotlari
class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'


# JAVOB YOZISH (Buni klass tashqarisiga chiqardik, shunda u URL'da ishlaydi)
@login_required
def add_reply(request, post_id):
    last_owner_post = Post.objects.filter(author__role='owner', is_pinned=True).order_by('-created_at').first()

    # Check for restriction
    if request.user.role != 'owner' and last_owner_post:
        has_replied_to_owner = Reply.objects.filter(post=last_owner_post, author=request.user).exists()
        if not has_replied_to_owner and int(post_id) != last_owner_post.id:
            return redirect('post_detail', pk=last_owner_post.id)

    if request.method == "POST":
        post_obj = get_object_or_404(Post, id=post_id)  # post o'rniga post_obj deb nomladim adashmaslik uchun
        content_text = request.POST.get('content')

        if content_text:
            # MANA SHU YERNI DIQQAT BILAN YOZING:
            Reply.objects.create(
                post=post_obj,
                author=request.user,
                content=content_text,
                is_anonymous=(post_obj.post_type == 'personal')
            )

            # Ball qo'shish
            request.user.points += 5
            request.user.save()

            # Agar owner postiga javob bergan bo'lsa, uyga qaytarish
            if last_owner_post and post_obj.id == last_owner_post.id:
                return redirect('home')

    return redirect('post_detail', pk=post_id)


# Yangi post yaratish
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/post_form.html'
    fields = ['post_type', 'content', 'source_name', 'lesson', 'is_anonymous']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user

        # AGAR POSTNI OWNER YOZAYOTGAN BO'LSA:
        if self.request.user.role == 'owner':
            form.instance.is_pinned = True  # Avtomatik pin qilinadi

        return super().form_valid(form)

    # Dispatch qismini ham qo'shib qo'ying (avvalgi xabardagidek)
    def dispatch(self, request, *args, **kwargs):
        last_owner_post = Post.objects.filter(author__role='owner', is_pinned=True).order_by('-created_at').first()
        if last_owner_post and request.user.role != 'owner':  # Ownerning o'zi cheklovga tushmasligi kerak
            has_replied = Reply.objects.filter(post=last_owner_post, author=request.user).exists()
            if not has_replied:
                return redirect('post_detail', pk=last_owner_post.id)
        return super().dispatch(request, *args, **kwargs)