# PI_MLOps

## STEAAM: MLOps for Steam (Data Engineering + Machine Learning)

![](https://github.com/paulusbrizzi/PI_MLOps/blob/main/banner.png?raw=true)

### Sobre el proyecto
A lo largo de este proyecto se ha trabajado sobre 3 tablas con datos crudos provenientes del sector australiano de la plataforma online de juegos Steam. Respectivamente, información relativa a Juegos (tags, categorías, precio, entre otros), Reviews (fecha, si recomendó, juego, opinión escrita, entre otros) e Items (usuario, juego, tiempo total jugado, entre otros).
[Diccionario de los datos crudos](https://shorturl.at/qst47)
El objetivo del proyecto consiste en realizar una API que facilite la consulta de ciertos datos definidos y formateados, entre ellos el resultado de un modelo de machine learning que recomienda 5 juegos similares a partir del id de un juego inicial.

### Desarrollo: Etapas
1. [EDA y ETL inicial](https://github.com/paulusbrizzi/PI_MLOps/blob/main/1_EDA%20y%20ETL%20inicial.ipynb)
El primer paso consistió en realizar un EDA preliminar para conocer en qué estado se encontraban cada una de las tablas, desde la búsqueda de datos nulos, tipos de datos e interpretación de los datos anidados. Este es uno de los puntos de desarrollo más fuerte del proyecto donde se tuvo en cuenta el objetivo final de datos a analizar para poder formatear los datos y facilitar enormemente el desarrollo de las tablas y funciones de la API.
Para el **SentimentAnalysis (Análisis de Sentimiento)** nos basamos en la columna reviews.reviews donde originalmente teníamos las opiniones escritas de los usuarios. Allí se trabajó con la librería NLTK (Natural Language Toolkit) que incluye un módulo llamado VADER (Valence Aware Dictionary and Sentiment Reasoner). Contiene un conjunto de palabras junto con sus puntuaciones de polaridad asociadas, permitiendo evaluar si una oración o documento tiene un tono positivo, negativo o neutro. Esta valoración finalmente se asoció a una nueva columna que facilitó su procesamiento.
A la par se desarrolló un [Nuevo Diccionario de Datos](https://docs.google.com/spreadsheets/d/1RmHLFxPNlqbSLH7GbCKKrIhiAyq_yW6PUq-9Y9YbphQ/edit?usp=sharing)
2. [ETL y defs para API](https://github.com/paulusbrizzi/PI_MLOps/blob/main/2_ETL%20y%20defs%20para%20API.ipynb)
Durante el desarrollo de este notebook nos basamos en las tablas resultantes del punto anterior [/Nuevo](https://github.com/paulusbrizzi/PI_MLOps/tree/main/nuevo) para producir nuevas tablas de consulta optimizadas a la información requerida por cada función de la API.
3. [EDA pre-ML](https://github.com/paulusbrizzi/PI_MLOps/blob/main/3_EDA%20pre-ML.ipynb)
Etapa explorativa de los datos. Se utilizaron gráficos para encontrar patrones de comportamiento.
4. [ML y def para API](https://github.com/paulusbrizzi/PI_MLOps/blob/main/4_ML%20y%20def%20para%20API.ipynb)
Durante esta etapa se transformaron datos de texto en un formato numérico de los que algoritmos de aprendizaje automático pueden entender. Este proceso se conoce como "vectorización de texto".
**CountVectorizer** toma una lista de documentos de texto y construye un vocabulario a partir de todas las palabras únicas presentes en esos documentos. Luego, transforma cada documento en un vector numérico, donde cada componente del vector representa la frecuencia de una palabra específica en ese documento. La matriz resultante es conocida como una matriz de términos de documento.
Mediante una función se creó una tabla con 5 juegos recomendados según la columna games.description que combinaba las características técnicas de dataframe original (games.specs) con los tags (games.tags). Luego se exportó para poder servir a la función de la API.

### Cómo usar
[Visite la API](https://pi-mlops-reb1.onrender.com/docs) y realice las consultas

Valores de entrada de ejemplo según función:
**developer:** valve, funcom
**userdata:** bigodo
**userforgenre:** action, education
**best_developer_year:** 2012, 2014
**developer_reviews_analysis:** 63200

### Cómo usar
[Video API en funcionamiento](https://youtu.be/I69cK6loEhg)

### Autoría
Pablo Juárez Brizzi
[Linkedin](https://www.linkedin.com/in/pablojbrizzi/)


