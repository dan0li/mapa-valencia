import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import folium_static
import openrouteservice

# Cargar los datos
barrios_geojson = "Barrios_valencia.geojson"
barrios_gdf = gpd.read_file(barrios_geojson)
pisos = pd.read_json("DATASET_FINAL.json")
colegios_con_barrio = pd.read_csv("colegios_por_barrio.csv")
hospitales_con_barrio = pd.read_csv("hospitales_por_barrio.csv")
parques_con_barrio = pd.read_csv("parques_por_barrio.csv")
buses_con_barrio = pd.read_csv("bus_por_barrio.csv")
tram_con_barrio = pd.read_csv("tram_por_barrio.csv")

# Configurar Streamlit
st.set_page_config(page_title="Mapa Interactivo Valencia", layout="wide")
st.title("Mapa Interactivo de Valencia")

# Crear el mapa centrado en Valencia
m = folium.Map(location=[39.4699, -0.3763], zoom_start=12)

# Añadir polígonos de barrios
for _, row in barrios_gdf.iterrows():
    folium.GeoJson(row["geometry"], name=row["name"], tooltip=row["name"]).add_to(m)

# Función para agregar marcadores
def agregar_puntos(df, color, nombre, icono):
    for _, row in df.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=row["nombre"],
            icon=folium.Icon(color=color, icon=icono, prefix='fa')
        ).add_to(m)

# Agregar marcadores para diferentes categorías
agregar_puntos(colegios_con_barrio, "blue", "Colegios", "graduation-cap")
agregar_puntos(hospitales_con_barrio, "red", "Hospitales", "plus")
agregar_puntos(parques_con_barrio, "green", "Parques", "tree")
agregar_puntos(buses_con_barrio, "orange", "Paradas de Bus", "bus")
agregar_puntos(tram_con_barrio, "purple", "Paradas de Tram", "train")

# Cliente de OpenRouteService
ORS_API_KEY = "5b3ce3597851110001cf624859af420fdd51467a9d1b5f39737c6113"
client = openrouteservice.Client(key=ORS_API_KEY)

# Sidebar para entrada de datos
st.sidebar.header("Calcula una ruta")
origen = st.sidebar.text_input("Origen (lat, lon)", "39.4699, -0.3763")
destino = st.sidebar.text_input("Destino (lat, lon)", "39.4702, -0.3761")

# Selección del tipo de transporte
transporte = st.sidebar.selectbox("Modo de transporte", [
    "foot-walking", "cycling-regular", "driving-car", "driving-hgv", "wheelchair"
])

# Cálculo de la ruta
def calcular_ruta():
    try:
        coords = [(float(origen.split(",")[1]), float(origen.split(",")[0])),
                  (float(destino.split(",")[1]), float(destino.split(",")[0]))]
        route = client.directions(coords, profile=transporte, format='geojson')
        folium.GeoJson(route, name='Ruta', style_function=lambda x: {
            'color': 'blue', 'weight': 5, 'opacity': 0.7
        }).add_to(m)
    except Exception as e:
        st.sidebar.error(f"Error al calcular la ruta: {e}")

if st.sidebar.button("Calcular ruta"):
    calcular_ruta()

# Mostrar el mapa
folium_static(m)
