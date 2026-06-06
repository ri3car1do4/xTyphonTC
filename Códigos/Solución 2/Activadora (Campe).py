import boto3
import json


def lambda_handler(event, context):
    """
    Función Lambda activadora de los fragmentos.
    
    """
    
    # Creamos el cliente de Lambda para invocar las funciones
    lc = boto3.client('lambda') 


    # Construimos la prole a liberar (nombres de los fragmentos en AWS Lambda)
    prole = [
        f"Typhon_Cerberus",
        f"Typhon_Scilla",
        f"Typhon_Chimera"
    ]
   
    for monstruo in prole:
        # Invocamos a la funcion lambda correspondiente a cada monstruo
        lc.invoke(FunctionName=monstruo, InvocationType='Event')
   

    exito = f'[SUCCESS] Fragmentos liberados.'
       
    return {
        'statusCode': 200,
        'body': json.dumps({
            'content' : exito
        })
    }
