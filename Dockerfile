# Используем официальный легковесный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем переменные окружения
# PYTHONDONTWRITEBYTECODE: Запрещает Python писать файлы .pyc
# PYTHONUNBUFFERED: Вывод Python идет напрямую в терминал без буферизации
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код и статику
COPY src/ ./src/
COPY static/ ./static/

# Открываем порт, на котором работает FastAPI
EXPOSE 8000

# Команда для запуска приложения
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
