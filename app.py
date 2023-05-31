import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from folium import FeatureGroup

# Load your data here
counties_gvd_prob = pd.read_csv('counties_gvd_prob.csv')


# Path to the GeoJSON file
geojson_path = 'georef-united-states-of-america-county.geojson'


# Create a Map instance
m = folium.Map(location=[37.8, -96], zoom_start=4)

# Add GeoJSON layer
folium.GeoJson(
    geojson_path,
    name='US Counties',
    style_function=lambda feature: {
        'fillColor': '#ffff00',
        'color': 'black',
        'weight': 0.4,
        'dashArray': '5, 5'
    }
).add_to(m)

# Define different dataframes
prob1_df = counties_gvd_prob[counties_gvd_prob['death_probability'] <= 0.5]
prob2_df = counties_gvd_prob[(counties_gvd_prob['death_probability'] > 0.5) & (counties_gvd_prob['death_probability'] <= 0.8)]
prob3_df = counties_gvd_prob[counties_gvd_prob['death_probability'] > 0.8]

# Create MarkerClusters
prob1 = MarkerCluster(name='Death Probability: 0.0-0.5')
prob2 = MarkerCluster(name='Death Probability: 0.5-0.8')
prob3 = MarkerCluster(name='Death Probability: 0.8-1.0')

# Add markers to the MarkerClusters
for idx, row in prob1_df.iterrows():
    folium.Marker(
        [row['lat'], row['lng']], 
        tooltip=f"{row['county']}, {row['state']}",
        popup=folium.Popup(f"The probability of a death occurring by gun in this county is {row['death_probability']:.3f}", max_width=300)
    ).add_to(prob1)


for idx, row in prob2_df.iterrows():
    folium.Marker(
        [row['lat'], row['lng']],
        tooltip=f"{row['county']}, {row['state']}",
        popup=folium.Popup(f"The probability of a death occurring by gun in this county is {row['death_probability']:.3f}", max_width=300)
    ).add_to(prob2)

for idx, row in prob3_df.iterrows():
    folium.Marker(
        [row['lat'], row['lng']],
        tooltip=f"{row['county']}, {row['state']}",
        popup=folium.Popup(f"The probability of a death occurring by gun in this county is {row['death_probability']:.3f}", max_width=300)
    ).add_to(prob3)

# Create three FeatureGroups for the different probabilities and add them to the map
group1 = folium.FeatureGroup(name="Probability: 0.0 - 0.5", show=False).add_child(prob1).add_to(m)
group2 = folium.FeatureGroup(name="Probability: 0.5 - 0.8", show=False).add_child(prob2).add_to(m)
group3 = folium.FeatureGroup(name="Probability: 0.8 - 1.0", show=False).add_child(prob3).add_to(m)

# Add layer control to the map
folium.LayerControl().add_to(m)

# to display the map in the app
folium_static(m)
