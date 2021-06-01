from dash_html_components.Summary import Summary
import pandas as pd
import numpy as np
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_leaflet as dl
from dash.dependencies import Input, Output

df = pd.read_csv('QuantitativerSzenarienvergleich2.csv', index_col=[0,1], encoding='utf-8', engine='python', quotechar='"', sep=';', error_bad_lines=False).fillna(0).sort_index()
        
# -----------------------------------------------------------------------------------------------------------------------------
# Daten Manipulation

app = dash.Dash(__name__,
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ],
                external_stylesheets=[dbc.themes.BOOTSTRAP]
                )

# -----------------------------------------------------------------------------------------------------------------------------
# Layout

app.layout = html.Div([

                    dl.Map([dl.TileLayer(), dl.LayerGroup(id='kreise')],
                        worldCopyJump=True, center=[51.845184, 10.405991],
                        zoom=6,
                        scrollWheelZoom=False,
                        style={'width': '45%', 'minHeight': '450px', 'margin': '0 auto 1.33em'}
                    ),

                    html.Div([

                        dcc.Graph(id='plotFlaeche',
                                config={'displayModeBar': False}
                        ),

                        html.P(['Windkraft: ca. 50km', html.Sup('2'), ' pro GW installierter Leistung', html.Br(), 'PV-Anlagen: ca. 20km', html.Sup('2'), ' pro GW installierter Leistung'],
                                style={'fontWeight': 'normal', 'fontSize': '0.9em'})

                    ], style={'width': '45%', 'margin': 'auto'}),

                ], className='flaeche')

