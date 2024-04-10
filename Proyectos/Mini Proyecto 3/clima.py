import requests

def obtener_clima():
   
    api_key = "3e5f1122769e41889e7201857240704 "
    latitud = 19.4767
    longitud = -70.6864

    url = "https://api.weatherapi.com/v1/current.json?key={}&q={},{}".format(api_key, latitud, longitud)
    respuesta = requests.get(url)


    datos = respuesta.json()

    temperatura = datos["current"]["temp_c"]
    estado_clima = datos["current"]["condition"]["text"]

    return temperatura , estado_clima