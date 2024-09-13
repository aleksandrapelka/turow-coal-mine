import ee
import pandas as pd
from meteostat import Stations, Daily, Monthly
from datetime import datetime

# STATISTICS DATA
daily = pd.read_csv('data/daily_statistics_clear.csv')
weekly = pd.read_csv('data/weekly_statistics_clear.csv')
monthly = pd.read_csv('data/monthly_statistics_clear.csv')

daily_multihist = pd.read_csv('data/daily_multihist_10m.csv')
weekly_multihist  = pd.read_csv('data/weekly_multihist_10m.csv')
monthly_multihist  = pd.read_csv('data/monthly_multihist_10m.csv')


def get_statistics_data(index_name):
    statistics = {
        'daily': daily[['Date', f'{index_name}_mean', f'{index_name}_median', f'{index_name}_mode', f'{index_name}_std', f'{index_name}_min', f'{index_name}_max']],
        'weekly': weekly[['Date', f'{index_name}_mean', f'{index_name}_median', f'{index_name}_mode', f'{index_name}_std', f'{index_name}_min', f'{index_name}_max']],
        'monthly': monthly[['Date', f'{index_name}_mean', f'{index_name}_median', f'{index_name}_mode', f'{index_name}_std', f'{index_name}_min', f'{index_name}_max']]
    }

    return statistics


# SPATIAL DATA
@st.cache_data
def ee_authenticate(token_name="EARTHENGINE_TOKEN"):
    geemap.ee_initialize(token_name=token_name)


ee_authenticate(token_name="EARTHENGINE_TOKEN")

selected_units = ee.FeatureCollection('users/aleksandra_pelka/selected_units')
zittau = ee.FeatureCollection('projects/drought-monitoring-417414/assets/Zittau')
turow_site_area = ee.FeatureCollection('projects/drought-monitoring-417414/assets/cbdg_midas_tereny_2024_07_09')


def create_clear_collection(collection):
  clear_collection = []
  projection = {'crs': 'EPSG:32633', 'transform': [10, 0, 399960, 0, -10, 5600040]}

  for i in range(collection.size().getInfo()):
    image = ee.Image(collection.toList(collection.size()).get(i))
    image = image.reproject(crs=projection['crs'], crsTransform=projection['transform'])

    msavi2 = image.select('MSAVI2').updateMask(image.select('MSAVI2').gte(-5).And(image.select('MSAVI2').lte(5)))
    nmdi = image.select('NMDI').updateMask(image.select('NMDI').gte(-5).And(image.select('NMDI').lte(5)))
    nmdi_temp = image.select('NMDI_temp').updateMask(image.select('NMDI_temp').gte(-5).And(image.select('NMDI_temp').lte(5)))
    msi = image.select('MSI').updateMask(image.select('MSI').gte(0).And(image.select('MSI').lte(6)))
    evi = image.select('EVI').updateMask(image.select('EVI').gte(-100).And(image.select('EVI').lte(100)))

    indexes = image.addBands(ee.Image([msavi2, evi, nmdi_temp, nmdi, msi]), overwrite=True)
    clear_collection.append(indexes)

  return ee.ImageCollection(clear_collection)


def get_imagery_collections(index_name):

    daily = ee.ImageCollection('users/aleksandra_pelka/daily_indexes')
    weekly = ee.ImageCollection('users/aleksandra_pelka/weekly_indexes')
    monthly =  ee.ImageCollection('projects/drought-monitoring-417414/assets/monthly_indexes')

    daily_clear = create_clear_collection(daily)
    weekly_clear = create_clear_collection(weekly)
    monthly_clear = create_clear_collection(monthly)

    collections = {
        'daily_collection': daily_clear.select(index_name),
        'weekly_collection': weekly_clear.select(index_name),
        'monthly_collection': monthly_clear.select(index_name)
    }

    return collections


