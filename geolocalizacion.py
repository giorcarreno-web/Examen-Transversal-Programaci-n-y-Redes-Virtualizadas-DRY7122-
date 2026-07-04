# geolocalizacion.py
import requests

# API Key de GraphHopper para el cálculo de la ruta
API_KEY = "9b642308-b11c-4b6d-96be-8f3f619e075c"

def obtener_coordenadas(ciudad, pais):
    """Obtiene latitud y longitud usando la API abierta de OpenStreetMap (Nominatim)."""
    headers = {'User-Agent': 'EvaluacionTransversal_DRY7122_StudentApp'}
    url_geocode = f"https://nominatim.openstreetmap.org/search?city={ciudad}&country={pais}&format=json&limit=1"
    
    try:
        response = requests.get(url_geocode, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"]), data[0]["display_name"]
        return None
    except Exception as e:
        print(f"Error al conectar con el servicio de mapas: {e}")
        return None

def calcular_ruta():
    print("==================================================")
    print("   Calculador de Rutas Chile - Perú (DRY7122)   ")
    print("==================================================")
    
    while True:
        ciudad_origen = input("\nIngrese la Ciudad de Origen en Chile (o 's' para salir): ").strip()
        if ciudad_origen.lower() == 's':
            print("Saliendo del programa...")
            break
            
        ciudad_destino = input("Ingrese la Ciudad de Destino en Perú (o 's' para salir): ").strip()
        if ciudad_destino.lower() == 's':
            print("Saliendo del programa...")
            break

        print("\nSeleccione el medio de transporte:")
        print("1) Auto (car)")
        print("2) Bicicleta (bike)")
        print("3) Caminando (foot)")
        opcion = input("Seleccione una opción (1-3): ").strip()
        
        perfiles = {"1": "car", "2": "bike", "3": "foot"}
        medios_es = {"1": "Auto", "2": "Bicicleta", "3": "Caminando"}
        
        if opcion not in perfiles:
            print("Opción inválida. Se utilizará 'Auto' por defecto.")
            opcion = "1"
            
        perfil_transporte = perfiles[opcion]
        
        print("\nBuscando coordenadas de las ciudades...")
        origen_geo = obtener_coordenadas(ciudad_origen, "Chile")
        destino_geo = obtener_coordenadas(ciudad_destino, "Peru")
        
        if not origen_geo or not destino_geo:
            print("No se pudieron encontrar las ubicaciones exactas. Intente de nuevo con otra ciudad.")
            continue
            
        lat1, lng1, nombre_orig = origen_geo
        lat2, lng2, nombre_dest = destino_geo
        
        print(f"-> Origen detectado: {nombre_orig}")
        print(f"-> Destino detectado: {nombre_dest}")
        print("Calculando itinerario de viaje...")
        
        # API de Routing de GraphHopper
        url_route = (
            f"https://graphhopper.com/api/1/route?"
            f"point={lat1},{lng1}&point={lat2},{lng2}"
            f"&profile={perfil_transporte}&locale=es&points_encoded=false&key={API_KEY}"
        )
        
        try:
            response = requests.get(url_route)
            if response.status_code == 200:
                data = response.json()
                ruta = data["paths"][0]
                
                # Datos de distancia y tiempo [cite: 110]
                distancia_km = ruta["distance"] / 1000
                distancia_millas = distancia_km * 0.621371
                
                tiempo_ms = ruta["time"]
                horas = int(tiempo_ms // 3600000)
                minutos = int((tiempo_ms % 3600000) // 60000)
                
                print("\n==================================================")
                print("               RESULTADO DEL VIAJE                ")
                print("==================================================")
                print(f"Medio de transporte: {medios_es[opcion]}")
                print(f"Distancia en Kilómetros: {distancia_km:.2f} km")
                print(f"Distancia en Millas: {distancia_millas:.2f} mi")
                print(f"Duración estimada del viaje: {horas} horas y {minutos} minutos")
                print("==================================================")
                
                # Narrativa del viaje [cite: 111]
                print("\nNarrativa del Viaje (Paso a Paso):")
                print("--------------------------------------------------")
                instrucciones = ruta.get("instructions", [])
                for idx, inst in enumerate(instrucciones, 1):
                    texto = inst["text"]
                    dist_paso = inst["distance"] / 1000
                    print(f"{idx}. {texto} ({dist_paso:.2f} km)")
                print("--------------------------------------------------")
            else:
                print(f"Error en el servicio de rutas (Código {response.status_code}).")
                print("Pruebe con ciudades conectadas por tierra firme (ej: Arica a Tacna).")
        except Exception as e:
            print(f"Error de conexión con la API de rutas: {e}")
            
        print("\n==================================================")

if __name__ == "__main__":
    calcular_ruta()