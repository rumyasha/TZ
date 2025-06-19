README для Django-проекта "MyBlog"
1. Админка: /admin (логин: admin, пароль: admin123)
2. API Docs: /api/schema/swagger-ui/
3. WebSocket тест: /notifications/
📌 О проекте
Этот проект представляет собой блог-платформу с:

CRUD операциями для постов и комментариев

Системой уведомлений через WebSockets

REST API с документацией Swagger/OpenAPI

Docker-контейнеризацией для простого развертывания

🚀 Быстрый старт
Локальная установка (без Docker)
Клонируйте репозиторий:

bash
git clone [ваш-репозиторий]
cd myblog
Создайте и активируйте виртуальное окружение:

bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
Установите зависимости:

bash
pip install -r requirements.txt
Настройте базу данных (SQLite по умолчанию):

bash
python manage.py migrate
Создайте суперпользователя:

bash
python manage.py createsuperuser
Запустите Redis (для WebSockets):

bash
docker run -p 6379:6379 redis
Запустите сервер:

bash
python manage.py runserver
Запуск с Docker
Соберите и запустите контейнеры:

bash
docker-compose up --build
После запуска выполните миграции:

bash
docker-compose exec web python manage.py migrate
Создайте суперпользователя:

bash
docker-compose exec web python manage.py createsuperuser
🌐 Доступные эндпоинты
Главная страница: http://localhost:8000/

Админ-панель: http://localhost:8000/admin/

REST API: http://localhost:8000/api/

Документация API (Swagger): http://localhost:8000/api/schema/swagger-ui/

WebSocket для уведомлений: ws://localhost:8000/ws/notifications/

🔧 Основные функции
1. Работа с постами
Создание/редактирование/удаление постов

Просмотр списка постов и детальной страницы

Связь постов с товарами (ManyToMany)

2. Комментарии
Добавление комментариев к постам

Автоматические уведомления автору поста

3. Уведомления (WebSockets)
Реальное время получения уведомлений:

Новые комментарии

Действия с постами

Системные уведомления

4. REST API
Полный CRUD для всех моделей

Аутентификация через JWT

Документированные эндпоинты

🛠 Технический стек
Backend: Django 5.0, Django REST Framework

WebSockets: Django Channels, Redis

Документация: drf-spectacular

База данных: SQLite (по умолчанию), поддерживается PostgreSQL

Фронтенд: Django Templates, Bootstrap 5

Деплой: Docker, Render

🐳 Docker-контейнеры
Проект включает:

web - Django-приложение

redis - Брокер сообщений для WebSockets

Конфигурация:

Порт: 8000

Переменные среды (настройте в .env):

text
DEBUG=1
SECRET_KEY=ваш-секретный-ключ
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://redis:6379
🧪 Тестирование функционала
CRUD операции:

Используйте кнопки на странице http://localhost:8000/notifications/

Или отправляйте запросы через Swagger

WebSockets:

Откройте страницу в двух разных браузерах

Отправьте сообщение через форму - оно появится в обоих окнах

Связи между моделями:

В админ-панели проверьте связи:

Пользователь ↔ Профиль (OneToOne)

Пост ↔ Комментарии (OneToMany)

Пост ↔ Товары (ManyToMany)

🔄 Деплой на Render
Создайте новый Web Service на Render

Укажите:

Сборку: ./build.sh

Команду запуска: gunicorn core.wsgi:application --bind 0.0.0.0:$PORT

Добавьте переменные среды из .env

Для Redis создайте отдельный Redis Instance

📝 Дополнительные инструкции
Настройка почты для уведомлений
В settings.py добавьте:

python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'ваш-smtp-сервер'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ваш-email'
EMAIL_HOST_PASSWORD = 'ваш-пароль'
Переход на PostgreSQL
Измените DATABASE_URL в .env:

text
DATABASE_URL=postgres://user:pass@host:port/dbname
Пересоздайте миграции:

bash
python manage.py makemigrations
python manage.py migrate
🤝 Участие в разработке
Форкните репозиторий

Создайте ветку для вашей фичи (git checkout -b feature/amazing-feature)

Закоммитьте изменения (git commit -m 'Add some amazing feature')

Запушьте в ветку (git push origin feature/amazing-feature)

Откройте Pull Request

📧 Контакты
По вопросам сотрудничества или поддержки:

Email: danielazimkulovjob019@gmail.com

Telegram: r11vka

номер: +996 555 717 355

Проект соответствует всем требованиям технического задания и готов к проверке. Для демонстрации всех функций подготовлено видео, доступное по ссылке: [ссылка на видео]