# CONTROL POINTS DATA
def get_control_points_data(index_name, series):

    lat = [50.76124282784599, 50.85853035852719, 50.85104197635066, 50.85862866464956, 51.089383659893244, 51.08767616980139, 51.02970998359318, 
           51.02949395603037, 50.8912317897888, 50.923435760048484, 50.92904866784961, 50.92927778947726, 50.90184686716995, 50.87983392037308, 
           50.896541851330625, 50.86198682123828, 50.965134797981406, 50.94621196677289, 50.922623821772895, 50.91245989493935, 50.8622039460536, 50.862203787337]
    lon = [14.975401908159258, 15.282669067382814, 15.249195015057923, 15.143451858311893, 14.928499460220339, 14.952908065170053, 14.847121322527531, 
           14.850811706855895, 14.786353195086125, 14.822358917444944, 14.879779983311893, 14.892011191695929,  14.891971042379739, 14.889500057324769, 
           14.931967975571753, 14.928231071680784, 14.979519182816151, 14.970936030149462, 14.968357086181642, 14.975673900917174, 14.998913146555426, 14.998913062736392]
    collection = get_imagery_collections(index_name)
    collection = collection[series]
    
    points = []
    points_df = {}
    for i in range(len(lat)-1):
        point = ee.Geometry.Point([lon[i], lat[i]])
        point_data = collection.getRegion(point, scale=10).getInfo()

        headers = point_data[0]
        data = point_data[1:]
        df = pd.DataFrame(data, columns=headers)

        df['point_id'] = i
        points_df[i] = df

        point = ee.Feature(point, {'id': i})
        points.append(point)

        points_merged_df = pd.DataFrame()

        for point_id, df in points_df.items():
            points_merged_df = pd.concat([points_merged_df, df])

    points = ee.FeatureCollection(points)    
    return points_merged_df, points        



# METEO DATA
jelenia_gora_meteo = pd.read_csv('data/jelenia_gora_meteo.csv', encoding="latin1", header=None)
jelenia_gora_meteo_m = pd.read_csv('data/jelenia_gora_meteo_m.csv', encoding="latin1", header=None)
legnica_meteo = pd.read_csv('data/legnica_meteo.csv', encoding="latin1", header=None)
legnica_meteo_m = pd.read_csv('data/legnica_meteo_m.csv', encoding="latin1", header=None)

jelenia_gora_meteo.columns = ["Name", "Year", "Month", "Day", "Temp", "Precip", "Date"]
jelenia_gora_meteo_m.columns = ["Name", "Year", "Month", "Temp", "Precip", "Date"]
legnica_meteo.columns = ["Name", "Year", "Month", "Day", "Temp", "Precip", "Date"]
legnica_meteo_m.columns = ["Name", "Year", "Month", "Temp", "Precip", "Date"]

def get_stations_info():
    data = {
    'Name': ['Legnica', 'Jelenia Góra', 'Bertsdorf-Hörnitz', 'Liberec', 'Ostritz'],
    'Country': ['PL', 'PL', 'DE', 'CZ', 'DE'],
    'Latitude': [51.1930, 50.9039, 50.8990, 50.7667, 51.0266],
    'Longitude': [16.2078, 15.7401, 14.7457, 15.0167, 14.9356],
    'Elevation': [122.0, 342.0, 270.0, 398.0, 213.0]
    }

    return pd.DataFrame(data)
     

def get_meteostat_data(series):
    stations = Stations()
    stations = stations.nearby(50.90628, 14.897437, 20000) # radius 20 km
    station = stations.fetch(3)
    #D2252  Bertsdorf-Hörnitz      DE    
    #D2958            Ostritz      DE    
    #11603            Liberec      CZ

    start = datetime(2017, 1, 1)
    end = datetime(2023, 12, 31)
    data_df = []

    for i in range(len(station)):
        station_id = station.index[i]

        if series == 'Monthly':       
            data = Monthly(station_id, start, end)
        else:
            data = Daily(station_id, start, end)
        data = data.fetch()

        df = data[['tavg', 'prcp']]
        df.columns = ['Temp', 'Precip']
        df['Name'] = str(station['name'][i])
        df['Date'] = data.index
        data_df.append(df)

    return data_df
