# BUS 216F-1: Python and Applications to Business Analytics II
# Yutong Li
# Part of this code is quoted from BUS216 Professor Namini's notes

# import libraries
import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go

from map_info import GIS
from open_weather_API import OpenWeather
from dash.dependencies import Input, Output, State


def map_dashboard(open_weather_obj):
    """
    This function will create a Dash dashboard
    Code source from Udemy: https://www.udemy.com/course/interactive-python-dashboards-with-plotly-and-dash/
    """

    fig = go.Figure()
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    # Build a dashboard to show the map
    # external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash()

    # option lists for country and state:
    all_country_names = GIS.get_countries_names()
    all_state_names = GIS.get_us_states()
    country_options = []
    for c in all_country_names:
        country_options.append({'label': c, 'value': c})

    state_options = []
    for c in all_state_names:
        state_options.append({'label': c, 'value': c})

    # start building our dash:
    app.layout = html.Div(children=[
        # title
        html.H1('Current Weather Information: ',
                style={
                    'font': 'sans serif',
                    'color': "orange",
                    'backgroundColor': 'black'
                }),

        # data info
        html.Div('This data was extracted from openWeather API. Please give some time for this App to run :)', style={'font': 'sans serif', 'color': "orange", 'backgroundColor': 'black'}),
        # select countries
        html.Div([
            html.H3('Select countries:', style={'paddingRight': '30px', 'color': "orange", 'backgroundColor': 'black'}),
            # replace dcc.Input with dcc.Options, set options=options
            dcc.Dropdown(
                id='my_countries',
                options=country_options,
                value=["US"],
                multi=True
            )], style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '30%', 'color': "orange", 'backgroundColor': 'black'}),

        # select states
        html.Div([
            html.H3('If US selected, you can also select states you want to see:'),
            # replace dcc.Input with dcc.Options, set options=options
            dcc.Dropdown(
                id='my_states',
                options=state_options,
                value=["MA"],
                multi=True
            )], style={'display': 'inline-block', 'color': "orange", 'backgroundColor': 'black'}),

        html.Div([
            html.Button(
                id='submit-button',
                n_clicks=0,
                children='Submit',
                style={'fontSize': 16, 'marginLeft': '30px', 'color': "orange", 'backgroundColor': 'black'}
            ),
        ], style={'display': 'inline-block', 'color': "orange", 'backgroundColor': 'black'}),

        html.Hr(),

        # graph
        html.Div([
            dcc.Graph(id='weather_graph', figure=fig)
        ])], style={'backgroundColor': 'black'}
    )

    # add a callback function to show map
    @app.callback(
        Output('weather_graph', 'figure'),
        [Input('submit-button', 'n_clicks')],
        [State('my_countries', 'value'), State('my_states', 'value')])
    def update_graph(n_clicks, country_select, state_select):
        """
        :param n_clicks: how many times the user click submit
        :param country_select: selected countries
        :param state_select: selected states
        :return: open weather app
        """
        # if user choose US or only some specific states:
        if (country_select == ['US'] or country_select == []) and state_select != []:
            cities_filtered = GIS.get_cities_by_us_states(state_select)

        # note that if the user selected a country (not US)
        # no matter what states user chose, we can ignore it
        else:
            cities_filtered = GIS.get_cities_by_country(country_select)

        weather_info_df = GIS.get_weather_info(cities_filtered, open_weather_obj)

        # Draw the map. (Reference: https://plotly.com/python/mapbox-layers/)
        fig = go.Figure(px.scatter_mapbox(weather_info_df, lat="Latitude", lon="Longitude", hover_name="City",
                                          hover_data=["Temperature", "Humidity", "Wind_Speed", "Longitude", "Latitude",
                                                      "Country"],
                                          color="Temperature",
                                          color_continuous_scale="RdBu_r", zoom=2, height=600))

        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_layout(plot_bgcolor="black")
        fig.update_layout(paper_bgcolor="black")

        return fig

    return app


def main():
    # Another way of doing this faster is to scrap all the data first then execute the app
    open_weather = OpenWeather()
    app = map_dashboard(open_weather)
    app.run_server(debug=True, use_reloader=False)


if __name__ == '__main__':
    main()
