# A través de este cliente se puede ver cómo se recibe la información con los tag del código html.
# Sin embargo también nos podemos conectar al servidor mediante cualquier navegador y así ver cómo se interpreta el html.

import http.client

PORT = 8000
headers=('Content-type', 'text/html')

conn = http.client.HTTPConnection('localhost', PORT) # El cliente se conecta con el servidor
conn.request("GET", "/") # Envía un mensaje de solicitud con un GET
r1 = conn.getresponse() # Lee el mensaje de respuesta que ha recibido del servidor
print(r1.status, r1.reason) # Se imprime el estado de la respuesta
data1 = r1.read().decode("utf-8") # Se lee el contenido de la respuesta y se convierte a una cadena
print(data1) # Se imprime el código html que ha recibido