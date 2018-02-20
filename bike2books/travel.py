import os
import urllib
import geojson
import bike2books
import pandas as pd


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


def neighborhood_location(name):
    """Return the (lat, long) of a neighborhoods center."""

    nns = neighborhoods()
    return nns[name]


def neighborhood_names():
    """Return the all neighborhood's names."""
    nns = neighborhoods()
    return nns.keys()


def neighborhoods():
    """Neighborhood names and centers (lat, long).

    Note: Names take from from the Parking meter data at:
    http://seshat.datasd.org/parking_meters/treas_parking_meters_loc_datasd.csv

    Location taken from wikipedia, or manual estimates derived via Google Maps.
    (This should be automated in the future).
    """

    return {
        'Barrio Logan': (32.697539, -117.142025),
        'Midtown': (32.738611, -117.175278),
        'Mission Beach': (32.775034, -117.251903),
        'Mission Hills': (32.752828, -117.186361),
        'Point Loma': (32.67, -117.241944),
        'Core - Columbia': (32.716678, -117.168244),
        'Cortez Hill': (32.721667, -117.16),
        'East Village': (32.724167, -117.167222),
        'Gaslamp': (32.711667, -117.159167),
        'Little Italy': (32.724167, -117.167222),
        'Marina': (32.711667, -117.169167),
        'Golden Hill': (32.718, -117.134),
        'North Park': (32.740831, -117.129719),
        'Talmadge': (32.764, -117.09),
        'University Heights': (32.76, -117.14),
        'Bankers Hill': (32.731, -117.164),
        'Five Points': (32.7431, -117.1848),
        'Hillcrest': (32.75, -117.166667)
    }


def nearest_library(location):
    """Locate nearest library, in miles.
    
    Parameters
    ----------
    location : 2-tuple
        (Lat, Long) coordinates
    """

    _get_data()  # Lazy. Only runs if the data is not present...

    pass


def bike_time(start, finish, penalty=10):
    """Estimate biking time from two sets of (lat, long)
    coordinates. 

    Penalizes time if there are no safe bike routes nearby.

    Parameters
    ----------
    state : 2-tuple
        Stating (Lat, Long) coordinates
    stop : 2-tuple
        Stating (Lat, Long) coordinates
    penalty : numeric
        Penalty time
    """

    _get_data()  # Lazy. Only runs if the data is not present...

    pass


def drive_time(start, finish, min_time=2, max_time=30):
    """Estimate drive time from two sets of (lat, long)
    coordinates. 
    
    Penalize time based on parking meter usage - more usage may increase
    parking times.

    Parameters
    ----------
    state : 2-tuple
        Stating (Lat, Long) coordinates
    stop : 2-tuple
        Stating (Lat, Long) coordinates
    min_time : numeric
        Minumum parking time (minutes)
    max_time : numeric
        Maximum parking time (minutes)
    """

    _get_data()  # Lazy. Only runs if the data is not present...

    pass
