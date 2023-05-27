from main import *


access_token = loginUser(registerUser()) # для регистрации нового аккаунта

#access_token = loginUser('01234567891011') # для входа в свой аккаунт
 
zones = getZones(access_token) # получаем список серверов

for i in filter_available_nodes(zones): # фильтруем доступные
    selectNode(access_token, i) # сохраняем конфиги в папку output
