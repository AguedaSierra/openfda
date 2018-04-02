import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov") #El programa se conecta con la página de la api fda
conn.request('GET', '/drug/label.json?search=results.openfda.generic_name="acetylsalicylic%20acid"&limit=100', None, headers)
#Con un GET pide la información de la etiqueta de todos (limit=100, límite máximo) los medicamentos que
#contengan "acetylsalicylic acid" en el nombre genérico. Se guarda en un fichero json
r1 = conn.getresponse()
r2 = r1.read().decode("utf-8") #Lee la respuesta y la decodifica en formato utf-8
conn.close()
data = json.loads(r2) #La respuesta en código utf-8 se convierte en un diccionario para que sea más
#fácil de trabajar en Python

manufacturer = [] #Se crea una lista para ir añadiendo e nombre de los fabricantes
for elem in data["results"]: #Se itera sobre los elementos que tienen como clave "results"
    if "manufacturer_name" in elem["openfda"]: #Si el elemento (valor de la clve "openfda") tiene la clve "manufacturer_name"
        manufacturer.append(str(elem["openfda"]["manufacturer_name"])[2:-2]) #Se añade el nombre a la lista
        #sin comillas ni corchetes ([2:-2])

a = 0 #Se inicializa una variable para ir contando el número de fabricantes
for name in set(manufacturer): #Con el set se cogen los nombres no repetidos
    a = a+1
    print("Fabricante nº", a, ":", name, "\n", end=" ")