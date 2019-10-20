import pandas as pd
import folium
import base64
from folium import IFrame

air_data = pd.read_json('./files/cities.json', orient='columns')

# generate a new map
folium_map = folium.Map(location=[40.738, -73.98],
                        zoom_start=5,
                        tiles="CartoDB dark_matter")
# json parse
def aqd_count(aqd):

    for i in range(len(aqd)):

        radius = 21000
        popup_text = '{}<br>Air Quality: {}'

        if aqd.AQI[i] <= 50:
            color = '#34eb5e'
            condition = 'Good'

        elif aqd.AQI[i] > 50 and aqd.AQI[i] <= 100:
            color = '#e8eb34'
            condition = 'Moderate'

        elif aqd.AQI[i] > 100 and aqd.AQI[i] <= 150:
            color = '#eb7d34'
            condition = 'Unhealthy for Sensitive Groups'

        elif aqd.AQI[i] > 150 and aqd.AQI[i] <= 200:
            color = '#eb3434'
            condition = 'Unhealthy'

        elif aqd.AQI[i] > 200 and aqd.AQI[i] <= 300:
            color = '#6e34eb'  
            condition = 'Very Unhealthy'

        elif aqd.AQI[i] > 300:
            color = '#6b0d0d'
            condition = 'Hazardous'
        
        popup_text = popup_text.format(aqd.ReportingArea[i], condition)

        folium.Circle(location=(aqd.Latitude[i], aqd.Longitude[i]),
                            radius=radius,
                            color=color,
                            popup=popup_text,
                            fill=True).add_to(folium_map)
    folium_map.save('./templates/map.html')
    return folium_map

def display_selected_data(aqd, date):
    for i in range(len(aqd)):
        if str(date) == aqd.DateForecast[i]:

            radius = aqd.AQI[i] / 0.0005
            popup_text = '{}<br> Air Quality: {}'

            if aqd.AQI[i] <= 50:
                color = '#34eb5e'
                condition = 'Good'

            elif aqd.AQI[i] > 50 and aqd.AQI[i] <= 100:
                color = '#e8eb34'
                condition = 'Moderate'

            elif aqd.AQI[i] > 100 and aqd.AQI[i] <= 150:
                color = '#eb7d34'
                condition = 'Unhealthy for Sensitive Groups'

            elif aqd.AQI[i] > 150 and aqd.AQI[i] <= 200:
                color = '#eb3434'
                condition = 'Unhealthy'

            elif aqd.AQI[i] > 200 and aqd.AQI[i] <= 300:
                color = '#6e34eb'  
                condition = 'Very Unhealthy'

            elif aqd.AQI[i] > 300:
                color = '#6b0d0d'
                condition = 'Hazardous'
            
            popup_text = popup_text.format(aqd.ReportingArea[i], condition)
            folium.Circle(location=(aqd.Latitude[i], aqd.Longitude[i]),
                            radius=radius,
                            color=color,
                            popup=popup_text,
                            fill=True).add_to(folium_map)
    folium_map.save('./templates/map.html')
    return folium_map

# csv parse

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


def plot_quality(aod_Data, selected_region1):
    # generate a new map
    if selected_region1 == "Los Angeles, USA":
        folium_map = folium.Map(location=[34.0522, -118.2437], zoom_start=11, tiles="CartoDB dark_matter")
        
        encoded = base64.b64encode(open('los angeles graph.png', 'rb').read())
        
        html = '<img src="data:image/png;base64,{}">'.format
        iframe = IFrame(html(encoded.decode('UTF-8')), width=370, height=270)
        
    elif selected_region1 == "AddisAbaba, Ethopia":
        folium_map = folium.Map(location=[9.02497, 38.74689], zoom_start=11, tiles="CartoDB dark_matter")
        
        encoded = base64.b64encode(open('addisababa graph.png', 'rb').read())
        
        html = '<img src="data:image/png;base64,{}">'.format
        iframe = IFrame(html(encoded.decode('UTF-8')), width=370, height=270)
        
    elif selected_region1 == "Dehli, India":
        folium_map = folium.Map(location=[28.6448, 77.2167], zoom_start=11, tiles="CartoDB dark_matter")

        encoded = base64.b64encode(open('dehli graph.png', 'rb').read())
        
        html = '<img src="data:image/png;base64,{}">'.format
        iframe = IFrame(html(encoded.decode('UTF-8')), width=370, height=270)
        
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
                            popup=folium.Popup(iframe, max_width=450),
                            fill=True).add_to(folium_map)
    folium_map.save('./templates/map1.html')
    return folium_map

region = "Dehli, India"

aod_Data = get_aod_data_by_time_and_region(2005, 1, 2, region)

plot_quality(aod_Data, region)

display_selected_data(air_data, '2019-10-20 ')