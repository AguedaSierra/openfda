import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request('GET', '/drug/label.json?search=results.openfda.generic_name="salicylic%20acid"&limit=100', None, headers)
r1 = conn.getresponse()
r2 = r1.read().decode("utf-8")
conn.close()
data = json.loads(r2)

manufacturer = []
for elem in data["results"]:
    if "manufacturer_name" in elem["openfda"]:
        manufacturer.append(str(elem["openfda"]["manufacturer_name"]))

a = 0
for name in set(manufacturer):
    a = a+1
    print("Fabricante nº", a, name, "\n", end=" ")