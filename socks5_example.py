import os
from main import Net4eburClient
from utils import parseSocks5

socks5 = Net4eburClient('socks5')

socks5.registerUser()

socks5.loginUser('firefox')

socks5.selectDomain()

socks_list = []

for node in socks5.getAvailableNodes():
    socks_list.append(parseSocks5(socks5.selectNode(node), node))

os.makedirs('output', exist_ok=True)
with open('output/socks5.txt', 'w') as f:
    f.write('\n'.join(socks_list))
