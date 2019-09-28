import aiovk
import features.user_features as uf
import features.weather as wth
from quart import Quart, request, jsonify

app = Quart(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/weather")
def weather_dashboard():
    return wth.get_dashboard("denpasar")


if __name__ == '__main__':
    app.run()
