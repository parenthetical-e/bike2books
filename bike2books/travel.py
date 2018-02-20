import os
import urllib
import geojson
import bike2books


def _get_data():
    base_path = os.path.split(bike2books.__file__)[0]
    data_path = os.path.join(base_path, "data")

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
        url = "http://seshat.datasd.org/parking_meters/treas_meters_2017_pole_by_month_datasd.csv"

        # Bike paths
        file_name = os.path.join(data_path, "bike_routes_datasd.geojson")
        url = "http://seshat.datasd.org/sde/bike_route/bike_routes_datasd.geojson"
        urllib.urlretrieve(url, file_name)


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


def drive_time(start, finish):
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
    """

    _get_data()  # Lazy. Only runs if the data is not present...

    pass
