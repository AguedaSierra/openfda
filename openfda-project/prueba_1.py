from flask import Flask
from flask import request
import json
import http.client

app = Flask(__name__)

@app.route("/searchDrug")
def get_ingredient():
    algo = request.args.get('active_ingredient')
    algo.replace(" ", "!")
    pepe = algo
    #print(algo)
    #pepe = "acetylsalicylic%20acid"
    print("algo")
    print(algo)
    print("La longitud de algo es:", len(algo))
    for index in range(len(algo)):
        print(ord(algo[index]))
    print("pepe")
    print(pepe)
    print(pepe.replace(" ", "%20"))
    print("La longitud de pepe es:", len(pepe))
    for index in range(len(pepe)):
        print(ord(pepe[index]))
    #pepe = algo
    datos = ""
    pepe = pepe.replace(" ", "%20")
    temp = '/drug/label.json?search=active_ingredient:"' + pepe + '"&limit=100'
    print(temp)
    print(type(temp))
    #print(pepe)
    #print(type(pepe))
    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request('GET', temp, None, headers)
    r1 = conn.getresponse()
    r2 = r1.read().decode("utf-8")
    conn.close()
    print("r2 es:", r2)
    data = json.loads(r2)

    if "results" in data:
        for elem in data["results"]:
            datos += elem["id"] + "////"

    else:
        datos = "nada"

    return pepe + '------' + datos

if __name__ == "__main__":
    app.run()
