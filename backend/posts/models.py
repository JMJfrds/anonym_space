from django.db import models
from django.conf import settings
from better_profanity import profanity


class Post(models.Model):
    POST_TYPES = (
        ('normal', 'Oddiy savol'),
        ('personal', 'Shaxsiy savol'),
        ('learning', 'O‘rganish posti'),
        ('thought', 'Fikr posti'),
    )

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=15, choices=POST_TYPES)
    content = models.TextField()

    # "Learning Post" uchun maxsus maydonlar
    source_name = models.CharField(max_length=255, null=True, blank=True)
    lesson = models.TextField(null=True, blank=True)

    is_anonymous = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False) # Owner postlari uchun
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Matnni yomon so'zlardan tozalash
        self.content = profanity.censor(self.content)

        if self.post_type == 'personal':
            self.is_anonymous = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.author.nickname} - {self.post_type}"

class Reply(models.Model):
    post = models.ForeignKey(Post, related_name='replies', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.post.post_type == 'personal':
            self.is_anonymous = True
        super().save(*args, **kwargs)