""" # -----------------------------------------------------------------------------------------------------------------------------
# Callbacks

ratioKm2ToGW = [50, 50, 20] #Wind-Onshore, Wind-Offshore, PV

@app.callback(
    Output('erzeugungGesamt1', 'children'),
    Output('erzeugungGesamt2', 'children'),
    Input('slct_scenario1', 'value'),
    Input('slct_scenario2', 'value')
)
def update_stromerzeugung(option_slctd1, option_slctd2):

    erzeugungGesamt1 = df.loc[('Stromerzeugung [TWh/a]', 'Gesamt'), [option_slctd1]].values[0][0]
    erzeugungGesamt2 = df.loc[('Stromerzeugung [TWh/a]', 'Gesamt'), [option_slctd2]].values[0][0]

    erzeugungGesamt1 = [f'{option_slctd1}:', html.Br(), f'{erzeugungGesamt1} [TWh/a]']
    erzeugungGesamt2 = [f'{option_slctd2}:', html.Br(), f'{erzeugungGesamt2} [TWh/a]']

    return erzeugungGesamt1, erzeugungGesamt2

@app.callback(
    Output('stromverbrauch1', 'children'),
    Output('stromverbrauch2', 'children'),
    Input('slct_scenario1', 'value'),
    Input('slct_scenario2', 'value')
)
def update_stromverbrauch(option_slctd1, option_slctd2):

    netto1 = int(df.loc[('Stromverbrauch [TWh/a]', 'Nettostromverbrauch'), [option_slctd1]].values[0][0])
    brutto1 = int(df.loc[('Stromverbrauch [TWh/a]', 'Bruttostromverbrauch'), [option_slctd1]].values[0][0])

    netto2 = int(df.loc[('Stromverbrauch [TWh/a]', 'Nettostromverbrauch'), [option_slctd2]].values[0][0])
    brutto2 = int(df.loc[('Stromverbrauch [TWh/a]', 'Bruttostromverbrauch'), [option_slctd2]].values[0][0])

    verbrauch1 = [f'{option_slctd1}:', html.Br()]
    verbrauch2 = [f'{option_slctd2}:', html.Br()]

    if netto1==0:
        verbrauch1.extend(['Nettostromverbrauch: Keine Daten', html.Br()])
    else:
        verbrauch1.extend([f'Nettostromverbrauch: {netto1} TWh/a', html.Br()])
    if brutto1==0:
        verbrauch1.append('Bruttostromverbrauch: Keine Daten')
    else:
        verbrauch1.append(f'Bruttostromverbrauch: {brutto2} TWh/a')

    if netto2==0:
        verbrauch2.extend(['Nettostromverbrauch: ', 'Keine Daten', html.Br()])
    else:
        verbrauch2.extend([f'Nettostromverbrauch: {netto1} TWh/a', html.Br()])
    if brutto2==0:
        verbrauch2.append('Bruttostromverbrauch: Keine Daten')
    else:
        verbrauch2.append(f'Bruttostromverbrauch: {brutto2} TWh/a')

    return verbrauch1, verbrauch2

@app.callback(
    Output('kosten1', 'children'),
    Output('kosten2', 'children'),
    Input('slct_scenario1', 'value'),
    Input('slct_scenario2', 'value')
)
def update_kosten(option_slctd1, option_slctd2):

    help1 = int(df.loc[('Kosten [Mrd EUR]', 'Kosten Netzausbau Gesamt [Mrd EUR]'), [option_slctd1]].values[0][0]) #hässlich, aber es macht folgendes
    help2 = int(df.loc[('Kosten [Mrd EUR]', 'Kosten Netzausbau Gesamt [Mrd EUR]'), [option_slctd2]].values[0][0])

    kosten1 = f'Kosten {option_slctd1}: {help1} Mrd. €'
    kosten2 = f'Kosten {option_slctd2}: {help2} Mrd. €'

    return kosten1, kosten2

@app.callback(
    Output('slct_scenario1', 'options'),
    Output('slct_scenario2', 'options'),
    Input('slct_scenario1', 'value'),
    Input('slct_scenario2', 'value')
)
def update_dropdowns(option_slctd1, option_slctd2):

    dropdownOptions1 = []
    for col in df.columns:
        if col == option_slctd2:
            dropdownOptions1.append({'label': col, 'value': col, 'disabled': True})
        else:
            dropdownOptions1.append({'label': col, 'value': col})

    dropdownOptions2 = []
    for col in df.columns:
        if col == option_slctd1:
            dropdownOptions2.append({'label': col, 'value': col, 'disabled': True})
        else:
            dropdownOptions2.append({'label': col, 'value': col})

    return dropdownOptions1, dropdownOptions2

@app.callback(
    Output('plotFlaeche', 'figure'),
    Output('plotInstallierteLeistung', 'figure'),
    Output('plotStromerzeugung', 'figure'),
    Output('plotStromverbrauch', 'figure'),
    Input('slct_scenario1', 'value'),
    Input('slct_scenario2', 'value')
)
def update_graphs(option_slctd1, option_slctd2):
    
    def berechneFlaeche(GW):
        flaeche = GW.copy()
        ind = flaeche.index
        for x in range(3):
            flaeche.loc[ind[x], [option_slctd1, option_slctd2]] = flaeche.loc[ind[x], [option_slctd1, option_slctd2]] * ratioKm2ToGW[x]
        return flaeche

    figFlaeche = px.bar(
        data_frame = berechneFlaeche(df.loc[[('Installierte Leistung [GW]', 'Wind offshore'), ('Installierte Leistung [GW]', 'Wind onshore'), ('Installierte Leistung [GW]', 'PV')], [option_slctd1, option_slctd2]].droplevel(0)),
        labels = {'Kategorie': 'Erneuerbare Energie', 'value': 'Quadratkilometer', 'variable': 'Studie'},
        barmode = 'group',
        color_discrete_map = {option_slctd1: '#c24430', option_slctd2: '#4c91e0'}        
    )
    figFlaeche.update_layout(
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        font_family = '-apple-system, BlinkMacSystemFont, sans-serif',
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis={'categoryorder': 'total descending'},
        xaxis_tickangle=45
    )  
    
    figInstallierteLeistung = px.bar(
        df.loc[('Installierte Leistung [GW]', 'Biomasse'):('Installierte Leistung [GW]', 'Wind onshore'), [option_slctd1, option_slctd2]].droplevel(0),
        labels = {'Kategorie': 'Erneuerbare Energie', 'value': 'Installierte Leistung [GW]', 'variable': 'Studie'},
        barmode= 'group',
        color_discrete_map={option_slctd1: '#c24430', option_slctd2: '#4c91e0'}
    )
    figInstallierteLeistung.update_layout(
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis={'categoryorder': 'total descending'},
        xaxis_tickangle=45
    )
    
    figStromerzeugung = px.bar(
        df.loc[('Stromerzeugung [TWh/a]', 'Biomasse'):('Stromerzeugung [TWh/a]', 'Wind onshore'), [option_slctd1, option_slctd2]]
            .droplevel(0)
            .drop(['Gesamt']),
        labels = {'Kategorie': 'Verbraucher', 'value': 'Stromerzeugung [TWh/a]', 'variable': 'Studie'},
        barmode= 'group',
        color_discrete_map={option_slctd1: '#c24430', option_slctd2: '#4c91e0'}
    )
    figStromerzeugung.update_layout(
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis={'categoryorder': 'total descending'},
        xaxis_tickangle=45
    )  

    figStromverbrauch = px.bar(
        df.loc[('Stromverbrauch [TWh/a]', 'GHD'):('Stromverbrauch [TWh/a]', 'Wärme elektrisch'), [option_slctd1, option_slctd2]]
            .droplevel(0)
            .drop(['Nettostromverbrauch']),
        labels = {'Kategorie': 'Verbraucher', 'value': 'Stromverbrauch [TWh/a]', 'variable': 'Studie'},
        barmode= 'group',
        color_discrete_map={option_slctd1: '#c24430', option_slctd2: '#4c91e0'}
    )
    figStromverbrauch.update_layout(
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis={'categoryorder': 'total descending'},
        xaxis_tickangle=45
    ) 
    
    return  figFlaeche, figInstallierteLeistung, figStromerzeugung, figStromverbrauch

@app.callback(
    Output(component_id='kreise', component_property='children'),
    Input(component_id='slct_scenario1', component_property='value'),
    Input(component_id='slct_scenario2', component_property='value')
)
def update_map(option_slctd1, option_slctd2):

    centers = [(53, 11), (54, 7), (49, 9)]

    def berechneRadius(GW, iterator):
        radius = np.sqrt((ratioKm2ToGW[iterator] * GW * 1000000) / np.pi)
        return radius

    circles = []
    for x in range(3):
        circles.append(dl.Circle(children=dl.Tooltip(df.loc[[('Installierte Leistung [GW]', 'Wind onshore'), ('Installierte Leistung [GW]', 'Wind offshore'), ('Installierte Leistung [GW]', 'PV')], [option_slctd1]]
                                                        .droplevel(0)
                                                        .index[x]),
                                center=centers[x],
                                radius=berechneRadius(df.loc[[('Installierte Leistung [GW]', 'Wind onshore'), ('Installierte Leistung [GW]', 'Wind offshore'), ('Installierte Leistung [GW]', 'PV')], [option_slctd1]]
                                                            .values
                                                            .flatten()[x],
                                                    x),
                                color='#c24430'))
    for x in range(3):
        circles.append(dl.Circle(children=dl.Tooltip(df.loc[[('Installierte Leistung [GW]', 'Wind onshore'), ('Installierte Leistung [GW]', 'Wind offshore'), ('Installierte Leistung [GW]', 'PV')], [option_slctd2]]
                                                        .droplevel(0)
                                                        .index[x]),
                                center=centers[x],
                                radius=berechneRadius(df.loc[[('Installierte Leistung [GW]', 'Wind onshore'), ('Installierte Leistung [GW]', 'Wind offshore'), ('Installierte Leistung [GW]', 'PV')], [option_slctd2]]
                                                        .values
                                                        .flatten()[x],
                                                    x),
                                color='#4c91e0'))

    return circles """

# -----------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)