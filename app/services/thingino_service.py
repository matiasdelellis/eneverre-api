import requests

def move(host, api_key, x, y):
    url = f"{host}/x/json-motor.cgi?d=g&x={x}&y={y}"
    headers = {'X-API-Key': api_key}

    r = requests.get(url, headers=headers, timeout=3)
    return r.json()
