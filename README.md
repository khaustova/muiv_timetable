### 1. О приложении ###
Приложение позволяет загружать файлы с расписанием в формате JSON, выгруженные из информационной системы "Сириус" Московского университета им. Витте, и обеспечивает удобный просмотр расписания с помощью фильтров.

:small_blue_diamond: Фильтр расписания по дате / диапазону дат  
:small_blue_diamond: Фильтр расписания по группе / преподавателю  
:small_blue_diamond: Собственная панель администратора  
:small_blue_diamond: Отслеживание загрузки расписания из JSON-файла в базу данных  
:small_blue_diamond: Ручное редактирование расписания  
:small_blue_diamond: API для получения расписания  
### 2. Технологии ###
:small_orange_diamond: Python 3.11.4  
:small_orange_diamond: Django 4.2.6  
:small_orange_diamond: Django Rest Framework 3.14.0  
### 3. Запуск ###
С помощью докера:
```python
docker-compose up --build
```
Без докера:
```python
pip install -r requirements.txt
```
```python
python3 manage.py runserver
```
Приложение запустится на http://127.0.0.1:8000. Примеры файлов с расписанием находятся в папке examples of scheduler files.
Также создан суперпользователь с логином и паролем admin.
### 4. Скриншоты ###
![timetable](https://github.com/khaustiv/timetable/assets/143105312/225b5d9d-9454-48f8-a761-0a3b9dcc74ec)
![files](https://github.com/khaustiv/timetable/assets/143105312/062aba6c-41b4-4a9e-b6eb-3c366c3db0e6)
