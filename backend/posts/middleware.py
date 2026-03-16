from django.shortcuts import redirect
from django.urls import reverse
from .models import Post, Reply

class OwnerPostRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Owner, Admin yoki Login qilmaganlar uchun yo'l ochiq
        if not request.user.is_authenticated or request.user.is_staff or request.user.role == 'owner':
            return self.get_response(request)

        # 2. Eng oxirgi qadalgan Owner postini topamiz
        last_owner_post = Post.objects.filter(author__role='owner', is_pinned=True).order_by('-created_at').first()

        if last_owner_post:
            # 3. Foydalanuvchi javob berganini tekshiramiz
            has_replied = Reply.objects.filter(post=last_owner_post, author=request.user).exists()

            if not has_replied:
                # 4. Ruxsat berilgan manzillarni aniqlaymiz
                detail_url = reverse('post_detail', kwargs={'pk': last_owner_post.id})
                reply_url = reverse('add_reply', kwargs={'post_id': last_owner_post.id})
                logout_url = reverse('logout')

                # Hozirgi manzilni tekshiramiz (sleshlar bilan muammo bo'lmasligi uchun)
                current_path = request.path
                if current_path not in [detail_url, reply_url, logout_url]:
                    return redirect(detail_url)

        return self.get_response(request)