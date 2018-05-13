from flask import Flask
from flask import request
import json
import http.client

app = Flask(__name__)

@app.route("/searchDrug")
def get_ingredient():
    nombre = request.args.get('active_ingredient')
    url = '/drug/label.json?search=active_ingredient:"' + nombre + '"&limit=10'
    datos = openfda(url)
    cosa = get_html(datos)
    print(cosa)
    return cosa

def openfda(url):
    datos = ""
    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request('GET', url, None, headers)
    r1 = conn.getresponse()
    r2 = r1.read().decode("utf-8")
    conn.close()
    data = json.loads(r2)

    if "results" in data:
        for elem in data["results"]:
            if "brand_name" in elem["openfda"]:
                datos += (str(elem["openfda"]["brand_name"]).lower()[2:-2])
                datos += "<br>"
            else:
                datos += "No hay resultados"
                datos += "<br>"
    return datos

def get_html(datos):
    contenido = """
              <!doctype html>
              <html>
              <body style='background-color: turquoise'>
                <h1>Nombres de medicamentos:</h1>
            """
    contenido += datos
    contenido += """
             </body>
             </html>
            """




if __name__ == "__main__":
    app.run(port=8000)