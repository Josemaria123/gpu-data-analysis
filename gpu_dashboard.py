import pandas as pd
import plotly_express as px
import plotly.graph_objects as go
import dash
from dash import dash_table
from dash import html as html
from dash import dcc as dcc
from dash.dependencies import Input, Output
import pyodbc
import datetime

# Leemos el dataset de la base de datos

try:
    conn = pyodbc.connect(Trusted_Connection='yes', 
                          driver = '{SQL Server}',
                          server = 'PC-JOSALO\SQLEXPRESSSERVER', 
                          database = 'GPU_DATABASE')
    
    data = pd.read_sql_query('select * from gpu_data', conn)
    print('Se han leído los datos correctamente')
    print(data.dtypes)
    print('Como viene de la BBDD: ', data['fecha_obtencion_info'].iloc[1])
    data['fecha_obtencion_info'] = pd.to_datetime(data['fecha_obtencion_info'], format='%Y-%m-%d')
    print('Formato después de: ', data['fecha_obtencion_info'].iloc[1])

except Exception as e:
    print(e)

data = data.rename(columns={'product_specs_gpu_line_family_brand_brand_name': 'marca',
                            'product_specs_gpu_name': 'modelo',
                            'product_brand_name': 'fabricante',
                            'product_specs_gpu_stream_processors': 'nucleos_de_procesamiento',
                            'product_specs_gpu_unicode': 'nombre_comercial',
                            'product_specs_core_clock': 'core_clock',
                            'product_specs_memory_quantity_value': 'cantidad_memoria_ram',
                            'product_specs_memory_bus_width_value': 'ancho_banda_bus',
                            'product_specs_memory_type_name': 'tipo_de_memoria',
                            'product_specs_gpu_tdp': 'consumo_tdp',
                            'product_specs_length': 'largo',
                            'product_specs_bus_unicode': 'puerto_pci',
                            'metadata_normal_price_usd': 'precio_normal_dolares',
                            'metadata_offer_price_usd': 'precio_oferta_dolares'
                           }
                  )


app = dash.Dash(__name__)

#Variables
models_dict = {'NVIDIA': data['modelo'].loc[data['marca'] == 'NVIDIA'].unique().tolist(),
               'AMD': data['modelo'].loc[data['marca'] == 'AMD'].unique().tolist()}

fabricantes_dict = {'NVIDIA': data['fabricante'].loc[data['marca'] == 'NVIDIA'].unique().tolist(),
                    'AMD': data['fabricante'].loc[data['marca'] == 'AMD'].unique().tolist()}

