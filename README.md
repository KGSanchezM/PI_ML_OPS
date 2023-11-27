![Steam](src/portada.png)
<br />
# Machine Learning Operations (MLOps): Sistema de Recomendación de Videojuegos para Usuarios de Steam

## Descripción del Proyecto

En este proyecto, trabajamos con tres conjuntos de datos en formato JSON, los cuales presentan una estructura anidada. Debemos extraer información para la creación de un sistema de recomendación. A través de un proceso de ETL (Extracción, Transformación y Carga).

Los conjuntos de datos son los siguientes:

1. **australian_user_reviews.json**
   - Ruta: [`Datsets/australian_user_reviews.json`](Datsets/australian_user_reviews.json)

2. **australian_user_items.json**
   - Ruta: [`Datsets/australian_users_items.json.gz`](Datsets/australian_users_items.json.gz)

3. **output_steam_games.json**
   - Ruta: [`Datsets/output_steam_games.json.gz`](Datsets/output_steam_games.json)

La información detallada sobre el contenido de cada conjunto se encuentra especificada en el diccionario de datos, disponible en el archivo Excel:
[`Datsets/Diccionario de Datos STEAM.xlsx`]([Datsets/Diccionario%de%Datos%STEAM.xlsx](https://github.com/KGSanchezM/PI_ML_OPS/blob/main/Datsets/Diccionario%20de%20Datos%20STEAM.xlsx))

Debido a restricciones de espacio en el repositorio, el archivo `australian_users_items` ha sido comprimido utilizando la herramienta Gzip.


## Objetivo

Desarrollar un sistema de recomendación de juegos utilizando los conjuntos de datos proporcionados. Abordaremos todas las fases clave de Data Engineering, desde la preparación de datos (ETL) hasta el análisis exploratorio y la implementación del modelo. <br />
<br />

## Proceso del Proyecto <br />
<br />

### **1.- ETL (Extracción, Transformación y Carga):** <br />

Esta primera etapa se centra en extraer los archivos JSON y convertirlos a archivos CSV. Se realiza la desanidación de las columnas, manteniendo solo aquellas necesarias para el sistema de recomendación y los endpoints propuestos. También se lleva a cabo el tratamiento de valores faltantes con el objetivo de dejar los datos limpios y preparados para su uso en los endpoints y el sistema de recomendación.

El proceso detallado se describe en el [proceso de ETL](Notebooks/1.-ETL.ipynb). Como resultado de aplicar el proceso de ETL, se generaron los siguientes archivos CSV: [steam_games](Datsets/CSV/steam_games.csv), [user_reviews](Datsets/CSV/user_reviews.csv) y [user_items](Datsets/CSV/users_items.csv.gz).

Cabe destacar que el archivo de user_items se comprimió con la herramienta GZIP debido a limitaciones de espacio.


### **2.-Feature Engineering:** 
Se ha creado la columna 'sentiment_analysis' aplicando análisis de sentimiento a las reseñas de los usuarios mediante la librería NLTK. La asignación de valores es la siguiente: '0' si es una reseña negativa, '1' si es neutral y '2' si es positiva. Esta nueva columna se ha introducido para reemplazar la columna original 'user_reviews.review', facilitando así el trabajo de los modelos de machine learning y el análisis de datos.

Para obtener más detalles sobre este proceso, puedes consultar la sección correspondiente en el [notebook de análisis de sentimiento](Notebooks/2.-analisis_sentiemientos.ipynb).



### **3.- Funciones de consultas** <br />

- **def PlayTimeGenre( genero : str ):** Debe devolver año con mas horas jugadas para dicho género.[Notebook](Notebooks/3.-play_time_genre.ipynb)

Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}. 

- **def UserForGenre( genero : str ):** Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.[Notebook](Notebooks/4.-user_for_genre.ipynb)

Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}.

- **def UsersRecommend( año : int ):** Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)[Notebook](Notebooks/5.-users_recommend.ipynb)

Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}].

- **def UsersWorstDeveloper( año : int ):** Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)[Notebook](Notebooks/6.-users_worst_developer.ipynb)

Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}].

- **def sentiment_analysis( empresa desarrolladora : str ):** Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.[Notebook](Notebooks/7.-sentiment_analysis.ipynb)

Ejemplo de retorno: {'Valve' : [Negative = 182, Neutral = 120, Positive = 278]}

### **4.- API**

Se implementó una API utilizando FastApi para exponer las funciones de consulta como endpoints y tambien se uso Reder. La documentación de la API se puede encontrar en https://api-steam-games-me3w.onrender.com/docs.

### **5.-EDA**

Realice el análisis exploratorio de datos (EDA). Durante este proceso, se exploraron y examinaron  los conjuntos de datos. 
[Notebook del Análisis Exploratorio de Datos (EDA)](Notebooks/8.-EDA.ipynb).


### **6.-. Sistema de recomendación** <br />

Crear el sistema de recomendación con dos enfoques distintos:

- **Sistema de Recomendación ítem-ítem:**
Mmodelo que recomienda juegos similares en función de un juego dado. Se utilizó la similitud del coseno como métrica principal para establecer la relación entre juegos.[Notebook](Notebooks/9.-sistema_recomendacion_item_item.ipynb)

- **Sistema de Recomendación usuario-ítem:**
Modelo que recomienda juegos a un usuario basándose en las preferencias de otros usuarios similares.[Notebook](Notebooks/10.-sistema_recomendacion_user_item.ipynb)


### **6.- Video Explicativo**

Creé un video explicativo detallando el uso de los endpoints desplegados en la plataforma Render.



## Estructura del Repositorio

**1. [/Notebooks](Notebooks/):** Contiene los Jupyter Notebooks donde se realizaron todas las operaciones de este proyecto. Cada notebook se explica paso a paso cómo se lograron los resultados.

**2. [/Datsets](Datsets/):** Almacena los datasets utilizados.
   - **Archivos_API:** Contiene los datasets consumidos por la API.
   - **CSV:** Contiene los archivos después de haber realizado el ETL.
   - **Modelo_ML:** Contiene los archivos consumidos por la API para hacer el sistema de recomendación.


