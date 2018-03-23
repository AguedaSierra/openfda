import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request('GET', '/drug/label.json?&limit=10', None, headers)
r1 = conn.getresponse()
r2 = r1.read().decode("utf-8")
conn.close()
data = json.loads(r2)

a = 0
for elem in data["results"]:
    a = a + 1
    print("El identificador del objeto nº", a, "es:", elem["id"])