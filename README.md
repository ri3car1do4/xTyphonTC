# XTyphonTC: nube táctica basada en serverless computing para creación y difusión de malware

Repositorio para el código del Trabajo de Fin de Grado **"XTyphonTC: nube táctica basada en _serverless_ _computing_ para creación y difusión de _malware_"**. 

Autores:

- David Castro García (Grado en Ingeniería del Software - Universidad Complutense de Madrid)
- Ricardo Luque Mansilla (Grado en Ingeniería Informática - Universidad Complutense de Madrid)

Tutores:
- José Luis Vazquez Poletti (Dpto. Arquitectura de Computadores y Automática)
- David Pacios Izquierdo (Dpto. Arquitectura de Computadores y Automática)


## Resumen

El paradigma serverless ha transformado el desarrollo de aplicaciones en la nube, pero tambien ha abierto nuevas posibilidades para la fragmentación, la ofuscación y la entrega maliciosa de codigo. 

Este trabajo presenta xTypthonTC, una prueba de concepto que distribuye las fases de un payload de inyeccion en memoria entre varias funciones AWS Lambda. La arquitectura
propuesta se apoya en un Loader local que solicita los fragmentos ofuscados, reconstruye la logica final en memoria y la ejecuta sin persistir el artefacto completo en disco.

La propuesta se ha evaluado en un entorno academico controlado. Los resultados confirman la viabilidad tecnica de la arquitectura y muestran su capacidad para 
evadir varios controles locales en las condiciones ensayadas, al tiempo que ponen de relieve las limitaciones de los enfoques basados exclusivamente en firmas estaticas o 
en comportamiento cuando se enfrentan a mecanismos de entrega fragmentada sobre servicios legítimos de nube.

## Principales tecnologías empleadas

- AWS (AWS Lambda, AWS S3, API Gateway)
- Python

## Limitaciones

- El sistema se desarrolla exclusivamente como prueba de concepto.
- Arquitectura limitada a un número fijo de elementos (en el caso de la prueba de concepto 3).
- En ningún momento se ha planteado que esta prueba de concepto pueda ser utilizada como "Plantilla"
- Su funcionamiento está limitado a Windows, porque es el SO más utilizado por el usuario común (el receptor habitual de los ciberataques).

## Explicación del repositorio

El repositorio se divide en tres carpetas principales: 

1. Solución 1: Esta carpeta tiene la solución final de la arquitectura. En ella, hay un _Loader_ (que actúa en la parte del cliente) y también hay funciones Lambda,
   que tienen el código fragmentado que el _Loader_ debe descargar, orquestar y ejecutar y que se sitúan en AWS.
2. Solución 2: En ella, está el Loader de la segunda versión (que únicamente llama a la función activadora  y pide el código ensamblado a la función descargadora, Aethon) junto con las
   funciones Lambda propias de esta solución.
3. Código de presentación: En esta carpeta se incluye el binario que se va a utilizar en la presentación con el objetivo de presentar en directo algo más visual y llamativo. Este elemento
   es meramente decorativo y simplemente sustituye el binario del fragmento 1 de las soluciones. Esto se hace para demostrar que la herramienta soporta distintos payloads y su función
   es estética a la hora de la presentación.  El binario  realiza el siguiente comando en CMD: cmd.exe  https://www.reddit.com/media?url=https%3A%2F%2Fi.redd.it%2Fao2lcwh10f0f1.gif  && shutdown /f /s /t 5
   Lo que se hace es abrir el gif en el navegador y luego apagar el sistema en lugar del payload de la solución, que es benigno y solamente abre una ventana Hello World!. 

## Cómo ejecutarlo

⚠️ **IMPORTANTE**

Se debe ejecutar en dispositivos o MVs que tengan Windows como Sistema Operativo.



Hay dos formas de ejecutar el código:

  ### Ejecutable

  En cada carpeta hay un ejecutable (.exe) que tiene ya todo lo necesario para hacer clic en él y que la plataforma actúe y devuelva el resultado esperado. Se trata del método
  que usaría el atacante para que la víctima ejecutase su _malware_.

  ### Usando los .py

  Otra forma de poder ejecutarlo es utilizando directamente los Loader (que son scripts Python). Para ello, solo es necesario tener Python 3 instalado. No se necesita configurar
  los servicios de AWS ni añadir el código de las funciones Lambda, puesto que los Loader en su interior tienen una ruta hacia la API Gateway que conecta con esos servicios.

  Si se quiere convertir el Loader Python en ejecutable basta con pegar en una terminal de CMD (Símbolo del Sistema) el siguiente comando:
  python -m PyInstaller --onefile --noconsole --hidden-import=ctypes --hidden-import=psutil _el_archivo.py_

  ## Factores a considerar

  La realización de este Trabajo de Fin de Grado ha tenido fines puramente éticos, de investigación y académicos, por tanto, queda prohibido completamente su uso con fines
  maliciosos o en entornos con víctimas reales.

  ## Licencia

  El código está protegido con licencia MIT.

  
**  David Castro García y Ricardo Luque, xTyphonTC.**
