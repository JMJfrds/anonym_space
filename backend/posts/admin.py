from django.contrib import admin
from .models import Post, Reply


# Javoblarni postning ichida ham ko'rish imkoniyati
class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 0  # Bo'sh qatorlar chiqmasligi uchun


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Ro'yxatda ko'rinadigan ustunlar
    list_display = ('id', 'author', 'post_type', 'is_anonymous', 'is_pinned', 'created_at')

    # Filtrlash imkoniyati
    list_filter = ('post_type', 'is_anonymous', 'is_pinned', 'created_at')

    # Qidiruv
    search_fields = ('content', 'author__nickname')

    # Postning ichida unga yozilgan javoblarni ko'rsatish
    inlines = [ReplyInline]


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'is_anonymous', 'created_at')
    list_filter = ('is_anonymous', 'created_at')
    search_fields = ('content', 'author__nickname')