import json
import boto3
from botocore.exceptions import ClientError


# Información de conexión al S3
s3_client = boto3.client('s3')
BUCKET_NAME = 'tfg-typhon-bucket'


def lambda_handler(event, context):
    """
    Función Lambda descargadora.
    
    """

    # Lee el archivo payload_final.json del s3
    file_key = f"payload_final.json"
   
   # Si el arcihvo existe, se lee (contenido en formato json) y se borra del S3 (estrategia de limpieza). Se devuelve la respuesta con codigo 200.
    try:
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
        contenido = json.loads(response['Body'].read().decode('utf-8'))


        s3_client.delete_object(Bucket=BUCKET_NAME, Key=file_key)
       
        return {
            'statusCode': 200,
            'body': json.dumps({
                'codigo_final': contenido['codigo_final']
            })
        }
    
    # Si hay un ClientError, se comprueba si el error es NoSuchKey (archivo no encontrado). En ese caso, se devuelve un mensaje con error 404
    # indicando que se debe esperar y reintentar.
    
    # Si el error no es NoSuchKey, se relanza la excepción para que sea manejada por AWS Lambda y se registre como un error en los logs.
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'content': f'Ensamblando en la nube, reintente.'
                })
            }
        raise