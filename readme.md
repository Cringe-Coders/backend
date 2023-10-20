## Запуск бэкенда

В первый запуск проекта:
1. `python -m venv venv`
2. `venv/Scripts/Activate.ps1`
3. `pip install -r requirements.txt`

Все последующие запуски проекта (терминале слева есть (venv)):
1. Перейти в /backend `cd backend`
2. `python manage.py makemigrations`
3. `python manage.py migrate`
4. `python manage.py runserver`

Все эндпоинты находятся в `swagger.yml`