# eneverre-api

A proof of concept API for an NVR...

The motivation is to provide a client independent of the different camera manufacturers. This client would be [enverre-android](https://github.com/matiasdelellis/eneverre-android), and that would consume the API of this service.

The main idea is to reuse existing services. For example, I don't want to write another rtsp streaming service. Use [mediamtx](https://github.com/bluenviron/mediamtx), [go2rtc](https://github.com/AlexxIT/go2rtc) or [lightNVR](https://github.com/opensensor/lightNVR) for this.

You can control [Thingino](https://thingino.com/) cameras that have PTZ using the [thingino-control](https://github.com/matiasdelellis/thingino-control) project. I would love to say it supports Onvif, but probably the whole reason for this project is that I can't find anything easy to manage Onvif cameras.

## Config
Edit the `eneverre.ini` (or `/etc/eneverre/eneverre.ini`) to configure the user's digest authentication and the port to publish the API.

```
[server]
username = adminuser
password = adminpass
port = 8080
```

To add cameras you must add their definition to ini files inside the `cameras.d` (or `/etc/eneverre/cameras.d`) folder.

```
[camera]
id = camera01
name = Outside
comment = Thingino 360 Camera
live = rtsp://username:password@camera_url:port
width = 1920
height = 1080
ptz = true
```

The most relevant:
* **id:** It can be anything, but it must match the name used in thingino-control if you want to control PTZ.
* **name** and **comment** is just friendly information.
* **Live:** This is the public URL for playing the camera. Security here is the responsibility of mediaMTX, go2rtc, or lightNVR.
* **width** and **height** It is useful to give correct proportion to the reproduction boxes.
* **ptz:** Indicates if the camera has PTZ support. I'll repeat that, although I'd like to expand this, it currently only works with Thigino.

## Run
```
user@nvr:~/eneverre-api$ make serve
flask run
Cameras folder: /etc/eneverre/cameras.d
Found 3 cameras
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8080
Press CTRL+C to quit
```

## API

**Test:**
```
user@nvr:~$ curl -u 'adminuser:adminpass' http://127.0.0.1:8080/api
{
  "message": "Hi, I'm a super awesome NVR!!"
}
```

**Cameras:**
```
user@nvr:~$ curl -u 'adminuser:adminpass' http://127.0.0.1:8080/api/cameras
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
  }
]
```

**move:**
```
user@nvr:~$ curl -X POST -u 'adminuser:adminpass' http://127.0.0.1:8080/api/camera/camera01/ptz/move?x=-30&y=-30"
{"code":200,"result":"success","message":{"status":"1","xpos":"1258","ypos":"857","speed":"900","invert":"0"}}
```

**home:**

```
user@nvr:~$ curl -X POST -u 'adminuser:adminpass' http://127.0.0.1:8080/api/camera/camera01/ptz/home
{"code":200,"result":"success","message":{"status":"0","xpos":"1065","ypos":"800","speed":"900","invert":"0"}}
```

**privacy:**
```
user@nvr:~$ curl -X POST -u 'adminuser:adminpass' http://127.0.0.1:8080/api/camera/camera01/privacy?enable=true
user@nvr:~$ curl -X POST -u 'adminuser:adminpass' http://127.0.0.1:8080/api/camera/camera01/privacy?enable=false
```
NOTE: This is almost the entire reason for the existence of this project, but I can't go into detail here.

**recalibrate:**
```
user@nvr:~$ curl -X POST -u 'adminuser:adminpass' http://127.0.0.1:8080/api/camera/camera01/reset



