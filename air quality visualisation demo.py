#!/usr/bin/env python
# coding: utf-8

# In[225]:


import pandas as pd
import folium


# In[226]:


def get_aod_data_by_time_and_region(selected_year, selected_month, selected_day, selected_region):
    
    if selected_region == "Los Angeles, USA":
        aodData = pd.read_csv("air quality losAngeles.csv", sep=";")
        aodData = aodData[aodData.AOD1 != -1.00]
        aodData = aodData[aodData.AOD1 > 0]
    elif selected_region == "AddisAbaba, Ethopia":
        aodData = pd.read_csv("air quality ethopia.csv", sep=";")
        aodData = aodData[aodData.AOD1 != -1.00]
        aodData = aodData[aodData.AOD1 > 0]
    elif selected_region == "Dehli, India":
        aodData = pd.read_csv("air quality dehli.csv", sep=";")
        aodData = aodData[aodData.AOD1 != -1.00]
        aodData = aodData[aodData.AOD1 > 0]
    
    aod_Data = aodData.loc[(aodData['Year'] == selected_year) & (aodData['Month'] == selected_month) & (aodData['Day'] == selected_day)]

    return aod_Data


# In[276]:


def plot_quality(aod_Data, selected_region1):
    # generate a new map
    if selected_region1 == "Los Angeles, USA":
        folium_map = folium.Map(location=[34.0522, -118.2437], zoom_start=11, tiles="CartoDB dark_matter", width='50%')
    elif selected_region1 == "AddisAbaba, Ethopia":
        folium_map = folium.Map(location=[9.02497, 38.74689], zoom_start=11, tiles="CartoDB dark_matter", width='50%')
    elif selected_region1 == "Dehli, India":
        folium_map = folium.Map(location=[28.6448, 77.2167], zoom_start=11, tiles="CartoDB positron", width='50%')
        
    # for each row in the data, add a cicle marker
    for index, row in aod_Data.iterrows():
        # calculate net departures
        aod_index = row["AOD1"]
        
        # radius of circles
        radius = 21000
        
        # choose the color of the marker
        if aod_index>0 and aod_index<=0.5:
            popup_text = "Air Quality: <br><b>Good"
            color="#007849" # green
        elif aod_index>0.5 and aod_index<=1: 
            popup_text = "Air Quality: <br><b>Moderate"
            color="#ffff00" # yellow
        elif aod_index>1 and aod_index<=1.5:
            popup_text = "Air Quality: <br><b>Unhealthy for Sensitive Groups"
            color="#ff8000" # orange
        elif aod_index>1.5 and aod_index<=2:
            popup_text = "Air Quality: <br><b>Unhealthy"
            color="#ff0000" # red
        elif aod_index>2 and aod_index<=3:
            popup_text = "Air Quality: <br><b>Very Unhealthy"
            color="#8000ff" # purple
        elif aod_index>3 and aod_index<=5:
            popup_text = "Air Quality: <br><b>Hazardous"
            color="#800000" # maroon
        
        # add marker to the map
        folium.Circle(location=(row["Longitude"],
                            row["Latitude"]),
                            radius=radius,
                            color=color,
                            popup=popup_text,
                            fill=True).add_to(folium_map)
    return folium_map


# In[277]:


region = "Dehli, India"

aod_Data = get_aod_data_by_time_and_region(2019, 1, 2, region)
plot_quality(aod_Data, region)

