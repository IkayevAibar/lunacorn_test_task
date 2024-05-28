# Электронный журнал для оценок

## Установка и запуск проекта

1. Клонируйте репозиторий:

   ```bash
   git clone lunacorn_test_task
   cd lunacorn_test_task
   ```
2. Создайте виртуальное окружение и активируйте его:

   ```
   python -m venv venv
   source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
   ```
3. Установите зависимости:

   ```
   pip install -r requirements.txt
   ```
4. Запустите сервер:

   ```
   uvicorn main:app --reload
   ```
5. Документация:

   [http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/)
