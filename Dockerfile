# Для Dockerfile:

# Какой язык программирования? (FROM)

# Какие библиотеки нужны системе (gcc, libpq)? (RUN apt-get)

# Какие библиотеки нужны языку (Flask, Stripe)? (COPY req.txt + RUN pip)

# Где лежит код? (COPY . .)

# Какой командой запускать? (CMD)

# 1. Используем официальный образ Python (легковесная версия)
FROM python:3.12-slim

# Отключаем буферизацию, чтобы логи выводились сразу
ENV PYTHONUNBUFFERED=1

# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 3. Устанавливаем системные зависимости (нужны для psycopg2 и компиляции)
# Это важно для работы PostgreSQL и некоторых библиотек Python
RUN apt-get update && apt-get install -y \
gcc \
libpq-dev \
&& rm -rf /var/lib/apt/lists/*

# 4. Копируем файл с зависимостями
COPY requirements.txt .

# 5. Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt && pip install gunicorn stripe

# 6. Копируем весь остальной код проекта в контейнер
COPY . .

# 7. Открываем порт 5000 (стандартный для Flask)
EXPOSE 5000

# 8. Команда для запуска приложения
# Используем gunicorn для продакшн-запуска (надо будет добавить его в requirements)
# Или пока что обычный python run.py для тестов
# Добавляем python nuke_db.py в начало
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:10000", "run:app"]