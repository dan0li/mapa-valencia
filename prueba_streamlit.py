import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv("DATASET_FINAL.csv")
    return df

data = load_data()

# Configuración de la página
st.set_page_config(page_title="Visualización de Propiedades", layout="wide")
st.title("Mapa de Propiedades")

# Filtros
barrios = data["Barrio"].unique().tolist()
selected_barrio = st.selectbox("Selecciona un barrio:", ["Todos"] + barrios)

# Filtrar datos
if selected_barrio != "Todos":
    data = data[data["Barrio"] == selected_barrio]

# Crear el mapa
m = folium.Map(location=[data["Latitud"].mean(), data["Longitud"].mean()], zoom_start=12)
marker_cluster = MarkerCluster().add_to(m)

# Agregar puntos
for _, row in data.iterrows():
    folium.Marker(
        location=[row["Latitud"], row["Longitud"]],
        popup=f"{row['Nombre']} - ${row['Precio']}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(marker_cluster)

# Mostrar el mapa en Streamlit
folium_static(m)
