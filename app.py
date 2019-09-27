import aiovk
import features.user_features as uf
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/userfeatures/photos")
def photos_info_by_user():
    photos_info = uf.photos_info_by_user()
    return jsonify(photos_info)


if __name__ == '__main__':
    app.run()
