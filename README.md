<br/>
<p align="center">
  <h3 align="center">4ebur.net Config Generator</h3>

  <p align="center">
    Генератор профилей Wireguard из VPN-сервиса 4ebur.net
    <br/>
    <br/>
    <a href="https://github.com/bulatorr/4eburnet-api/issues">Сообщить об ошибке</a>
  </p>
</p>

## О проекте

VPN-сервис 4ebur.net использует протокол Wireguard. Это позволяет нам немного зареверсить приложение и cкачать конфигурационные файлы напрямую.

## Предварительные требования

* Python 3.\*

## Установка

#### 1. Клонирование репозитория
```
git clone https://github.com/bulatorr/4eburnet-api
```
#### 2. Установка requests
```
pip install requests
```
#### 3. Редактирование example.py
Создание нового аккаунта
```python
from main import *

access_token = loginUser(registerUser()) # регистрация нового аккаунта
 
zones = getZones(access_token) # получаем список серверов

for i in filter_available_nodes(zones): # фильтруем доступные
    selectNode(access_token, i) # сохраняем конфигурационные файлы в папку output
```
Использование существующего
```python
from main import *

access_token = loginUser('0123456789101112') # 0123456789101112 ключ аккаунта
 
zones = getZones(access_token) # получаем список серверов

for i in filter_available_nodes(zones): # фильтруем доступные
    selectNode(access_token, i) # сохраняем конфигурационные файлы в папку output

```
#### 4. Запуск
```python
python example.py
```

## Дальнейшее развитие

Для продолжения данного проекта мне необходим премиум аккаунт. Если кто-то готов поделиться, пишите на почту:
```
galinaivanovna301965@gmail.com
```
