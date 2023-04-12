#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
pd.set_option('display.max_columns', None)


# In[2]:


import requests

session = requests.Session()

# El yield agrega a una lista las responses que va capturando. Es diferente al return porque no retorna un solo valor
# Luego hago un loop sobre esa lista y agrego los datos a un dataframe
def get_items_pages():
  url = "https://publicapi.solotodo.com/products/browse/?ordering=discount&websites=2&categories=2&exclude_refurbished=true&stores=1085&stores=30&stores=3&stores=4253&stores=4913&stores=279&stores=128&stores=920&stores=5739&stores=2570&stores=4418&stores=4847&stores=1712&stores=4&stores=722&stores=5771&stores=788&stores=2603&stores=3758&stores=201&stores=398&stores=397&stores=755&stores=3626&stores=4056&stores=31&stores=61&stores=193&stores=7&stores=5705&stores=1052&stores=5639&stores=4187&stores=3164&stores=656&stores=3131&stores=16&stores=426&stores=261&stores=4979&stores=4451&stores=1911&stores=88&stores=3791&stores=1580&stores=283&stores=172&stores=38&stores=2801&stores=559&stores=9&stores=326&stores=4682&stores=2735&stores=4484&stores=1976&stores=2240&stores=1217&stores=1448&stores=1811&stores=3692&stores=393&stores=232&stores=5573&stores=87&stores=27&stores=281&stores=4287&stores=56&stores=1283&stores=1845&stores=2967&stores=4814&stores=292&stores=5540&stores=5&stores=524&stores=199&stores=43&stores=4154&stores=228&stores=294&stores=23&stores=290&stores=392&stores=887&stores=260&stores=225&stores=4583&stores=3395&stores=265&stores=287&stores=3362&stores=37&stores=118&stores=5078&stores=39&stores=5144&stores=2339&stores=921&stores=257&stores=5738&stores=266&stores=3263&stores=986&stores=3890&stores=4880&stores=3659&stores=11&stores=278&stores=34&stores=12&stores=198&stores=3098&stores=1547&stores=4946&stores=1118&stores=28&stores=3824&stores=5177&stores=186&stores=2471&stores=18&stores=2009&stores=223&stores=2306&stores=2768&stores=194&stores=956&stores=2042&stores=293&stores=1877&stores=623&stores=67&stores=47&stores=86&stores=183&stores=22&stores=5672&stores=4550&stores=4352&stores=1514&stores=3165&stores=955&stores=2999&stores=1086&stores=2670&stores=2438&stores=4121&stores=2669&stores=176&stores=181&stores=4616&stores=167&stores=3032&stores=4715&stores=173&stores=264&stores=4220&stores=35&stores=170&stores=231&stores=2636&stores=6&stores=280&stores=2174&stores=2141&stores=789&stores=359&stores=2835&stores=44&stores=821&stores=63&stores=14&stores=239&stores=45&stores=1613&stores=85&stores=4386&stores=1151&stores=3230&stores=91&stores=3099"

  # Fetch the first page and return it
  response = session.get(url).json()
  yield response

  for page in range(2, 40): #Este valor puede ir cambiando
    response = session.get(url, params={'page': page}).json()
    yield response


df = pd.DataFrame()
for i in get_items_pages():    
    for j in range(len(i['results'])):
        try:
            df = pd.concat([df, pd.json_normalize(i['results'][j]['product_entries'][0])], axis='rows')
        except:
            print('Error al unir los datos')

    
df.shape


# In[3]:


df.head()


