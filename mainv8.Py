import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc, callback_context, dash_table
import dash_bootstrap_components as dbc

import dash_admin_components as dac

from dash.exceptions import PreventUpdate

from openbb_terminal import api as openbb

import pandas as pd

from io import StringIO
import sys

# =============================================================================
# Dash App and Flask Server
# =============================================================================
app = dash.Dash(__name__)
server = app.server 

#NEXT STEPS
'''
Generation auto output
'''

# Navbar                       
navbar = dac.Navbar(color = "white")

#ici liste de fonctions, ID = unique

function_list = [
    {'id':'1', 'label':'Stocks', 'tier':'0'},
    {'id':'2', 'label':'Search', 'function':openbb.stocks.search, 'icon':'', 'tier':'1', 'active':'yes'},
    {'id':'3', 'label':'Load', 'function':openbb.stocks.load, 'icon':'', 'tier':'1', 'active':'yes'},  
    {'id':'4', 'label':'Candle', 'function':openbb.stocks.candle, 'icon':'', 'tier':'1', 'active':'yes'},  
    {'id':'5', 'label':'Quote', 'function':openbb.stocks.quote, 'icon':'', 'tier':'1', 'active':'yes'},
    {'id':'6', 'label':'Get News', 'function':openbb.stocks.get_news, 'icon':'', 'tier':'1', 'active':'yes'},         
    {'id':'7', 'label':'Display News', 'function':openbb.stocks.display_news, 'icon':'', 'tier':'1', 'active':'yes'},     
    {'id':'8', 'label':'Discovery', 'icon':'box', 'tier':'2'},
    {'id':'9', 'label':'Pipo', 'function':openbb.stocks.disc.pipo, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'10', 'label':'Fipo', 'function':openbb.stocks.disc.fipo, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'11', 'label':'Gainers', 'function':openbb.stocks.disc.gainers, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'12', 'label':'Losers', 'function':openbb.stocks.disc.losers, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'13', 'label':'Ugs', 'function':openbb.stocks.disc.ugs, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'14', 'label':'Gtech', 'function':openbb.stocks.disc.gtech, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'15', 'label':'Active', 'function':openbb.stocks.disc.active, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'16', 'label':'Ulc', 'function':openbb.stocks.disc.ulc, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'17', 'label':'Asc', 'function':openbb.stocks.disc.asc, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'18', 'label':'Ford', 'function':openbb.stocks.disc.ford, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'19', 'label':'Arkord', 'function':openbb.stocks.disc.arkord, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'20', 'label':'Upcoming', 'function':openbb.stocks.disc.upcoming, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'21', 'label':'Cnews', 'function':openbb.stocks.disc.cnews, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'22', 'label':'Trending', 'function':openbb.stocks.disc.trending, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'23', 'label':'Lowfloat', 'function':openbb.stocks.disc.lowfloat, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'24', 'label':'Hotpenny', 'function':openbb.stocks.disc.hotpenny, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'25', 'label':'Rtat', 'function':openbb.stocks.disc.rtat, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'26', 'label':'Sector Industry', 'icon':'box', 'tier':'2'},
    {'id':'27', 'label':'Industry', 'function':openbb.stocks.sia.industry, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'28', 'label':'Sector', 'function':openbb.stocks.sia.sector, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'29', 'label':'Country', 'function':openbb.stocks.sia.country, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'30', 'label':'Cps', 'function':openbb.stocks.sia.cps, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'31', 'label':'Cpic', 'function':openbb.stocks.sia.cpic, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'32', 'label':'Cpis', 'function':openbb.stocks.sia.cpis, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'33', 'label':'Cpcs', 'function':openbb.stocks.sia.cpcs, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'34', 'label':'Cpci', 'function':openbb.stocks.sia.cpci, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'35', 'label':'Metric', 'function':openbb.stocks.sia.metric, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'36', 'label':'Dark Pool Shorts', 'icon':'box', 'tier':'2'},
    {'id':'37', 'label':'Shorted', 'function':openbb.stocks.dps.shorted, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'38', 'label':'Ctb', 'function':openbb.stocks.dps.ctb, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'39', 'label':'Hsi', 'function':openbb.stocks.dps.hsi, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'40', 'label':'Prom', 'function':openbb.stocks.dps.prom, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'41', 'label':'Pos', 'function':openbb.stocks.dps.pos, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'42', 'label':'Sidtc', 'function':openbb.stocks.dps.sidtc, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'43', 'label':'Dpotc', 'function':openbb.stocks.dps.dpotc, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'44', 'label':'Ftd', 'function':openbb.stocks.dps.ftd, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'45', 'label':'Spos', 'function':openbb.stocks.dps.spos, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'47', 'label':'Insider Trading', 'icon':'box', 'tier':'2'},
    {'id':'49', 'label':'Act', 'function':openbb.stocks.ins.act, 'icon':'', 'tier':'3', 'active':'yes'},
    {'id':'50', 'label':'Cryptocurrency', 'tier':'0'},
    {'id':'51', 'label':'Load', 'function':openbb.crypto.load, 'icon':'', 'tier':'1', 'active':'yes'},
    {'id':'52', 'label':'Economy', 'tier':'0'},
    {'id':'53', 'label':'Overview', 'function':openbb.economy.overview, 'icon':'', 'tier':'1', 'active':'yes'},
    {'id':'54', 'label':'Futures', 'function':openbb.economy.futures, 'icon':'', 'tier':'1', 'active':'yes'},
    {'id':'55', 'label':'Map S&P500', 'function':openbb.economy.map_sp500, 'icon':'', 'tier':'1', 'active':'yes'},
    {'id':'56', 'label':'Bigmac', 'function':openbb.economy.bigmac, 'icon':'', 'tier':'1', 'active':'yes'},
    {'id':'57', 'label':'Macro', 'function':openbb.economy.macro, 'icon':'', 'tier':'1', 'active':'yes'},
    {'id':'58', 'label':'Index', 'function':openbb.economy.index, 'icon':'', 'tier':'1', 'active':'yes'},
    {'id':'59', 'label':'Treasury', 'function':openbb.economy.treasury, 'icon':'', 'tier':'1', 'active':'yes'},
    {'id':'60', 'label':'RTPS', 'function':openbb.economy.rtps, 'icon':'', 'tier':'1', 'active':'yes'},
    {'id':'61', 'label':'Valuation', 'function':openbb.economy.valuation, 'icon':'', 'tier':'1', 'active':'yes'},
    {'id':'62', 'label':'Performance', 'function':openbb.economy.performance, 'icon':'', 'tier':'1', 'active':'yes'},
    {'id':'63', 'label':'Spectrum', 'function':openbb.economy.spectrum, 'icon':'', 'tier':'1', 'active':'yes'},
    {'id':'__last__', 'label':'', 'function':'', 'icon':'', 'tier':'0'},
]


