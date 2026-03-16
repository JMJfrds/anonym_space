# Pythonning rasmiy obrazidan foydalanamiz
FROM python:3.10-slim

# Terminalda loglarni ko'rib turish uchun
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Ishchi papkani yaratamiz
WORKDIR /code

# Kutubxonalarni o'rnatamiz
COPY backend/requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha fayllarini ko'chiramiz
COPY backend/ /code/

# Statik fayllar uchun papka yaratamiz
RUN mkdir -p /code/staticfiles

# start.sh ga ruxsat beramiz
RUN chmod +x /code/start.sh

# 8000-portni ochamiz
EXPOSE 8000

# Serverni start.sh orqali yurgizamiz
CMD ["/code/start.sh"]