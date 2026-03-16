#!/bin/sh

# Statik fayllarni yig'ish (agar build vaqtida yig'ilmagan bo'lsa)
python manage.py collectstatic --noinput

# Ma'lumotlar bazasini migratsiya qilish
python manage.py migrate --noinput

# Gunicorn serverini ishga tushirish
gunicorn core.wsgi:application --bind 0.0.0.0:8000
