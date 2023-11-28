from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
import pandas as pd


app = FastAPI(title='API Steam Games')

#Mensaje de bienvenida
@app.get("/")
async def root():
    return {"Mensaje": "Bienvenidos a mi proyecto individual del bootcamp SoyHenry"}

#PlayTimeGenre
@app.get("/PlayTimeGenre/{genero :str}")
async def user(genero: str):
    """
    Obtiene el año de lanzamiento con más horas jugadas
    para un género de juegos específico.

    Parámetros:
        genero (str): El género de juegos para el cual se quiere obtener la información.

    Returns:
        JSONResponse: Una respuesta JSON con el año de lanzamiento con más horas jugadas
        para el género especificado, ó un mensaje de error si no se encuentra información.
    """
    try:
        # Cargar el DataFrame desde el archivo CSV
        df_genero = pd.read_csv("Datsets/Archivos_API/PlayTimeGenre.csv")

        # Filtrar el DataFrame para obtener solo las filas del género especificado
        df_genero = df_genero[df_genero['genres'] == genero]

        if not df_genero.empty:
            # Encontrar el año con la máxima cantidad de horas jugadas
            anio_mas_jugado = df_genero.loc[df_genero['playtime_forever'].idxmax()]['release_year']
            
            # Crear y devolver una respuesta exitosa
            return JSONResponse(
                status_code=200,
                content={
                    "results": f'Año de lanzamiento con más horas jugadas para el género {genero}: {int(anio_mas_jugado)}'
                }
            )
        else:
            # Devolver una respuesta de error si no se encuentra información para el género
            return JSONResponse(
                status_code=404,
                content={'error': f"No se encontró información del género '{genero}'"}
            )

    except Exception as e:
        # Manejar cualquier excepción y devolver una respuesta de error
        return JSONResponse(
            status_code=500,
            content={'error': f"Error interno: {str(e)}"}
        )

#UserForGenre
@app.get("/UserForGenre/{genero :str}")
async def user(genero: str):
    """
    Obtiene el usuario con el mayor tiempo de juego para un género dado.

    Parámetros:
    - genero: El género para el cual se solicita la información del usuario.

    Devuelve:
    - Respuesta JSON que contiene al usuario con mayor tiempo de juego para el género especificado y su tiempo de juego por año.
    """
    try:
        # Leer el archivo CSV que contiene la información del usuario para el género dado
        df_usuario_por_genero = pd.read_csv("Datsets/Archivos_API/UserForGenre.csv")

        # Filtrar datos para el género especificado
        datos_genero = df_usuario_por_genero[df_usuario_por_genero['genres'] == genero]

        if not datos_genero.empty:
            # Crear una lista de diccionarios para el tiempo de juego por año
            tiempo_juego_por_anio = [{'Año': int(anio), 'Tiempo de Juego': int(tiempo_juego)} for anio, tiempo_juego in datos_genero[['release_year', 'playtime_forever']].values]

            # Crear el diccionario de salida
            resultado = {
                'Usuario con mayor tiempo de juego para el género ' + genero: datos_genero.iloc[0]['user_id'],
                'Horas jugadas': tiempo_juego_por_anio
            }

            return resultado
        else:
            # Devolver una respuesta de error si no se encuentra información para el género
            return JSONResponse(
                status_code=404,
                content={'error': f"No se encontró información del género '{genero}'"}
            )

    except Exception as e:
        # Manejar cualquier excepción y devolver una respuesta 500
        raise HTTPException(
            status_code=500,
            detail=f"Error Interno del Servidor: {str(e)}"
        )

#UsersRecommend
@app.get("/UsersRecommend/{año :int}")
async def user(año: int):
    """
    Obtiene los 3 juegos más recomendados por usuarios para el año ingresado.

    Parámetros:
    - año (int): El año para el cual se desean obtener las recomendaciones.

    Returns:
    - dict: Un diccionario que contiene el top 3 de juegos recomendados en el formato:
        {"Puesto 1": "Nombre del Juego1", "Puesto 2": "Nombre del Juego2", "Puesto 3": "Nombre del Juego3"}
        En caso de no haber recomendaciones para el año especificado, devuelve una respuesta de error.
    """
    try:
        # Leer el archivo CSV que contiene la información de las recomendaciones para el año dado
        recomendaciones_anio = pd.read_csv("Datsets/Archivos_API/UsersRecommend.csv")

        # Verificar si hay revisiones para el año dado
        if not recomendaciones_anio.empty:
            # Filtrar las revisiones para el año dado y recomendaciones positivas/neutrales
            recomendaciones = recomendaciones_anio[recomendaciones_anio['posted_year'] == int(año)]
            
            # Ordenar en orden descendente por la cantidad de recomendaciones
            recomendaciones = recomendaciones.sort_values('recommend', ascending=False)
            
            # Crear una única línea de resultado
            resultado = {
                "Puesto 1": recomendaciones.iloc[0]['app_name'],
                "Puesto 2": recomendaciones.iloc[1]['app_name'],
                "Puesto 3": recomendaciones.iloc[2]['app_name']
            }
            
            return resultado
        else:
            # Devolver una respuesta de error si no se encuentra información para el año
            return JSONResponse(
                status_code=404,
                content={'error': f"No hay recomendaciones para el año {año}"}
            )
    except Exception as e:
        # Manejar cualquier excepción y devolver una respuesta 500
        raise HTTPException(
            status_code=500,
            detail=f"Error Interno del Servidor: {str(e)}"
        )

