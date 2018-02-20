import os
import urllib
import geojson
import bike2books
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopy.distance import vincenty


def _get_dat_path():
    base_path = os.path.split(bike2books.__file__)[0]
    data_path = os.path.join(base_path, "data")
    return data_path


def _get_data():
    data_path = _get_dat_path()

    if not os.path.isdir(data_path):
        # Create data dir
        os.mkdir(data_path)

        # And get all the needed data 
        # Lib
        file_name = os.path.join(data_path, "libraries_datasd.geojson")
        url = "http://seshat.datasd.org/sde/library/libraries_datasd.geojson"
        urllib.urlretrieve(url, file_name)

        # Parking data
        file_name = os.path.join(data_path,
                                 "treas_meters_2016_pole_by_month_datasd.csv")
        url = "http://seshat.datasd.org/parking_meters/treas_meters_2017_pole_by_month_datasd.csv"
        urllib.urlretrieve(url, file_name)

        # Parking locations
        file_name = os.path.join(data_path,
                                 "treas_parking_meters_loc_datasd.csv")
        url = "http://seshat.datasd.org/parking_meters/treas_parking_meters_loc_datasd.csv"
        urllib.urlretrieve(url, file_name)

        # Bike paths
        file_name = os.path.join(data_path, "bike_routes_datasd.geojson")
        url = "http://seshat.datasd.org/sde/bike_route/bike_routes_datasd.geojson"
        urllib.urlretrieve(url, file_name)


# ------------------------------------------------------------
# RUN ON IMPORT OF TRAVEL
_get_data()  # Lazy. Only runs if the data is not present...

# ------------------------------------------------------------


def neighborhood_location(name, as_geo=False):
    """Return the (lat, long) of a neighborhoods center."""

    nns = neighborhoods()

    loc = nns[name]
    if as_geo:
        loc = Point(loc)

    return loc


def neighborhood_names():
    """Return the all neighborhood's names."""

    nns = neighborhoods()
    return nns.keys()


def neighborhoods(as_geo=False):
    """Neighborhood names and centers (lat, long).

    Note: Names take from from the Parking meter data at:
    http://seshat.datasd.org/parking_meters/treas_parking_meters_loc_datasd.csv

    Location taken from wikipedia, or manual estimates derived via Google Maps.
    (This should be automated in the future).
    """

    data = {
        'Barrio Logan': (-117.142025, 32.697539),
        'Midtown': (-117.175278, 32.738611),
        'Mission Beach': (-117.251903, 32.775034),
        'Mission Hills': (-117.186361, 32.752828),
        'Point Loma': (-117.241944, 32.67),
        'Core - Columbia': (-117.168244, 32.716678),
        'Cortez Hill': (-117.16, 32.721667),
        'East Village': (-117.167222, 32.724167),
        'Gaslamp': (-117.159167, 32.711667),
        'Little Italy': (-117.167222, 32.724167),
        'Marina': (-117.169167, 32.711667),
        'Golden Hill': (-117.134, 32.718),
        'North Park': (-117.129719, 32.740831),
        'Talmadge': (-117.09, 32.764),
        'University Heights': (-117.14, 32.76),
        'Bankers Hill': (-117.164, 32.731),
        'Five Points': (-117.1848, 32.7431),
        'Hillcrest': (-117.166667, 32.75)
    }

    if as_geo:
        # To DF
        data = [(k, v[0], v[1]) for k, v in data.items()]
        data = pd.DataFrame(data, columns=["location", "lon", "lat"])

        # ...To GeoDF
        geometry = [Point(xy) for xy in zip(data.lon, data.lat)]
        data = data.drop(['lon', 'lat'], axis=1)
        crs = {'init': 'epsg:4326'}
        data = gpd.GeoDataFrame(data, crs=crs, geometry=geometry)

    return data


def distance_in_miles(x, y):
    """Return distance between two points
    x : 2-tuple
        First (lon, lat) coordinate
    y : 2-tuple
        Second (lon, lat) coordinate
    """

    return vincenty(x, y).miles


def nearest_library(location):
    """Locate nearest library, in miles.
    
    Parameters
    ----------
    location : 2-tuple
        (lon, lat) coordinates
    """

    location_point = Point(location)

    # Load
    data_path = _get_dat_path()

    library_data = gpd.read_file(
        os.path.join(data_path, "libraries_datasd.geojson"))

    library_points = library_data["geometry"]

    # Measure (unitless) distances
    distances = []
    for p in library_points:
        distances.append(location_point.distance(p))

    # Find the smallest distance
    i = np.argmin(distances)

    name = library_data["name"][i]
    closest = library_points[i]

    # Convert smallest point to a tuple ...(kluge?)
    closest = tuple(p.coords)[0]

    # How far?
    d = distance_in_miles(location, closest)

    return name, d


def bike_time(start, finish, penalty=10, speed=9.6):
    """Estimate biking time from two sets of (lat, long)
    coordinates. 

    Penalizes time if there are no safe bike routes nearby.

    Parameters
    ----------
    state : 2-tuple
        Stating (lon, lat) coordinates
    stop : 2-tuple
        Stating (lon, lat) coordinates
    penalty : numeric
        Penalty time (minutes)
    speed : numeric
        Avg. speed (MPH) [Default of 9.6 from Wikipedia]

    Note:
    ---
    The safety penalty is a total kluge to ge this working. It simply checks 
    if there is any single bike lane near the start point. 
    
    A correct/better approach would be to use google to plot a route 
    and examine how much of that is on a bike lane, or some similar thing.
    """

    # Get raw distance
    d = distance_in_miles(start, finish)

    # Find closest bike lane to the start.

    # Is it close enough to avoid a penalty?

    return d / speed


def drive_time(start, finish, speed=25, min_time=2, max_time=30):
    """Estimate drive time from two sets of (lat, long)
    coordinates. 
    
    Penalize time based on parking meter usage - more usage may increase
    parking times.

    Parameters
    ----------
    state : 2-tuple
        Stating (lon, lat) coordinates
    stop : 2-tuple
        Stating (lon, lat) coordinates
    speed : numeric
        Avg. speed (MPH)
    min_time : numeric
        Minumum parking time (minutes)
    max_time : numeric
        Maximum parking time (minutes)
    
    Note:
    ----
    The method used for the parking penalty is a total kluge to
    get this working. A better/correct model would examine raw
    parking times and develop good spatial distribution
    of parking availability from that data. 
    """

    # Get raw distance
    d = distance_in_miles(start, finish)

    # Lookup all parking data to get the range of value

    # Find the closest meter to the finish

    # Interpolate parking time using the range and min/max times, 
    # and the closest meter.

    return d / speed
