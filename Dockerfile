
FROM python:3.12

WORKDIR /app

COPY . /app

# Установка зависимостей
RUN pip install -r requirements.txt

# Команда для запуска бота
CMD ["python", "./bot.py"]
