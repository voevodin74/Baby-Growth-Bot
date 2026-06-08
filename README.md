# Baby Growth Bot

Telegram-бот для родителей, который на основе даты рождения ребенка формирует персональный календарь скачков развития и присылает уведомления о предстоящих этапах роста и развития.

## Возможности

- Регистрация ребенка
- Выбор даты рождения через встроенный календарь
- Автоматический расчет скачков развития
- Просмотр ближайших событий
- Изменение даты рождения
- Удаление данных ребенка
- Уведомления в Telegram за 1 день до скачка

## Стек

- Python 3.9.5
- Aiogram 3
- APScheduler
- Docker
- JSON Storage

---

## Установка

### Клонирование репозитория

```bash
git clone https://github.com/voevodin74/baby-growth-bot.git

cd baby-growth-bot
```

### Создание файла .env

Создайте файл:

```bash
nano .env
```

Содержимое:

```env
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

### Создание директории пользователей

```bash
mkdir -p users
```

### Сборка контейнера

```bash
docker compose build
```

### Запуск контейнера

```bash
docker compose up -d
```

### Просмотр логов

```bash
docker compose logs -f
```

---

## Первый запуск

1. Отправьте боту команду:

```text
/start
```

2. Введите имя ребенка.

3. Выберите дату рождения через встроенный календарь.

4. Бот автоматически сформирует персональный календарь скачков развития.

5. За день до начала скачка вы получите уведомление.

---

## Обновление проекта

Получить последние изменения:

```bash
git pull
```

Полностью пересобрать контейнер:

```bash
docker compose down

docker compose build --no-cache

docker compose up -d
```

Проверить работу:

```bash
docker compose logs -f
```

---

## Структура проекта

```text
baby-growth-bot/

├── bot.py
├── generator.py
├── scheduler.py
├── storage.py
├── calendar_widget.py
│
├── growth_spurts.json
│
├── users/
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env
```

---
