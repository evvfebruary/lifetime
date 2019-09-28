import plotly
import requests
import calendar
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots


plotly.io.orca.config.executable = "/home/ubuntu/anaconda3/bin/orca"
pio.orca.config.save()


def get_historical_data(destination, year=2018):
    wth_key = "ORBhhIoK"
    # Static dict for station ( MVP style )
    station_city = {"denpasar": '97230',
                    "courshavel": '06700',
                    "phuket": '48564',
                    "verona": '16090'}
    wth_data_monthly = f"https://api.meteostat.net/v1/history/monthly?station={station_city[destination]}&start={year}-01&end={year}-12&key={wth_key}"
    wth_data = requests.get(wth_data_monthly).json()['data']
    stats = {"months": [], "tmp_mean": [], "raindays": []}
    for stat in wth_data:
        stats["months"].append(calendar.month_name[int(stat['month'].split("-")[-1])])
        stats["tmp_mean"].append(float(stat['temperature_mean']))
        stats["raindays"].append(int(stat['raindays']))
    return stats


def get_dashboard(destination):
    weather_data = get_historical_data(destination)
    fig = make_subplots(
        rows=2, cols=1,
        specs=[[{"type": "xy"}],
               [{"type": "xy"}]],
        subplot_titles=("Mean temperatures", "Raindays cont"),
    )
    x = weather_data['months']
    fig.add_trace(go.Scatter(x=x,
                             y=weather_data['tmp_mean']),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=x,
                             y=weather_data['raindays'], ),
                  row=2, col=1)

    fig.update_layout(height=700, width=700, showlegend=False)
    fig.update_yaxes(title_text="Raindays count", row=1, col=1)
    fig.update_yaxes(title_text="C*", row=2, col=1)

    return fig.write_image("tst.png")
