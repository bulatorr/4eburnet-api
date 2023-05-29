from main import *
from utils import *

device_type = "CHROMIUM"

access_token = loginUser(registerUser(), device_type)

selectDomain(access_token)

zones = getZones(access_token)

list = []

for node in filter_available_nodes(zones, "SOCKS5"):
    list.append(parse_socks5(selectNode(access_token, node), node))

os.makedirs('output', exist_ok=True)
with open('output/socks5.txt', 'w') as f:
    f.write('\n'.join(list))
