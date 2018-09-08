# Прогноз погоды
Поддерживаются следующие 7 дней после текущей даты.
Если дата не входит в данный промежуток, в json'е будет погода на текущий день.
Запускается на порте 8003

#Install
##1 - git clone https://github.com/Ho7/mai_forecast.git
##2 - cd mai_forecast
##3 - sudo apt install python3 python3-pip
##4 - pip3 install -r requirements
##5 - python3 manage.py runserver


#Пример запросов
#### curl "127.0.0.1:8003/v1/forecast/?city=Tambov&dt=2018-09-11" 
{"city": "Tambov", "unit": "celsius", "temperature": 25}%  

#### curl "127.0.0.1:8003/v1/current/?city=Tambov"
{"city": "Tambov", "unit": "celsius", "temperature": 16} 