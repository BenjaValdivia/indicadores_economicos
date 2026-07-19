import requests
import json
import time
from collections import defaultdict

#Config
URL_APPS_SCRIPT = 'https://script.google.com/macros/s/AKfycbxF67geZ8b9YNn-o5sB-swELG1BKxBt6IwXCzIpyvCWkzrYyCeQlKVrkOcVWNyxJsC3Mw/exec'
INDICADORES = ["dolar", 'uf', "euro"]

#Asignamos rango de anios
ANIOS_A_EXTRAER = range(2016,2027)

print("Iniciando Web Scraping")

for indicador in INDICADORES:
    #Agrupamios los valores de un mismo mes
    datos_mensuales = defaultdict(list)

    #Extraemos data
    print(f"Descargando data{indicador.upper()}")
    for anio in ANIOS_A_EXTRAER:
        url_api = f'https://mindicador.cl/api/{indicador}/{anio}'
        respuesta = requests.get(url_api)

        if respuesta.status_code == 200:
            serie = respuesta.json().get('serie',[])
            for dia in serie:
                #Nos quedamos solo con el anio y mes
                mes_anio = dia['fecha'][:7]
                datos_mensuales[mes_anio].append(dia['valor'])

        #Pausa para el consumo de datos de la API
        time.sleep(0.2)

    #Transformamos y Cargamos
    print(f"Promediando y enviando {indicador.upper()} a Sheets")
    for mes, valores in datos_mensuales.items():
        promedio = sum(valores) / len(valores)
        datos = {
            "fecha": f"{mes}-01",
            "indicador": indicador.upper(),
            "valor": round(promedio, 2)
        
        }

        headers = {'Content-Type': 'application/json'}
        requests.post(URL_APPS_SCRIPT, data=json.dumps(datos), headers=headers)    
        time.sleep(0.1)

print('Carga de datos finalizada')