import aiovk
import features.user_features as uf
from quart import Quart, request, jsonify

app = Quart(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/userfeatures/photos")
async def photos_info_by_user():
    photos = await uf.photos_info_by_user()
    return jsonify(photos)


if __name__ == '__main__':
    app.run()