#TAB ID LIST
tab_id_list = []
button_id_list = []
tab_id_list_input = []
tab_id_list_output = []
content_id_list = []
button_id_list_output = []
query_id_list = []
function_id_list = []
for function in function_list:
    if (function['tier'] == '1' or function['tier'] == '3') and function['active']=='yes':
        tab_id_list.append("tab_"+function["id"])
        button_id_list.append("button_"+function["id"])
        tab_id_list_input.append(Input("tab_"+function["id"], 'n_clicks'))
        tab_id_list_output.append(Output("tab_"+function["id"], 'active'))
        content_id_list.append(Output("content_"+function["id"], 'active'))
        button_id_list_output.append(Input("button_"+function['id'], 'n_clicks'))
        query_id_list.append(Output("query_"+function['id'], 'children'))
        function_id_list.append(function['function'])

#Construction de la sidebar
SidebarMenuItem_function_list = []
parent_children = []
previous_tier = None
for function in function_list:
    if previous_tier=='3' and function['tier']!='3':
        SidebarMenuItem_function_list += dac.SidebarMenuItem(label=parent_label, icon=parent_icon, children=parent_children),
        parent_children = []
        previous_tier = None
    if function['tier']=='0':
        SidebarMenuItem_function_list += [dac.SidebarHeader(children=function['label'])]
    if function['tier']=='1':
        if function['active']=='yes':
            SidebarMenuItem_function_list += [dac.SidebarMenuItem(id="tab_"+function['id'], label=function['label'], icon=function['icon'])]
        else:
            SidebarMenuItem_function_list += [dac.SidebarMenuItem(id="tab_"+function['id'], label=function['label'], icon=function['icon'], badge_label='dev', badge_color='success')]
    if function['tier']=='2':
        parent_label = function['label']
        parent_icon = function['icon']
    if function['tier']=='3':
        if function['active']=='yes':
            parent_children += [dac.SidebarMenuItem(id="tab_"+function['id'], label=function['label'], icon=function['icon'])]
        else:
            parent_children += [dac.SidebarMenuItem(id="tab_"+function['id'], label=function['label'], icon=function['icon'], badge_label='dev', badge_color='success')]
        previous_tier = '3'
        #pas de trigger si 3 = last, d'où le __last__

