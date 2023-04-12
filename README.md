# gpu-data-analysis
En este proyecto veremos como varían los precios de las GPU's en Chile y realizaremos un dashboards que nos permita saber cual es la mejor opción para comprar

El objetivo de este proyecto es construir un dashboard que permita visualizar datos sobre tarjetas gráficas, para monitorizar su precio y hacer comparativas entre ellas para todas las personas que quieran comprarse una tarjeta gráfica. 

En base a los aprendido en la certificación IBM data science vamos a poner en práctica este proyecto utilizando la metodología para ciencia de datos. Esta consta de los siguientes pasos:

1. Entendimiento del problema
2. Enfoque analítico
3. Requerimiento de datos
4. Recolección de datos
5. Entendimiento de los datos recopilados
6. Preparación de los datos
7. Modelado
8. Evaluación
9. Despliegue
10. Feedback

En este proyecto no vamos a usar todos los pasos, porque no vamos a construir un modelo ni evaluarlo ni desplegarlo, sino solo vamos a recopilar los datos para ver si los podemos representar de mejor manera en un dashboard interactivo para tomar mejores decisiones con ellos.

## Fase 1: Entendimiento del problema

**Problema**: El mercado de tarjetas gráficas no está pasando por su mejor momento. La escasez de stock y los precios inflados hacen que sea difícil decidir qué tarjeta gráfica comprar, ya sea para uso gamer o para trabajar. Con este dashboard, que se actualiza cada 3 días, podrá monitorear los precios y tomar una decisión más informada.

**Como podemos ocupar los datos para responder y dar solución al problema?:** Podemos recolectar datos de distintas fuentes como el precio, las especificaciones técnicas, las tiendas donde se venden las tarjetas gráficas, las ofertas y en base a eso construir un dashboard interactivo para que las personas interesadas en comprar algún modelo, puedan hacerlo viendo cual es el mejor momento y el mejor precio para comprar.

**Cuál es el objetivo?**: Mejorar la toma de decisión para comprar tarjetas gráficas en el mercado actual.

## Fase 2: Enfoque analítico a utilizar

Como dijimos, no vamos a crear un modelo de predicción en este proyecto, sino que vamos a construir un dashboard en base a datos recopilados de internet.

## Fase 3: Requerimientos de datos

**Qué requisitos deben cumplir los datos (Domain Knowledge)?:** Para cada tarjeta gráfica debo obtener su:

1. ID
2. Marca
3. Modelo de la tarjeta gráfica
4. Fabricante de la tarjeta
5. Número de núcleos: Es el número de unidades de procesamiento de flujo (stream processors) que tiene la tarjeta gráfica.
6. Chip de la GPU (Unidad de Procesamiento Gráfico): es el chip principal que realiza los cálculos necesarios para renderizar gráficos en la pantalla.
7. Velocidad del reloj de la GPU: se mide en MHz o GHz y determina la velocidad a la que la GPU realiza los cálculos.
8. Memoria de video (VRAM): la cantidad de memoria RAM dedicada a la tarjeta gráfica. Se mide en gigabytes (GB) y afecta a la cantidad de datos que se pueden almacenar y procesar simultáneamente.
9. Ancho de banda del Bus de la tarjeta gráfica: la cantidad de datos que pueden ser transferidos entre la GPU y la placa base del ordenador. Se mide en bits, y un bus más ancho significa una transferencia de datos más rápida.
10. Interfaz de memoria: el tipo de memoria que utiliza la tarjeta gráfica para almacenar y acceder a los datos. Los tipos comunes incluyen DDR, GDDR, GDDR2, GDDR3, GDDR4, GDDR5, GDDR5, GDDR6, HBM y HBM2.
11. Resolución máxima soportada: la resolución máxima que puede admitir la tarjeta gráfica para la salida de la pantalla.
12. Consumo de energía: Es la cantidad de energía que consume la tarjeta gráfica en funcionamiento. Se mide en vatios (W).
13. Conectores de video: Es el tipo de conector que se utiliza para conectar la tarjeta gráfica al monitor, como HDMI, DisplayPort, VGA, DVI, entre otros.
14. Fecha de recopilación de la información
15. Link de la fuente
16. Largo de la tarjeta
17. Precio normal de la tarjeta pesos chilenos
18. Precio oferta de la tarjeta pesos chilenos
19. Precio normal de la tarjeta en dólares
20. Precio oferta de la tarjeta en dólares

**Cuál es el formato que tienen que tener los datos?:** Queremos que los datos tengan el formato correcto. Lo vamos a definir a continuación: 

