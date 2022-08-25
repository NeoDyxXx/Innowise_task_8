from urllib import request
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import requests as req
from collections import defaultdict
import pandas as pd

app = Dash(__name__)

def convert_request_to_df(request):
    request_data = req.get(request).json()['data']
    def_dict = defaultdict(list)
    for item in request_data:
        for key, value in item.items():
            def_dict[key].append(value)
    return pd.DataFrame(def_dict)


parse_data_type_one = convert_request_to_df('http://localhost:5050/get_parse_data_type_one')
parse_data_type_two = convert_request_to_df('http://localhost:5050/get_parse_data_type_two')

parse_data_type_one['return'] = parse_data_type_one['return'].astype('int64')
parse_data_type_two['return'] = parse_data_type_two['return'].astype('int64')

fig_parse_type_one = px.bar(parse_data_type_one, x="departure_name", y="return", orientation='v')
fig_parse_type_two = px.bar(parse_data_type_two, x="departure_name", y="return", orientation='h')

app.layout = html.Div(children=[
    dcc.Graph(
        id='fig_parse_type_one',
        figure=fig_parse_type_one
    ),
    dcc.Graph(
        id='fig_parse_type_two',
        figure=fig_parse_type_two
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)