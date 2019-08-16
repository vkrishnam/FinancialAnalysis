import dash
import dash_html_components as html
import dash_core_components as dcc
from getAllTheLargeCapStocks import getAllCapStocks
from getAllTheLargeCapStocks import checkForCoffeeCanInvestingStocks
from getAllTheLargeCapStocks import getAllTheLargeCapStocks
from getAllTheLargeCapStocks import getAllTheMidCapStocks
from getAllTheLargeCapStocks import getAllTheSmallCapStocks
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import gc

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
    html.H1('Coffee Can Investing',id='Heading',style={
            'textAlign': 'center',
            'color': colors['title-text']
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
                    dcc.Graph(id='indicator-graphic')
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

'''
@app.callback(Output('tab-1-2-content', 'children'), [Input('radio-tab1', 'value'),Input('ROCE-Slider', 'value'),Input('RevenueGrowth-Slider', 'value')])
def render_button1(choice,roce_valuee,rev_valuee):
    g_choice = choice
    g_roce_valuee = roce_valuee
    g_rev_valuee = rev_valuee
    return html.Div([
        html.H3('Please Click the bellow Button for new Analysis as parameters/choices have been modified.')
        ],style={'font-size': '20px', 'color':'red'})

'''


@app.callback(Output('indicator-graphic', 'figure'), [Input('button', 'n_clicks'), Input('radio-tab1', 'value'),Input('ROCE-Slider', 'value'),Input('RevenueGrowth-Slider', 'value')])
def render_graph_content(n_clicks,g_choice,g_roce_valuee,g_rev_valuee):
    if g_choice == 'L':
        l_dictLargeCap =  getAllTheLargeCapStocks(False)
        l_ccp_L = checkForCoffeeCanInvestingStocks(l_dictLargeCap, 'Large', g_roce_valuee, g_rev_valuee, False, True)
        l_df_ccp_L = pd.DataFrame(l_ccp_L, columns=columnsOfDataInPortfolio)
        l_df_portfolio = l_df_ccp_L.copy(deep=True)
        l_df_portfolio['text'] = l_df_portfolio['FullName']+'          MarketCap: INR(Cr) '+l_df_portfolio['MarketCap'].map(str)
        scale_factor = 5000
    elif g_choice == 'M':
        l_dictMidCap =  getAllTheMidCapStocks(False)
        l_ccp_M = checkForCoffeeCanInvestingStocks(l_dictMidCap, 'Mid', g_roce_valuee, g_rev_valuee, False, True)
        l_df_ccp_M = pd.DataFrame(l_ccp_M, columns=columnsOfDataInPortfolio)
        l_df_portfolio = l_df_ccp_M.copy(deep=True)
        l_df_portfolio['text'] = l_df_portfolio['FullName']+'          MarketCap: INR(Cr) '+l_df_portfolio['MarketCap'].map(str)
        scale_factor = 500
    else:
        l_dictSmallCap =  getAllTheSmallCapStocks(False)
        l_ccp_S = checkForCoffeeCanInvestingStocks(l_dictSmallCap, 'Small', g_roce_valuee, g_rev_valuee, False, True)
        l_df_ccp_S = pd.DataFrame(l_ccp_S, columns=columnsOfDataInPortfolio)
        l_df_portfolio = l_df_ccp_S.copy(deep=True)
        l_df_portfolio['text'] = l_df_portfolio['FullName']+'          MarketCap: INR(Cr) '+l_df_portfolio['MarketCap'].map(str)
        scale_factor = 10

    #while semaphoreVar:
    #    pass

    #print("scale factor: {}".format(scale_factor))
    #print('ROCE')
    #print(df_portfolio['ROCE'])
    #print('Sales')
    #print(df_portfolio['Sales'])
    #print('MarketCap')
    #print(df_portfolio['MarketCap'])
    #print(df_portfolio['Symbol'])
    #semaphoreVar = 1
    return {'data': [go.Scatter(
                x=l_df_portfolio['ROCE'],
                y=l_df_portfolio['Sales'],
                text=l_df_portfolio['text'],
                mode='markers',
                marker={
                    'size': l_df_portfolio['MarketCap']/scale_factor,
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


@app.callback(Output('tab-1-content', 'children'),[Input('button', 'n_clicks'),Input('radio-tab1', 'value'),Input('ROCE-Slider', 'value'),Input('RevenueGrowth-Slider', 'value')])
def render_tab1_content(n_clicks, choice, roce_valuee,rev_valuee):
    g_choice = choice
    g_roce_valuee = roce_valuee
    g_rev_valuee = rev_valuee

    #print("n_clicks : {}".format(n_clicks))
    #print("g_n_clicks : {}".format(g_n_clicks))

    #if g_n_clicks == n_clicks:
    #    return html.Div([
    #        html.Hr()
    #        ],style={'font-size': '20px'})

    g_n_clicks = n_clicks

    if g_choice == 'L':
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
    elif g_choice == 'M':
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




if __name__ == '__main__':
    app.run_server(debug=True)
