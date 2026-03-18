import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a superuser if it does not exist using environment variables'

    def handle(self, *args, **options):
        User = get_user_model()
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        nickname = os.environ.get('DJANGO_SUPERUSER_NICKNAME', 'Admin')

        if not email or not password:
            self.stdout.write(self.style.WARNING('DJANGO_SUPERUSER_EMAIL yoki DJANGO_SUPERUSER_PASSWORD topilmadi. Superuser yaratilmadi.'))
            return

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email,
                nickname=nickname,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Superuser muvaffaqiyatli yaratildi: {email}'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser allaqachon mavjud.'))
