import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Get data
glassdoor_data=pd.read_csv("Glassdoor Gender Pay Gap.csv")


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


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


page_1_layout = html.Div([
    html.H1('Page 1'),
    html.Div([
        html.Div([
            html.H3('Education'),
            dcc.Graph(id='g1', figure=fig1)
        ], className="six columns"),

        html.Div([
            html.H3('Eval'),
            dcc.Graph(id='g2', figure=fig2)
        ], className="six columns"),
    ], className="row"),
    html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/choropleth_map'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])




# if __name__ == '__main__':
#     app.run_server(debug=True)