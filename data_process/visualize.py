import pandas as pd
import plotly.express as px
import data_process.organise as organise
import numpy as np
import plotly.graph_objects as go

base_path = './json_dataset'
name_path = './processed_dataset/cleaned_names.csv'


def show_pie():
    test = organise.OrganiseData(base_path, name_path)
    percent_data = test.get_percent()

    fig = px.pie(percent_data, names='name', color='name',
                 values='percent', title='Percent: ', hole=0.5)
    fig.update_traces(textposition='inside', textinfo='label+percent')
    fig.update_layout(uniformtext_minsize=14, uniformtext_mode='hide')
    fig.update_layout(
        title='市场占比',
        titlefont=dict(size=30)
    )
    return fig


def line_race():
    dp = organise.OrganiseData(base_path, name_path)
    data = dp.ohlc('decentraland')
    trace1 = go.Scatter(x=data['Date'], y=data['Open'], mode='lines+markers', name='Open')
    trace2 = go.Scatter(x=data['Date'], y=data['Close'], mode='lines+markers', name='Close')
    trace3 = go.Scatter(x=data['Date'], y=data['High'], mode='lines+markers', name='High')
    trace4 = go.Scatter(x=data['Date'], y=data['Low'], mode='lines+markers', name='Low')

    frames = [dict(data=[dict(type='scatter',
                              x=data['Date'][::-1][:k + 1],
                              y=data['Open'][::-1][:k + 1]),
                         dict(type='scatter',
                              x=data['Date'][::-1][:k + 1],
                              y=data['Close'][::-1][:k + 1]),
                         dict(type='scatter',
                              x=data['Date'][::-1][:k + 1],
                              y=data['High'][::-1][:k + 1]),
                         dict(type='scatter',
                              x=data['Date'][::-1][:k + 1],
                              y=data['Low'][::-1][:k + 1]),
                         ],
                   traces=[0, 1, 2, 3],
                   ) for k in range(1, len(data['Date']) - 1)]

    layout = go.Layout(
        showlegend=True,
        hovermode='x unified',

        xaxis=dict(title='date',  # 设置坐标轴的标签
                   titlefont=dict(size=20),
                   tickfont=dict(size=18, ),
                   # tickangle=45,  # 刻度旋转的角度
                   showticklabels=True,  # 是否显示坐标轴
                   # 刻度的范围及刻度
                   # autorange=False,
                   # range=pd.date_range('2021-10-05', '2022-02-01').strftime('%Y-%m-%d').tolist(),
                   # type='linear',
                   ),

        # y轴的刻度和标签
        yaxis=dict(title='price',  # 坐标轴的标签
                   titlefont=dict(size=18),  # 坐标轴标签的字体及颜色
                   tickfont=dict(size=20),  # 刻度的字体大小及颜色
                   showticklabels=True,  # 设置是否显示刻度
                   # tickangle=-45,
                   # 设置刻度的范围及刻度
                   autorange=True,
                   # range=[0, 100],
                   # type='linear',
                   ),

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
                    dict(
                        args=[{"yaxis.type": "log"}],
                        label="LOG",
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

    return fig

def close_heatmap():
    test = organise.OrganiseData(base_path, name_path)
    nameset = test.get_name_set()
    close = []
    category = []
    remove_name = ['illuvium', 'monavale', 'decentral games old', 'gamefi', 'axie infinity']
    for name in nameset.iloc[:10, 0]:
        if not name in remove_name:
            dataset = test.ohlc(name)[::-1]
            close.append(dataset.iloc[:, 3])
            category.append(name)

    layout = go.Layout(title='Heatmap(date-kind-close)', titlefont=dict(size=40),
                       xaxis=dict(title='日期',  # 设置坐标轴的标签
                                  titlefont=dict(size=20),
                                  tickfont=dict(size=18, ),
                                  # tickangle=45,  # 刻度旋转的角度
                                  showticklabels=True,  # 是否显示坐标轴
                                  # 刻度的范围及刻度
                                  # autorange=False,
                                  # range=pd.date_range('2021-10-05', '2022-02-01').strftime('%Y-%m-%d').tolist(),
                                  # type='linear',
                                  ),

                       # y轴的刻度和标签
                       yaxis=dict(title='类名',  # 坐标轴的标签
                                  titlefont=dict(size=18),  # 坐标轴标签的字体及颜色
                                  tickfont=dict(size=20),  # 刻度的字体大小及颜色
                                  showticklabels=True,  # 设置是否显示刻度
                                  # tickangle=-45,
                                  # 设置刻度的范围及刻度
                                  autorange=True,
                                  # range=[0, 100],
                                  # type='linear',
                                  ),
                       )

    fig = go.Figure(data=go.Heatmap(
        z=np.log2(close),
        y=category,
        colorscale='Viridis'
    ),
        layout=layout
    )

    return fig

def close_earning_rate_scatter():
    test = organise.OrganiseData(base_path, name_path)
    nameset = test.get_name_set()
    # close_set = []
    name_set = []
    mkc_set = []
    aver_earning_rate_set = []
    aver_fluctuation = []
    for name in nameset.iloc[:, 0]:
        # close = test.ohlc(name).iloc[0, 4]
        mkc = test.mkcap(name).iloc[0, 2]
        fluctuation = test.average_fluctuation(name)
        # close_set.append(close)
        name_set.append(name)
        mkc_set.append(mkc)
        aver_fluctuation.append(fluctuation)
        aver_earning_rate_set.append(test.average_earning_rate(name))
    fig = px.scatter(x=aver_earning_rate_set, y=np.log(aver_fluctuation), size=mkc_set, color=name_set)
    fig.update_layout(
        xaxis=dict(title='平均收益率',  # 设置坐标轴的标签
                   titlefont=dict(size=20),
                   tickfont=dict(size=18, ),
                   # tickangle=45,  # 刻度旋转的角度
                   showticklabels=True,  # 是否显示坐标轴
                   # 刻度的范围及刻度
                   # autorange=False,
                   # range=pd.date_range('2021-10-05', '2022-02-01').strftime('%Y-%m-%d').tolist(),
                   # type='linear',
                   ),

        # y轴的刻度和标签
        yaxis=dict(title='平均波动率',  # 坐标轴的标签
                   titlefont=dict(size=18),  # 坐标轴标签的字体及颜色
                   tickfont=dict(size=20),  # 刻度的字体大小及颜色
                   showticklabels=True,  # 设置是否显示刻度
                   # tickangle=-45,
                   # 设置刻度的范围及刻度
                   autorange=True,
                   # range=[0, 100],
                   # type='linear',
                   ),
        title='平均收益率-平均波动率-总市场价值',
        titlefont=dict(size=30)
    )
    return fig







