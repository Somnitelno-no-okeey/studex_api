# StudEx API

Полнофункциональный веб-сервис для оценки учебных дисциплин, позволяющий студентам оставлять отзывы и оценки по предметам, а администраторам управлять системой.

## 🚀 Возможности

### Для студентов
- **Аутентификация**: регистрация, вход в систему, восстановление пароля
- **Главная страница**: просмотр списка дисциплин с поиском и фильтрацией
- **Страница дисциплины**: детальная информация с отзывами и оценками
- **Личный кабинет**: управление профилем и авторизация
- **Отзывы**: создание и редактирование отзывов о дисциплинах

### Для администраторов
- **Управление пользователями**: контроль ролей и доступа
- **Управление дисциплинами**: добавление и настройка предметов
- **Настройка критериев**: конфигурация параметров оценивания
- **Управление преподавателями**: добавление и редактирование данных
- **Модерация**: контроль отзывов и расчет рейтингов

## 🛠 Технологии

- **Backend**: Django REST Framework
- **База данных**: PostgreSQL
- **Аутентификация**: JWT (Simple JWT)
- **API документация**: drf-spectacular (Swagger/OpenAPI)
- **Email**: SMTP (настраивается через .env)

## 📋 Установка и запуск

### Предварительные требования
- Python 3.8+
- pip
- Git

### Быстрый старт

1. **Клонирование репозитория**
   ```bash
   git clone <repository-url>
   cd studex_api
   ```

2. **Создание виртуального окружения**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate     # Windows
   ```

3. **Установка зависимостей**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройка переменных окружения**
   ```bash
   cp .env.example .env
   ```
   Отредактируйте `.env` файл, добавив ваши настройки:
   ```
   SECRET_KEY=your_secret_key_here
   DEBUG=True
   
   # База данных PostgreSQL
   DB_NAME=studex_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   
   # Email настройки
   EMAIL_HOST=smtp.yandex.ru
   EMAIL_PORT=465
   EMAIL_USE_SSL=True
   EMAIL_HOST_USER=your_email@example.com
   EMAIL_HOST_PASSWORD=your_app_password
   ```

5. **Применение миграций**
   ```bash
   python manage.py migrate
   ```

6. **Создание суперпользователя**
   ```bash
   python manage.py createsuperuser
   ```

7. **Запуск сервера**
   ```bash
   python manage.py runserver
   ```

Сервер будет доступен по адресу: `http://127.0.0.1:8000/`

## 📖 API Документация

После запуска сервера API документация доступна по адресам:
- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- ReDoc: `http://127.0.0.1:8000/api/redoc/`
- OpenAPI Schema: `http://127.0.0.1:8000/api/schema/`

## 🔧 Основные эндпоинты

### Аутентификация (`/auth/`)
- `POST /auth/registration/` - Регистрация
- `POST /auth/login/` - Вход в систему
- `POST /auth/logout/` - Выход из системы
- `POST /auth/refresh/` - Обновление токена
- `POST /auth/verify/` - Подтверждение аккаунта
- `POST /auth/verify/resend-code/` - Повторная отправка кода
- `POST /auth/password-reset/request/` - Запрос восстановления пароля
- `POST /auth/password-reset/verify/` - Проверка кода восстановления
- `POST /auth/password-reset/confirm/` - Подтверждение нового пароля

### Пользователи (`/auth/`)
- `GET /auth/profile/` - Профиль пользователя
- `PUT /auth/update-fullname/` - Обновление ФИО
- `PUT /auth/change-password/` - Смена пароля

### Дисциплины (`/disciplines/`)
- `GET /disciplines/` - Список дисциплин
- `GET /disciplines/{id}/` - Детали дисциплины
- `GET /disciplines/modules/` - Список модулей

### Отзывы (`/disciplines/{discipline_id}/reviews/`)
- `GET /disciplines/{discipline_id}/reviews/` - Список отзывов по дисциплине
- `POST /disciplines/{discipline_id}/reviews/` - Создание отзыва
- `GET /disciplines/{discipline_id}/reviews/{id}/` - Детали отзыва
- `PUT /disciplines/{discipline_id}/reviews/{id}/update/` - Обновление отзыва
- `DELETE /disciplines/{discipline_id}/reviews/{id}/delete/` - Удаление отзыва
- `GET /disciplines/{discipline_id}/user_review/` - Отзыв текущего пользователя

## 🔐 Аутентификация

Система использует JWT токены с механизмом refresh token в HTTP-only куки:
- Access token возвращается в теле ответа
- Refresh token хранится в защищенных куки
- Автоматическое обновление токенов

## 🗂 Структура проекта

```
studex_api/
├── apps/
│   ├── accounts/       # Модуль пользователей и аутентификации
│   ├── common/         # Базовые классы и утилиты
│   ├── disciplines/    # Дисциплины, модули, преподаватели
│   └── reviews/        # Модуль отзывов и оценок
├── core/              # Настройки Django
├── requirements.txt   # Зависимости
├── manage.py         # Django CLI
└── README.md         # Документация
```

## 🚀 Развертывание

### Production настройки
1. Установите `DEBUG=False` в `.env`
2. Настройте `ALLOWED_HOSTS`
3. Используйте PostgreSQL в production
4. Настройте статические файлы и медиа
5. Используйте веб-сервер (nginx + gunicorn)

### Docker (опционально)
```bash
docker build -t studex-api .
docker run -p 8000:8000 studex-api
```

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для фичи (`git checkout -b feature/amazing-feature`)
3. Закоммитьте изменения (`git commit -m 'Add amazing feature'`)
4. Запушьте ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📝 Лицензия

Информация о лицензии будет добавлена позже.

## 📞 Поддержка

Если у вас есть вопросы или проблемы:
- Создайте Issue в репозитории
- Свяжитесь с командой разработки

---

**StudEx API** - современное решение для оценки учебных дисциплин 🎓