import numpy as np
import pandas as pd
import geopandas as gpd

from shapely.geometry import Point


def trips(N, center, radius=6, prng=None, as_geo=False):
    """Simulate N trips.

    Parameters
    ---------
    N : numeric
        Number of trips
    center : 2-tuple
        Stating (Lat, Long) coordinates
    radius : numeric
        Radius of neighborhoods to sample (in miles).
    as_geo : Bool
        If True, return a GeoDataFrame
    prng : None, np.random.RandomState
        Control random seeding in a sensible way.
    """

    samples = []
    for i in range(N):
        d = sample_location(center, radius, prng=prng)
        samples.append((i, d[0], d[1]))

    if as_geo:
        data = pd.DataFrame(samples, columns=["location", "lon", "lat"])
        geometry = [Point(xy) for xy in zip(data.lon, data.lat)]
        data = data.drop(['lon', 'lat'], axis=1)
        crs = {'init': 'epsg:4326'}
        samples = gpd.GeoDataFrame(data, crs=crs, geometry=geometry)

    return samples


def sample_location(center, radius=6, prng=None):
    """Draw a sample, starting from the city center.
    
    Parameters
    ---------
    center : 2-tuple
        Stating (Lat, Long) coordinates
    radius : numeric
        Radius of neighborhoods to sample (in miles).
    prng : None, np.random.RandomState
        Control random seeding in a sensible way.
    """

    # Handle random seed
    if prng is None:
        prng = np.random.RandomState()

    # Take sample
    r = prng.uniform(0, radius / 66.9)  # Crude conversion
    theta = prng.uniform(0, 2 * np.pi)

    # Convert to cartesian
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    return (center[0] + x, center[1] + y)
