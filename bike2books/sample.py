import numpy as np


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
