import os
import subprocess
import string
import random
import configparser
from flask import Flask, jsonify, request, Response
from flask_basicauth import BasicAuth
import requests
import urllib.parse


"""
Read config
"""
config = configparser.ConfigParser()
config_file = './eneverre.ini'
if os.path.exists('/etc/eneverre/eneverre.ini'):
    config_file = '/etc/eneverre/eneverre.ini'

config.read(config_file)
app_config_user = config['server']['username']
app_config_pass = config['server']['password']
app_config_port = config['server']['port']

app_config_mediamtx_server = config['server'].get('mediamtx_server', None)
app_config_mediamtx_rtsp_port = config['server'].get('mediamtx_rtsp_port', "8554")
app_config_mediamtx_playback_port = config['server'].get('mediamtx_playback_port', "9996")


"""
Helpers for MediaMTX integration.
"""
def generate_username(length):
    characters = string.ascii_letters
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def generate_password(length):
    characters = string.ascii_letters + string.digits + "¡_-*+,.!"
    password = ''.join(random.choice(characters) for i in range(length))
    return password

if app_config_mediamtx_server is not None:
    mediamtx_username = generate_username(8)
    mediamtx_password = generate_password(8)

def get_live_url(camera):
    if app_config_mediamtx_server is None:
        return camera['live']

    camera_id = camera['id']
    return f"rtsp://{mediamtx_username}:{mediamtx_password}@{app_config_mediamtx_server}:{app_config_mediamtx_rtsp_port}/{camera_id}"

def has_playback(camera):
    if app_config_mediamtx_server is None:
        return False

    return camera.getboolean('playback', False)


"""
Get the list of cameras
"""
cameras_folder = './cameras.d'
if os.path.exists('/etc/eneverre/cameras.d'):
    cameras_folder = '/etc/eneverre/cameras.d'

cameras = []
for filename in os.listdir(cameras_folder):
    config.read(os.path.join(cameras_folder, filename))
    camera_conf = config['camera']
    camera = {
        "id": camera_conf['id'],
        "name": camera_conf['name'],
        "comment": camera_conf['comment'],
        "live": get_live_url(camera_conf),
        "width": camera_conf['width'],
        "playback": has_playback(camera_conf),
        "ptz": camera_conf.getboolean('ptz', False),
        "height": camera_conf['height'],
        "privacy": False
    }
    cameras.append(camera)

print("Cameras folder: " + cameras_folder)
print ("Found " + str(len(cameras)) + " cameras")


"""
And here is the API..
"""
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = app_config_user
app.config['BASIC_AUTH_PASSWORD'] = app_config_pass
basic_auth = BasicAuth(app)


@app.route('/api')
@basic_auth.required
def hello_world():
    return jsonify(message="Hi, I'm a super awesome NVR!!")

@app.route('/api/cameras', methods=['GET'])
@basic_auth.required
def get_cameras():
    return jsonify(cameras)


"""
PTZ control and privacy features only work for Thingino cameras.
See:
 * https://github.com/matiasdelellis/thingino-control
"""
@app.route('/api/camera/<string:camera_id>/ptz/<string:action>', methods=['POST'])
@basic_auth.required
def ptz_camera(camera_id, action):
    camera = next((camera for camera in cameras if camera["id"] == camera_id), None)
    if camera is None:
        return jsonify({"error": "Camera not found"}), 404
    if not camera['ptz']:
        return jsonify({"error": "Camera does not support PTZ control"}), 404

    x = request.args.get('x', 0);
    y = request.args.get('y', 0);

    return subprocess.check_output(f"thingino-control {camera_id} {action} {x} {y}", shell=True)

@app.route('/api/camera/<string:camera_id>/privacy', methods=['POST'])
@basic_auth.required
def privacy_camera(camera_id):
    camera = next((camera for camera in cameras if camera["id"] == camera_id), None)
    if camera is None:
        return jsonify({"error": "Camera not found"}), 404

    enable = (request.args.get('enable') == 'true')

    camera['privacy'] = enable

    if not camera['ptz']:
        return jsonify(camera)

    if enable:
        subprocess.check_output(f"thingino-control {camera_id} privacy", shell=True)
    else:
        subprocess.check_output(f"thingino-control {camera_id} home", shell=True)

    return jsonify(camera)

"""
The next section is specific to the integration with MediaMTX.
In particular, it uses HTTP-based authentication to try to improve the security
of RTSP streams by generating random passwords.
See:
 * https://github.com/bluenviron/mediamtx?tab=readme-ov-file#http-based
"""
@app.route('/api/auth', methods=['POST'])
def auth_api():
    if app_config_mediamtx_server is None:
        return jsonify({"error": "Not Found"}), 404

    username = request.json.get('user')
    if not username:
        return jsonify(message="Unauthorized"), 401
    password = request.json.get('password')
    if not password:
        return jsonify(message="Unauthorized"), 401

    if mediamtx_username == username and mediamtx_password == password:
        return jsonify(message="Authorized"), 200
    else:
        return jsonify(message="Unauthorized"), 401

"""
This is the integration with MediaMTX recordings.
Note that it obviously depends on MediaMTX, but also on the configuration of each camera.
"""
@app.route('/api/camera/<string:camera_id>/playback/list', methods=['GET'])
@basic_auth.required
def playback_list(camera_id):
    if app_config_mediamtx_server is None:
        return jsonify({"error": "Not Found"}), 404

    camera = next((camera for camera in cameras if camera["id"] == camera_id), None)
    if camera is None:
        return jsonify({"error": "Camera not found"}), 404

    if not camera["playback"]:
        return jsonify({"error": "Not found"}), 404

    response = requests.get(f"http://{mediamtx_username}:{mediamtx_password}@localhost:{app_config_mediamtx_playback_port}/list?path={camera_id}")
    response.raise_for_status()

    return Response(response.content, response.status_code, content_type = response.headers['content-type'])

@app.route('/api/camera/<string:camera_id>/playback/get', methods=['GET'])
@basic_auth.required
def playback_get(camera_id):
    if app_config_mediamtx_server is None:
        return jsonify({"error": "Not Found"}), 404

    start = request.args.get('start')
    if not start:
        return jsonify({"error": "Bad Request"}), 400

    duration = request.args.get('duration')
    if not duration:
        return jsonify({"error": "Bad Request"}), 400

    camera = next((camera for camera in cameras if camera["id"] == camera_id), None)
    if camera is None:
        return jsonify({"error": "Camera not found"}), 404

    if not camera["playback"]:
        return jsonify({"error": "Not found"}), 404

    """
    FIXME: The idea is not to expose more ports than the minimum necessary. So,
    here here we are getting the recordings locally and sending the video file.
    Can this cause problems? The files are small, But to say the least, it's
    probably inefficient.
    """
    base_url = f"http://{mediamtx_username}:{mediamtx_password}@{app_config_mediamtx_server}:{app_config_mediamtx_playback_port}/get/?"
    url_params = {
        "path": camera_id,
        "start": start,
        "duration": duration,
        "format": "mp4"
    }

    response = requests.get(base_url + urllib.parse.urlencode(url_params))
    response.raise_for_status()

    return Response(response.content, response.status_code, content_type = response.headers['content-type'])


"""
Run flask server...
"""
if __name__ == "__main__":
    app.run(port=app_config_port, debug=True)
