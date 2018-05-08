import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot

data = pd.read_csv("/Users/leesa/Downloads/Viz_project/airport.csv")

df = data[['Origin_state', 'Passengers', 'Seats', 'Fly_date']]
df = df.groupby(['Origin_state', 'Fly_date']).sum().reset_index()
df = df.groupby(['Origin_state']).mean().reset_index()


data_viz = df


app = dash.Dash(__name__)

all_options = {
    'Passengers': ['Passengers',
                        'Average passengers per day<br>(Hover for breakdown)'],
    'Seats': ['Seats', 
                        'Average Seats per day'
                        '<br>(Hover for breakdown)']}

app.layout = html.Div([
    dcc.RadioItems(
        id='information',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='Passengers'
    ),


    html.Hr(),

html.Div([dcc.Graph(id='bargraph')],
             style={'width': '49%', 'float': 'left', 'display': 'inline-block'})
    ])


@app.callback(
    dash.dependencies.Output('bargraph', 'figure'),
    [dash.dependencies.Input('information', 'value')])
def update_bargraph(filter_choice):
    average = all_options[filter_choice][0]
    title_text = all_options[filter_choice][1]
    dff = data_viz


    return {
        'data': [go.Bar(
            x= dff['Origin_state'].unique(),
            y= dff[average].astype(float).unique(),
            marker=dict(
                color='rgb(84,39,143)'
            )
    )],
        'layout': go.Layout(
            title=title_text,
            yaxis=dict(
                title='Daily Average',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            )
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)