1. ID: Debe ser un número, puede ser secuencial del 1 al X
2. Marca: La marca de la tarjeta deber ser “Nvidia” o “AMD”
3. Modelo: El modelo deber ser “”RTX 3070”, “RX 6700 XT”, etc
4. Fabricante: El fabricante debe ser “Gigabyte”, “Powercolor”, “XFX”, etc
5. Núcleos de procesamiento: Debe ser un número indicando cantidad
6. Chip de la tarjeta: Debe ser “AMD Radeon RX 6700 XT”, “Nvidia Geforce RTX 3070 Ti”, etc
7. Velocidad de reloj: Debe ser “2357”. Se mide en MHz.
8. Memoria de video(VRAM): Debe ser “16”, “8”. Se mide en GB.
9. Ancho de banda del bus de memoria: Debe ser “256”. Se mide en bits
10. Interfaz de memoria: Debe ser “GDDR6”, “GDDR5”, etc.
11. Resolución máxima soportada: Debe ser “1440p”, “4k”, “1080p”, etc.
12. Consumo de energía: Debe ser “”250”, “300”, etc. Se mide en Watts
13. Conectores de video: Debe ser “2xHDMI 2.1 1xDisplayPort 1.4”, etc.
14. Fecha de recopilación de la información: Debe ser “14/03/2023”. Formato date
15. Link de la página web: Debe ser “https://www.amazon.com”, etc.
16. Largo de la tarjeta: Debe ser “30”. Se mide en cm
17. Precio: Debe ser “1250”. Se mide en dólares.
18. Precio oferta de la tarjeta pesos chilenos
19. Precio normal de la tarjeta en dólares
20. Precio oferta de la tarjeta en dólares
21. Tipo de bus: Debe ser “PCI Express 3.0”

**De donde vamos a recopilar los datos?:** A continuación se muestran las fuentes desde donde vamos a recopilar los datos de las tarjetas gráficas.

1. Solotodo: Tiene API pública

**Qué datos no vamos a tener en cuenta?:** Es importante señalar esto porque no vamos a recopilar información de todas las tarjetas gráficas del mercado sino solamente de la anterior y de la nueva generación, es decir series 3000 y 4000 de Nvidia y serie 6000 y 7000 de AMD. Todas las demás se dejan fuera de la recolección. Las tarjetas Intel también se dejan de lado.

**Vista previa de como se debería ver la información representada en un DataFrame:**

| ID(integer) | Marca (string) | Modelo (string) | Fabricante (string) | Núcleos de procesamiento (integer o float) | Chip de la tarjeta (GPU, string) | Velocidad del reloj (float) | Memoria de video (integer) | Ancho de banda del bus de memoria (float) | Interfaz de memoria (string) | Resolución maxima soportada (string) | Consumo de energía (integer) | Conectores de video (string) | Fecha de recopilación de la información (date) | Link de la pagina web (string) | Largo de la tarjeta | Ancho de la tarjeta | Precio (float) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

## Fase 4: Data Collection

**Quiénes son los fabricantes de tarjetas gráficas?:** 

| Nvidia | Amd |
| --- | --- |
| Asus | ASRock
Colorful | Asus
EVGA (Ya no) | Biostar
Gainward | Diamond Multimedia
Galax | Gigabyte
Gigabyte | HIS
Inno3D | MSI
KFA2 | PowerColor
Leadtek | Sapphire
Manli | VisionTek
MSI | XFX
Palit | Yeston
PNY
Zotac 

**Qué modelos de tarjetas voy a considerar?:**

| Nvidia | AMD |
| --- | --- |
| GeForce RTX 3050 | Radeon RX 6500 XT
GeForce RTX 3060 | Radeon RX 6600
GeForce RTX 3060 Ti | Radeon RX 6600 XT
GeForce RTX 3070 | Radeon RX 6650 XT
GeForce RTX 3070 Ti | Radeon RX 6700 XT
GeForce RTX 3080 | Radeon RX 6750 XT
GeForce RTX 3080 Ti | Radeon RX 6800
GeForce RTX 3090 | Radeon RX 6800 XT
GeForce RTX 3090 Ti | Radeon RX 6900 XT
GeForce RTX 4090 | Radeon RX 7900 XTX
GeForce RTX 4080 | Radeon RX 7900 XT
GeForce RTX 4070 Ti | 

**Cómo voy a recolectar los datos?:** A través de la API pública de Solotodo.

**Es necesario guardar los datos por más tiempo?:** Podría almacenar todo el registro de datos que se recolecta en una base de datos y luego mostrar en un dashboard los resultados más recientes, a excepción de la linea de tiempo mostrando la evolución en los precios. Pero eso lo puedo hacer con consultas sql directamente desde jupyter haciendo la conexión a la base de datos para extraer la información.

Por el momento los csv generados los voy añadiendo manualmente a la base de datos pero debo crear un script que lo haga de forma automática.
