import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov") #El programa se conecta con la página de la api fda
conn.request('GET', '/drug/label.json?&limit=10', None, headers) #Con un GET pide la información de la etiqueta
#de diez medicamentos (limit=10) en un fichero json
r1 = conn.getresponse()
r2 = r1.read().decode("utf-8") #Lee la respuesta y la decodifica en formato utf-8
conn.close()
data = json.loads(r2) #La respuesta en código utf-8 se convierte en un diccionario para que sea más
#fácil de trabajar en Python

a = 0 #Se inicializa una variable para ir contando el número de medicamentos
for elem in data["results"]: #Se itera sobre los elementos que tienen como clave "results"
    #Dentro de esos valores hay más diccionarios
    a = a + 1
    print("El identificador del objeto nº", a, "es:", elem["id"]) #Se obtiene el valor cuya clave es "id"