import requests

class Net4eburClient:
    """
    A client for the 4ebur.net API.
    """
    DOMAIN = 'candypall.cyou'

    API_ENDPOINT = f'https://api.{DOMAIN}/graphql'

    HEADERS = {
        'Host': f'api.{DOMAIN}',
        'accept': '*/*',
        'content-type': 'application/json',
        'user-agent': 'okhttp/4.9.2',
    }

    def __init__(self, serverProtocol=None):
        """
        Initializes the client.
        """
        self.headers = Net4eburClient.HEADERS.copy()
        self.domain = Net4eburClient.API_ENDPOINT
        self.accessToken = None
        self.key = None
        self.serverProtocol = serverProtocol.upper()

    def registerUser(self):
        """
        Registers a new user and returns the license key.
        """
        data = {
            "operationName": "RegisterUser",
            "variables": {},
            "query": "mutation RegisterUser {\n  registerUser {\n    __typename\n    ...RegisterUserResponse\n    ...TooManyRequestsResponse\n  }\n}\n\nfragment RegisterUserResponse on RegisterUserOutput {\n  success\n  licenseKey\n  __typename\n}\n\nfragment TooManyRequestsResponse on TooManyRequestsException {\n  success\n  tooManyRequestsExceptionError: error\n  __typename\n}"
        }
        response = requests.post(Net4eburClient.API_ENDPOINT, headers=Net4eburClient.HEADERS, json=data)
        self.key = response.json()['data']['registerUser']['licenseKey']
        return self.key

    def loginUser(self, device_type):
        """
        Logs in the user with the given license key and device type, and returns the access token.
        available_types = ['ANDROID', 'IOS', 'WEB', 'WINDOWS', 'MACOS', 'LINUX', 'FIREFOX', 'CHROMIUM']
        """
        if device_type.upper() in ['ANDROID', 'IOS', 'MACOS', 'LINUX', 'WINDOWS']:
            device_id = 'mobile:0LHQu9GP0YLRjCwg0Y3QutGB0YLQtdGA0LDQs9GA0LDQvCDQvtCx0L3QvtCy0LjQu9GB0Y8='
        elif device_type.upper() in ['CHROMIUM', 'FIREFOX']:
            device_id = 'extension:test'
        elif device_type.upper() == 'WEB':
            device_id = ''
            print('Attention, WEB does not support config extraction.')
        else:
            print("ERROR!!! Wrong device type.")
            return None
        data = {
            "operationName": "LoginUser",
            "variables": {
                "payload": {
                    "deviceType": device_type.upper(),
                    "licenseKey": self.key,
                    "deviceUniqueId": device_id,
                }
            },
            "query": "mutation LoginUser($payload: LoginUserInput!) {\n  loginUser(payload: $payload) {\n    __typename\n    ...LoginUserResponse\n    ...TooManyRequestsResponse\n  }\n}\n\nfragment LoginUserResponse on LoginUserOutput {\n  success\n  error\n  accessToken\n  refreshToken\n  __typename\n}\n\nfragment TooManyRequestsResponse on TooManyRequestsException {\n  success\n  tooManyRequestsExceptionError: error\n  __typename\n}",
        }
        response = requests.post(Net4eburClient.API_ENDPOINT, headers=Net4eburClient.HEADERS, json=data)
        self.accessToken = response.json()['data']['loginUser']['accessToken']
        return self.accessToken

    def selectDomain(self):
        """
        Selects the user's domain and updates the API endpoint and headers accordingly.
        Returns the name of the selected domain.
        """
        data = {
            'operationName': 'SelectDomain',
            'variables': {},
            'query': 'query SelectDomain {\n  selectDomain {\n    __typename\n    ...SelectDomainResponse\n    ...TooManyRequestsResponse\n    ...UnauthorizedResponse\n  }\n}\n\nfragment SelectDomainResponse on SelectDomainOutput {\n  success\n  error\n  domain {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment TooManyRequestsResponse on TooManyRequestsException {\n  success\n  tooManyRequestsExceptionError: error\n  __typename\n}\n\nfragment UnauthorizedResponse on UnauthorizedException {\n  success\n  unauthorizedExceptionError: error\n  __typename\n}',
        }
        headers = {**self.headers, 'authorization': f'Bearer {self.accessToken}'}
        response = requests.post(Net4eburClient.API_ENDPOINT, headers=headers, json=data)
        self.DOMAIN = response.json()['data']['selectDomain']['domain']['name']
        self.domain = f'https://api.{self.DOMAIN}/graphql'
        self.headers['Host'] = f'api.{self.DOMAIN}'
        return self.domain

    def getUser(self):
        """
        Get user info and returns them as a dictionary.
        """
        data = {
            "operationName": "GetUser",
            "variables": {},
            "query": "query GetUser {\n  getUser {\n    __typename\n    ...GetUserResponse\n    ...UnauthorizedResponse\n  }\n}\n\nfragment GetUserResponse on GetUserOutput {\n  success\n  user {\n    licenseKey\n    __typename\n  }\n  userRiskLevelType\n  permissionsSummary {\n    ACTIVE_SUBSCRIPTION {\n      permitted\n      data {\n        __typename\n        ...SubscriptionDataResponse\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment SubscriptionDataResponse on SubscriptionData {\n  expirableAt\n  __typename\n}\n\nfragment UnauthorizedResponse on UnauthorizedException {\n  success\n  unauthorizedExceptionError: error\n  __typename\n}"
        }
        headers = {**self.headers, 'authorization': f'Bearer {self.accessToken}'}
        response = requests.post(self.domain, headers=headers, json=data)
        return response.json()['data']['getUser']
    
    def getPurchases(self):
        """
        Get purchases info and returns them as a dictionary.
        """
        data = {
            "operationName": "GetPurchases",
            "variables": {},
            "query": "query GetPurchases {\n  getPurchases {\n    __typename\n    ...GetPurchasesResponse\n    ...TooManyRequestsResponse\n    ...UnauthorizedResponse\n  }\n}\n\nfragment GetPurchasesResponse on GetPurchasesOutput {\n  success\n  purchases {\n    status\n    type\n    purchaseDetailsSubscription {\n      expirableAt\n      type\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment TooManyRequestsResponse on TooManyRequestsException {\n  success\n  tooManyRequestsExceptionError: error\n  __typename\n}\n\nfragment UnauthorizedResponse on UnauthorizedException {\n  success\n  unauthorizedExceptionError: error\n  __typename\n}"
        }
        headers = {**self.headers, 'authorization': f'Bearer {self.accessToken}'}
        response = requests.post(self.domain, headers=headers, json=data)
        return response.json()['data']['getPurchases']

    def getZones(self):
        """
        Gets the available server zones and returns them as a dictionary.
        """
        data = {
            "operationName": "GetZones",
            "variables": {},
            "query": "query GetZones {\n  getZones {\n    __typename\n    ...GetZonesResponse\n    ...TooManyRequestsResponse\n    ...UnauthorizedResponse\n  }\n}\n\nfragment GetZonesResponse on GetZonesOutput {\n  success\n  zones {\n    regionId\n    regionCode\n    countryAlpha2\n    serverProtocol\n    serverHost\n    regionName\n    nodeIsAvailable\n    serverType\n    nodeEfficiency\n    __typename\n  }\n  __typename\n}\n\nfragment TooManyRequestsResponse on TooManyRequestsException {\n  success\n  tooManyRequestsExceptionError: error\n  __typename\n}\n\nfragment UnauthorizedResponse on UnauthorizedException {\n  success\n  unauthorizedExceptionError: error\n  __typename\n}"
        }
        headers = {**self.headers, 'authorization': f'Bearer {self.accessToken}'}
        response = requests.post(self.domain, headers=headers, json=data)
        self.zones = response.json()
        return response.json()

    def getAvailableNodes(self):
        """
        Filters the available server zones by server protocol and returns them as a list.
        """
        zones = self.getZones()['data']['getZones']['zones']
        return [i for i in zones if i['nodeIsAvailable'] and i['serverProtocol'] == self.serverProtocol]

    def selectNode(self, node):
        """
        Selects the given node and returns its data.
        """
        data = {
            "operationName": "SelectNode",
            "variables": {
                "payload": {
                    "serverType": node['serverType'],
                    "regionId": node['regionId'],
                    "serverProtocol": node['serverProtocol'],
                }
            },
            "query": "query SelectNode($payload: SelectNodeInput!) {\n  selectNode(payload: $payload) {\n    __typename\n    ...SelectNodeResponse\n    ...TooManyRequestsResponse\n    ...UnauthorizedResponse\n    ...ForbiddenResponse\n  }\n}\n\nfragment SelectNodeResponse on SelectNodeOutput {\n  success\n  selectNodeOutputError: error\n  node {\n    regionCode\n    countryAlpha2\n    serverProtocol\n    serverHost\n    data\n    __typename\n  }\n  __typename\n}\n\nfragment TooManyRequestsResponse on TooManyRequestsException {\n  success\n  tooManyRequestsExceptionError: error\n  __typename\n}\n\nfragment UnauthorizedResponse on UnauthorizedException {\n  success\n  unauthorizedExceptionError: error\n  __typename\n}\n\nfragment ForbiddenResponse on ForbiddenException {\n  success\n  forbiddenExceptionError: error\n  __typename\n}"
        }
        headers = {**self.headers, 'authorization': f'Bearer {self.accessToken}'}
        response = requests.post(self.domain, headers=headers, json=data)
        try:
            resp = response.json()['data']['selectNode']['node']['data']
            return resp
        except:
            print(response.json())
