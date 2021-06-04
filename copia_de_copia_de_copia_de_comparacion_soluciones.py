# -*- coding: utf-8 -*-
"""Copia_de_Copia_de_Copia_de_comparacion_soluciones.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yBVGA4qrADGt55Rxm23k05HZIo2kjVhi
"""

import plotly
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import codecs
from plotly.subplots import make_subplots


optima = pd.read_csv('sol_optima_065ventas_100dist.csv')
inicial = pd.read_csv('matriz_solucion_inicial_mundi_TA.csv',
                      delimiter=';',
                      decimal=',')
df_ventas = pd.read_csv('Ventas_Producto_y_Mdo_Hospital_Referencia.csv',
                      delimiter=';',
                      decimal=',')

delegados = optima['DELEGADO'].values
delegados
dels = []
for d in delegados:
  dels.append(d[:4])

optima.drop(['DELEGADO'],axis=1,inplace=True)
inicial.drop(['DELEGADO'],axis=1,inplace=True)
hospi = optima.columns.values
hospitales = []
for h in hospi:
  hospitales.append(h[:30])
sol_opt = optima.values
sol_ini = inicial.values

dif = sol_ini+3*sol_opt
dif/4
colorscale = [[0, 'white'],
              [0.25, 'rgb(100,145,255)'],
              [0.5, 'white'],
              [0.75, 'rgb(255,199,64)'],
              [1, 'rgb(96,204,51)']]
my_layout = go.Layout(
              yaxis = dict(
                    title = 'Delegados'
                    ),
              xaxis = dict(
                  title = 'Hospitales'
                  ),
                  font=dict(size=5))
fig = go.Figure(data=go.Heatmap(
                        z=dif,
                        x=hospitales,
                        y=dels,
                        hoverinfo='text',
                        colorscale = colorscale),
                layout = my_layout)
fig.update_xaxes(side="top",
                 tickangle = -90)
fig.update_layout(
    # title='GitHub commits per day',
    xaxis_nticks=265,
    yaxis_nticks=44)
fig.update_traces(showscale=False)
# fig.update_coloraxes(colorbar_tickfont_size=1)
# plotly.offline.plot(fig, filename='heatmap.html')
# f=codecs.open("heatmap.html", 'r')
heat_fig = fig

def ventas_solucion(sol):
  pesos = [0.5, 0.5]
  ventas_prod = df_ventas['VTAS_PRODUCTO'].tolist()
  ventas_mdo =df_ventas['VTAS_MERCADO'].tolist()
  ventas_prod = [i * pesos[0] for i in ventas_prod]
  ventas_mdo = [i * pesos[1] for i in ventas_mdo]
  ventas = [x + y for x, y in zip(ventas_prod, ventas_mdo)]
  v = []
  for row in sol:
    ventas_delegado = [a * b for a, b in zip(ventas, row)]
    v.append(sum(ventas_delegado))
  return v

v_ini = ventas_solucion(sol_ini)
v_opt = ventas_solucion(sol_opt)

