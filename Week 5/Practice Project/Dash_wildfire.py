import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import datetime as dt

#Create app

app = dash.Dash(__name__)

# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Read the wildfire data into pandas dataframe
df =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')

#Extract year and month from the date column

df['Month'] = pd.to_datetime(df['Date']).dt.month_name() #used for the names of the months
df['Year'] = pd.to_datetime(df['Date']).dt.year
print(df['Region'])
print(df['Year'])
#Layout Section of Dash

#Task 2.1 Add the Title to the Dashboard
dropdown_options = [{'label': str(year), 'value': year} for year in range(2005, 2021)]

app.layout = html.Div(children=[
    html.H1('Australia Wildfire Dashboard'),

# TASK 2.2: Add the radio items and a dropdown right below the first inner division
#outer division starts

    html.Div(children = [
        # First inner divsion for  adding dropdown helper text for Selected Drive wheels
        html.Div(children = [
            html.H2('Select Region:'),
            #Radio items to select the region
            #dcc.RadioItems(['NSW',.....], value ='...', id='...',inline=True)]),
            # ['NSW', 'NT', 'QL', 'SA', 'TA', 'VI', 'WA']
            dcc.RadioItems(
                [
                    {"label":"New South Wales","value": "NSW"},
                    {"label":"Northern Teritory", "value": "NT"},
                    {"label":"Queensland", "value": "QL"},
                    {"label":"South Australia", "value": "SA"},
                    {"label":"Tasmania", "value": "TA"},
                    {"label":"Victoria", "value": "VI"},
                    {"label":"Western Australia","value": "WA"}
                ],
                value = "NSW", id='regionRadio',inline=True
            ),
            #Dropdown to select year
            html.Div(children = [
                html.H2('Select Year:', style={"color":"#656565"}),
                dcc.Dropdown(dropdown_options, id = 'year_select', value = '2005')
            ]),
            #Second Inner division for adding 2 inner divisions for 2 output graphs
            #TASK 2.3: Add two empty divisions for output inside the next inner division.
            html.Div(children = [
                html.Div(children = [ dcc.Graph( id = 'pie_plot') ]),
                html.Div(children = [ dcc.Graph( id = 'bar_plot') ])
            ], style={'display': 'flex'})
        ])
    ])
])
    #outer division ends
#layout ends
#TASK 2.4: Add the Ouput and input components inside the app.callback decorator.
#Place to add @app.callback Decorator
@app.callback([Output(component_id='pie_plot', component_property='figure'),
                Output(component_id='bar_plot', component_property='figure')],
                [Input(component_id='regionRadio', component_property='value'),
                Input(component_id='year_select', component_property='value')])
# TASK 2.5: Add the callback function.
# Place to define the callback function .

def reg_year_display(input_region,input_year):
    #data
    region_data = df[df['Region'] == input_region]
    y_r_data = region_data[region_data['Year']==input_year]
    #Plot one - Monthly Average Estimated Fire Area

    est_data = y_r_data.groupby('Month', as_index = False).sum()

    fig1 = px.pie(est_data, values='Estimated_fire_area', title="{} : Monthly Average Estimated Fire Area in year {}".format(input_region,input_year), names = 'Month' )

    #Plot two - Monthly Average Count of Pixels for Presumed Vegetation Fires
    veg_data = y_r_data[['Month','Count']].groupby('Month').mean()

    fig2 = px.bar(veg_data['Count'], title='{} : Average Count of Pixels for Presumed Vegetation Fires in year {}'.format(input_region,input_year), labels = {'value': 'Count'})

    return [fig1, fig2 ]




if __name__ == '__main__':
    app.run_server()

