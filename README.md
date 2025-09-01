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

### 5. Настройка окружения

Скопируйте файл `.env.example` в `.env` и настройте параметры:

```bash
cp .env.example .env
```

Отредактируйте файл `.env`, заменив значения на свои (см. раздел "Настройка окружения" ниже).

### 6. Настройка базы данных

```bash
python manage.py migrate
```

### 7. Заполнение базы тестовыми данными (опционально)

```bash
python manage.py seed_quotes
```

### 8. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 9. Запуск сервера разработки

```bash
python manage.py runserver
```

Приложение будет доступно по адресу: http://127.0.0.1:8000

## 🔐 Настройка окружения

### 1. Создание файла .env

Скопируйте файл `.env.example` в `.env` и настройте параметры:

```bash
cp .env.example .env
```

### 2. Генерация SECRET_KEY

Сгенерируйте безопасный секретный ключ для Django:

**Способ 1: Используя Django**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Способ 2: Используя Python**
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

**Способ 3: Онлайн генератор**
Используйте любой онлайн генератор Django secret key.

### 3. Настройка .env файла

Отредактируйте файл `.env` и замените значения:

```env
DEBUG=False
SECRET_KEY=ваш-сгенерированный-секретный-ключ-здесь
ALLOWED_HOSTS=yourusername.pythonanywhere.com
```

### 4. Настройка для PythonAnywhere

Для развертывания на PythonAnywhere обновите настройки базы данных в `.env`:

```env
# Комментируйте SQLite и раскомментируйте MySQL настройки
# DATABASE_ENGINE=django.db.backends.sqlite3
# DATABASE_NAME=db.sqlite3

DATABASE_ENGINE=django.db.backends.mysql
DATABASE_NAME=yourusername$quotes_db
DATABASE_USER=yourusername
DATABASE_PASSWORD=ваш-пароль-mysql
DATABASE_HOST=yourusername.mysql.pythonanywhere-services.com
DATABASE_PORT=3306
```

### 5. Установка python-dotenv

Убедитесь, что установлен пакет для работы с .env файлами:

```bash
pip install python-dotenv
```

Добавьте в `requirements.txt`:
```txt
python-dotenv==1.0.0
```

### ⚠️ Важные замечания

1. **Никогда не коммитьте `.env` файл в Git** - добавьте его в `.gitignore`
2. На продакшене (PythonAnywhere) установите `DEBUG=False`
3. Используйте разные SECRET_KEY для разработки и продакшена
4. Регулярно обновляйте SECRET_KEY в продакшен окружении

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
├── .env.example      # Пример файла окружения
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

# Убедитесь, что установлен python-dotenv
pip install python-dotenv
```

### 2. Настройка на PythonAnywhere

1. Создайте аккаунт на [pythonanywhere.com](https://www.pythonanywhere.com)
2. Создайте MySQL базу данных через панель управления
3. Загрузите код через Git или ZIP архив
4. Настройте virtualenv указав путь к `.venv`
5. Создайте файл `.env` с настройками для production
6. Настройте WSGI конфигурацию
7. Запустите миграции: `python manage.py migrate`

### 3. Production настройки

В `.env` файле убедитесь, что есть:

```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourusername.pythonanywhere.com
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
Настройки автоматически определяют окружение через переменные `.env` файла.

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
4. Убедитесь, что файл `.env` правильно настроен
5. Посмотрите логи Django для диагностики ошибок

---

**Приятного использования!** 🎉