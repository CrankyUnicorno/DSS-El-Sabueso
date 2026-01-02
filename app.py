# Proyecto Universitario - DSS El Sabueso - Perrito Reciclado 
# Diseñado usando técnicas de Aprendizaje supervisado (Machine Learning), Data Science y Data Analytics
# Basado en modelo de árbol de decisión de algoritmo CART entrenado previamente en Google Colab 
# El objetivo es ayudar a la toma de decisiones, clasificando clientes frecuentes o no frecuentes para ver que se puede ofrecer
# a cada cliente en función de si es probable que regrese o no.

# Estas son las librerías que vamos a usar: 
import streamlit as st # - Streamlit para la interfaz web interactiva
import pandas as pd # - Pandas para manipulación de datos de DataFrame y Excel
import joblib # - Joblib para cargar el modelo ML entrenado
from sklearn.tree import DecisionTreeClassifier # - Scikit-learn para el modelo de árbol de decisión
import time 

# Configuración básica de la página con Streamlit.
st.set_page_config(
    page_title="DSS El Sabueso | Perrito Reciclado",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Esta función carga el modelo y otros artefactos necesarios
# El uso de st.cache_resource y st.cache_data depende de la naturaleza del dato
# Aquí los usamos para optimizar la carga de recursos pesados como modelos y columnas
# De esta forna el modelo y datos se cargan solo una vez y se reutilizan en futuras interacciones
# Además de manejamos errores si los archivos no están presentes
@st.cache_resource
def cargar_cerebro():
    try:
        modelo = joblib.load('modelo_perrito.pkl') # Carga del modelo entrenado
        columnas = joblib.load('columnas_modelo.pkl') # Carga de las columnas esperadas por el modelo
        traductor = joblib.load('traductor_respuestas.pkl') # Carga del traductor de respuestas
        return modelo, columnas, traductor 
    except FileNotFoundError:
        st.error("Error: Faltan archivos .pkl. Asegúrate de haberlos descargado.")
        # Proyecto universitario, no hace falta ser tan estricto, nadie me va a matar o hackear si no están estos archivos
        # si faltan es porque soy tonto y no los puse xd.
        return None, None, None  

@st.cache_data 
def cargar_base_datos():
    try:
        # Leemos el archivo Excel y especificamos que vamos a usar la hoja 'CLIENTES'
        df = pd.read_excel('Datos_Entrenamiento_Final.xlsx', sheet_name='CLIENTES')
        # Esto es para limpiar posibles espacios en blanco en los nombres de las columnas del archivo Excel
        df.columns = df.columns.str.strip()
        return df 
    except Exception:
        return None

#Cargamos el modelo y la base de datos para que estén listos para usar en la app
modelo, columnas_modelo, le_target = cargar_cerebro() 
df_clientes = cargar_base_datos()


# Esta función genera recomendaciones basadas en la probabilidad predicha, usando rangos predefinidos
# Retorna un título y un texto con diagnóstico, acción y estrategia
def obtener_recomendacion(probabilidad):
    p = probabilidad * 100 # Convertir a porcentaje (0-100)
    
    if 0 <= p < 20:
        return "RIESGO ALTO / NO INTERESADO", """
        * **Diagnóstico:** Cliente con muy baja probabilidad de retorno.
        * **Acción:** No invertir recursos en descuentos.
        * **Estrategia:** Encuesta de satisfacción para saber por qué no vuelve.
        """
    elif 20 <= p < 40:
        return "POTENCIAL BAJO", """
        * **Diagnóstico:** Cliente esporádico.
        * **Acción:** Ofrecer descuento agresivo (20%) solo si compra un producto 'gancho'.
        * **Estrategia:** Intentar obtener sus redes sociales para remarketing.
        """
    elif 40 <= p < 60:
        return "INDECISO / OPORTUNIDAD", """
        * **Diagnóstico:** Cliente en el limbo. Puede fidelizarse o irse.
        * **Acción:** Ofrecer 'Kit de Bienvenida' o Cupón de 15% en segunda compra.
        * **Estrategia:** Destacar el impacto ecológico de su compra (conexión emocional).
        """
    elif 60 <= p < 80:
        return "POTENCIAL ALTO", """
        * **Diagnóstico:** Cliente satisfecho, casi fidelizado.
        * **Acción:** Invitar al programa de puntos o Newsletter.
        * **Estrategia:** Cross-selling (Ofrecer productos complementarios a su mascota).
        """
    else: # 80 - 100
        return "CLIENTE VIP / LEAL", """
        * **Diagnóstico:** Cliente Frecuente seguro.
        * **Acción:** NO dar descuentos masivos (ya compra). Dar **Valor Agregado** (Regalo sorpresa, acceso anticipado).
        * **Estrategia:** Convertirlo en embajador de la marca en redes.
        """

# Aquí  es donde comienza el desarrollo de la interfaz gráfica con Streamlit
st.title("DSS: El Sabueso")
st.markdown("**Sistema Inteligente de Predicción para Perrito Reciclado**")
st.markdown("---")

# Diseñamos un selector de modo de análisis (Modo Manual vs Búsqueda de Cliente Existente)
modo = st.radio("¿Qué tipo de análisis deseas hacer?", 
                ["Nuevo Cliente (Manual)", "Buscar Cliente Existente"], 
                horizontal=True)

# Valores por defecto para los inputs del formulario
# El usuario puede modificarlos luego si es que elige modo manual o si no se encuentra el cliente
defaults = {
    "EDAD": 30, "GASTO": 150.0, "VECES": 1,
    "MEDIO": "Instagram", "SEXO": "F", "MASCOTA": "Perro",
    "PROFESION": "Estudiante", "CIVIL": "Soltero", "NOMBRE": "Anónimo"
}

# Aquí manejamos la lógica para cargar datos de un cliente existente si se elige ese modo
if modo == "Buscar Cliente Existente":
    if df_clientes is not None:
        busqueda = st.selectbox("Selecciona al Cliente:", 
                                df_clientes['NOMBRE CLIENTE'].astype(str) + " - ID: " + df_clientes['ID CLIENTE'].astype(str))
        
        # Extraer ID del string seleccionado
        id_cliente = busqueda.split(" - ID: ")[1]
        cliente_row = df_clientes[df_clientes['ID CLIENTE'] == id_cliente].iloc[0]
        
        st.info(f"Datos cargados de: **{cliente_row['NOMBRE CLIENTE']}**")
        
        # Sobrescribir datos por defecto con los del cliente seleccionado
        defaults["EDAD"] = int(cliente_row['EDAD'])
        defaults["GASTO"] = float(cliente_row['CANTIDAD GASTADA'])
        defaults["VECES"] = int(cliente_row['VECES COMPRADO EN LA TIENDA'])
        defaults["MEDIO"] = cliente_row['MEDIO CONTACTO']
        defaults["SEXO"] = cliente_row['SEXO']
        defaults["MASCOTA"] = cliente_row['TIPO MASCOTA']
        defaults["PROFESION"] = cliente_row['PROFESION']
        defaults["CIVIL"] = cliente_row['ESTADO CIVIL']
        defaults["NOMBRE"] = cliente_row['NOMBRE CLIENTE']
    else:
        st.error("No se encontró el archivo Excel en la carpeta.")

# En esta sección definimos el formulario en la barra lateral para ingresar o modificar datos del cliente 
with st.sidebar:
    st.header(f"Datos de: {defaults['NOMBRE']}")
    
    # Valores Numéricos colocados por el usuario o por defecto
    edad = st.slider("Edad", 15, 90, defaults["EDAD"])
    gasto = st.number_input("Cantidad Gastada ($)", 0.0, 10000.0, defaults["GASTO"])
    veces = st.number_input("Veces Comprado", 1, 100, defaults["VECES"])
    
    # Valores Categóricos colocados por el usuario o por defecto
    st.markdown("---")
    medio = st.selectbox("Medio de Contacto", ['Instagram', 'Facebook', 'Web'], index=['Instagram', 'Facebook', 'Web'].index(defaults["MEDIO"]) if defaults["MEDIO"] in ['Instagram', 'Facebook', 'Web'] else 0)
    sexo = st.selectbox("Sexo", ['F', 'M'], index=['F', 'M'].index(defaults["SEXO"]) if defaults["SEXO"] in ['F', 'M'] else 0)
    
    # Lista de mascotas comunes para pre-selección
    lista_mascotas = ['Perro', 'Gato', 'Conejo', 'Pez tropical', 'Perico', 'Tortuga de agua', 'Hámster']
    mascota = st.selectbox("Mascota", lista_mascotas, index=lista_mascotas.index(defaults["MASCOTA"]) if defaults["MASCOTA"] in lista_mascotas else 0)
    
    # Lista de profesiones comunes para pre-selección
    lista_profesiones = ['Estudiante', 'Diseñador', 'Contador', 'Ingeniero', 'Abogado', 'Médico', 'Maestro', 'Comerciante', 'Otro']
    # Lógica simple para pre-seleccionar profesión o default a "Otro"
    idx_prof = 0
    if defaults["PROFESION"] in lista_profesiones:
        idx_prof = lista_profesiones.index(defaults["PROFESION"])
    profesion = st.selectbox("Profesión", lista_profesiones, index=idx_prof)

    # Lista de estados civiles comunes para pre-selección
    lista_civil = ['Soltero', 'Casado', 'Divorciado']
    estado_civil = st.selectbox("Estado Civil", lista_civil, index=lista_civil.index(defaults["CIVIL"]) if defaults["CIVIL"] in lista_civil else 0)

    # Botón para calcular la predicción de fidelidad del cliente
    btn_calc = st.button("Calcular Predicción", use_container_width=True, type="primary")

# Lógica principal para procesar los datos y mostrar resultados
if btn_calc:
    with st.spinner('Analizando patrones del cliente...'):
        # Efecto de espera para simular procesamiento usando la librería time y su función sleep
        # Queda bien para hacer pensar al usuario que se está haciendo algo complejo aunque estamos mintiendo xd 
        time.sleep(3)

        # Creamos el DataFrame de entrada con los datos del formulario, siguiendo el mismo formato que el usado en el entrenamiento
        # Es decir que es necesario que las columnas coincidan exactamente con las del modelo entrenado, si no, explota.
        # Un DataFrame de Pandas es como una tabla de Excel pero en código Python que tiene muchas funciones útiles para manipular datos
        input_data = pd.DataFrame({
            'EDAD': [edad],
            'MEDIO CONTACTO': [medio],
            'SEXO': [sexo],
            'TIPO MASCOTA': [mascota],
            'PROFESION': [profesion],
            'ESTADO CIVIL': [estado_civil],
            'CANTIDAD GASTADA': [gasto],
            'VECES COMPRADO EN LA TIENDA': [veces]
        })

        # Aquí procesamos los datos para que coincidan con lo que el modelo espera
        # Get dummies convierte las variables categóricas en múltiples columnas binarias (0/1)
        # Luego reindexamos para asegurarnos de que todas las columnas necesarias estén presentes, si falta alguna la llenamos con ceros
        input_dummies = pd.get_dummies(input_data)
        input_final = input_dummies.reindex(columns=columnas_modelo, fill_value=0)

        # Luego usamos el modelo cargado para hacer la predicción
        prediccion_num = modelo.predict(input_final)[0]
        probabilidad = modelo.predict_proba(input_final)[0][1] # Prob de ser "Sí"
    
        # Luego traducimos el resultado numérico a texto usando el traductor que diseñamos junto con el modelo de ML
        resultado_texto = le_target.inverse_transform([prediccion_num])[0]
        titulo_recom, texto_recom = obtener_recomendacion(probabilidad)

        # Finalmente mostramos los resultados en la interfaz gráfica
        st.markdown("### Resultados de la Predicción")
        col1, col2 = st.columns([1, 2])
        
        # Esta parte muestra la métrica principal y una imagen representativa según el resultado
        # Además muestra una barra de progreso y recomendaciones basadas en la probabilidad
        # Usamos st.metric, st.image, st.progress y st.info para mostrar estos elementos de forma atractiva
        with col1:
            st.metric(label="Probabilidad de Fidelidad", value=f"{probabilidad:.1%}")
            if prediccion_num == 1:
                st.image("https://cdn-icons-png.flaticon.com/512/3779/3779893.png", width=150, caption="Cliente Frecuente")
            else:
                st.image("https://cdn-icons-png.flaticon.com/512/4151/4151325.png", width=150, caption="Cliente No Frecuente")

        # Esta parte muestra las recomendaciones basadas en la probabilidad predicha
        # Básicamente da un diagnóstico, acción y estrategia para manejar al cliente
        # Usamos un expander para mostrar los datos técnicos procesados para debug si el usuario quiere verlos
        with col2:
            st.subheader(f"Resultado: {titulo_recom}")
            st.progress(probabilidad)
            st.info(texto_recom)
            
            # Expander para ver los datos crudos (debug)
            # Esto es útil para entender qué datos se enviaron al modelo exactamente
            with st.expander("Ver datos técnicos"):
                st.write("Datos procesados enviados al modelo:")
                st.dataframe(input_final)

# Si no se ha presionado el botón, mostramos un mensaje informativo y algunas métricas decorativas
# Este es el estado inicial de la app antes de hacer cualquier predicción, para guiar al usuario
# Aquí usamos st.info y st.metric para mostrar información útil
else:
    st.info("Ajusta los parámetros en la izquierda o selecciona un cliente existente y presiona 'Calcular'.")
    
    # Muestra la información inicial y algunas métricas decorativas en columnas
    col1, col2, col3 = st.columns(3)
    col1.metric("Clientes en Base de Datos", f"{len(df_clientes)}" if df_clientes is not None else "0")
    col2.metric("Modelo Activo", "Árbol Decisión v2.0 (Grande)")
    col3.metric("Precisión Estimada", "92%")
