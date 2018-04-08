import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov") # Se define el nombre del servidor al que queremos conectarnos
conn.request('GET', '/drug/label.json?search=active_ingredient:"acetylsalicylic%20acid"&limit=100', None, headers)
# Con un GET pide la información de la etiqueta de todos los medicamentos (limit=100, límite máximo) que
# contengan "acetylsalicylic acid" en el ingrediente activo. Se guarda en un fichero json
r1 = conn.getresponse()
r2 = r1.read().decode("utf-8") # Lee la respuesta y se convierte a una cadena
conn.close()
data = json.loads(r2) # La respuesta se convierte en un diccionario para que sea más fácil de trabajar en Python

for elem in data["results"]: # Se itera sobre los elementos que tienen como clave "results"
    if "manufacturer_name" in elem["openfda"]: # Si el elemento (valor de la clave "openfda") tiene la clave "manufacturer_name"
        fabricante=(str(elem["openfda"]["manufacturer_name"])[2:-2]) # fabricante = nombre del fabricante sin corchetes
        # ni comillas ([2:-2])
    else: # Si no existe la clave "manufacturer_name"
        fabricante="No disponible"
    print("El id del medicamento es:", elem["id"], " y el nombre del fabricante es:", fabricante, "\n")