import pandas as pd
from plotly import graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input,Output

airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str,
                                   'Div2Airport': str, 'Div2TailNum': str})

print(airline_data.head())


# Create a dash application layout
app = dash.Dash(__name__)

# Get the layout of the application and adjust it.
# Create an outer division using html.Div and add title to the dashboard using html.H1 component
# Add a html.Div and core input text component
# Finally, add graph component.
app.layout = html.Div(
    children = [
       html.H1('Airline Performance Dashboard',style = {
           "text-align" : "center",
           'color': '#503D36',
           'font-size': 40
       } ),
       html.Div(children = [
              "Input Year" , dcc.Input(
                  id = 'input-year',
                  value = '2010',
                  type = 'number',
                  style = {
                      'height': 50,
                      'font-size' : 35
                  }
              ),
              dcc.Graph(id = 'line-plot')
       ], style = {
           'font-size': '40px'
       }),
       html.Br(),
       html.Br(),
       html.Br()
    ]
)

@app.callback(
    Output(component_id = 'line-plot', component_property= 'figure'),
    Input(component_id = 'input-year', component_property = 'value')
)
def create_graph(year):
    # Select data based on the entered year
    df = airline_data[airline_data['Year'] == int(year)]
    # Group the data by Month and compute the average over arrival delay time.
    line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()

    fig = go.Figure(data = go.Scatter(
                               x = line_data['Month'],
                               y = line_data['ArrDelay'],
                               mode = 'lines',
                               marker = dict(color = 'green')))
    fig.update_layout(
       xaxis_title='Month',
       yaxis_title = 'ArrDelay',
       title = 'Month vs Average Flight Delay Time')
    return fig

if __name__ == '__main__':
    app.run_server()
