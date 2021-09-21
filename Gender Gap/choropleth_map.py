# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# Use ctrl + C to terminate the server, otherwise, it will have error " socket.error: [Errno 48] Address already in use "

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv("gggr_all.csv")


app.layout = html.Div([
dcc.Dropdown(options=[{'label': i, 'value': i} for i in df['type'].unique()]
            ,id='category',multi=False),

    html.Div(id='output_container', children=[]),
    html.Br(),
    dcc.Graph(
        id='map',
        figure={}
    )
])


@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='map', component_property='figure')],
    [Input(component_id='category', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The category chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["type"] == option_slctd]

    fig= px.choropleth(data_frame=dff,
              locations="country",
              locationmode = "country names",
              color="score",
              hover_name="country",
              animation_frame="year",
              color_continuous_scale='RdBu',
              height=600)

    return container, fig

# if __name__ == '__main__':
#     app.run_server(debug=True)