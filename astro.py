from skyfield.api import load,wgs84
import requests

eph = load('./de421.bsp')
terra = eph['earth']
ts = load.timescale()

def buscar_astro(latitude,longitude,nome_astro):
    
    astro = eph[nome_astro]
    
    t = ts.now()
    
    observatory = wgs84.latlon(latitude,longitude,1)
    
    diferenca = terra + observatory 
    astrometrico = diferenca.at(t).observe(astro)
    
    alt, az, distancia = astrometrico.apparent().altaz()

    rastrear(az,alt)
    
    return {"name":nome_astro,"latitude":latitude,"longitude":longitude,"alt":alt.degrees,"az":az.degrees,"distancia":distancia.km}

def rastrear(az,alt):
    try:
        url = f"http://10.13.37.2/mover?az={az.degrees:.2f}&alt={alt.degrees:.2f}"
        requests.get(url, timeout=2)
    except Exception as e:
        print(f"[ESP32] Falha: {e}")
