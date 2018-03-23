import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("https://api.fda.gov/drug/event.json?")
conn.request('GET', 'search=patient.reaction.reactionmeddrapt:"fatigue"+AND+occurcountry:"ca"&limit=1', body=None)
r1 = conn.getresponse()
print(r1)