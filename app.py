import aiovk
import features.user_features as uf
import features.weather as wth
from quart import Quart, request, jsonify, send_file
import glob

app = Quart(__name__)


@app.route('/wthdash')
async def hello_world():
    form = request.args
    destination = form.get('destination')
    # dashboard = await send_file(f"/Users/evv/PycharmProjects/lifetime/dashboards/weather/{destination}_weather.png")
    return await send_file(f"/home/ubuntu/lifetime/dashboards/weather/{destination}_weather.png")
    # return await send_from_directory("/Users/evv/PycharmProjects/lifetime/dashboards/weather", f"{destination}_weater")


# For realtime handling
# @app.route("/weather")
# async def weather_dashboard():
#     return wth.get_dashboard("denpasar")

# @app.route("/wthdash")
# async def weather_dashboard():
#     destination = "denpasar"
#     return await send_from_directory("/Users/evv/PycharmProjects/lifetime/dashboards/weather", f"{destination}_weater")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
