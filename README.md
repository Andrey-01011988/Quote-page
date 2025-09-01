
# Quote Project - Цитатник

Django проект для отображения случайных цитат из фильмов, книг и других источников.

## 🚀 Возможности

- Просмотр случайных цитат с учетом веса
- Добавление новых цитат
- Лайки и дизлайки цитат
- Топ-10 самых популярных цитат
- Административная панель для управления контентом
- Ограничение: не более 3 цитат на один источник

## 🛠️ Технологии

- Python 3.12
- Django 5.1
- SQLite (разработка) / MySQL (продакшен)
- HTML/CSS/JavaScript

## 📦 Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <your-repo-url>
cd Quotes_page
```

### 2. Создание виртуального окружения

```bash
python -m venv .venv
```

### 3. Активация виртуального окружения

**Linux/Mac:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

### 4. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 5. Настройка базы данных

```bash
python manage.py migrate
```

### 6. Заполнение базы тестовыми данными (опционально)

```bash
python manage.py seed_quotes
```

### 7. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 8. Запуск сервера разработки

```bash
python manage.py runserver
```

Приложение будет доступно по адресу: http://127.0.0.1:8000

## 📁 Структура проекта

```
Quotes_page/
├── quote_project/     # Настройки Django проекта
├── quotes/           # Основное приложение
│   ├── models.py     # Модели данных
│   ├── views.py      # Представления
│   ├── urls.py       # Маршруты
│   ├── forms.py      # Формы
│   ├── templates/    # Шаблоны
│   └── management/   # Кастомные команды
├── .venv/           # Виртуальное окружение
├── requirements.txt # Зависимости проекта
└── manage.py        # Управление Django
```

## 🎯 Основные команды

```bash
# Запуск сервера разработки
python manage.py runserver

# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Запуск тестов
python manage.py test

# Заполнение базы тестовыми данными
python manage.py seed_quotes

# Доступ к админке
python manage.py createsuperuser
```

## 🌐 Деплой на PythonAnywhere

### 1. Подготовка к деплою

```bash
# Соберите статические файлы
python manage.py collectstatic

# Создайте requirements.txt для продакшена
echo "mysqlclient==2.2.0" >> requirements.txt
```

### 2. Настройка на PythonAnywhere

1. Создайте аккаунт на [pythonanywhere.com](https://www.pythonanywhere.com)
2. Создайте MySQL базу данных через панель управления
3. Загрузите код через Git или ZIP архив
4. Настройте virtualenv указав путь к `.venv`
5. Обновите настройки в `settings.py` для production
6. Настройте WSGI конфигурацию
7. Запустите миграции: `python manage.py migrate`

### 3. Production настройки

В `settings.py` убедитесь, что есть:

```python
DEBUG = False
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']
STATIC_ROOT = '/home/yourusername/Quotes_page/staticfiles'
```

## 📊 Административная панель

Админка доступна по адресу: `/admin`
- Управление цитатами и источниками
- Редактирование веса цитат
- Просмотр статистики (лайки, просмотры)

## 🔧 Кастомные команды

### Заполнение базы тестовыми данными

```bash
python manage.py seed_quotes
```

Добавляет 30 тестовых цитат от различных авторов и произведений.

## ⚙️ Настройки разработки

Проект использует SQLite для разработки и MySQL для продакшена. 
Настройки автоматически определяют окружение.

## 🤝 Разработка

### Добавление новых функций

1. Создайте миграции для моделей
2. Добавьте представления в `views.py`
3. Зарегистрируйте маршруты в `urls.py`
4. Создайте шаблоны в `templates/quotes/`

## 📝 Лицензия

MIT License

## 🆘 Поддержка

При возникновении проблем:
1. Проверьте активацию виртуального окружения
2. Убедитесь, что все зависимости установлены
3. Проверьте применение миграций
4. Посмотрите логи Django для диагностики ошибок

---

**Приятного использования!** 🎉
```