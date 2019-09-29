import aiovk
import features.user_features as uf
import features.weather as wth
import os
from quart import Quart, request, jsonify, send_file
import glob
import pathlib

app = Quart(__name__)
dash_index = 0
prev_ond = ''


@app.route('/wthdash')
async def hello_world():
    diving_logo = f"/home/ubuntu/lifetime/dashboards/diving/logo_diving.jpg"
    weather_logo = f"/home/ubuntu/lifetime/dashboards/weather/logo_weather.jpg"
    food_logo = f"/home/ubuntu/lifetime/dashboards/food/logo_food.jpg"
    skiing_logo = f"/home/ubuntu/lifetime/dashboards/skiing/logo_skiing.jpg"

    logos = {"weather": weather_logo,
             "diving": diving_logo,
             "food": food_logo,
             "skiing": skiing_logo}

    global dash_index
    global prev_ond
    dash_info = ["food", "weather", "diving", "skiing"]
    form = request.args
    destination = form.get('destination')
    if prev_ond == '':
        prev_ond = destination
    if prev_ond != destination:
        dash_index = 0
        prev_ond = destination
    files_tmp = []
    for info in dash_info:
        info_file = []
        directory = f"/home/ubuntu/lifetime/dashboards/{info}"
        urls = [each.absolute() for each in pathlib.Path(directory).glob('**/*') if destination in each]
        if len(urls) != 0:
            info_file.insert(0, logos[info])
            files_tmp.append(urls)
    files = [item for sublist in files_tmp for item in sublist]
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
