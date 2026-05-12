# Eneverre API 🎥
A ~~proof of concept~~ API for an NVR...

The motivation behind this project is to offer a service independent of the different camera manufacturers.

The main idea is to reuse existing services. For example, I don't want to write another rtsp streaming service. Use [mediamtx](https://github.com/bluenviron/mediamtx), [go2rtc](https://github.com/AlexxIT/go2rtc) or [lightNVR](https://github.com/opensensor/lightNVR) for this.

**NOTE:** You can control [Thingino](https://thingino.com/) cameras. I would love to say it supports Onvif, but probably the whole reason for this project is that I can't find anything easy to manage Onvif cameras. 😅

## Friends' projects 🤗
* [Eneverre Android](https://github.com/matiasdelellis/eneverre-android): This is the official Android client. You can view live cameras, recordings, and control PTZ cameras.
* [Eneverre TV](https://github.com/matiasdelellis/eneverre-tv): Client for Android TVs. For now, can only view the live stream.
* [Eneverre Web](https://github.com/matiasdelellis/eneverre-web): Under development, and you can see the cameras and fully control it.

## MediaMTX integration ⏺️
As mentioned previously, we want to reuse the various projects that already exist. This API optionally integrates with [MediaMTX](https://mediamtx.org/), specifically to maintain camera recordings.

On the other hand, probably the main purpose of this API is to securely share the public URLs of the cameras. These are initially configured as rtsp and hls parameters of the configuration files.

When MediaMTX integration is enabled, these URLs are dynamically generated, creating random passwords to enhance security. But if you're not interested in recordings, you can use LightNVR, go2rtc, or simply Caddy as a reverse proxy to expose the cameras to the internet and placing the public URL with basic authentication in the corresponding configuration file.

## Screenshots 😍
This is Eneverre Android Client. 😉

Login | Cameras View | Pip Camera | PTZ Camera | Private Camera | Playback
-- | -- | -- | -- | -- | --
![](https://raw.githubusercontent.com/matiasdelellis/eneverre-docs/refs/heads/main/images/android/eneverre-login.png) | ![](https://raw.githubusercontent.com/matiasdelellis/eneverre-docs/refs/heads/main/images/android/cameras-list.png) | ![](https://raw.githubusercontent.com/matiasdelellis/eneverre-docs/refs/heads/main/images/android/pip-camera.png) | ![](https://raw.githubusercontent.com/matiasdelellis/eneverre-docs/refs/heads/main/images/android/ptz-camera.png) | ![](https://raw.githubusercontent.com/matiasdelellis/eneverre-docs/refs/heads/main/images/android/privacy.png) | ![](https://raw.githubusercontent.com/matiasdelellis/eneverre-docs/refs/heads/main/images/android/playback.png)