fig = go.Figure()
fig.update_layout(
    title={
        'text': "Ventas alcanzadas por delegado",
         'y':0.9,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'},
        legend=dict(
        x=0.2,
        y=-0.2,
        traceorder='normal',
        orientation="h",
        font=dict(
            size=12)
            )
)
fig.add_trace(go.Bar(
    x=dels,
    y=v_ini,
    name='Solucion MundiPharma',
    marker_color='#6491FF'
))
fig.add_trace(go.Bar(
    x=dels,
    y=v_opt,
    name='Solucion optimizada',
    marker_color='#FFC740'
))

fig.add_trace(go.Scatter(
    x=dels, y=[1]*44,
    mode='lines',
    line_color='#EE5656',
    name='Objetivo de ventas')
)

# Here we modify the tickangle of the xaxis, resulting in rotated labels.
fig.update_layout(barmode='group', xaxis_tickangle=-90)
fig.show()
ventas_fig = fig

h_ini = np.sum(sol_ini, axis=1)
h_opt = np.sum(sol_opt, axis=1)

fig = go.Figure()
fig.update_layout(
    title={
        'text': "Hospitales asignados por delegado",
         'y':0.9,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'},
        legend=dict(
        x=0.2,
        y=-0.2,
        traceorder='normal',
        orientation="h",
        font=dict(
            size=12)
            )
)
fig.add_trace(go.Bar(
    x=dels,
    y=h_ini,
    name=f'Solucion MundiPharma - Media:{ round(h_ini.mean(),3)}',
    marker_color='#6491FF'
    
))
fig.add_trace(go.Bar(
    x=dels,
    y=h_opt,
    name=f'Solucion optimizada - Media:{ round(h_opt.mean(),3)}',
    marker_color='#FFC740'
))
# Here we modify the tickangle of the xaxis, resulting in rotated labels.
fig.update_layout(barmode='group', xaxis_tickangle=-90)
fig.show()
hospitales_fig= fig

matrix_dist = pd.read_csv('Matriz_distancias_delegado_centroides_hospitales_referencia.csv',
                          delimiter=';',
                          decimal=',')
matrix_dist.drop(['DELEGADO'],axis=1,inplace=True)
m_dist= matrix_dist.values

def get_max_distances(sol, m_dsit):
  distancias=[]
  for i in range(0,44):
    dist_del = 0
    for j in range(0,265):
      if sol[i][j] == 1:
        if m_dsit[i][j] > dist_del:
          dist_del = m_dsit[i][j]
    distancias.append(dist_del)
  return distancias

distancias_ini = np.array(get_max_distances(sol_ini, m_dist))
distancias_opt =np.array(get_max_distances(sol_opt, m_dist))

fig = go.Figure()
fig.update_layout(
    title={
        'text': "Distancia máxima asignada a cada delegado",
         'y':0.9,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'},
        legend=dict(
        x=0.2,
        y=-0.2,
        traceorder='normal',
        orientation="h",
        font=dict(
            size=12)
            )
)
fig.add_trace(go.Bar(
    x=dels,
    y=distancias_ini,
    name=f'Solucion MundiPharma - Media:{ round(distancias_ini.mean(),3)}',
    marker_color='#6491FF'
    
))
fig.add_trace(go.Bar(
    x=dels,
    y=distancias_opt,
    name=f'Solucion optimizada - Media:{ round(distancias_opt.mean(),3)}',
    marker_color='#FFC740'
))
# Here we modify the tickangle of the xaxis, resulting in rotated labels.
fig.update_layout(barmode='group', xaxis_tickangle=-90)
fig.show()

distancias_fig=fig

n_ventas_ini=sum(v_ini)
n_hosp_ini = np.array(sol_ini).sum()
n_vend_ini=len((np.array(sol_ini).sum(axis=1)))-(np.array(sol_ini).sum(axis=1) ==0).sum()

n_ventas_opt=sum(v_opt)
n_hosp_opt = np.array(sol_opt).sum()
n_vend_opt=len((np.array(sol_opt).sum(axis=1)))-(np.array(sol_opt).sum(axis=1) ==0).sum()

# Define color sets of paintings
ventas_colors = ['rgb(100,145,255)', 'rgb(193,211,255)']
hospitales_colors = ['rgb(238,86,86)', 'rgb(248,187,187)']
vendedores_colors = ['rgb(248,196,103)', 'rgb(252,237,209)']
layout = go.Layout(
    autosize=False,
    width=500,
    height=10)
# Create subplots, using 'domain' type for pie charts
specs = [[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]]
fig = make_subplots(rows=1, cols=3, 
                    specs=specs,
                    subplot_titles=['Total ventas', 
                                    'Total hospitales', 
                                    'Total vendedores'])

# Define pie charts
fig.add_trace(go.Pie(labels=['% ventas alcanzadas','% ventas perdido'], values=[n_ventas_ini, 44-n_ventas_ini], 
                     marker_colors=ventas_colors), 1, 1)
fig.add_trace(go.Pie(labels=['Nº hospitales visitados','Nº hospitales no visitados'], values=[n_hosp_ini, 265-n_hosp_ini], 
                     marker_colors=hospitales_colors), 1, 2)

fig.add_trace(go.Pie(labels=['Nº vendedores utilizados','Nº vendedores no utilizados'], values=[44,0],
                     marker_colors=vendedores_colors), 1,3)
# Tune layout and hover info
fig.update_traces(hoverinfo='label+value', textinfo='none')
fig.update(layout_title_text = '<b> Solución Mundipharma <b>',
           layout_showlegend=False)

fig = go.Figure(fig, layout=layout)
fig.show()

# Create subplots, using 'domain' type for pie charts
specs = [[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]]
fig = make_subplots(rows=1, cols=3, 
                    specs=specs,
                    subplot_titles=['Total ventas', 
                                    'Total hospitales', 
                                    'Total vendedores'])

# Define pie charts
fig.add_trace(go.Pie(labels=['% ventas alcanzadas','% ventas perdido'], values=[n_ventas_opt, 44-n_ventas_opt], 
                     marker_colors=ventas_colors),1, 1)
fig.add_trace(go.Pie(labels=['Nº hospitales visitados','Nº hospitales no visitados'], values=[n_hosp_opt, 265-n_hosp_opt], 
                     marker_colors=hospitales_colors), 1, 2)

fig.add_trace(go.Pie(labels=['Nº vendedores utilizados','Nº vendedores no utilizados'], values=[44,0],
                     marker_colors=vendedores_colors), 1,3)

# Tune layout and hover info
fig.update_traces(hoverinfo='label+value', textinfo='none')
fig.update(layout_title_text = '<b> Solución optimizada <b>',
           layout_showlegend=False)

fig = go.Figure(fig,layout=layout)
fig.show()

pie_fig = fig

import io
from base64 import b64encode

import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
# Load Data
# df = px.data.tips()
# Build App
buffer = io.StringIO()
fig.write_html(buffer)
html_bytes = buffer.getvalue().encode()
encoded = b64encode(html_bytes).decode()

app = dash.Dash()

app.layout = html.Div([
    html.H1("Comparación de soluciones"),
    dcc.Graph(
        id='graph2',
        figure=pie_fig
    ),
    dcc.Graph(
        id='example-graph',
        figure=heat_fig
    ),
    dcc.Graph(
        id='graph3',
        figure=ventas_fig
    ),
      dcc.Graph(
        id='graph4',
        figure=hospitales_fig
    ),
    html.A(
        html.Button("Download HTML"), 
        id="download",
        href="data:text/html;base64," + encoded,
        download="plotly_graph.html"
    )])
# Run app and display result inline in the notebook
app.run_server()

