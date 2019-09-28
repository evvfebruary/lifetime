import aiovk
import features.user_features as uf
import features.weather as wth
from quart import Quart, request, jsonify

app = Quart(__name__)


@app.route('/')
async def hello_world():
    return 'Hello World!'


@app.route("/weather")
async def weather_dashboard():
    return wth.get_dashboard("denpasar")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
