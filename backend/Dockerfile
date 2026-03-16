# Pythonning rasmiy obrazidan foydalanamiz
FROM python:3.10-slim

# Terminalda loglarni ko'rib turish uchun
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Ishchi papkani yaratamiz
WORKDIR /code

# Kutubxonalarni o'rnatamiz
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha fayllarini ko'chiramiz
COPY . /code/

# 8000-portni ochamiz
EXPOSE 8000

# Serverni Gunicorn orqali yurgizamiz
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]