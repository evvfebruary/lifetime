import aiovk
import features.user_features as uf
import features.weather as wth
import os
from quart import Quart, request, jsonify, send_file
import glob

app = Quart(__name__)
dash_index = 0
prev_ond = ''


@app.route('/wthdash')
async def hello_world():
    weather_logo = f"/home/ubuntu/lifetime/dashboards/weather/logo_weather.jpg"
    global dash_index
    global prev_ond
    dash_info = ["weather", "sea_temp"]
    form = request.args
    destination = form.get('destination')
    if prev_ond == '':
        prev_ond = destination
    if prev_ond != destination:
        dash_index = 0
    files = []
    for info in dash_info:
        if info == "weather":
            files.append(weather_logo)
        url = f"/home/ubuntu/lifetime/dashboards/{info}/{destination}_{info}.png"
        print(url)
        if os.path.exists(url):
            files.append(url)
    # files = [f"/home/ubuntu/lifetime/dashboards/{info}/{destination}_{info}.png" for info in dash_info if os.path.exists(f"/home/ubuntu/lifetime/dashboards/{info}/{destination}_{info}.png")]
    # dashboard = await send_file(f"/Users/evv/PycharmProjects/lifetime/dashboards/weather/{destination}_weather.png")
    if dash_index > len(files) - 1:
        dash_index = 0
    to_return = files[dash_index]
    dash_index += 1
    print(files, dash_index, to_return)
    return await send_file(to_return)
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