# ### Diccionario para mapear la info que necesitamos con la data de la API
# 
# 1. ID: Debe ser un número, puede ser secuencial del 1 al X -> Podemos setear un index después
# 2. Marca: La marca de la tarjeta deber ser “Nvidia” o “AMD” -> Columna `product.specs.gpu_line_family_brand_brand_name`
# 3. Modelo: El modelo deber ser “”RTX 3070”, “RX 6700 XT”, etc -> Columna `product.specs.gpu_name`
# 4. Fabricante: El fabricante debe ser “Gigabyte”, “Powercolor”, “XFX”, etc -> Columna `product.brand_name`
# 5. Núcleos de procesamiento: Debe ser un número indicando cantidad -> Columna `product.specs.gpu_stream_processors`
# 6. Chip de la tarjeta: Debe ser “AMD Radeon RX 6700 XT”, “Nvidia Geforce RTX 3070 Ti”, etc -> Columna `product.specs.gpu_unicode`
# 7. Velocidad de reloj: Debe ser “2357”. Se mide en MHz. -> Columna `product.specs.core_clock`
# 8. Memoria de video(VRAM): Debe ser “16”, “8”. Se mide en GB. -> Columna `product.specs.memory_quantity_value` o sino `product.specs.memory_quantity_unicode`
# 9. Ancho de banda del bus de memoria: Debe ser “256”. Se mide en bits -> Columna `product.specs.memory_bus_width_value`
# 10. Interfaz de memoria: Debe ser “GDDR6”, “GDDR5”, etc. -> Columna `product.specs.memory_type_name` o `product.specs.memory_type_unicode`
# 11. Resolución máxima soportada: Debe ser “1440p”, “4k”, “1080p”, etc. -> No está ese dato **Ver como crearlo**
# 12. Consumo de energía o TDP: Debe ser “”250”, “300”, etc. Se mide en Watts -> Columna `product.specs.gpu_tdp`
# 13. Conectores de video: Debe ser “2xHDMI 2.1 1xDisplayPort 1.4”, etc. -> Columna `product.specs.video_ports` pero falta arreglarlo. **Hacer una función para extraer esos datos**
# 14. Fecha de recopilación de la información: Debe ser “14/03/2023”. Formato date -> Hacer una columna datetime
# 15. Link de la página web: Debe ser “https://www.solotodo.cl/{id}”, etc. -> Ver como creo el link en base a la info.
# 16. Largo de la tarjeta: Debe ser “30”. Se mide en cm -> Columna `product.specs.length`
# 17. Precio normal en dolares: Debe ser “1250”. Se mide en dólares. -> Columna `metadata.normal_price_usd` o `metadata.offer_price_usd` pero hay que arreglarlo bien. **Crear una función para extraer el precio o los precios de la API.**
# 18. Precio oferta de la tarjeta pesos chilenos
# 19. Precio normal de la tarjeta pesos chilenos
# 20. Precio oferta de la tarjeta en dólares
# 21. Tipo de bus de la tarjeta: Debe ser "PCI Express 3.0 x8" -> Columna `product.specs.bus_unicode`

# ## Creación del dataframe base

# In[4]:


columnas = ['product.specs.gpu_line_family_brand_brand_name', 'product.specs.gpu_name',
            'product.brand_name', 'product.specs.gpu_stream_processors',
            'product.specs.gpu_unicode', 'product.specs.core_clock',
            'product.specs.memory_quantity_value', 'product.specs.memory_bus_width_value',
            'product.specs.memory_type_name', 'product.specs.gpu_tdp',
            'product.specs.length', 'product.specs.bus_unicode',
            'metadata.normal_price_usd', 'metadata.offer_price_usd']
            
#Estas dos columnas son en pesos chilenos 'metadata.prices_per_currency.normal_price', 'metadata.prices_per_currency.offer_price'
# Hacer función para extraer esa data.

df_base = df[columnas]


# In[5]:


df_base.shape


# In[6]:


df.columns


# ## Columnas que nos falta agregar bien
# 
# <ol>
#     <li><del>Precio normal de la tarjeta en pesos chilenos</del></li>
#     <li><del>Precio oferta de la tarjeta en pesos chilenos</del></li>
#     <li><del>Conectores de video disponibles en la tarjeta</del></li>
#     <li><del>Link URL de la tarjeta</del></li>
#     <li><del>Fecha de obtención de la información</del></li>
#     <li><del>Resolución máxima soportada por la tarjeta</del></li>
# </ol>

# ### Creacion de la columna `precio_normal_pesos_chilenos`

# In[7]:


