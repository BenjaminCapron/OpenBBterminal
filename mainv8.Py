from openbb_terminal import api as openbb

import dash
from dash.dependencies import Input, Output

from dash import dcc, html, dash_table
import dash_admin_components as dac
import dash_bootstrap_components as dbc
from dash import callback_context

from dash.exceptions import PreventUpdate

import inspect

from io import StringIO
import sys

# =============================================================================
# Dash App and Flask Server
# =============================================================================
app = dash.Dash(__name__)
server = app.server 
# =============================================================================
# Dash Admin Components
# =============================================================================
# Navbar
navbar = dac.Navbar(color = "white") 

SIDEBAR_DATA_LEVEL = [
              ("Search", 1),
              ("Load", 1),
              ("Candle", 1),
              ("Quote", 1),
        ]

#SIDEBAR
sidebarmenu_variable = []
subitems=[]
for item, tab in SIDEBAR_DATA_LEVEL:
    if tab==0:
        sidebarmenu_variable += [dac.SidebarHeader(children=item)]
    elif tab==1:
        sidebarmenu_variable += [dac.SidebarMenuItem(id="tab_"+item, label=item, icon='box')]
    elif tab==2:       
        sidebarmenu_variable += [dac.SidebarMenuItem(label=item, icon='cubes', children=subitems)]
    elif tab==3:
        subitems += [dac.SidebarMenuSubItem(id="tab_"+item, label=item)]
#print(subitems) # add list dans list, ajouter ID par tab=2 et iterate l'id a chaque id=2 trigger
sidebar = dac.Sidebar(
	dac.SidebarMenu(
            sidebarmenu_variable
	),
    title='OpenBB Terminal',
	skin="light",
    color="dark",
	brand_color="dark",
    url="https://google.com",
    src="https://www.e-pass.education/themes/template/img/160x160/img4.jpg",
    elevation=3,
    opacity=0.8
)


# Body
body_item = []
for item, tab in SIDEBAR_DATA_LEVEL:
    body_content = []
    try:
        openbb_call = getattr(openbb, "stocks")
        openbb_call = getattr(openbb_call, item.lower())
        if (tab==1 or tab==3):
            for parameter in inspect.signature(openbb_call).parameters:
                current_parameter = inspect.signature(openbb_call).parameters[parameter]
                label_parameter = str(current_parameter).split(" ")[0][:-1]
                type_parameter = str(current_parameter).split(" ")[1]
                if type_parameter == "str":
                    body_content += [dbc.Input(id="input_"+label_parameter+"_"+item, placeholder=label_parameter+" ("+type_parameter+")", type="text"), html.Br()]
                if type_parameter == "int":
                    body_content += [dbc.Input(id="input_"+label_parameter+"_"+item, placeholder=label_parameter+" ("+type_parameter+")", type="number"), html.Br()]
        body_content += [html.Div([html.Button("Button", id="button-"+item)] + [html.Div("", id="log"+item)])]
        body_item += [dac.TabItem(html.Div(body_content), id="content_"+item)]
    except Exception as e:
        print(e)
        body_content += [dbc.Input(id="input_"+item, placeholder="Sans fonction", type="text")]
        body_item+= [dac.TabItem(html.Div(body_content), id="content_"+item)]
        #print(e)

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
            step=10,
            value=20
        )
    ],
    title = "API Keys",
    skin = "light"
)

footer = dac.Footer(
	html.A("@Benjamin Capron",
		href = "https://twitter.com/quanteeai", 
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
def activate_output(input_id, *args):
    result = []
    for item, tab in SIDEBAR_DATA_LEVEL:
        if (tab==1 or tab==3):
            if input_id == 'button-'+item:
                method_called_by_user = getattr(openbb, "stocks")
                method_called_by_user = getattr(method_called_by_user, item.lower())
                df = method_called_by_user("GME")
                #différente chose à restituer selon le type
                if isinstance(df, type(None)):
                    save_stdout = sys.stdout
                    result_IO = StringIO()
                    sys.stdout = result_IO
                    method_called_by_user("GME")
                    sys.stdout = save_stdout
                    result+=[dcc.Markdown(result_IO.getvalue(), id='tbl2')]
                else:
                    result+=[dash_table.DataTable(df.to_dict('records'), id='tbl')]
            else:
                result+=[""]
    return result


output_list_div = []
input_list_button = []
for item, tab in SIDEBAR_DATA_LEVEL:
    if (tab==1 or tab==3):
        output_list_div += [Output("log"+item, "children")]
        input_list_button += [Input("button-"+item, "n_clicks")]

@app.callback(output_list_div, input_list_button)
def display_tab(*args):
    
    ctx = dash.callback_context # Callback context to recognize which input has been triggered

    # Get id of input which triggered callback  
    if not ctx.triggered:
        raise PreventUpdate
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]   

    return activate_output(input_id, *args)
#Liste d'input avec id_input et un output unique, comment limiter l'update à 1 seul ?, output avec content_ en variable ?




def activate(input_id, *args):
    result = []
    for item, tab in SIDEBAR_DATA_LEVEL:
        if (tab==1 or tab==3):
            # Depending on tab which triggered a callback, show/hide contents of app
            if input_id == 'tab_'+item:
                result+=[True]
            else:
                result+=[False]
    return result
    
output_list = []
input_list = []
for item, tab in SIDEBAR_DATA_LEVEL:
    if (tab==1 or tab==3):
        output_list += [Output('content_'+item, 'active')]
        input_list += [Input('tab_'+item, 'n_clicks')]
    
    
@app.callback(output_list, input_list)

def display_tab(*args):
    
    ctx = dash.callback_context # Callback context to recognize which input has been triggered

    # Get id of input which triggered callback  
    if not ctx.triggered:
        raise PreventUpdate
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]   

    return activate(input_id, *args)



output_list2 = []
input_list2 = []
for item, tab in SIDEBAR_DATA_LEVEL:
    if (tab==1 or tab==3):
        output_list2 += [Output('tab_'+item, 'active')]
        input_list2 += [Input('tab_'+item, 'n_clicks')]
@app.callback(output_list2, input_list2)

def activate_tab(*args):
    
    ctx = dash.callback_context # Callback context to recognize which input has been triggered

    # Get id of input which triggered callback  
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

