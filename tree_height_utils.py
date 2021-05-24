import json
import geopandas as gpd

def cleaning_data(path_tree_results: str):
    with open(path_tree_results) as json_file:
        data_tree_height = json.load(json_file)

    number_of_tiles = len(data_tree_height["features"])

    # for each tile get the features and concatenate them in a list
    tree_feature_list = []
    for i in range(number_of_tiles):
        try:
            features = data_tree_height["features"][i]["features"]["features"] # get each tree height feature list
            tree_feature_list = tree_feature_list + features  # combine all tree height features into one list
        except KeyError as e:
            pass

    # write tree height features into geojson file if you want to visualize file in GIS
    with open(f"treeheight_asturias.geojson", "w") as dst:
        collection = {
            "type": "FeatureCollection",
            "features": tree_feature_list
        }
        dst.write(json.dumps(collection))

    trees_gdf = gpd.read_file('treeheight_asturias.geojson')
    # kepler requires crs in lat/long, thus transforming crs is required
    trees_gdf.set_crs(epsg=3857, inplace=True, allow_override=True)
    geo_trees_gdf = trees_gdf.to_crs(epsg=4326)

    # create separate dataframe with only tall trees (above 6m)
    high_trees_gdf = geo_trees_gdf.loc[(geo_trees_gdf['height'] >= 6)]

    return geo_trees_gdf, high_trees_gdf


def get_kepler_config(trees_gdf):
# configuration for kepler map
 config = {
  "version": "v1",
  "config": {
    "visState": {
      "filters": [],
      "layers": [
        {
          "id": "j688u9",
          "type": "geojson",
          "config": {
            "dataId": "all trees",
            "label": "all trees",
            "color": [
              18,
              92,
              119
            ],
            "columns": {
              "geojson": "geometry"
            },
            "isVisible": True,
            "visConfig": {
              "opacity": 0.8,
              "strokeOpacity": 0.8,
              "thickness": 0.5,
              "strokeColor": [
                77,
                193,
                156
              ],
              "colorRange": {
                "name": "Custom Palette",
                "type": "custom",
                "category": "Custom",
                "colors": [
                  "#fbf36a",
                  "#fe950f",
                  "#ff0004"
                ]
              },
              "strokeColorRange": {
                "name": "Global Warming",
                "type": "sequential",
                "category": "Uber",
                "colors": [
                  "#5A1846",
                  "#900C3F",
                  "#C70039",
                  "#E3611C",
                  "#F1920E",
                  "#FFC300"
                ]
              },
              "radius": 10,
              "sizeRange": [
                0,
                10
              ],
              "radiusRange": [
                0,
                50
              ],
              "heightRange": [
                0,
                500
              ],
              "elevationScale": 0.2,
              "stroked": False,
              "filled": True,
              "enable3d": True,
              "wireframe": False
            },
            "hidden": False,
            "textLabel": [
              {
                "field": None,
                "color": [
                  255,
                  255,
                  255
                ],
                "size": 18,
                "offset": [
                  0,
                  0
                ],
                "anchor": "start",
                "alignment": "center"
              }
            ]
          },
          "visualChannels": {
            "colorField": {
              "name": "height",
              "type": "real"
            },
            "colorScale": "quantile",
            "sizeField": None,
            "sizeScale": "linear",
            "strokeColorField": None,
            "strokeColorScale": "quantile",
            "heightField": {
              "name": "height",
              "type": "real"
            },
            "heightScale": "linear",
            "radiusField": None,
            "radiusScale": "linear"
          }
        }
      ],
      "interactionConfig": {
        "tooltip": {
          "fieldsToShow": {
            "all trees": [
              {
                "name": "height",
                "format": None
              }
            ]
          },
          "compareMode": False,
          "compareType": "absolute",
          "enabled": True
        },
        "brush": {
          "size": 0.5,
          "enabled": False
        },
        "geocoder": {
          "enabled": False
        },
        "coordinate": {
          "enabled": False
        }
      },
      "layerBlending": "normal",
      "splitMaps": [],
      "animationConfig": {
        "currentTime": None,
        "speed": 1
      }
    },
    "mapState": {
      "bearing": 24,
      "dragRotate": True,
      "latitude": trees_gdf['geometry'][0].centroid.y,
      'longitude': trees_gdf['geometry'][0].centroid.x,
      "pitch": 50,
      "zoom": 15.9,
      "isSplit": False
    },
    "mapStyle": {
      "styleType": "satellite",
      "topLayerGroups": {},
      "visibleLayerGroups": {},
      "threeDBuildingColor": [
        3.7245996603793508,
        6.518049405663864,
        13.036098811327728
      ],
      "mapStyles": {}
    }
  }
}
 return config