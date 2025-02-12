Приложение позволяет загружать расписание занятий в формате JSON, выгруженное из информационной системы «Сириус» Московского университета им. Витте, и предоставляет удобные инструменты для просмотра и управления расписаниями через фильтры.

## Основные возможности 
:calendar: Поиск расписания по дате / диапазону дат   
:busts_in_silhouette: Поиск расписания по группе / преподавателю   
:control_knobs: Панель администратора для управления расписанием   
:arrow_up: Загрузка расписаний из JSON-файлов в базу данных  
:pencil2: Ручное редактирование расписания   
:globe_with_meridians: API для интеграции с другими системами  
 
## Запуск

1. Клонируйте репозиторий проекта на свой компьютер:

```
git clone https://github.com/khaustova/muiv_timetable.git
```
2. Запустите приложение одним из двух способов:
<details>
  <summary>В Docker</summary>

```
docker-compose up --build
```
  
</details>  

<details>
  <summary>В виртуальном окружении</summary>

  * Создайте виртуальное окружение:
    

  ```
  python3 -m venv .venv
  ```

  * Активируйте виртуальное окружение:  

    * Для Linux/MacOS:  

    ```
    source .venv/bin/activate
    ```
   
    * Для Windows:  

    ```
    .venv\Scripts\activate
    ```

  * Установите необходимые библиотеки:

  ```
  pip install -r requirements.txt
  ```

  * Выполните миграции базы данных:
    

  ```
  python3 manage.py migrate
  ```

  * Запустите сервер:

  ```
  python3 manage.py runserver
  ```
  
</details> 

3. Приложение будет доступно по адресу http://127.0.0.1:8000.  
  
Примеры файлов с расписанием находятся в папке `examples of scheduler files`.

### Скриншоты
![timetable](https://github.com/khaustiv/timetable/assets/143105312/225b5d9d-9454-48f8-a761-0a3b9dcc74ec)
![files](https://github.com/khaustiv/timetable/assets/143105312/062aba6c-41b4-4a9e-b6eb-3c366c3db0e6)
