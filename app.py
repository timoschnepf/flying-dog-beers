import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"

import pandas as pd

###############################################################################
## Load data
preferences_koeln= pd.read_excel("preferences_koeln.xlsx"
				   , sheet_name=0)   # kein Index

# Create percent out of decimale
preferences_koeln  = preferences_koeln.round(2)
preferences_koeln[preferences_koeln.select_dtypes(include=['number']).columns] *= 100

preferences_koeln = preferences_koeln.sort_values(by=['All'], ascending=False)

dftemp = preferences_koeln[(preferences_koeln['All'] > 3)]
dftemp = dftemp.sort_values('All', ascending=True)


###############################################################################

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/superhero/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
		
    html.H1(children='Real estate demand on Ebay-Kleinanzeigen'),

	html.Div([
        dcc.Graph(id='hbar')
    ],className='nine columns'),
		
    html.Div([

        #html.Br(),
        #html.Div(id='output_data'),
        #html.Br(),

        html.Label(['Choose column:'],style={'font-weight': 'bold', "text-align": "center"}),

        dcc.Dropdown(id='my_dropdown',
            options=[
                     {'label': 'High SES', 'value': 'High SES'},
                     {'label': 'Low SES', 'value': 'Low SES'}
            ],
            optionHeight=25,                    #height/space between dropdown options
            value='High SES',                    #dropdown value selected automatically when page loads
            disabled=False,                     #disable dropdown value selection
            multi=False,                        #allow multiple dropdown values to be selected
            searchable=False,                    #allow user-searching of dropdown values
            search_value='',                    #remembers the value searched in dropdown
            placeholder='Please select...',     #gray, default text shown when no option is selected
            clearable=False,                     #allow user to removes the selected value
            style={'width':"100%"},             #use dictionary to define CSS styles of your dropdown
            # className='select_box',           #activate separate CSS document in assets folder
            # persistence=True,                 #remembers dropdown value. Used with persistence_type
            # persistence_type='memory'         #remembers dropdown value selected until...
            ),                                  #'memory': browser tab is refreshed
                                                #'session': browser tab is closed
                                                #'local': browser cookies are deleted
    ],className='three columns')	
			 
])



@app.callback(
    Output(component_id='hbar', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')]
)

def build_graph(column_chosen):
    dftemp2=dftemp
    fig = px.bar(dftemp2,y="Stadtteil", x=column_chosen, orientation="h",
				 color = column_chosen, color_continuous_scale='ylgn', hover_name="Stadtteil")
	
    fig.update_layout({
		'plot_bgcolor': 'rgba(0, 0, 0, 0)',
		'paper_bgcolor': 'rgba(0, 0, 0, 0)',
		})


    fig.update_layout(
			font_family="Courier New",
			font_color="white")
	
    fig.update(layout_coloraxis_showscale=False)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