app.layout = html.Div(children=[html.H1('GPU Data',
                                        style={'textAllign': 'center', 
                                           'color':'#503D36', 
                                           'font-size': 40}),
                                html.Div([
                                html.Div([
                                    html.Div([dcc.Dropdown(id='marca-dropdown', options=[
                                                                          {'label': i, 'value': i} for i in models_dict.keys()],
                                                                          placeholder='Seleccione la marca de la GPU',
                                                                          searchable=True
                                                                          )], style={'width': '350px'}),

                                    #Rellenamos este dropdown según la marca de GPU que se escoja arriba
                                    html.Div([dcc.Dropdown(id='modelo-dropdown', 
                                                                          options=[],
                                                                          placeholder='Seleccione el modelo de la GPU',
                                                                          searchable=True,
                                                                          value=''
                                                                          )], style={'width': '350px', 'padding-left': '20px'}),

                                    #Rellenamos este dropdown según el modelo de GPU que se escoja arriba
                                    html.Div([dcc.Dropdown(id='fabricante-dropdown',
                                                                          options = [],
                                                                          placeholder='Seleccione el fabricante de la GPU',
                                                                          searchable=True,
                                                                          value=''
                                                                          )], style={'width': '350px', 'padding-left': '20px'})                                      
                                    ], style={'display': 'flex'}),
                                ]),

                                html.Br(),
                                html.Div([
                                        html.Div([html.H2('Tabla de precios más recientes'),
                                                dash_table.DataTable(id='gpu-table', data=data[['marca', 'modelo', 'fabricante', 'precio_normal_pesos_chilenos', 'precio_oferta_pesos_chilenos']].to_dict('records'), 
                                                                       page_size=10,
                                                                       style_data={'max-width':'50%'},
                                                                       style_header={'backgroundColor': 'rgb(210, 210, 210)',
                                                                                     'color': 'black',
                                                                                     'fontWeight': 'bold'},
                                                                       tooltip_data=[{column: {'value': str(value), 'type': 'markdown'} for column, value in row.items()} for row in data[['marca', 'modelo', 'fabricante', 'precio_normal_pesos_chilenos', 'precio_oferta_pesos_chilenos']].to_dict('records')],
                                                                       tooltip_duration=None,
                                                                       style_table={'overflowX': 'auto'}
                                                                    )], 
                                        style={'max-width': '50%'}),
                                        html.Div([html.H2('Gráfico de precios vs Tiempo'),
                                                dcc.Graph(id='lineplot-precio-tiempo')]
                                        )], 
                                                
                                style={'display': 'flex'}),
                                
                        html.Br(),
                        html.Div([
                                    html.P('Precio promedio: \n', 
                                           style={'box-shadow': '2px 2px 2px #1f2c56',
                                                  'background-color': '#1f2c56', 
                                                  'position': 'relative',
                                                  'color': 'white'}
                                          ),

                                    html.P(id='precio-promedio', 
                                           style={'box-shadow': '2px 2px 2px #1f2c56',
                                                  'background-color': '#1f2c56', 
                                                  'position': 'relative',
                                                  'color': 'white'}
                                          ),

                                    html.P('Precio Mínimo', 
                                           style={'box-shadow': '2px 2px 2px #1f2c56',
                                                  'background-color': '#1f2c56', 
                                                  'position': 'relative',
                                                  'color': 'white'}
                                          ),
                                    
                                    html.P(id='precio-minimo', 
                                           style={'box-shadow': '2px 2px 2px #1f2c56',
                                                  'background-color': '#1f2c56', 
                                                  'position': 'relative',
                                                  'color': 'white'}
                                          ),

                                    html.P('Precio Máximo', 
                                           style={'box-shadow': '2px 2px 2px #1f2c56',
                                                  'background-color': '#1f2c56', 
                                                  'position': 'relative',
                                                  'color': 'white'}
                                          ),
                                    
                                    html.P(id='precio-maximo', 
                                           style={'box-shadow': '2px 2px 2px #1f2c56',
                                                  'background-color': '#1f2c56', 
                                                  'position': 'relative',
                                                  'color': 'white'}
                                          )
                                ]),

                        html.Div([
                            dcc.Graph(id='top-3-gpus-baratas')
                        ])
                    
                    ]
                                
                                
)

# Seteamos el callback para el dropdown de modelos de GPU según la marca
@app.callback(
    Output(component_id='modelo-dropdown', component_property='options'),
    Input(component_id='marca-dropdown', component_property='value')
)

def set_gpu_model_options(marca_seleccionada):
    if marca_seleccionada == 'NVIDIA':
        opciones = [{'label': i, 'value': i} for i in models_dict[marca_seleccionada]]
    elif marca_seleccionada == 'AMD':
        opciones = [{'label': i, 'value': i} for i in models_dict[marca_seleccionada]]
    else:
        opciones = []
    return opciones

# Callback para setear el dropdown de fabricante
@app.callback(
    Output(component_id='fabricante-dropdown', component_property='options'),
    Input(component_id='marca-dropdown', component_property='value')
)                                                                                                                                   

