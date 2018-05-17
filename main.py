import plotly as py
import plotly.graph_objs as go

from datetime import datetime, timedelta
import pandas_datareader.data as web

import dash
import dash_html_components as html
import dash_core_components as dcc

data_source = "morningstar"
end_datetime = datetime.now()
start_datetime = end_datetime - timedelta(days=365)

ticker="aapl"

def read_data(ticker):
    df = web.DataReader(ticker, data_source,
    start_datetime,
    end_datetime).reset_index()
    return df

def update(ticker):
    print("Updating... {0}".format(ticker))
    df = read_data(ticker)
    cs = go.Candlestick(name=ticker,
        x=df.Date,
        open=df.Open,
        high=df.High,
        low=df.Low,
        close=df.Close,
        increasing=dict(line=dict(color= '#00CC00')),
        decreasing=dict(line=dict(color= '#CC0000'))
    ) 

    fig=dict(data=[cs], layout=dict(autosize=True))
    return fig

fig = update(ticker)

app = dash.Dash()
app.layout = html.Div([
    html.H1("Interactive Stock Chart", style={'font': 'arial', 'color': 'black', 'fontSize': 18}),
    html.Div(dcc.Input(id='input-box', placeholder=ticker, type='text')),
    html.Button('Submit', id='button'),
    html.Div([ dcc.Graph( id="stock-chart", figure=fig) ])
])


@app.callback(
    dash.dependencies.Output('stock-chart', 'figure'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks, value):
    return update(value)


if __name__ == '__main__':
    app.run_server(debug=True)