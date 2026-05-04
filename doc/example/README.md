# Config

## eneverre.ini
Edit the `data/eneverre.ini` (or `/etc/eneverre/eneverre.ini`) to configure the
user's digest authentication and the port to publish the API. Integration with
mediaMTX is optional and allows us to play recordings.

```
[server]
username = adminuser
password = adminpass
port = 8080

;mediamtx_server = mediamtx.server.com
;mediamtx_rtsp_port' = 8554
;mediamtx_playback_port = 9996
```

## [camera_name].ini
To add cameras you must add their definition to ini files inside the
`data/cameras.d` (or `/etc/eneverre/cameras.d`) folder.

```
[camera]
id = camera01
name = Outside
comment = Thingino 360 Camera
live = rtsp://username:password@camera_url:port
playback = true
ptz = true
width = 1920
height = 1080
```

## The most relevant:
 * **id:** Id of camera that match with MediaMTX if use this integration.
 * **name:** Friendly info
 * **comment:** Friendly info
 * **live:* This is the public URL for playing the camera. Security here is the
   responsibility of mediaMTX, go2rtc, or lightNVR. In particular, if you use
   the integration with MediaMTX, this option is ignored since it will be
   dynamically generated with the configuration and a random username and
   password to improve security.
 * **playback:** This option inform to clients that this camera supports
   recording via MediaMTX. Without this integration, this option is ignored.
 * **ptz:** Indicates if the camera has PTZ support. I'll repeat that, although
   I'd like to expand this, it currently only works with Thigino.
 * **width:** Is useful to give correct proportion to the reproduction boxes.
 * **height** Is useful to give correct proportion to the reproduction boxes.