def set_fabricante_options(marca_seleccionada):
    if marca_seleccionada == 'NVIDIA':
        opciones = [{'label': i, 'value': i} for i in fabricantes_dict[marca_seleccionada]]
    elif marca_seleccionada == 'AMD':
        opciones = [{'label': i, 'value': i} for i in fabricantes_dict[marca_seleccionada]]
    else:
        opciones = []
    return opciones                                                    

# Callback para setear los datos mas recientes que se muestran de la tabla en base a los filtros marca, modelo, fabricante
@app.callback(
    Output(component_id='gpu-table', component_property='data'),
    [Input(component_id='marca-dropdown', component_property='value'),
     Input(component_id='modelo-dropdown', component_property='value'),
     Input(component_id='fabricante-dropdown', component_property='value')]
)

def update_gpu_table(marca, modelo, fabricante):
    filtered_df = data.copy()
    filtered_df = filtered_df[['marca', 'modelo', 'fabricante', 'precio_normal_pesos_chilenos', 'precio_oferta_pesos_chilenos', 'link_tarjeta', 'fecha_obtencion_info']]
    #Filtramos por la fecha mas reciente
    filtered_df = filtered_df.loc[filtered_df['fecha_obtencion_info'] == max(filtered_df['fecha_obtencion_info'])]

    #Lógica para mostrar otros datos según la búsqueda
    if marca and modelo and fabricante:
        filtered_df = filtered_df.query("marca == @marca and modelo == @modelo and fabricante == @fabricante")
    elif marca and modelo:
        filtered_df = filtered_df.query("marca == @marca and modelo == @modelo")
    elif marca:
        filtered_df = filtered_df.query("marca == @marca")

    return filtered_df.drop_duplicates().to_dict('records')

# Callback para setear el gráfico de precios
@app.callback(
    Output(component_id='lineplot-precio-tiempo', component_property='figure'),
    [Input(component_id='marca-dropdown', component_property='value'),
     Input(component_id='modelo-dropdown', component_property='value'),
     Input(component_id='fabricante-dropdown', component_property='value')]
)

def plot_graph(marca, modelo, fabricante):
    # Si no hay ninguna opción seleccionada entonces muestra el precio normal promedio de AMD y NVIDIA
    avg_price_df = data.copy()
    avg_price_df = data.groupby(['marca', 'fecha_obtencion_info'])['precio_normal_pesos_chilenos'].agg(['mean']).reset_index()
    fig = px.line(avg_price_df, x='fecha_obtencion_info', y='mean', color='marca')
    fig.update_layout(autosize=False, width=1000, yaxis_range=[0,2000000])
    
    # Si se selecciona alguna opcion el gráfico debe ir variando
    # Si selecciono marca y modelo entonces me tiene que mostrar eso, pero debe ser específico del fabricante también
    # sino voy a tener muchos modelos iguales y no voy a saber que precio mostrar
    if marca and modelo and fabricante:
        filtered_df = data.copy()
        
        filtered_df = data[['marca', 'modelo', 'fabricante', 'precio_normal_pesos_chilenos', 'fecha_obtencion_info']].query("marca == @marca and modelo == @modelo and fabricante == @fabricante")
        filtered_df = filtered_df.groupby(['marca', 'modelo', 'fabricante', 'fecha_obtencion_info'])['precio_normal_pesos_chilenos'].agg(['min']).reset_index()
        filtered_df = filtered_df.rename(columns={'min': 'precio_min_peso_chileno'})
        print(filtered_df)
        fig = px.line(filtered_df, x='fecha_obtencion_info', y='precio_min_peso_chileno', color='modelo')
    # filtered_df = data.loc[data['modelo'] == modelo]
    # fig = px.line(, x='fecha_obtencion_info', y='precio_normal_pesos_chilenos')
    # if modelo:
    #     fig = px.line(filtered_df, x='fecha_obtencion_info', y='precio_normal_pesos_chilenos', color=modelo)
    return fig

