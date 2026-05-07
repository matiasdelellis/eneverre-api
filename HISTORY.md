# Project History

## Some context, explanation or catharsis 🙈😅
We have a house which we don't live in permanently, and therefore we have an alarm and cameras... and here the sequence begins... 🙈

1. My couple's friends get scared because there's a camera in the dining room, so they hide, unplug, or break my camera. 😞
2. I bought a Wyze Cam Pan V3 clone camera that can be hidden in a nice way to show that it is not recording. 😬
3. I want to use it together with my other Tp Link Tapo cameras. Impossible!. 🤦
4. I found [LightNVR](https://github.com/opensensor/lightNVR) and love that. 😄
5. I created the [LightNVR android](https://github.com/matiasdelellis/lightNVR-viewer-android) project, to see all the cameras. 😄
6. Great, now I have to control the movements of this camera and activate privacy mode. 🤔
   Well.. I'm searching the internet for a simple project to control these cameras via Onvif. Impossible!. 😞
7. I found the [Thingnino](https://thingino.com/) project and fell in love again!. ❤️
8. I installed it on this camera and it works great. 😄 ...but has no concept of privacy..
   Maybe [one](https://github.com/themactep/thingino-firmware/issues/290) day..
   **NOTE:** This day has arrived... we have [privacy mode](https://github.com/themactep/thingino-firmware/pull/736#issuecomment-3689167715) in thingino. 😃
9. Ok, It seems to support onvif, maybe I can simulate it. Impossible, I prefer to read the 795 pages of ISAPI documentation for Hikvision, which is more understandable. 😞
10. Let's see how to move the camera from the administration panel? Ohhhh.. A GET call with Digest authentication. I can do that!. 😄
    It's as simple as this: `curl -s http://USERNAME:PASSWORD@THINGINO_IP/x/json-motor.cgi?d=g&x=DX&y=DY` 😙
    Well, do we really need Onvif? That's how [thingino-control](https://github.com/matiasdelellis/thingino-control) was born with 34 lines of bash. 😅
    **NOTE:** Thingino control was deprecated since Thingino added control tokens which are much better.
12. In the meantime, I abandoned LightNVR and migrated to [MediaMTX](https://mediamtx.org/) to exposing the cameras to the Internet and making recordings.
13. Does it make sense to keep the other client I wrote? Well, lightNVR isn't going to control the motors, so we built a simple API that puts everything together.
14. This is how this project was born with just 95 lines of code in Python. 🎉

Well, Much to do, but it does the minimum I need
* A simple Android app where my couple and I can see all the cameras.
* Being able to control my Thingino cameras.
* Let the camera hide itself in a friendly way when my couple's friends come over.

I hope you like it... 😃
