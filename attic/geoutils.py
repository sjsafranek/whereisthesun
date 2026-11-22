import geopandas
from geopy.distance import great_circle
from shapely import buffer 
from shapely.geometry import Point
from shapely.geometry import MultiPoint
from shapely.geometry import Polygon
from shapely.geometry import GeometryCollection


def getConvexHullFromGeoDataFrame(gdf, geoColumnId='geometry'):
	geometries = gdf[geoColumnId].to_list()
	collection = GeometryCollection(geometries)
	geometry = collection.convex_hull
	if Polygon is not type(geometry):
		return buffer(geometry, 0.0000001)
	return geometry


def getCoordsFromPolygon(geometry):
	geom_type = type(geometry)
	if Polygon is not geom_type:
		raise Exception('Only Polygon geometries are supported: {0}'.format(geom_type))
	xx, yy = geometry.exterior.coords.xy
	x = xx.tolist()
	y = yy.tolist()
	return [Point(xy) for xy in tuple(zip(x,y))]


def getDistanceBetweenPoints(point1, point2):
	return great_circle((point1.y, point1.x), (point2.y, point2.x)).meters

