from __init__ import post, api_url
api_key = ''

class Address(object):
    """
    A shipping address. Name is not required for most API calls.
    """
    def __init__(self,
        name="",
        street1="",
        street2="",
        city="",
        state="",
        zip=""):

        self.name = name
        self.street1 = street1
        self.street2 = street2
        self.city = city
        self.state = state
        self.zip = zip

    def as_json(self):
        return {
            'name': self.name,
            'street1': self.street1,
            'street2': self.street2,
            'city': self.city,
            'state': self.state,
            'zip': self.zip
        }

    def verify(self):
        params = {
            'address': self.as_json()
        }

        result = post(api_url("address", "verify"), params, api_key)

        if 'error' in result:
            raise InvalidAddress(result['error'])
        else:
            self.street1 = result['address'].get('street1', '')
            self.street2 = result['address'].get('street2', '')
            self.city = result['address'].get('city', '')
            self.state = result['address'].get('state', '')
            self.zip = result['address'].get('zip', '')

            return self


class Package(object):
    """
    A parcel with dimensions. Height, width, length and weight are required.
    """
    def __init__(self, height, width, length, weight):
        self.height = height
        self.width = width
        self.length = length
        self.weight = weight

    def as_json(self):
        return {
            'weight': self.weight,
            'height': self.height,
            'width': self.width,
            'length': self.length
        }


class Shipment(object):
    """
    A parcel with destination and origin addresses.
    """
    def __init__(self, to_address, from_address, package):
        self.to_address = to_address
        self.from_address = from_address
        self.package = package

    def rates(self):
        params = {
            'parcel': self.package.as_json(),
            'to': self.to_address.as_json(),
            'from': self.from_address.as_json()
        }

        results = post(api_url('postage', 'rates'), params, api_key)

        if 'error' in results:
            raise InvalidShipment(results['error'])
        else:
            rates = []

            for result in results['rates']:
                rates.append(Rate(result['rate'],
                                  result['carrier'],
                                  result['service']))
            return rates


class Rate(object):
    """
    A shipping rate for a shipment.
    """
    def __init__(self, price=0, carrier="", service=""):
        self.price = price
        self.carrier = carrier
        self.service = service


class Postage(object):
    """
    Postage for a shipment, at a rate, that can be bought or has been bought already.
    """
    def __init__(self, shipment, rate):
        self.shipment = shipment
        self.rate = rate
        self.label_file_name = None
        self.tracking_code = None
        self.label_url = None
        self.label_file_type = None

    def buy(self):
        params = {
            'parcel': self.shipment.package.as_json(),
            'to': self.shipment.to_address.as_json(),
            'from': self.shipment.from_address.as_json(),
            'service': self.rate.service,
            'carrier': 'USPS'
        }

        result = post(api_url("postage", "buy"), params, api_key)

        self.label_file_name = result['label_file_name']
        self.tracking_code = result['tracking_code']
        self.label_url = result['label_url']
        self.label_file_type = result['label_file_name']


def get_postage(filename):
    """
    Returns postage by filename.
    """
    result = post(api_url("postage", "get"), {"label_file_name": filename}, api_key)

    rate = Rate(result['rate']['rate'], result['rate']['carrier'], result['rate']['service'])
    postage = Postage(None, rate)

    postage.label_file_name = result['label_file_name']
    postage.tracking_code = result['tracking_code']
    postage.label_url = result['label_url']
    postage.label_file_type = result['label_file_name']

    return postage


def list_postage():
    """
    Returns all available postage for the account.
    """
    results = post(api_url("postage", "list"), {}, api_key)
    postages = []

    for result in results['postages']:
        postage = get_postage(result)
        postages.append(postage)

    return postages


class InvalidAddress(Exception):
    def __init__(self, message):
        super(InvalidAddress, self).__init__(message)
        self.message = message


class InvalidShipment(Exception):
    def __init__(self, message):
        super(InvalidShipment, self).__init__(message)
        self.message = message
