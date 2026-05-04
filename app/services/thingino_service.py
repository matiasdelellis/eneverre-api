import requests

def move(camera, x, y):
    url = f"{camera['thingino_url']}/x/json-motor.cgi?d=g&x={x}&y={y}"
    headers = {'X-API-Key': camera['thingino_api_key']}

    r = requests.get(url, headers=headers, timeout=3)
    return r.json()
