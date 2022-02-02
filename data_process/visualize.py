import pandas as pd
import plotly.express as px
import data_process.organise as organise
import numpy as np
import plotly.graph_objects as go

base_path = '../json_dataset'
name_path = '../processed_dataset/cleaned_names.csv'


def show_pie():
    test = organise.OrganiseData(base_path, name_path)

    all_mk = test.get_all_mk()
    all_volume = test.get_all_volume()
    all_close = test.get_all_close()
    result = pd.merge(all_mk, all_volume).merge(all_close)

    result['volume'] = np.log(result['volume'])
    result['close'] = np.log(result['close'])
    percent_data = test.get_percent()

    cleaned_percent = percent_data.iloc[0:9, :].copy(deep=True)
    other_mkc = percent_data.iloc[9:, 1].sum()
    other_per = 1 - percent_data.iloc[:9, 2].sum()
    cleaned_percent.loc[9] = ['other', other_mkc, other_per]

    fig = px.pie(percent_data, names=percent_data['name'], color=percent_data['name'],
                 values=percent_data['percent'])
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    return fig


# decentraland
def show_ecdf():
    dp = organise.OrganiseData(base_path, name_path)
    data = dp.ohlc('decentraland')
    fig = go.Figure()
    fig.add_traces([
        go.Scatter(x=data['Date'], y=data['Open'], mode='lines+markers', name='Open'),
        go.Scatter(x=data['Date'], y=data['Close'], mode='lines+markers', name='Close'),
        go.Scatter(x=data['Date'], y=data['High'], mode='lines+markers', name='High'),
        go.Scatter(x=data['Date'], y=data['Low'], mode='lines+markers', name='Low'),
        ]
    )

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=7,
                         label="7day",
                         step="day",
                         stepmode="backward"),
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    fig.update_layout(hovermode='x unified')

    annotations = []
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                            xanchor='left', yanchor='bottom',
                            text='Decentraland',
                            font=dict(family='Arial',
                                      size=50,
                                      color='rgb(37,37,37)'),
                            showarrow=False))
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                            xanchor='center', yanchor='top',
                            text='Source: CoinMarketCap',
                            font=dict(family='Arial',
                                      size=12,
                                      color='rgb(150,150,150)'),
                            showarrow=False))

    annotations.append(dict(x='2022-02-01', y=2.89, text='High: 2.89',
                       xanchor='left', yanchor='bottom',
                       font=dict(
                           size=20,
                       )))

    annotations.append(dict(x='2021-10-27', y=0.8562, text='High: 0.8562',
                       xanchor='left', yanchor='bottom',
                       font=dict(
                           size=20,
                       )))

    annotations.append(dict(x='2021-10-30', y=4.69, text='High: 4.69',
                       xanchor='left', yanchor='bottom',
                       font=dict(
                           size=20,
                       )))

    annotations.append(dict(x='2021-11-25', y=5.9, text='High: 5.9',
                       xanchor='right', yanchor='top',
                       font=dict(
                           size=20,
                       )))

    fig.update_layout(annotations=annotations)

    return fig

def line_race():
    dp = organise.OrganiseData(base_path, name_path)
    data = dp.ohlc('decentraland')
    trace1 = go.Scatter(x=data['Date'], y=data['Open'], mode='lines+markers', name='Open')
    trace2 = go.Scatter(x=data['Date'], y=data['Close'], mode='lines+markers', name='Close')
    trace3 = go.Scatter(x=data['Date'], y=data['High'], mode='lines+markers', name='High')
    trace4 = go.Scatter(x=data['Date'], y=data['Low'], mode='lines+markers', name='Low')

    frames = [dict(data=[dict(type='scatter',
                              x=data['Date'][:k + 1],
                              y=data['Open'][:k + 1]),
                         dict(type='scatter',
                              x=data['Date'][:k + 1],
                              y=data['Close'][:k + 1]),
                         dict(type='scatter',
                              x=data['Date'][:k + 1],
                              y=data['High'][:k + 1]),
                         dict(type='scatter',
                              x=data['Date'][:k + 1],
                              y=data['Low'][:k + 1]),
                         ],
                   traces=[0, 1, 2, 3],
                   ) for k in range(1, len(data['Date']) - 1)]

    layout = go.Layout(
                       showlegend=False,
                       hovermode='x unified',
                       updatemenus=[
                           dict(
                               type="buttons",
                               direction="down",
                               buttons=list([
                                   dict(
                                       args=[{"yaxis.type": "linear"}],
                                       label="LINEAR",
                                       method="relayout"
                                   ),
                                   dict(label='Play',
                                        method='animate',
                                        args=[None,
                                              dict(frame=dict(duration=60,
                                                              redraw=False),
                                                   transition=dict(duration=0),
                                                   fromcurrent=True,
                                                   mode='immediate')]
                                        )
                               ]),
                           ),
                       ])


    # layout.update(xaxis=dict(range=['2021-10-03', '2022-02-05'], autorange=False),
    #               yaxis=dict(range=[0, 6], autorange=False))
    fig = go.Figure(data=[trace1, trace2, trace3, trace4], frames=frames, layout=layout)

    annotations = []
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                            xanchor='left', yanchor='bottom',
                            text='Decentraland',
                            font=dict(family='Arial',
                                      size=50,
                                      color='rgb(37,37,37)'),
                            showarrow=False))
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                            xanchor='center', yanchor='top',
                            text='Source: CoinMarketCap',
                            font=dict(family='Arial',
                                      size=12,
                                      color='rgb(150,150,150)'),
                            showarrow=False))

    annotations.append(dict(x='2022-02-01', y=2.89, text='High: 2.89',
                            xanchor='left', yanchor='bottom',
                            font=dict(
                                size=20,
                            )))

    annotations.append(dict(x='2021-10-27', y=0.8562, text='High: 0.8562',
                            xanchor='left', yanchor='bottom',
                            font=dict(
                                size=20,
                            )))

    annotations.append(dict(x='2021-10-30', y=4.69, text='High: 4.69',
                            xanchor='left', yanchor='bottom',
                            font=dict(
                                size=20,
                            )))

    annotations.append(dict(x='2021-11-25', y=5.9, text='High: 5.9',
                            xanchor='right', yanchor='top',
                            font=dict(
                                size=20,
                            )))
    fig.update_layout(annotations=annotations)
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=7,
                         label="7day",
                         step="day",
                         stepmode="backward"),
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    fig.show()

def line_races():
    data_prepare = organise.OrganiseData(base_path, name_path)
    dataset = data_prepare.ohlc('decentraland')
    dataset['Date_parsed'] = dataset['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    print(dataset)
    fig = px.scatter(dataset, x='Date_parsed', y='Open', animation_frame=dataset['Date_parsed'])
    fig.show()


line_races()

