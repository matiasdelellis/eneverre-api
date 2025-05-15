import configparser
import subprocess
import os

from flask import Flask, jsonify, request
from flask_basicauth import BasicAuth


config = configparser.ConfigParser()
config_file = './eneverre.ini'
if os.path.exists('/etc/eneverre/eneverre.ini'):
    config_file = '/etc/eneverre/eneverre.ini'

config.read(config_file)
app_config_user = config['server']['username'];
app_config_pass = config['server']['password'];
app_config_port = config['server']['port'];


app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = app_config_user
app.config['BASIC_AUTH_PASSWORD'] = app_config_pass
basic_auth = BasicAuth(app)


cameras_folder = './cameras.d'
if os.path.exists('/etc/eneverre/cameras.d'):
    cameras_folder = '/etc/eneverre/cameras.d'

cameras = []
for filename in os.listdir(cameras_folder):
    config.read(os.path.join(cameras_folder, filename))
    camera = {
        "id": config['camera']['id'],
        "name": config['camera']['name'],
        "comment": config['camera']['comment'],
        "live": config['camera']['live'],
        "width": config['camera']['width'],
        "height": config['camera']['height'],
        "ptz": config.getboolean('camera', 'ptz'),
        "privacy": False
    }
    cameras.append(camera)


print("Cameras folder: " + cameras_folder)
print ("Found " + str(len(cameras)) + " cameras")


@app.route('/api')
def hello_world():
    return jsonify(message="Hi, I'm a super awesome NVR!!")

@app.route('/api/cameras', methods=['GET'])
@basic_auth.required
def get_cameras():
    return jsonify(cameras)

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

    if not camera['ptz']:
        return jsonify(camera)

    if enable:
        subprocess.check_output(f"thingino-control {camera_id} privacy", shell=True)
    else:
        subprocess.check_output(f"thingino-control {camera_id} home", shell=True)

    camera['privacy'] = enable

    return jsonify(camera)

if __name__ == "__main__":
    app.run(port=app_config_port, debug=True)
