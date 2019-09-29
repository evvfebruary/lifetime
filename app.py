import aiovk
import features.user_features as uf
import features.weather as wth
import os
from quart import Quart, request, jsonify, send_file
import glob
import pathlib
import prediction.image_tagging as pr_img
import prediction.lda_topics as pr_lda

USERS_CACHING = {}

app = Quart(__name__)
app.config['JSON_AS_ASCII'] = False
dash_index = 0
prev_ond = ''

USERS_FEATURES = {}

CARDS_STACK = {
    "diving": [{"src": 'courshevel.jpg', "name": 'Courchevel', "country": "France"}],
    "skiing": [{"src": 'denpasar.jpg', "name": 'Denpasar', "country": "Indonesia"}],
    "default": [{"src": 'madrid.jpg', "name": 'Madrid', "country": "Spain"},
                {"src": 'barsa.jpg', "name": 'Barcelona', "country": "Spain"},
                {"src": 'sochi.jpg', "name": 'Sochi', "country": "Indonesia"}]
}


@app.route("/user_features")
async def user_features_cus():
    global USERS_FEATURES
    form = request.args
    user_id = form.get('user_id')
    if user_id in USERS_FEATURES:
        return jsonify(USERS_FEATURES[user_id])
    urls = await uf.photos_info_by_user(user_id=user_id)
    result_features, url_predict = pr_img.summarize_user_interests(urls, user_id)
    USERS_FEATURES[user_id] = result_features
    return jsonify({"sum": result_features, "links": url_predict})


@app.route("/cards")
async def user_cards():
    form = request.args
    user_id = form.get('user_id')
    playable = USERS_FEATURES[user_id]["interests_playable"]
    cards = []
    print(user_id, playable)
    for key in playable.keys():
        cards += CARDS_STACK[key]
    print(cards)
    return jsonify(cards)


@app.route("/user_features_all")
async def user_features_all():
    global USERS_FEATURES
    form = request.args
    user_id = form.get('user_id')
    if user_id in USERS_FEATURES:
        return jsonify(USERS_FEATURES[user_id])
    for_lda = await uf.group_txt_photos_by_user(user_id)
    for_image = await uf.photos_info_by_user(user_id=user_id)
    for each in for_lda:
        for_image += each["post_photos"]
    # print(urls)
    img_results, url_predict = pr_img.summarize_user_interests(for_image, user_id)
    lda_results = pr_lda.group_topics(for_lda)
    features_results = {"lda_results": lda_results, "img_url": url_predict, "img_results": img_results}
    interests = {}
    interests["default"] = True
    ### Call it euristic threshold
    skii_intents = ["лыж", "сноу"]
    dive_intents = ["дайв"]
    for interest in lda_results:
        for ski_int, dive_int in zip(skii_intents, dive_intents):
            if ski_int in interest:
                interests["diving"] = True
            if dive_int in interest:
                interests["skiiing"] = True
    features_results["interests_playable"] = interests
    USERS_FEATURES[user_id] = features_results
    return jsonify(features_results)


@app.route('/wthdash')
async def dashboards_info():
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
    user_id = form.get('destination')
    if prev_ond == '':
        prev_ond = destination
    if prev_ond != destination:
        dash_index = 0
        prev_ond = destination
    files_tmp = []
    for info in dash_info:
        directory = f"/home/ubuntu/lifetime/dashboards/{info}"
        print(destination)
        urls = [str(each.absolute()) for each in pathlib.Path(directory).glob('**/*') if
                destination in str(each.absolute())]
        print(urls)
        if len(urls) != 0:
            urls.insert(0, logos[info])
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
