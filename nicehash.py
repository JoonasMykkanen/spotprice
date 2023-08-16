from datetime import datetime
from hashlib import sha256
from time import mktime
import optparse
import requests
import uuid
import hmac
import json

class private_api:

    def __init__(self, host, organisation_id, key, secret, verbose=False):
        self.key = key
        self.secret = secret
        self.organisation_id = organisation_id
        self.host = host
        self.verbose = verbose

    def request(self, method, path, query, body):

        xtime = self.get_epoch_ms_from_now()
        xnonce = str(uuid.uuid4())

        message = bytearray(self.key, 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(str(xtime), 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(xnonce, 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(self.organisation_id, 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(method, 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(path, 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(query, 'utf-8')

        if body:
            body_json = json.dumps(body)
            message += bytearray('\x00', 'utf-8')
            message += bytearray(body_json, 'utf-8')

        digest = hmac.new(bytearray(self.secret, 'utf-8'), message, sha256).hexdigest()
        xauth = self.key + ":" + digest

        headers = {
            'X-Time': str(xtime),
            'X-Nonce': xnonce,
            'X-Auth': xauth,
            'Content-Type': 'application/json',
            'X-Organization-Id': self.organisation_id,
            'X-Request-Id': str(uuid.uuid4())
        }

        s = requests.Session()
        s.headers = headers

        url = self.host + path
        if query:
            url += '?' + query

        if self.verbose:
            print(method, url)

        if body:
            response = s.request(method, url, data=body_json)
        else:
            response = s.request(method, url)

        if response.status_code == 200:
            return response.json()
        elif response.content:
            raise Exception(str(response.status_code) + ": " + response.reason + ": " + str(response.content))
        else:
            raise Exception(str(response.status_code) + ": " + response.reason)

    def get_epoch_ms_from_now(self):
        now = datetime.now()
        now_ec_since_epoch = mktime(now.timetuple()) + now.microsecond / 1000000.0
        return int(now_ec_since_epoch * 1000)
    
    # My own functions
    def get_accounts(self):
        return self.request('GET', '/main/api/v2/accounting/accounts2/', '', None)
    
    def get_rigs(self):
        return self.request('GET', '/main/api/v2/mining/rigs2', '', None)
    
    def get_currencies(self):
        return self.request('GET', '/exchange/api/v2/info/prices', '', None)


if __name__ == "__main__":
    parser = optparse.OptionParser()

    parser.add_option('-b', '--base_url', dest="base", help="Api base url", default="https://api2.nicehash.com")
    parser.add_option('-o', '--organization_id', dest="org", help="Organization id")
    parser.add_option('-k', '--key', dest="key", help="Api key")
    parser.add_option('-s', '--secret', dest="secret", help="Secret for api key")
    parser.add_option('-m', '--method', dest="method", help="Method for request", default="GET")
    parser.add_option('-p', '--path', dest="path", help="Path for request", default="/")
    parser.add_option('-q', '--params', dest="params", help="Parameters for request")
    parser.add_option('-d', '--body', dest="body", help="Body for request")

    options, args = parser.parse_args()

    private_api = private_api(options.base, options.org, options.key, options.secret)

    params = ''
    if options.params is not None:
        params = options.params

    try:
        response = private_api.request(options.method, options.path, params, options.body)
    except Exception as ex:
        print("Unexpected error:", ex)
        exit(1)

    print(response)
    exit(0)