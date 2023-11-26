from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
import pandas as pd


app = FastAPI(title='API Steam Games')

#Mensaje de bienvenida
@app.get("/")
async def root():
    return {"Mensaje": "Proyecto Individual"}

@app.get("/PlayTimeGenre/{genero}")
async def user(genero: str):
    """
    Endpoint para obtener el año de lanzamiento con más horas jugadas
    para un género de juegos específico.

    Parameters:
        genero (str): El género de juegos para el cual se quiere obtener la información.

    Returns:
        JSONResponse: Una respuesta JSON con el año de lanzamiento con más horas jugadas
        para el género especificado, o un mensaje de error si no se encuentra información.
    """
    try:
        # Cargar el DataFrame desde el archivo CSV
        df_genero = pd.read_csv("..\\Datsets\\Archivos_API\\PlayTimeGenre.csv")

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

@app.get("/sentiment_analysis/{developer:str}")
async def user(developer: str):
    """
    Obtiene la cantidad de comentarios positivos , negativos y neutrales de los desarrolladores.

    Parameters:
    - developer (str): Nombre del desarrollador para el que se desea obtener el análisis de sentimientos.

    Returns:
    - dict: Un diccionario que contiene el análisis de sentimientos para el desarrollador especificado.

    Raises:
    - HTTPException(404): Se produce cuando no se encuentra información para el desarrollador especificado.
    - HTTPException(500): Se produce en caso de un error interno durante el procesamiento.
    """

    try:
        # Cargar el DataFrame desde el archivo CSV
        analisis_sentimientos_df = pd.read_csv("..\\Datsets\\Archivos_API\\sentiment_analysis.csv")

        developer_column = analisis_sentimientos_df["developer"].tolist()

        if developer in developer_column:
            index = developer_column.index(developer)
            sentiment_counts = analisis_sentimientos_df.iloc[index, 1:].to_dict()
            return {developer: sentiment_counts}
        else:
            # Devolver una respuesta de error si no se encuentra información para el desarrollador
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró información del desarrollador '{developer}'"
            )

    except Exception as e:
        # Manejar cualquier excepción y devolver una respuesta de error
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}"
        )


@app.get("/recomendacion_juego/{id:str}")
async def user(id: str):
    """
    Obtiene las recomendaciones para un juego basándose en sus características.

    Parameters:
    - id (str): El ID del juego.

    Returns:
    - dict: Un diccionario que contiene las recomendaciones del juego. 
            En caso de éxito, se devuelve {"recomendaciones": [...]}.
            Si el ID no es un número o no se encuentran recomendaciones, se devuelve {"mensaje": "..."}. 
    """
    try:
        # Lectura del DataFrame
        df_recomendaciones = pd.read_csv("..\\Datsets\\Modelo_ML\\recomendacion_item_item.csv")

        # Convertir el ID de cadena a número
        id_num = int(id)
        
        # Filtrar el DataFrame para obtener las recomendaciones del juego con el ID dado
        recomendaciones = df_recomendaciones[df_recomendaciones['id'] == id_num]['recomendaciones'].values.tolist()

        if not recomendaciones:
            raise HTTPException(status_code=404, detail=f"No se encontraron recomendaciones para el ID {id}")

        return {"recomendaciones": recomendaciones}
    except ValueError:
        # Manejar el caso en el que el ID no sea un número
        raise HTTPException(status_code=400, detail=f"El id {id} no es un número válido")