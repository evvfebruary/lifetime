import aiovk
import features.user_features as uf
import features.weather as wth
from quart import Quart, request, jsonify, send_from_directory
import glob

app = Quart(__name__)


@app.route('/')
async def hello_world():
    return 'Hello World!'


# For realtime handling
# @app.route("/weather")
# async def weather_dashboard():
#     return wth.get_dashboard("denpasar")

@app.route("/weather_dash")
async def weather_dashboard():
    destination = "denpasar"
    return send_from_directory("/home/ubuntu/lifetime/dashboards/weather", f"{destination}_weater")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