# Sidebar
sidebar = dac.Sidebar(
	dac.SidebarMenu(SidebarMenuItem_function_list),
    title='OpenBB App',
	skin="dark",
    color="primary",
	brand_color="secondary",
    url="https://google.com",
    src="https://adminlte.io/themes/AdminLTE/dist/img/user2-160x160.jpg",
    elevation=3,
    opacity=0.8
)

# Body
import inspect
body_item = []
parameter_list_item = []
for function in function_list:
    if (function['tier'] == '1' or function['tier'] == '3') and function['active']=='yes':
        body_content = []
        parameter_list_content = []
        for parameter in inspect.signature(function['function']).parameters:
            current_parameter = inspect.signature(function['function']).parameters[parameter]
            label_parameter = str(current_parameter).split(" ")[0][:-1].replace('.','_')
            #hard fix replace
            try:
                type_parameter = str(current_parameter).split(" ")[1]
            except:
                type_parameter = "str"
                #got triggered, dunno from which API yet <function show_macro_data at 0x000001785F974280>, maybe link to the hard fix replace ?
            if type_parameter == "str":
                body_content += [dbc.Input(id="input_"+label_parameter+"_"+function['id'], placeholder=label_parameter+" ("+type_parameter+")", type="text"), html.Br()]
            elif type_parameter == "int" or type_parameter == "float":
                body_content += [dbc.Input(id="input_"+label_parameter+"_"+function['id'], placeholder=label_parameter+" ("+type_parameter+")", type="number"), html.Br()]
            else:
                body_content += [dbc.Input(id="input_"+label_parameter+"_"+function['id'], placeholder=label_parameter+" ("+type_parameter+")", type="text"), html.Br()]
            #if type = bool ?
            parameter_list_content.append(State("input_"+label_parameter+"_"+function['id'], 'value'))
        tab_id_list_input.append(Input("tab_"+function["id"], 'n_clicks'))
        body_content += [dbc.Button("Query", color="primary", id="button_"+function['id'])]
        body_content += [html.Div(id="query_"+function['id'])]
        body_item += [dac.TabItem(html.Div(body_content), id="content_"+function['id'])]
        parameter_list_item += [parameter_list_content]

body = dac.Body(
    dac.TabItems(body_item)
)

# Controlbar
controlbar = dac.Controlbar(
    [
        html.Br(),
        html.P("Slide to change graph in Basic Boxes"),
        dcc.Slider(
            id='controlbar-slider',
            min=10,
            max=50,
            step=1,
            value=20
        )
    ],
    title = "My right sidebar",
    skin = "light"
)

# Footer
footer = dac.Footer(
	html.A("@Benjamin Capron",
		href = "https://google.com", 
		target = "_blank", 
	),
)

# =============================================================================
# App Layout
# =============================================================================
app.layout = dac.Page([navbar, sidebar, body, controlbar, footer])

# =============================================================================
# Callbacks
# =============================================================================
#Init output list pour conserver entre les tab
output_list = [None]*len(tab_id_list)
#None dans arg provoque pbs

def activate_output(input_id, *args):
    save_stdout = sys.stdout
    result_IO = StringIO()
    sys.stdout = result_IO
    current_id = button_id_list.index(input_id)
    current_function = function_id_list[current_id](*args[len(tab_id_list)+int(current_id)])
    sys.stdout = save_stdout
    if type(current_function) == str:
        output_list[current_id] = [dcc.Markdown(current_function)]
    elif isinstance(current_function, pd.DataFrame):
        output_list[current_id] = [dash_table.DataTable(current_function.to_dict('records'))]
    elif current_function == None:
        output_list[current_id] = [dcc.Markdown(result_IO.getvalue())]
    return output_list

@app.callback(query_id_list, button_id_list_output, parameter_list_item)
def display_tab(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]   
    return activate_output(input_id, *args)

def activate(input_id, *args):
    activate_list = [False]*len(tab_id_list)
    activate_list[tab_id_list.index(input_id)]=True
    return activate_list

@app.callback(content_id_list, tab_id_list_input)
def display_tab(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]   
    return activate(input_id, *args)

@app.callback(tab_id_list_output, tab_id_list_input)
def activate_tab(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]   
    return activate(input_id, *args)
# =============================================================================
# Run app    
# =============================================================================
if __name__ == '__main__':
    app.run_server(debug=True)
