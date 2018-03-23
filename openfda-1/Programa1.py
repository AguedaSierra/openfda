import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("https://api.fda.gov/drug/event.json?")
conn.request('GET', 'search="results":"openfda":"spl_id"AND"generic_name"', body=None)
r1 = conn.getresponse()
print(r1)