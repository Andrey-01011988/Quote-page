# Quote Project - Цитатник

Django проект для отображения случайных цитат из фильмов, книг и других источников.

## 🚀 Возможности

- Просмотр случайных цитат с учетом веса
- Добавление новых цитат
- Лайки и дизлайки цитат
- Топ-10 самых популярных цитат
- Административная панель для управления

## 🌐 Демо версия

Проект развернут по адресу:  
**https://andrey88.pythonanywhere.com/**

## 📦 Быстрый запуск

```bash
git clone <your-repo-url>
cd Quotes_page
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
cp .env.example .env
# Отредактируйте .env файл
python manage.py migrate
python manage.py runserver
```

## 🔐 Настройка окружения

1. Скопируйте `.env.example` в `.env`
2. Сгенерируйте SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
3. Настройте параметры базы данных в `.env`

## 🛠️ Основные команды

```bash
python manage.py runserver      # Запуск сервера
python manage.py migrate        # Миграции БД
python manage.py seed_quotes    # Тестовые данные
python manage.py createsuperuser # Админка
```

## 📊 Административная панель

Доступна по адресу: `/admin`  
- Управление цитатами и источниками
- Редактирование веса цитат
- Просмотр статистики

---

**Приятного использования!** 🎉
```
