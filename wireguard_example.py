from main import Net4eburClient
from utils import parseWireguard

wireguard = Net4eburClient('wireguard')

wireguard.registerUser()

wireguard.loginUser('ios')

wireguard.selectDomain()

for node in wireguard.getAvailableNodes():
    parseWireguard(wireguard.selectNode(node), node)
