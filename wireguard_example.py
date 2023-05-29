from main import *
from utils import *

device_type = "ANDROID"

access_token = loginUser(registerUser(), device_type)

selectDomain(access_token)

zones = getZones(access_token)

for node in filter_available_nodes(zones, "WIREGUARD"):
    parse_wireguard(selectNode(access_token, node), node)
