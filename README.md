# Прогноз погоды
Поддерживаются следующие 7 дней после текущей даты.
Если дата не входит в данный промежуток, в json'е будет погода на текущий день.

# Установка
- Склоним репозиторий - ``` git clone https://github.com/Ho7/mai_forecast.git ```
- Перейдем в директорию проекта - ```cd mai_forecast```
- Установим питон и менеджер питон-пакетов - ```sudo apt install python3 python3-pip```
- Установим зависимости - ```pip3 install -r requirements.txt```
- Экспортируем перменную окружения и установим значение порта - ```export LISTEN_PORT = 8003```
- Запустим сервер -  ```python3 manage.py runserver```


# Пример запросов
request:
```curl "127.0.0.1:8003/v1/forecast/?city=Tambov&dt=2018-09-11" ```

response: 
```{"city": "Tambov", "unit": "celsius", "temperature": 25}```

request:
```curl "127.0.0.1:8003/v1/current/?city=Tambov"```

response:
```{"city": "Tambov", "unit": "celsius", "temperature": 16} ```