# Callback para actualizar el precio promedio de las tarjetas gráficas seleccionadas por el usuario
@app.callback(
    Output(component_id='precio-promedio', component_property='children'),
    [Input(component_id='marca-dropdown', component_property='value'),
     Input(component_id='modelo-dropdown', component_property='value'),
     Input(component_id='fabricante-dropdown', component_property='value')]
)

def obtener_precio_promedio(marca, modelo, fabricante):
    filtered_df = data.copy()
    if marca and modelo and fabricante:
        filtered_df = filtered_df.query('marca == @marca and modelo == @modelo and fabricante == @fabricante')
        precio_promedio = filtered_df['precio_normal_pesos_chilenos'].mean()
    elif marca and modelo:
        filtered_df = filtered_df.query('marca == @marca and modelo == @modelo')
        precio_promedio = filtered_df['precio_normal_pesos_chilenos'].mean()
    elif marca:
        filtered_df = filtered_df.query('marca == @marca')
        precio_promedio = filtered_df['precio_normal_pesos_chilenos'].mean()
    else:
        precio_promedio = filtered_df['precio_normal_pesos_chilenos'].mean()
    return precio_promedio

# Callback para mostrar el precio mínimo según los parámetros escogidos por el usuario
@app.callback(
    Output(component_id='precio-minimo', component_property='children'),
    [Input(component_id='marca-dropdown', component_property='value'),
     Input(component_id='modelo-dropdown', component_property='value'),
     Input(component_id='fabricante-dropdown', component_property='value')]
)

def obtener_precio_minimo(marca, modelo, fabricante):
    filtered_df = data.copy()
    if marca and modelo and fabricante:
        filtered_df = filtered_df.query('marca == @marca and modelo == @modelo and fabricante == @fabricante')
        precio_minimo = filtered_df['precio_normal_pesos_chilenos'].min()
    elif marca and modelo:
        filtered_df = filtered_df.query('marca == @marca and modelo == @modelo')
        precio_minimo = filtered_df['precio_normal_pesos_chilenos'].min()
    elif marca:
        filtered_df = filtered_df.query('marca == @marca')
        precio_minimo = filtered_df['precio_normal_pesos_chilenos'].min()
    else:
        precio_minimo = filtered_df['precio_normal_pesos_chilenos'].min()
    return precio_minimo

# Callback para mostrar el precio máximo según los parámetros escogidos por el usuario
@app.callback(
    Output(component_id='precio-maximo', component_property='children'),
    [Input(component_id='marca-dropdown', component_property='value'),
     Input(component_id='modelo-dropdown', component_property='value'),
     Input(component_id='fabricante-dropdown', component_property='value')]
)

def obtener_precio_maximo(marca, modelo, fabricante):
    filtered_df = data.copy()
    if marca and modelo and fabricante:
        filtered_df = filtered_df.query('marca == @marca and modelo == @modelo and fabricante == @fabricante')
        precio_maximo = filtered_df['precio_normal_pesos_chilenos'].max()
    elif marca and modelo:
        filtered_df = filtered_df.query('marca == @marca and modelo == @modelo')
        precio_maximo = filtered_df['precio_normal_pesos_chilenos'].max()
    elif marca:
        filtered_df = filtered_df.query('marca == @marca')
        precio_maximo = filtered_df['precio_normal_pesos_chilenos'].max()
    else:
        precio_maximo = filtered_df['precio_normal_pesos_chilenos'].max()
    return precio_maximo

@app.callback(
    Output(component_id='top-3-gpus-baratas', component_property='figure'),
    [Input(component_id='marca-dropdown', component_property='value'),
     Input(component_id='modelo-dropdown', component_property='value')]
)

def plot_cheapest_gpus(marca, modelo):
    filtered_df = data.copy()
    filtered_df = filtered_df.groupby(['marca', 'modelo'])['precio_normal_pesos_chilenos'].agg(['mean'])
    filtered_df = filtered_df.sort_values(by='mean', ascending=True)
    fig = px.bar(data_frame=filtered_df)
    pass

if __name__ == '__main__':
    app.run_server()
    

