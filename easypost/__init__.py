import urllib
import base64
import json

_httplib = None
try:
    from google.appengine.api import urlfetch
    _httplib = 'urlfetch'
except ImportError:
    pass

if not _httplib:
    import urllib2
    _httplib = "urllib2"

base_url = 'https://geteasypost.com/api/'

def api_url(ttype='', action=''):
    return '%s/%s/%s' % (base_url, ttype, action)

def post(url, params, api_key):
    if api_key == '':
        raise InvalidApiKey('API key is empty. Set the API key before using the API.')

    headers = {
        'User-Agent': 'EasyPost-Python-v1',
        'Authorization': 'Basic %s' % (base64.b64encode(api_key + ':'), )
    }
    data = encode(params)
    if _httplib == "urlfetch":
        res = urlfetch.fetch(url, payload=data, headers=headers, method="POST")
        return json.loads(res.content)
    else:
        req = urllib2.Request(url, data, headers)
        try:
            response = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            if e.code == 401:
                raise InvalidApiKey('Invalid API key.')
            else:
                raise e

        response_html = response.read()
        return json.loads(response_html)

# The following methods in the EasyPost class are based on Stripe's python bindings
# which are under the MIT licnese. See https://github.com/stripe/stripe-python
def encode_dict(stk, key, dictvalue):
    n = {}
    for k, v in dictvalue.iteritems():
        k = _utf8(k)
        v = _utf8(v)
        n["%s[%s]" % (key, k)] = v
    stk.extend(_encode_inner(n))

def _encode_inner(d):
    """
    We want post vars of form:
    {'foo': 'bar', 'nested': {'a': 'b', 'c': 'd'}}
    to become:
    foo=bar&nested[a]=b&nested[c]=d
    """
    # special case value encoding
    ENCODERS = {
        dict: encode_dict
    }

    stk = []
    for key, value in d.iteritems():
        key = _utf8(key)
        try:
            encoder = ENCODERS[value.__class__]
            encoder(stk, key, value)
        except KeyError:
            # don't need special encoding
            value = _utf8(value)
            stk.append((key, value))
    return stk

def _utf8(value):
    if isinstance(value, unicode):
        return value.encode('utf-8')
    else:
        return value

def encode(d):
    """
    Internal: encode a string for url representation
    """
    return urllib.urlencode(_encode_inner(d))

# End of Stripe methods.

class InvalidApiKey(Exception):
    def __init__(self, message):
        super(InvalidApiKey, self).__init__(message)
        self.message = message
