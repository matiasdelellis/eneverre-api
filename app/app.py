from flask import Flask
from flask_cors import CORS

from app.db import close_db
from app.db_init import init_db

from app.routes.health import bp as health_bp
from app.routes.cameras import bp as cameras_bp
from app.routes.ptz import bp as ptz_bp
from app.routes.playback import bp as playback_bp
from app.routes.auth_api import bp as auth_api_bp
from app.routes.users import bp as users_bp
from app.routes.device_auth import bp as device_auth_bp

init_db()

app = Flask(__name__)
CORS(app)

app.register_blueprint(health_bp)
app.register_blueprint(cameras_bp)
app.register_blueprint(ptz_bp)
app.register_blueprint(playback_bp)
app.register_blueprint(auth_api_bp)
app.register_blueprint(device_auth_bp)

app.register_blueprint(users_bp)

app.teardown_appcontext(close_db)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
