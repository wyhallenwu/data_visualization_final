import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objs as go

app = dash.Dash(__name__)

data = pd.read_csv('./processed_dataset/marketcap_close.csv')
name = data.iloc[:, 0]
close = data.iloc[:, 1]
marketcap = data.iloc[:, 2]
close = np.log(close)
marketcap = np.log(marketcap)

# fig = go.Figure(data=[go.Scatter(x=marketcap, y=close)])
fig = px.scatter(x=close, y=marketcap, hover_name=name)

app.layout = html.Div(children=[
    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(figure=fig)
])



if __name__ == '__main__':
    app.run_server(debug=True)
