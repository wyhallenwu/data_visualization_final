import dash
import dash_core_components as dcc
import dash_html_components as html
import data_process.visualize as dv

app = dash.Dash(__name__)

fig1 = dv.line_race()
fig2 = dv.show_pie()
fig3 = dv.close_heatmap()
fig4 = dv.close_earning_rate_scatter()

app = dash.Dash()
app.layout = html.Div(style={"height": "100vh", "weight": "100vh"},
                      children=[dcc.Graph(figure=fig2, style={"height": "inherit"}),
                                dcc.Graph(figure=fig1, style={"height": "inherit"}),
                                dcc.Graph(figure=fig3, style={"height": "inherit"}),
                                dcc.Graph(figure=fig4, style={"height": "inherit"})
                                ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
