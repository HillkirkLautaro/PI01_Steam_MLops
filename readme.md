# Proyecto SteamSuggest: Plataforma de Recomendación de Videojuegos para Usuarios de Steam

![Banner de Presentación](https://github.com/HillkirkLautaro/PI01_Steam_MLops/blob/main/assets/mlops.png)

## Descripción del Proyecto
Este proyecto se centra en la aplicación práctica de habilidades técnicas y blandas esenciales en el entorno laboral. Se ha desarrollado un caso de negocio auténtico utilizando conjuntos de datos públicos provenientes de la industria de videojuegos, específicamente de la plataforma en línea reconocida como STEAM.

## Propósito
El objetivo principal es construir el primer modelo de Machine Learning (end to end) que aborde un problema de negocio en Steam, a través de un enfoque integral que abarca desde la Ingeniería de Datos (ETL, EDA, API) hasta la implementación del ML. Se persigue lograr un desarrollo rápido y obtener un Producto Mínimo Viable (MVP).

## Etapas del Proyecto



### 1. Ingeniería de Datos (ETL y API)

![Pasos del Proyecto](https://github.com/HillkirkLautaro/PI01_Steam_MLops/blob/main/assets/Etapas.png)

#### 1.1 Transformaciones de Datos
Inicialmente, se recibieron tres (3) archivos en formato JSON, alojados en la carpeta de Entrada de un repositorio público en Google Drive. Se llevaron a cabo transformaciones esenciales para cargar los conjuntos de datos en el formato adecuado, con el propósito de optimizar tanto el rendimiento de la API como el entrenamiento del modelo.

- australian_user_reviews.json: Contiene reseñas de juegos realizadas por usuarios australianos. Puedes consultar el cuaderno ETL_user_reviews para más detalles sobre el procesamiento de las reseñas, resultando en un nuevo archivo con datos limpios, user_reviews_cleaned.csv.
- output_steam_games.json: Proporciona información detallada sobre los juegos disponibles en la plataforma Steam. Incluye datos como géneros, etiquetas, especificaciones, desarrolladores, año de lanzamiento, precio y otros atributos relevantes de cada juego. En el cuaderno ETL_steam_game, puedes revisar el proceso de limpieza y transformación de datos, culminando en la creación de un nuevo archivo llamado steam_games_cleaned.csv.
- australian_users_items.json: Contiene información sobre los ítems relacionados con usuarios australianos. Este conjunto de datos ha pasado por un proceso de Extracción, Transformación y Carga (ETL), detallado en el cuaderno ETL_user_items. Como resultado, se generó un nuevo archivo user_items_cleaned.csv para facilitar su manipulación y análisis, brindando una estructura lista para su integración en el modelo.

#### 1.2 Ingeniería de Características
Se introdujo la columna de análisis de sentimientos aplicando análisis de sentimiento a las reseñas de los usuarios. Se optó por utilizar la biblioteca NLTK (Natural Language Toolkit) con el analizador de sentimientos de Vader, que proporciona una puntuación compuesta para clasificar la polaridad de las reseñas en negativas (valor '0'), neutrales (valor '1') o positivas (valor '2'). A las reseñas no disponibles, se les asignó el valor '1'. Puedes ver los detalles del desarrollo en el cuaderno ETL_user_reviews y profundizar en el análisis en el EDA_Análisis Exploratorio de Datos.

#### 1.3 Desarrollo de la API
Se implementó una API con FastAPI y se desplegó en Render, proporcionando cinco (5) consultas sobre información de videojuegos. Los detalles del código están disponibles en los cuadernos Funciones y Consultas.

- Endpoint 1 (Developer): Devuelve el año con más horas jugadas para un género dado.
- Endpoint 2 (Userdata): Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
- Endpoint 3 (UserForGenre): Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.
- Endpoint 4 (BestDeveloper): Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado.
- Endpoint 5 (developer_review_analysis): Según la empresa desarrolladora, devuelve un diccionario con el nombre de la desarrolladora como clave y una lista con la cantidad total de registros de reseñas de usuarios categorizados con un análisis de sentimiento como valor.

Para acceder a la funcionalidad completa de la API y explorar las recomendaciones de juegos, visita este [enlace URL de la API](#).

### 2. Análisis Exploratorio de Datos (EDA)
Se investigaron las relaciones entre variables, se identificaron valores atípicos y se buscaron patrones interesantes en los datos. El cuaderno EDA_Análisis Exploratorio de Datos contiene más detalles al respecto.

### 3. Modelo de Aprendizaje Automático
Se desarrolló un sistema de recomendación con uno de los enfoques propuestos:

#### 3.1 Sistema de Recomendación Ítem-Ítem
Se creó un modelo que recomienda juegos similares basados en un juego dado, utilizando similitud del coseno. Con CountVectorizer, se convirtieron los textos de la columna 'specs' en vectores numéricos para calcular posteriormente la similitud del coseno.

Se empleó la métrica de similitud del coseno, ya que mide el coseno del ángulo entre dos vectores. Cuanto más cercano a 1, más similares son los vectores. Este método fue crucial para determinar qué tan parecidos son los juegos entre sí, y se utiliza para generar recomendaciones, considerando que los juegos con vectores similares son considerados como recomendaciones potenciales.

### 4. Implementación de MLOps
Despliegue del Modelo: El modelo de recomendación se desplegó como parte de la API, la cual puedes consultar en la URL de la API.

### 5. Video Explicativo
Se realizó un video explicativo que muestra el funcionamiento de la API, las consultas realizadas y una breve explicación de los modelos de ML utilizados en YouTube.

## Estructura del Repositorio
1. **/Notebooks:** Contiene los Jupyter Notebooks con el código completo y bien comentado donde se llevaron a cabo las extracciones, transformaciones y carga de datos (ETL), análisis exploratorio de los datos (EDA), el archivo con Diccionario de datos, donde se trabajó el modelo y las funciones.
2. **/Data:** Almacena los conjuntos de datos utilizados en una versión limpia y procesada. Las fuentes de datos iniciales se encuentran almacenadas en la carpeta de entrada en el repositorio de Google Drive.
3. **/assets:** Carpeta con imágenes y recursos utilizados en el desarrollo del proyecto.
## Posibles Mejoras

1. **Crear otro modelo basado en recomendación usando el filtro user-item:**
   - Esta mejora implica desarrollar un modelo adicional que se base en la recomendación de ítems utilizando la relación entre usuarios y ítems. El enfoque sería identificar usuarios similares y recomendar ítems que hayan gustado a esos usuarios similares.

2. **Mejora del código para hacerlo más legible:**
   - Esta mejora implica revisar y refacturar el código existente para hacerlo más legible y comprensible. Un código limpio y bien estructurado facilita el mantenimiento y la colaboración en el proyecto.

3. **Mejorar la carga de archivos a Render para asegurar una mayor retención de los datos:**
   - Trabajar con Render implica enfrentarse a limitaciones de espacio, donde el límite puede ser de alrededor de 500 MB. Para mejorar la carga de archivos, se puede implementar un enfoque que asegure una mayor retención de los datos, como limitar los dataframes a un número específico de registros (por ejemplo, dataframe.head(1000)). Esto puede generar errores al realizar las consultas si los datos que se buscan obtener de la consulta fueron recortados.
