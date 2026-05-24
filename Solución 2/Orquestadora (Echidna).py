import json
import boto3
import time
import base64
from botocore.exceptions import ClientError


s3_client = boto3.client('s3')


def lambda_handler(event, context):
    """    
    La funcion lambda Orquestadora (Echidna) se encarga de esperar a que los fragmentos 1,2 y 3 esten disponibles en el S3 para descargarlos,
    ensamblarlos en el orden correcto, codificar el resultado final en base64 y guardarlo otra vez en el S3 para que la lambda Aethon lo recoja.
    
    Se utiliza unos intentos maximos con un tiempo de espera para no estar constantemente haciendo peticiones y no esperar indefinidamente
    a que lleguen los fragmentos 1 y 2, que a veces pueden ir con retraso. (polling)
    
    Si no llegan a tiempo, se lanza una excepción. 
    
    """
    # Extraemos dinámicamente el nombre del bucket del evento S3 que despertó a la Lambda.
    # Así no tenemos que escribir el nombre a mano.
    try:
        bucket_name = event['Records'][0]['s3']['bucket']['name']


    except KeyError:
        return {"statusCode": 400, "body": "Evento S3 no generado correctamente."}


    # Definición dinámica de rutas
    archivos_esperados = [f'fragmento1.json', f'fragmento2.json', f'fragmento3.json']
    payload_final_key = f'payload_final.json'
   
    # Definimos cuánto tiempo máximo vamos a esperar a las Lambdas 1 y 2 por si van con retraso.
    intentos_maximos = 15
    tiempo_espera_segundos = 2
   
    # BUCLE DE SINCRONIZACIÓN
    for intento in range(intentos_maximos):
        todos_existen = True
       
        # Comprobamos si cada archivo esperado ya está en el S3
        for archivo in archivos_esperados:
            if not existe_en_s3(bucket_name, archivo):
                todos_existen = False
                break # Si falta uno, dejamos de comprobar y esperamos
       
        if todos_existen:
            print("[SUCCESS] Todos los fragmentos sincronizados.")
            break # Salimos del bucle porque ya podemos empezar a trabajar
        else:
            print(f"[INFO] Faltan fragmentos. Esperando (Intento {intento+1}/{intentos_maximos})...")
            time.sleep(tiempo_espera_segundos)
    else:
        # Agotados los intentos
        raise Exception("TIMEOUT: Los fragmentos 1 y 2 no llegaron. Abortando orquestación.")


    # Descargamos el contenido de los 3 archivos y los convertimos de texto a diccionarios de Python
    # Hacer bucle? (Y si hay más de 3?)
    f1 = json.loads(s3_client.get_object(Bucket=bucket_name, Key=archivos_esperados[0])['Body'].read())
    f2 = json.loads(s3_client.get_object(Bucket=bucket_name, Key=archivos_esperados[1])['Body'].read())
    f3 = json.loads(s3_client.get_object(Bucket=bucket_name, Key=archivos_esperados[2])['Body'].read())


    # Limpiamos el bucket
    for ruta in archivos_esperados:
        s3_client.delete_object(Bucket=bucket_name, Key=ruta)
   
    # Creamos un diccionario para acceder a ellos fácilmente por su ID
    diccionario_fragmentos = {"1": f1, "2": f2, "3": f3}
   
    # ENSAMBLADO DEL PAYLOAD
    action = ""
   
    # Recorremos en el orden estricto que necesita tu TFG
    for num in ["1", "2", "3"]:
        frag_body = diccionario_fragmentos[num]
       
        # El contenido viene en base64 desde las Lambdas originales, lo decodificamos a bytes
        raw_bytes = base64.b64decode(frag_body['content'])
       
        # Replicamos la lógica de tu Versión 1: (cambiar a si es binario?)
        if str(frag_body['is_bin']) == "1":
            action += f"payload = {repr(raw_bytes)}\n"
        # Los demás módulos se decodifican a texto normal en utf-8
        else:
            action += raw_bytes.decode('utf-8') + "\n"


    # Volvemos a codificar en base64 todo el bloque de código unido.
    codigo_final = base64.b64encode(action.encode('utf-8')).decode('utf-8')
   
    # Lo empaquetamos en un JSON limpio
    resultado_json = json.dumps({"codigo_final": codigo_final})
   
    # Guardamos el archivo final en el mismo bucket
    s3_client.put_object(
        Bucket=bucket_name,
        Key=payload_final_key,
        Body=resultado_json
    )


    return {"statusCode": 200, "body": "Ensamblaje exitoso."}




def existe_en_s3(bucket, key):
    """
    Función auxiliar para comprobar si un archivo existe.
    Usa 'head_object', que solo lee los metadatos y no descarga el archivo,
    por lo que es mucho más rápido que usar 'get_object'.
    """
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        # Si es otro error, dejamos que el programa falle para darnos cuenta de cual es
        raise
