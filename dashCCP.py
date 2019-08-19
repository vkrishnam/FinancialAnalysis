import dash
import dash_html_components as html
import dash_core_components as dcc
from getAllTheLargeCapStocks import getAllCapStocks
from getAllTheLargeCapStocks import checkForCoffeeCanInvestingStocks
from getAllTheLargeCapStocks import getAllTheLargeCapStocks
from getAllTheLargeCapStocks import getAllTheMidCapStocks
from getAllTheLargeCapStocks import getAllTheSmallCapStocks
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
import gc
import json
from nsepy import get_history
from datetime import date
import datetime
import numpy as np


semaphoreVar = 1
scale_factor = 5000
colorLookUp = {'L':'red','M':'green','S':'blue','A':'orange'}
g_n_clicks = 0

markdown_text = '''
### Coffee Can Investing - Concept/Philosophy

[Coffee Can Investing](https://www.upwardly.in/blog/coffee-can-investing-better-mutual-funds-india/) approach has picked up lot of attraction and significance in recent times, esp when majority of the MFs and other investor funds failing to generate decent Alpha above market benchmark indices.

**Coffee Can Investing** refers to *“buy and forget”* approach to investing in shares of *"quality"* companies which have performed well consistently. The concept of Coffee Can investing has originated from the US markets where it is highly successful.

The idea of the Coffee Can portfolio traces its roots back to the American Old West, when people would secure their valuables by putting them in a coffee can. The coffee can was then placed under their mattress for safe-keeping, where it stayed for years, or even decades. A portfolio manager by the name of Robert Kirby proposed in 1984 that investors could the follow the same approach — identify a diversified portfolio of consistently performing companies, invest in their stocks and keep invested for at least 10 years.

In the Indian context, Coffee Can Portfolio has been defined in book “The Unusual Billionaires” to refer to companies which have generated consistent **Return on Capital (ROCE)** over *15% every year* and **Revenue Growth** of more than *10% every year*, over the last 10 years..
'''

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
colors = {
    'background': '#111111',
    'title-text': '#7F7F7F',
    'text': '#7FDBFF'
}
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
[dictLargeCap, dictMidCap, dictSmallCap] =  getAllCapStocks(False)
g_roce_valuee = 15
g_rev_valuee = 8

ccp_L = checkForCoffeeCanInvestingStocks(dictLargeCap, 'Large', 15, 8, False, True)
ccp_M = checkForCoffeeCanInvestingStocks(dictMidCap, 'Mid', 15, 8, False, True)
ccp_S = checkForCoffeeCanInvestingStocks(dictSmallCap, 'Small', 15, 8, False, True)

columnsOfDataInDict = ['FullName','Desc','MarketCap','pAndL', 'BalanceSheet', 'CashFlow', 'Ratios']
columnsOfDataInPortfolio = ['Symbol','FullName','Desc','MarketCap','pAndL', 'BalanceSheet', 'CashFlow', 'Ratios', 'ROCE','Sales']
colL = ((i, columnsOfDataInDict[i]) for i in range(0, 7))
#print(colL)

df_dictLargeCap = pd.DataFrame.from_dict(dictLargeCap, orient='index')
df_dictLargeCap.rename(columns = dict(colL), inplace=True)
df_dictMidCap = pd.DataFrame.from_dict(dictMidCap, orient='index')
df_dictMidCap.rename(columns = dict(colL), inplace=True)
df_dictSmallCap = pd.DataFrame.from_dict(dictSmallCap, orient='index')
df_dictSmallCap.rename(columns = dict(colL), inplace=True)
#print(df_dictLargeCap.columns)

df_ccp_L = pd.DataFrame(ccp_L, columns=columnsOfDataInPortfolio)
df_ccp_M = pd.DataFrame(ccp_M, columns=columnsOfDataInPortfolio)
df_ccp_S = pd.DataFrame(ccp_S, columns=columnsOfDataInPortfolio)
#print(df_ccp_L.head())
df_portfolio = df_ccp_L.copy(deep=True)
df_portfolio['text'] = df_portfolio['FullName']+'          MarketCap: INR(Cr) '+df_portfolio['MarketCap'].map(str)

g_choice = 'L'


