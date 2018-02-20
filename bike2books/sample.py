import numpy as np

# City center
CENTER = (32.7157, 117.1611)


def sample_location(radius=6, prng=None):
    """Draw a sample, starting from the city center.
    
    Parameters
    ---------
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

    x = r * np.cos(theta)
    y = r * np.sin(theta)

    return (CENTER[0] + x, CENTER[1] + y)
