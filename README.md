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

VPN-сервис 4ebur.net использует протокол Wireguard. Это позволяет нам немного зареверсить приложение и cкачать конфигурационные файлы напрямую. Ещё и socks5 прихватим.

## А как скачать?

Cкачать конфиги и прокси можно из Actions (актуальные, требуется аккаунт Github), или из релизов (старее)

## Вход в аккаунт
Вход в свой аккаунт через ключ:
```python
from main import Net4eburClient

client = Net4eburClient()

client.key = '0123456789101112'

client.loginUser('web')
```
Регистрация нового аккаунта:
```python
from main import Net4eburClient

client = Net4eburClient()

client.registerUser()

client.loginUser('web')
```

## Предварительные требования

* Python 3.6+
* Windows/Linux/Termux

## Установка и использование

#### 1. Клонирование репозитория
```
git clone https://github.com/bulatorr/4eburnet-api
cd 4eburnet-api
```
#### 2. Установка requests
```
pip install requests
```
#### 3. Пример получения wireguard конфигов
```python
python wireguard_example.py
```
#### 3. Пример получения SOCKS5 прокси
```python
python socks5_example.py
```

Результат будет в папке output

## Дальнейшее развитие

Для продолжения данного проекта мне необходим премиум аккаунт. Если кто-то готов поделиться, создайте issue
