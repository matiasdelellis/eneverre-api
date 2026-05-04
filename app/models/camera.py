def public(cam):
    return {
        k: v for k, v in cam.items()
        if k not in ('thingino_url', 'thingino_api_key')
    }