app.layout = html.Div([
    html.H1('Coffee Can Investing Dashboard',id='Heading',style={
            'textAlign': 'center',
            'color': colors['title-text'],
            'font-size':25
        }),
    dcc.Markdown(children=markdown_text),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Data Analysis', value='tab-1', style={
                'textAlign': 'center',
                'color': colors['text'],
                'font-size': '30px'
                },
                children = html.Div([
                    html.H3('Analyze the stocks for CC investing parameters.',style={'font-size': '20px'}),
                    dcc.RadioItems(id="radio-tab1", options=[
                                    {'label': 'Large Cap', 'value': 'L'},
                                    {'label': 'Mid Cap', 'value': 'M'},
                                    {'label': 'Small Cap', 'value': 'S'}],
                                    value='L',style={'font-size': '20px'}),
                    html.Hr(),
                    html.Label('ROCE (%)',style={'font-size': '20px'}),
                    html.P(
                        dcc.Slider( id='ROCE-Slider',
                            min=1,
                            max=30,
                            step=1,
                            marks={i: str(i) for i in range(1,31)},
                            value=15
                            )),
                    html.Hr(),
                    html.Label('Revenue Growth (%)',style={'font-size': '20px'}),
                    html.P(
                        dcc.Slider( id='RevenueGrowth-Slider',
                            min=1,
                            max=30,
                            step=1,
                            marks={i: str(i) for i in range(1,31)},
                            value=8
                            )),
                    html.Hr(),
                    html.Div(id='tab-1-content'),
                    html.Div(id='tab-1-2-content'),
                    html.Hr(),
                    html.Hr(),
                    html.Button('Analyze & Update Charts', id='button'),
                    html.Hr(),
                    dcc.Tabs(id="graphtabs", value='tab-1', children=[
                            dcc.Tab(label='ScatterPlot', value='grph-tab-1', style={
                                'textAlign': 'center',
                                'color': colors['text'],
                                'font-size': '30px'
                            },
                            children = html.Div([html.Div(dcc.Graph(id='indicator-graphic'),style={'width':'60%', 'float':'left'}),dcc.Markdown(id='hover-data', style={'paddingTop':35,'font-size':20,'display':'inline-block'}),html.Hr(),html.Div(dcc.Graph(id='sub-indicator-graphic'),style={'width':'30%', 'float':'right','paddingTop':20})])),
                            dcc.Tab(label='BarCharts', value='grph-tab-2', style={
                                'textAlign': 'center',
                                'color': colors['text'],
                                'font-size': '30px'
                            },
                            children = html.Div([html.Div(dcc.Graph(id='indicator-graphic-2'),style={'width':'60%', 'float':'left'}),dcc.Markdown(id='hover-data-2', style={'paddingTop':35,'font-size':20,'display':'inline-block'}),html.Div(dcc.Graph(id='sub-indicator-graphic-2'),style={'width':'30%', 'float':'right'})]))
                            ])
                    ])
                ),
        dcc.Tab(label='Data Mining', value='tab-2', style={
                'textAlign': 'center',
                'color': colors['text'],
                'font-size': '30px'
                },
                children = html.Div([
                    html.H3('Mine data from NSE and WebScrapping on the whole universe of stocks.',style={'font-size': '20px'}),
                    dcc.RadioItems(id="radio-tab2", options=[
                                    {'label': 'Large Cap', 'value': 'L'},
                                    {'label': 'Mid Cap', 'value': 'M'},
                                    {'label': 'Small Cap', 'value': 'S'},
                                    {'label': 'All Cap', 'value': 'A'}],
                                    value='A',style={'font-size': '20px'})
                ])
                ),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(
    Output('hover-data-2', 'children'),
    [Input('indicator-graphic-2', 'hoverData')])
def callback_image(hoverData):
    global df_portfolio
    v_index = hoverData['points'][0]['pointIndex']
    stats = """
        Symbol : **{}**    
        FullName : **{}**   
        MarketCap INR(Cr) : **{}**       
        """.format(df_portfolio.iloc[v_index]['Symbol'],
            df_portfolio.iloc[v_index]['FullName'],
            df_portfolio.iloc[v_index]['MarketCap'])
    return stats

@app.callback(
    Output('hover-data', 'children'),
    [Input('indicator-graphic', 'hoverData')])
def callback_image(hoverData):
    global df_portfolio
    v_index = hoverData['points'][0]['pointIndex']
    stats = """
        Symbol : **{}**    
        FullName : **{}**   
        MarketCap INR(Cr) : **{}**       
        """.format(df_portfolio.iloc[v_index]['Symbol'],
            df_portfolio.iloc[v_index]['FullName'],
            df_portfolio.iloc[v_index]['MarketCap'])
    return stats


