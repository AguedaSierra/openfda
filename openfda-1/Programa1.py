import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request('GET', '/drug/label.json?search=results.openfda:spl_id&limit=1', None, headers)
r1 = conn.getresponse()
print(r1)
for elem in r1:
    print(elem)