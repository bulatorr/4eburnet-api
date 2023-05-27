import os
import zipfile
import requests
import json
import base64

API_ENDPOINT = 'https://api.mimestan.xyz/graphql'
HEADERS = {
    'Host': 'api.mimestan.xyz',
    'accept': '*/*',
    'content-type': 'application/json',
    'user-agent': 'okhttp/4.9.2',
}

def registerUser():
    data = {
        "operationName": "RegisterUser",
        "variables": {},
        "query": "mutation RegisterUser {\n  registerUser {\n    __typename\n    ...RegisterUserResponse\n    ...TooManyRequestsResponse\n  }\n}\n\nfragment RegisterUserResponse on RegisterUserOutput {\n  success\n  licenseKey\n  __typename\n}\n\nfragment TooManyRequestsResponse on TooManyRequestsException {\n  success\n  tooManyRequestsExceptionError: error\n  __typename\n}"
    }
    response = requests.post(API_ENDPOINT, headers=HEADERS, json=data)
    return response.json()['data']['registerUser']['licenseKey']

def loginUser(key):
    data = {
        "operationName": "LoginUser",
        "variables": {
            "payload": {
                "deviceType": "ANDROID",
                "licenseKey": key,
                "deviceUniqueId": "mobile:0LHQu9GP0YLRjCwg0Y3QutGB0YLQtdGA0LDQs9GA0LDQvCDQvtCx0L3QvtCy0LjQu9GB0Y8="
            }
        },
        "query": "mutation LoginUser($payload: LoginUserInput!) {\n  loginUser(payload: $payload) {\n    __typename\n    ...LoginUserResponse\n    ...TooManyRequestsResponse\n  }\n}\n\nfragment LoginUserResponse on LoginUserOutput {\n  success\n  error\n  accessToken\n  refreshToken\n  __typename\n}\n\nfragment TooManyRequestsResponse on TooManyRequestsException {\n  success\n  tooManyRequestsExceptionError: error\n  __typename\n}"
    }
    response = requests.post(API_ENDPOINT, headers=HEADERS, json=data)
    return response.json()['data']['loginUser']['accessToken']

def getZones(accessToken):
    data = {
        "operationName": "GetZones",
        "variables": {},
        "query": "query GetZones {\n  getZones {\n    __typename\n    ...GetZonesResponse\n    ...TooManyRequestsResponse\n    ...UnauthorizedResponse\n  }\n}\n\nfragment GetZonesResponse on GetZonesOutput {\n  success\n  zones {\n    regionId\n    regionCode\n    countryAlpha2\n    serverProtocol\n    serverHost\n    regionName\n    nodeIsAvailable\n    serverType\n    nodeEfficiency\n    __typename\n  }\n  __typename\n}\n\nfragment TooManyRequestsResponse on TooManyRequestsException {\n  success\n  tooManyRequestsExceptionError: error\n  __typename\n}\n\nfragment UnauthorizedResponse on UnauthorizedException {\n  success\n  unauthorizedExceptionError: error\n  __typename\n}"
    }
    headers = {**HEADERS, 'authorization': f'Bearer {accessToken}'}
    response = requests.post(API_ENDPOINT, headers=headers, json=data)
    return response.json()

def filter_available_nodes(data):
    return [i for i in data['data']['getZones']['zones'] if i['nodeIsAvailable'] and i['serverProtocol'] == 'WIREGUARD']

def selectNode(accessToken, node):
    data = {
        "operationName": "SelectNode",
        "variables": {
            "payload": {
                "serverType": node['serverType'],
                "regionId": node['regionId'],
                "serverProtocol": "WIREGUARD"
            }
        },
        "query": "query SelectNode($payload: SelectNodeInput!) {\n  selectNode(payload: $payload) {\n    __typename\n    ...SelectNodeResponse\n    ...TooManyRequestsResponse\n    ...UnauthorizedResponse\n    ...ForbiddenResponse\n  }\n}\n\nfragment SelectNodeResponse on SelectNodeOutput {\n  success\n  selectNodeOutputError: error\n  node {\n    regionCode\n    countryAlpha2\n    serverProtocol\n    serverHost\n    data\n    __typename\n  }\n  __typename\n}\n\nfragment TooManyRequestsResponse on TooManyRequestsException {\n  success\n  tooManyRequestsExceptionError: error\n  __typename\n}\n\nfragment UnauthorizedResponse on UnauthorizedException {\n  success\n  unauthorizedExceptionError: error\n  __typename\n}\n\nfragment ForbiddenResponse on ForbiddenException {\n  success\n  forbiddenExceptionError: error\n  __typename\n}"
    }
    headers = {**HEADERS, 'authorization': f'Bearer {accessToken}'}
    response = requests.post(API_ENDPOINT, headers=headers, json=data)
    response_data = response.json()['data']['selectNode']['node']['data']
    wireguard = base64.b64decode(response_data).decode()
    regionCode = node['regionCode']
    os.makedirs('output', exist_ok=True)
    with open(f'output/{regionCode}.conf', 'w') as f:
        f.write(wireguard)