#UsersWorstDeveloper 
@app.get("/UsersWorstDeveloper/{año :int}")
async def Users(año: int):
    """
    Obtiene las tres desarrolladoras con menos recomendaciones por usuarios para el año dado.

    Parámetros:
    - año (int): Año para el cual se desea obtener el top 3 de desarrolladoras con menos recomendaciones.

    Returns:
    - List[Dict[str, str]]: Lista con las 3 desarrolladoras menos recomendadas.
      Ejemplo de retorno: [{"Puesto 1": X}, {"Puesto 2": Y}, {"Puesto 3": Z}]
    """
    try:
        # Leer el archivo CSV que contiene la información de las recomendaciones por desarrollador
        recomendaciones = pd.read_csv("Datsets/Archivos_API/UsersWorstDeveloper.csv")

        # Filtrar desarrolladoras para el año dado
        desarrolladoras = recomendaciones[recomendaciones['posted_year'] == int(año)]

        if not desarrolladoras.empty:
            # Encuentra las 3 desarrolladoras con menos recomendaciones
            desarrolladoras_top3 = desarrolladoras.nsmallest(3, 'recommend')
            resultado = [{"Puesto 1": desarrolladoras_top3.iloc[0]['developer']},
                         {"Puesto 2": desarrolladoras_top3.iloc[1]['developer']},
                         {"Puesto 3": desarrolladoras_top3.iloc[2]['developer']}]
            return resultado
        else:
            # Devolver una respuesta de error si no se encuentra información para el año
            return JSONResponse(
                status_code=404,
                content={'error': f"No se encontraron datos para el año '{año}'"}
            )
    except Exception as e:
        # Manejar cualquier excepción y devolver una respuesta 500
        raise HTTPException(
            status_code=500,
            detail=f"Error Interno del Servidor: {str(e)}"
        )

#Sentimen_analysis
@app.get("/sentiment_analysis/{developer :str}")
async def user(developer: str):
    """
    Obtiene la cantidad de comentarios positivos, negativos y neutrales del desarrollador ingresado.

    Parámetros:
    - developer (str): Nombre del desarrollador para el que se desea obtener la cantidad de comentarios.

    Returns:
    - dict: Un diccionario que contiene el análisis de sentimientos para el desarrollador especificado.
    """

    try:
        # Cargar el DataFrame desde el archivo CSV
        analisis_sentimientos_df = pd.read_csv("Datsets/Archivos_API/sentiment_analysis.csv")

        developer_column = analisis_sentimientos_df["developer"].tolist()

        if developer in developer_column:
            index = developer_column.index(developer)
            sentiment_counts = analisis_sentimientos_df.iloc[index, 1:].to_dict()
            return {developer: sentiment_counts}
        else:
            # Devolver una respuesta de error si no se encuentra información para el género
            return JSONResponse(
                status_code=404,
                content={'error': f"No se encontró información del desarrollador '{developer}'"}
            )

    except Exception as e:
        # Manejar cualquier excepción y devolver una respuesta de error
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}"
        )

#Recomendación_juegos
@app.get("/recomendacion_juego/{id_juego :str}")
async def user(id: str):
    """
    Obtiene las recomendaciones para un juego basándose en juegos similares a él.

    Parámetros:
    - id_juego (str): El código id del juego.

    Returns:
    - dict: Un diccionario que contiene las recomendaciones del juego. 
            En caso de éxito, se devuelve {"recomendaciones": [...]}.
            Si el ID no es un número o no se encuentran recomendaciones, se devuelve {"mensaje": "..."}. 
    
    Ejemplos de id_juego : 773570 , 57696 , 208796 , 348960     
    """
    try:
        # Lectura del DataFrame
        df_recomendaciones = pd.read_csv("Datsets/Modelo_ML/recomendacion_item_item.csv")

        # Convertir el ID de cadena a número
        id_num = int(id)
        
        # Filtrar el DataFrame para obtener las recomendaciones del juego con el ID dado
        recomendaciones = df_recomendaciones[df_recomendaciones['id'] == id_num]['recomendaciones'].values.tolist()

        if not recomendaciones:
            return JSONResponse(
                status_code=404,
                content={'error': f"No se encontró información del id_juego '{id}'"})

        return {"recomendaciones": recomendaciones}
    except ValueError:
        # Manejar el caso en el que el ID no sea un número
        raise HTTPException(status_code=400, detail=f"El id {id} no es un número válido")
    
#Recomendacioón usuarios
@app.get("/recomendacion_usuario/{user_id: str}")
async def user(user_id: str):
    """
    Obtiene recomendaciones de juegos basándose en usuarios similares.

    Parámetros:
    - user_id: El usuario para el cual se desea obtener las recomendaciones.

    Returns:
    - Lista de recomendaciones para el usuario especificado.

    Ejemplos de user_id : 16395 , 2greasy , 350176 , chun437
    """

    try:
        # Leer el DataFrame de recomendaciones desde el archivo CSV
        df_recomendaciones = pd.read_csv("Datsets/Modelo_ML/recomendacion_user_item.csv")
        
        # Filtrar el DataFrame para obtener solo las filas correspondientes al usuario dado
        usuario_filtro = df_recomendaciones[df_recomendaciones['user_id'] == user_id]

        # Verificar si el usuario existe en el DataFrame
        if usuario_filtro.empty:
            return JSONResponse(
                status_code=404,
                content={'error': f"No se encontró información del jugador  '{user_id}'"})

        # Concatenar las listas de recomendaciones correspondientes al usuario
        recomendaciones_usuario = usuario_filtro['recomendaciones'].sum()

        return recomendaciones_usuario
    
    except Exception as e:
        return f"Error: {e}"