precio_normal_chileno = []
for i in df['metadata.prices_per_currency']:
    precio_normal_chileno.append(i[0]['normal_price'])

precio_normal_chileno[:5]


# In[8]:


df1 = df_base.copy()
df1['precio_normal_pesos_chilenos'] = precio_normal_chileno


# In[9]:


df1.head()


# ### Creacion de la columna `precio_oferta_pesos_chilenos`

# In[10]:


precio_oferta_chileno = []
for i in df['metadata.prices_per_currency']:
    precio_oferta_chileno.append(i[0]['offer_price'])

precio_oferta_chileno[:5]


# In[11]:


df2 = df1.copy()
df2['precio_oferta_pesos_chilenos'] = precio_oferta_chileno


# In[12]:


df2.head()


# ### Creacion de la columna `conectores_de_video`

# In[13]:


import numpy as np
lista_conectores_video = []
for i in df['product.specs.video_ports']:
    try:
        #DisplayPort            #HDMI
        lista_conectores_video.append(i[0]['unicode'] + '; ' + i[1]['unicode'])
    except:
        lista_conectores_video.append(np.nan)

lista_conectores_video[:5]


# In[14]:


df3 = df2.copy()
df3['conectores_de_video'] = lista_conectores_video


# In[15]:


df3.head()


# ### Creacion del link de búsqueda de la tarjeta

# Para el link podemos buscar el producto de la siguiente manera: "https://www.solotodo.cl/products/{id}" siendo el id el identificador de la tarjeta que podemos obtener de los datos obtenidos por la api

# In[16]:


lista_urls = []
for i in df['product.id']:
    lista_urls.append(f'https://www.solotodo.cl/products/{i}')
lista_urls[:5]


# In[17]:


df4 = df3.copy()
df4['link_tarjeta'] = lista_urls


# In[18]:


df4.head()


# ### Creacion de la columna `fecha_obtencion_info`

# In[19]:


import datetime
lista_fechas = [datetime.datetime.now().strftime("%d/%m/%Y") for i in range(len(df))]
lista_fechas[:5]    


# In[20]:


df5 = df4.copy()
df5['fecha_obtencion_info'] = lista_fechas


# In[21]:


df5


# ### Creación de la columna `resolucion_maxima_soportada`

# In[22]:


df_resolution = pd.read_csv('resoluciones_maximas_tarjetas.csv', sep=';')
df_resolution


# In[23]:


df6 = df5.copy()
df6['resolucion_maxima_soportada'] = df6['product.specs.gpu_name'].map(df_resolution.set_index('Tarjeta Gráfica')['Resolución máxima para jugar juegos'])
df6.head()


# ### Creacion del dataframe que contenga solo informacion de las tarjetas que queremos
# 
# En particular se definió la siguiente lista de tarjetas a analizar:

# | Nvidia              | AMD                |
# |---------------------|--------------------|
# | RTX 3050    | RX 6500 XT  |
# | RTX 3060    | RX 6600     |
# | RTX 3060 Ti | RX 6600 XT  |
# | RTX 3070    | RX 6650 XT  |
# | RTX 3070 Ti | RX 6700 XT  |
# | RTX 3080    | RX 6750 XT  |
# | RTX 3080 Ti | RX 6800     |
# | RTX 3090    | RX 6800 XT  |
# | RTX 3090 Ti | RX 6900 XT  |
# | RTX 4090    | RX 7900 XTX |
# | RTX 4080    | RX 7900 XT  |
# | RTX 4070 Ti |                    |

# In[24]:


lista_tarjetas = ['RTX 3050', 'RTX 3060', 'RTX 3060 Ti', 'RTX 3070', 'RTX 3070 Ti', 'RTX 3080', 'RTX 3080 Ti',
                'RTX 3090', 'RTX 3090 Ti', 'RTX 4090', 'RTX 4080', 'RTX 4070 Ti', 'RX 6500 XT', 'RX 6600', 
                'RX 6600 XT', 'RX 6650 XT', 'RX 6700 XT', 'RX 6750 XT', 'RX 6800', 'RX 6800 XT',
                'RX 6900 XT', 'RX 7900 XTX', 'RX 7900 XT']


