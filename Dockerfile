# Указываем базовый образ
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы приложения
COPY . /app

# Устанавливаем зависимости
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "main_bot.py"]