@app.callback(
    Output('sub-indicator-graphic', 'figure'),
    [Input('indicator-graphic', 'clickData')])
def callback_sub_image(hoverData):
    global df_portfolio
    v_index = hoverData['points'][0]['pointIndex']
    symbol_sel = df_portfolio.iloc[v_index]['Symbol']
    #print(symbol_sel)
    stockdata = get_history(symbol=symbol_sel, start=(date.today()- datetime.timedelta(days=1*365)), end=date.today())
    
    fig = {'data':[go.Scatter(x=stockdata.index,y=stockdata['Close'],
            mode='lines',
            marker = {'color':'green'},
            name='52Wk Trend'
            ),
            go.Scatter(x=stockdata.index,y=stockdata['Close'].rolling(20).mean(),
                    mode='lines',
                    marker = {'color':'red'},
                    name='50 Day MA'
                    ),
            go.Scatter(x=stockdata.index,y=stockdata['Close'].rolling(200).mean(),
                    mode='lines',
                    marker = {'color':'blue'},
                    name='200 Day MA'
                    ),], 
        'layout':go.Layout(
                title = 'Last 1Yr Trend - {}'.format(symbol_sel),
                
                xaxis={
                    'title': 'Date Range',
                #    'type': 'linear'
                },
                yaxis={
                    'title': 'Stock price (INR)',
                #    'type': 'linear'
                },
                
                hovermode='closest'
            )}
    #fig = {}
    return fig

@app.callback(
    Output('sub-indicator-graphic-2', 'figure'),
    [Input('indicator-graphic-2', 'clickData')])
def callback_sub_image(hoverData):
    global df_portfolio
    v_index = hoverData['points'][0]['pointIndex']
    symbol_sel = df_portfolio.iloc[v_index]['Symbol']
    #print(symbol_sel)
    stockdata = get_history(symbol=symbol_sel, start=(date.today()- datetime.timedelta(days=1*365)), end=date.today())
    
    fig = {'data':[go.Scatter(x=stockdata.index,y=stockdata['Close'],
            mode='lines',
            marker = {'color':'green'},
            name='52Wk Trend'
            ),
            go.Scatter(x=stockdata.index,y=stockdata['Close'].rolling(20).mean(),
                    mode='lines',
                    marker = {'color':'red'},
                    name='50 Day MA'
                    ),
            go.Scatter(x=stockdata.index,y=stockdata['Close'].rolling(200).mean(),
                    mode='lines',
                    marker = {'color':'blue'},
                    name='200 Day MA'
                    ),], 
        'layout':go.Layout(
                title = 'Last 1Yr Trend - {}'.format(symbol_sel),
                
                xaxis={
                    'title': 'Date Range',
                #    'type': 'linear'
                },
                yaxis={
                    'title': 'Stock price (INR)',
                #    'type': 'linear'
                },
                
                hovermode='closest'
            )}
    #fig = {}
    return fig



g_clocks = 0

@app.callback(Output('tab-1-2-content', 'children'), [Input('radio-tab1', 'value'),Input('ROCE-Slider', 'value'),Input('RevenueGrowth-Slider', 'value'),Input('button','n_clicks')])
def render_button1(choice,roce_valuee,rev_valuee, n_clicks):
    global g_clocks
    if g_clocks == n_clicks:
        return html.Div([
            html.H3('Please Click the bellow Button for new Analysis as parameters/choices have been modified.')
            ],style={'font-size': '20px', 'color':'red'})
    else:
        g_clocks = n_clicks
        return html.Div([
            html.Hr()
            ],style={'font-size': '20px', 'color':'red'})


@app.callback(Output('indicator-graphic-2', 'figure'), [Input('button', 'n_clicks')])
def render_graph_content(n_clicks):
    global df_portfolio
    listOfBars = ['ROCE','Sales']
    return {'data': [go.Bar(
            y = df_portfolio['Symbol'],     # reverse your x- and y-axis assignments
            x = df_portfolio[col],
            orientation='h',  # this line makes it horizontal!
            name=col
            ) for col in listOfBars],
    'layout':go.Layout(
            title='Comparison of Ratios',
            hovermode='closest'
        )}



