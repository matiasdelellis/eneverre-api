# Config

## Server config
The main configuration is just an `eneverre.ini` file and another ini file for each camera definition.  Look at the [examples](/doc/example), it's quite easy.

## User management
By default, it creates an administrator user named `Admin` with the password `enverre`.
Then, the user management is done via the command line using the [manage_users.py](/cmd/manage_users.py) script.

``` bash
$ ./manage_users.py 
usage: manage_users.py [-h] {list,create,passwd,role,delete} ...

Manage users

positional arguments:
  {list,create,passwd,role,delete}

options:
  -h, --help            show this help message and exit

```

## API

### Test
``` bash
user@nvr:~$ curl -u 'Admin:eneverre' http://127.0.0.1:8080/api
{
  "message": "Hi, I'm a super awesome NVR!!"
}
```

### Cameras
``` bash
user@nvr:~$ curl -u 'Admin:eneverre' http://127.0.0.1:8080/api/cameras
[
  {
    "comment": "Thingino 360 Camera",
    "height": "1080",
    "id": "camera01",
    "live": "rtsp://username:password@camera_url:port",
    "name": "Outside",
    "privacy": false,
    "ptz": false,
    "width": "1920"
  },
  {
    ...
  }
]
```

### Move
``` bash
user@nvr:~$ curl -X POST -u 'Admin:eneverre' http://127.0.0.1:8080/api/camera/camera01/ptz/move?x=-30&y=-30"
{"code":200,"result":"success","message":{"status":"1","xpos":"1258","ypos":"857","speed":"900","invert":"0"}}
```

### Home
``` bash
user@nvr:~$ curl -X POST -u 'Admin:eneverre' http://127.0.0.1:8080/api/camera/camera01/ptz/home
{"code":200,"result":"success","message":{"status":"0","xpos":"1065","ypos":"800","speed":"900","invert":"0"}}
```

### Privacy
``` bash
user@nvr:~$ curl -X POST -u 'Admin:eneverre' http://127.0.0.1:8080/api/camera/camera01/privacy?enable=true
user@nvr:~$ curl -X POST -u 'Admin:eneverre' http://127.0.0.1:8080/api/camera/camera01/privacy?enable=false
```

### Recalibrate
``` bash
user@nvr:~$ curl -X POST -u 'Admin:eneverre' http://127.0.0.1:8080/api/camera/camera01/reset
```

## MediaMTX Integration API

### List recordings
``` bash
user@nvr:~$ curl -u 'Admin:eneverre' http://127.0.0.1:8080/api/camera/camera01/playback/list" | jq .
[
  {
    "start": "2025-05-22T21:03:27.242037-03:00",
    "duration": 45740.130479
  },
  {
    ...
  }
]
```

### Get recording
``` bash
user@nvr:~$ curl -u 'Admin:eneverre' http://127.0.0.1:8080/api/camera/camera01/playback/get?start=2025-05-27T02:48:44-03:00&duration=60.0" -o recording.mp4
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 4834k  100 4834k    0     0   392k      0  0:00:12  0:00:12 --:--:-- 1089k
```
