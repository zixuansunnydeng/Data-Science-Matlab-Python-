import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Get data
glassdoor_data=pd.read_csv("Glassdoor Gender Pay Gap.csv")
df = pd.read_csv("gggr_all.csv")

# Data preprocessing
glassdoor_data['TotalPay']=glassdoor_data['BasePay']+glassdoor_data['Bonus']
gender_ed_dept_pay=glassdoor_data.groupby(['Dept','Education','PerfEval','Gender'],axis=0,as_index=False).mean()
gender_ed_dept_pay['PerfEval'] = gender_ed_dept_pay.PerfEval.astype('category')


# Plots
fig1 = px.sunburst(gender_ed_dept_pay, path=['Dept','Education','Gender'], values='TotalPay',
                 color='TotalPay', color_continuous_scale='Blues',title="Earning disparity in levels of education",
                  labels={"TotalPay":'Average Total Pay'})
#fig1.show()
#
# Fig 2
fig2 = px.sunburst(gender_ed_dept_pay, path=['Dept','PerfEval','Gender'], values='TotalPay',
                 color='TotalPay', color_continuous_scale='amp',title="Earning disparity in levels of Performance",
                  labels={"TotalPay":'Average Total Pay'})
#fig2.show()




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Income', children=[
        html.H1('Is there gender gap in income?'),
            html.Div([
                #html.H1('Is there gender gap in income'),
                html.Div([
                    #html.H1('Is there gender gap in income'),
                    html.H3('Education'),
                    dcc.Graph(id='g1', figure=fig1)
                ], className="six columns"),

                html.Div([
                    html.H3('Eval'),
                    dcc.Graph(id='g2', figure=fig2)
                ], className="six columns"),
            ], className="row")
        ]),
        dcc.Tab(label='World Gender Equality', children=[
        html.H1('Gender Equality Score in the World?'),
            html.Div([
                dcc.Dropdown(options=[{'label': i, 'value': i} for i in df['type'].unique()]
                             , id='category', multi=False),

                html.Div(id='output_container', children=[]),
                html.Br(),
                dcc.Graph(
                    id='map',
                    figure={}
                )
            ])
        ]),
    ])
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


if __name__ == '__main__':
    app.run_server(debug=True)