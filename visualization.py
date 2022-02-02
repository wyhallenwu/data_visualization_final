import dash
import dash_core_components as dcc
import dash_html_components as html
import data_process.visualize as dv

app = dash.Dash(__name__)

fig1 = dv.show_ecdf()

app.layout = html.Div(children=[
    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(figure=fig1)
])



if __name__ == '__main__':
    app.run_server(debug=True)
