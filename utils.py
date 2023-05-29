import base64
import os
import json

def parseWireguard(response_data, node):
    wireguard = base64.b64decode(response_data).decode()
    regionCode = node['regionCode']
    os.makedirs('output', exist_ok=True)
    with open(f'output/{regionCode}.conf', 'w') as f:
        f.write(wireguard)

def parseSocks5(response_data, node):
    socks5 = json.loads(base64.b64decode(response_data))
    return f"{socks5['host']}:{socks5['port']} - {node['regionCode']}"
