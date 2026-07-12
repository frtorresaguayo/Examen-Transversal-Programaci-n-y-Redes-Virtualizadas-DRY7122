import urllib.parse
import requests

geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
key = "9aac865f-b85e-4f0a-b0c2-892d747889e5"


def geocoding(location, key):
    while location == "":
        location = input("Ingresa la ubicación nuevamente: ")

    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key, "locale": "es"})
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")
        
        if state and country:
            new_loc = name + ", " + state + ", " + country
        elif state:
            new_loc = name + ", " + state
        else:
            new_loc = name

        print("Geocoding URL para " + new_loc + " (" + value + "):\n" + url)
    else:
        lat = lng = "null"
        new_loc = location
        if json_status != 200:
            print("Error " + str(json_status) + ": " + json_data["message"])

    return json_status, lat, lng, new_loc


traduccion_vehiculos = {
    "auto": "car",
    "bici": "bike",
    "pie": "foot"
}


while True:
    print("\n" + "+" * 50)
    print("Perfiles disponibles: auto, bici, pie  (si quieres salir presiona 's')")
    print("+" * 50)

    entrada_usuario = input("Ingresa perfil de vehículo: ").strip().lower()

    if entrada_usuario == "s":
        print("Saliendo del programa. ¡Buen viaje!")
        break

    if entrada_usuario in traduccion_vehiculos:
        vehicle_api = traduccion_vehiculos[entrada_usuario]
        vehicle_print = entrada_usuario
    else:
        vehicle_api = "car"
        vehicle_print = "auto"
        print("Perfil inválido. Se usará 'auto'.")

    loc1 = input("Ciudad de Origen: ").strip()
    if loc1.lower() == "s":
        print("Saliendo del programa. ¡Buen viaje!")
        break
    orig = geocoding(loc1, key)
    if orig[0] != 200 or orig[1] == "null":
        continue

    loc2 = input("Ciudad de Destino: ").strip()
    if loc2.lower() == "s":
        print("Saliendo del programa. ¡Buen viaje!")
        break
    dest = geocoding(loc2, key)
    if dest[0] != 200 or dest[1] == "null":
        continue

    print("=" * 50)

    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle_api, "locale": "es"}) + op + dp
        
        paths_response = requests.get(paths_url)
        paths_status = paths_response.status_code
        paths_data = paths_response.json()

        print("Directions from " + orig[3] + " to " + dest[3] + " by " + vehicle_print)
        print("=" * 50)

        if paths_status == 200:
            km = paths_data["paths"][0]["distance"] / 1000
            litros = km * 0.08
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            minutos = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)

            print("Distancia: {:.2f} km".format(km))
            print("Duración: {:02d} horas, {:02d} minutos, {:02d} segundos".format(hr, minutos, sec))
            print("Combustible estimado: {:.2f} litros".format(litros))
            print("=" * 50)
            print("--- Narrativa del viaje ---")

            for instruccion in paths_data["paths"][0]["instructions"]:
                texto = instruccion["text"]
                distancia = instruccion["distance"] / 1000
                print(" {0} ( {1:.2f} km )".format(texto, distancia))

            print("=" * 50)
        else:
            print("Error en la ruta: " + paths_data["message"])

    print("*" * 50)

