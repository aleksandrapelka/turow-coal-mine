import ee
import geemap.foliumap as geemap
from maps.visualization import get_vis_params, get_breaks, get_labels, get_palette
import data.data as data
import folium


projection = {'crs': 'EPSG:32633', 'transform': [10, 0, 399960, 0, -10, 5600040]}

def get_image(index_name, date, collection):
   collection = collection.select(index_name)
   image = ee.Image(collection.filterMetadata('date', 'equals', date).first())
   image = image.reproject(crs=projection['crs'], crsTransform=projection['transform'])

   return image


def classify_image(index_name, image):
   breaks = get_breaks()[index_name]
   image = image.updateMask(image.gte(breaks[0]).And(image.lte(breaks[10])))
   image = image.gte(breaks[0]).add(image.gte(breaks[1])).add(image.gte(breaks[2])).add(image.gte(breaks[3])).add(image.gte(breaks[4])).add(image.gte(breaks[5])).add(image.gte(breaks[6])).add(image.gte(breaks[7])).add(image.gte(breaks[8])).add(image.gte(breaks[9]).And(image.lte(breaks[10])))

   return image


def get_classified_image(index_name, date, collection):
   image = get_image(index_name, date, collection)
   classified_image = classify_image(index_name, image)

   return classified_image


def create_trends_map(collection, index_name):
   new_image_list = []
   collection_size = collection.size().getInfo()

   for i in range(collection_size):
      img = ee.Image(collection.toList(collection_size).get(i))

      date = (ee.Date(img.get('date'))).millis().getInfo()
      image = img.set('system:time_start', date)
      new_image_list.append(image)

   new_collection = ee.ImageCollection(new_image_list)


   def createTimeBand(image):
      return image.addBands(image.metadata('system:time_start').divide(1e12))

   collection = new_collection.map(createTimeBand)
   linearFit = collection.select(['system:time_start', index_name]).reduce(ee.Reducer.linearFit())

   return linearFit


def detect_chages(image1, image2):
   threshold = 0.3
   change = image2.subtract(image1)
   change = change.updateMask(change.abs().gt(threshold))
   classified_changes = change.gt(-100).add(change.gt(-0.6)).add(change.gt(0)).add(change.gt(0.6))

   return classified_changes


def create_control_points_map(features, collection, index_name):
   Map = geemap.Map(basemap="Esri.WorldGrayCanvas", center=(50.95, 14.95), zoom=10)
   collection_size = features.size().getInfo()

   for i in range(collection_size):
      poi = ee.Feature(features.toList(collection_size).get(i))

      icon = folium.Icon(color='red', icon='chart-line', icon_color="white", prefix='fa')
      poi_coordinates = poi.geometry().coordinates().getInfo()
      marker = folium.Marker(location=[poi_coordinates[1], poi_coordinates[0]], popup=f"Point id: {poi.get('id').getInfo()}", icon=icon)
      Map.add_child(marker)
   linearFit = create_trends_map(collection, index_name)   

   Map.addLayer(linearFit.select('scale'), {'min': -1, 'max': 1, 'palette': ["#8B0000", 'white', "#0D3672"]}, 'Trends')
   Map.add_colorbar({'min': -1, 'max': 1, 'palette': ["#8B0000", 'white', "#0D3672"]}, layer_name='Trends')

   Map.to_streamlit()


def add_image_to_map(image, index_name, label):
   style_params_zittau = {
    'color': 'cyan',
    'fillColor': '00000000', 
    'width': 3  
   }
   style_params_turow = {
    'color': 'red',
    'fillColor': '00000000', 
    'width': 3  
   }

   map = geemap.Map(basemap="Esri.WorldGrayCanvas") 
   map.centerObject(data.selected_units, 11)
   map.addLayer(image, get_vis_params()[index_name], label)
   map.addLayer(data.zittau.style(**style_params_zittau), {}, 'Zittau Basin')
   map.addLayer(data.turow_site_area.style(**style_params_turow), {}, 'Mining site')

   icon = folium.Icon(color='blue', icon='water', icon_color="white", prefix='fa')
   marker = folium.Marker(location=[50.865769162068524, 14.89948172073119], popup="Uhelna", icon=icon)
   feature_group = folium.FeatureGroup(name='Uhelna')
   feature_group.add_child(marker)
   map.add_child(feature_group)
   
   map.add_legend(title=index_name, colors=(get_palette()[index_name])[::-1], labels=(get_labels()[index_name])[::-1])
   map.to_streamlit()