@app.callback(Output('indicator-graphic', 'figure'), [Input('button', 'n_clicks')])
def render_graph_content(n_clicks):
    global df_portfolio
    global g_choice
    
    if g_choice == 'L':
        scale_factor = 5000
    elif g_choice == 'M':
        scale_factor = 500
    else:
        scale_factor = 10

    return {'data': [go.Scatter(
                x=df_portfolio['ROCE'],
                y=df_portfolio['Sales'],
                text=df_portfolio['text'],
                mode='markers',
                marker={
                    'size': df_portfolio['MarketCap']/scale_factor,
                    'opacity': 0.5,
                    'color':colorLookUp[g_choice],
                    'line': {'width': 0.5, 'color': 'red'}}
    )],
    'layout':go.Layout(
            xaxis={
                'title': 'ROCE (%)',
                'type': 'linear'
            },
            yaxis={
                'title': 'Sales/Revenue Growth (%)',
                'type': 'linear'
            },
            margin={'l': 50, 'b': 80, 't': 10, 'r': 0},
            hovermode='closest'
        )}


@app.callback(Output('tab-1-content', 'children'),[Input('radio-tab1', 'value'),Input('ROCE-Slider', 'value'),Input('RevenueGrowth-Slider', 'value')])
def render_tab1_content(choice, roce_valuee,rev_valuee):
    global df_portfolio
    global dictLargeCap
    global dictMidCap
    global dictSmallCap
    global g_choice
    g_choice = choice
    g_roce_valuee = roce_valuee
    g_rev_valuee = rev_valuee
    g_choice = choice
    


    if choice == 'L':
        #del df_portfolio
        dictLargeCap =  getAllTheLargeCapStocks(False)
        ccp_L = checkForCoffeeCanInvestingStocks(dictLargeCap, 'Large', g_roce_valuee, g_rev_valuee, False, True)
        df_ccp_L = pd.DataFrame(ccp_L, columns=columnsOfDataInPortfolio)
        df_portfolio = df_ccp_L.copy(deep=True)
        df_portfolio['text'] = df_portfolio['FullName']+'          MarketCap: INR(Cr) '+df_portfolio['MarketCap'].map(str)
        #semaphoreVar = 0
        return html.Div([
            html.H3('Your choice is Large-Cap stocks.'),
            html.H3('This Universe is made of {} stocks'.format(len(dictLargeCap))),
            html.H3('Number of stocks which qualify Coffee Can criteria : {}'.format(len(ccp_L)))
            ],style={'font-size': '20px'})
    elif choice == 'M':
        #del df_portfolio
        dictMidCap =  getAllTheMidCapStocks(False)
        ccp_M = checkForCoffeeCanInvestingStocks(dictMidCap, 'Mid', g_roce_valuee, g_rev_valuee, False, True)
        df_ccp_M = pd.DataFrame(ccp_M, columns=columnsOfDataInPortfolio)
        df_portfolio = df_ccp_M.copy(deep=True)
        df_portfolio['text'] = df_portfolio['FullName']+'          MarketCap: INR(Cr) '+df_portfolio['MarketCap'].map(str)
        #semaphoreVar = 0
        return html.Div([
            html.H3('Your choice is Mid-Cap stocks.'),
            html.H3('This Universe is made of {} stocks'.format(len(dictMidCap))),
            html.H3('Number of stocks which qualify Coffee Can criteria : {}'.format(len(ccp_M)))
            ],style={'font-size': '20px'})
    else:
        #del df_portfolio
        dictSmallCap =  getAllTheSmallCapStocks(False)
        ccp_S = checkForCoffeeCanInvestingStocks(dictSmallCap, 'Small', g_roce_valuee, g_rev_valuee, False, True)
        df_ccp_S = pd.DataFrame(ccp_S, columns=columnsOfDataInPortfolio)
        df_portfolio = df_ccp_S.copy(deep=True)
        df_portfolio['text'] = df_portfolio['FullName']+'          MarketCap: INR(Cr) '+df_portfolio['MarketCap'].map(str)
        #semaphoreVar = 0
        return html.Div([
            html.H3('Your choice is Small-Cap stocks.'),
            html.H3('This Universe is made of {} stocks'.format(len(dictSmallCap))),
            html.H3('Number of stocks which qualify Coffee Can criteria : {}'.format(len(ccp_S)))
            ],style={'font-size': '20px'})


PORT = 8050
ADDRESS = '10.24.53.55'

if __name__ == '__main__':
    #app.run_server(debug=True,port=PORT, host=ADDRESS)
    app.run_server(debug=True)