# In[25]:


df7 = df6.loc[df5['product.specs.gpu_name'].isin(lista_tarjetas)]
df7


# ### Creación del dataframe final

# In[26]:


df7 = df7.reset_index(drop=True)
df7


# ### Formateamos las columnas del dataframe a sus valores correspondientes

# In[27]:


df7['metadata.normal_price_usd'] = df7['metadata.normal_price_usd'].astype('float')
df7['metadata.offer_price_usd'] = df7['metadata.offer_price_usd'].astype('float')
df7['precio_normal_pesos_chilenos'] = df7['precio_normal_pesos_chilenos'].astype('float')
df7['precio_oferta_pesos_chilenos'] = df7['precio_oferta_pesos_chilenos'].astype('float')


# ## Insertamos la columna ID para identificar las tarjetas

# In[ ]:


# El id va a ser un número del 1 al x


# ### Exportamos el dataframe a csv

# In[28]:


path = f'Data/gpu-data-{datetime.datetime.now().strftime("%d-%m-%Y")}.csv'
df7.to_csv(path, decimal=',', sep=';', index=False)


# In[29]:


df7.head()


# # Iteraciones para recopilar datos y ponerlos en una BBDD

# In[ ]:


# !pip install ipython-sql
# !pip install sqlalchemy==1.3.24 #%load_ext sql es compatible con esta version de sqlalchemy.


# In[36]:


# Una vez ejecutado el codigo de arriba y obtenido los datos en un dataframe, vamos a conectarnos
# a la BBDD y subir los datos.

# Creamos la conexion a SQL Server
import pyodbc

try:
    conn = pyodbc.connect(Trusted_Connection='yes', 
                          driver = '{SQL Server}',
                          server = 'PC-JOSALO\SQLEXPRESSSERVER', 
                          database = 'GPU_DATABASE')
    cur = conn.cursor()

    for index, row in df7.iterrows():    
        cur.execute('''INSERT INTO dbo.gpu_data 
                        (product_specs_gpu_line_family_brand_brand_name,
                         product_specs_gpu_name,
                         product_brand_name,
                         product_specs_gpu_stream_processors,
                         product_specs_gpu_unicode,
                         product_specs_core_clock,
                         product_specs_memory_quantity_value,
                         product_specs_memory_bus_width_value,
                         product_specs_memory_type_name,
                         product_specs_gpu_tdp,
                         product_specs_length,
                         product_specs_bus_unicode,
                         metadata_normal_price_usd,
                         metadata_offer_price_usd,
                         precio_normal_pesos_chilenos,
                         precio_oferta_pesos_chilenos,
                         conectores_de_video,
                         link_tarjeta,
                         fecha_obtencion_info,
                         resolucion_maxima_soportada) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                                                          row['product.specs.gpu_line_family_brand_brand_name'],
                                                                          row['product.specs.gpu_name'], 
                                                                          row['product.brand_name'], 
                                                                          row['product.specs.gpu_stream_processors'],
                                                                          row['product.specs.gpu_unicode'],
                                                                          row['product.specs.core_clock'],
                                                                          row['product.specs.memory_quantity_value'],
                                                                          row['product.specs.memory_bus_width_value'],
                                                                          row['product.specs.memory_type_name'],
                                                                          row['product.specs.gpu_tdp'],
                                                                          row['product.specs.length'],
                                                                          row['product.specs.bus_unicode'],
                                                                          row['metadata.normal_price_usd'],
                                                                          row['metadata.offer_price_usd'],
                                                                          row['precio_normal_pesos_chilenos'],
                                                                          row['precio_oferta_pesos_chilenos'],
                                                                          row['conectores_de_video'],
                                                                          row['link_tarjeta'],
                                                                          row['fecha_obtencion_info'],
                                                                          row['resolucion_maxima_soportada'])

    conn.commit()
    cur.close()
    print('|-------------------Datos guardados exitosamente en la base de datos-------------------|')

except Exception as e:
    print(e)

