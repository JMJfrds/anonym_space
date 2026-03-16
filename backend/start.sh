#!/bin/sh

# Statik fayllarni yig'ish (agar build vaqtida yig'ilmagan bo'lsa)
python manage.py collectstatic --noinput

# Ma'lumotlar bazasini migratsiya qilish
python manage.py migrate --noinput

# Site ID 1 mavjudligini ta'minlash (allauth uchun kerak)
python manage.py shell -c "from django.contrib.sites.models import Site; Site.objects.get_or_create(id=1, defaults={'domain': 'anonym-space.pdpedu.uz', 'name': 'Anonym Space'})"

# Gunicorn serverini ishga tushirish
gunicorn core.wsgi:application --bind 0.0.0.0:8000
