import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request('GET', '/drug/label.json?&limit=1', None, headers)
r1 = conn.getresponse()
r2 = r1.read().decode("utf-8")
conn.close()
data = json.loads(r2)

for elem in data["results"]:
    print("El identificador es:", elem["id"])
    print("El propósito es:", str(elem["purpose"])[2:-2])
    print("El nombre del fabricante es:", str(elem["openfda"]["manufacturer_name"])[2:-2])

