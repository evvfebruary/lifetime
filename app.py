import aiovk
import features.user_features as uf
import features.weather as wth
import os
from quart import Quart, request, jsonify, send_file
import glob

app = Quart(__name__)
dash_index = 0

@app.route('/wthdash')
async def hello_world():
    global dash_index
    dash_info = ["weather", "sea_temp"]
    form = request.args
    destination = form.get('destination')
    files = []
    for info in dash_info:
        url = f"/home/ubuntu/lifetime/dashboards/{info}/{destination}_{info}.png"
        print(url)
        if os.path.exists(url):
            files.append(url)
    # files = [f"/home/ubuntu/lifetime/dashboards/{info}/{destination}_{info}.png" for info in dash_info if os.path.exists(f"/home/ubuntu/lifetime/dashboards/{info}/{destination}_{info}.png")]
    # dashboard = await send_file(f"/Users/evv/PycharmProjects/lifetime/dashboards/weather/{destination}_weather.png")
    to_return = files[dash_index]
    dash_index += 1
    if len(files) > dash_index - 1:
        dash_index = 0
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
