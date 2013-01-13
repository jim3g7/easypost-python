from easypost import EasyPost, Address, Postage

## Testing
test_values = {
  'street1': '388 Townsend St',
  'street2': 'Apt 20',
  'city': 'San Francisco',
  'state': 'CA',
  'zip': '94107'
}

test_url = EasyPost.api_url("address", "verify")

print Address.verify(street1="388 Townsend St", street2="Apt 20", city="San Francisco", state="CA", zip="94107")
print Address.verify(**test_values)

compare_data = {
  "parcel": {
    "weight": 1.1,
    "height": 12,
    "width": 14,
    "length": 7
  },
  "to": {
      "name": "Reed Rothchild",
      "street1": "101 California St",
      "street2": "Suite 1290",
      "city": "San Francisco",
      "state": "CA",
      "zip": "94111"
  },
  "from": {
      "name": "Dirk Diggler",
      "phone": "8149777556",
      "street1": "300 Granelli Ave",
      "city": "Half Moon Bay",
      "state": "CA",
      "zip": "94019"
  },
  "carrier": "USPS",
  "service": "Priority"
}

print Postage.compare(**compare_data)
print Postage.buy(**compare_data)
print Postage.get("test.png")
listt = Postage.list()
print listt["postages"][0]
