import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov") #El programa se conecta con la página de la api fda
conn.request('GET', '/drug/label.json?&limit=1', None, headers) #Con un GET pide la información de la etiqueta
# de un medicamento (limit=1) en un fichero json
r1 = conn.getresponse()
r2 = r1.read().decode("utf-8") #Lee la respuesta y la decodifica en formato utf-8
conn.close()
data = json.loads(r2) #La respuesta en código utf-8 se convierte en un diccionario para que sea más
#fácil de trabajar en Python

for elem in data["results"]: #Se itera sobre los elementos que tienen como clave "results"
    #Dentro de esos valores hay más diccionarios
    print("El identificador es:", elem["id"]) #Se obtiene el valor cuya clave es "id"
    print("El propósito es:", str(elem["purpose"])[2:-2]) #Se obtiene el valor cuya clave es "purpose"
    print("El nombre del fabricante es:", str(elem["openfda"]["manufacturer_name"])[2:-2]) #Se obtiene el valor
    #cuya clave es "manufacturer_name" que está dentro de la clve "openfda"
    # Con [2:-2] se coge el valor sin los corchetes ni las comillas 8después de convertirlo a string)

