# bike2books

The City of San Diego is investing in substantial improvements in biking [infrastructure](https://www.sandiego.gov/sites/default/files/legacy/planning/programs/transportation/mobility/pdf/bicycle_master_plan_final_dec_2013.pdf). Such complex a and long-term effort can be difficult to explain to the community in way they find intuitive and meaningful....

The `bike2books` project provides a simple and meaningful metric of a neighborhood's bike-a-bility: _how long does it take to bike safely to your nearest library?_ 

Libraries are often centrally located in their neighborhoods, they are familiar landmarks, and are used by a wide range of community members. The main idea here is that if someone feels comfortable biking to their library, they should feel comfortable biking elsewhere in their neighborhood. This is not a complete measure - it may not be good metric for commuting - but may be useful in helping San Diego developing a bike friendly brand.

This Python module includes *the beginning* of a tool set for re-sampling based statistical simulations to analyze the bike "bike-a-bility" of each neighborhood in San Diego.

## Key details

- Bike travel time is penalized when the route does not *easily* include a bike lane or path. This penalty may not reflect the actual travel time, but for biking to become popular it needs to be seen as safe. Providing several measures of bike-a-bility (e.g. one for time, one for safety) can make understanding and quantifying progress difficult. By converting safety (as measure by bike lane availability) into units of time, we can introduce a single bike-a-bility metric. One that lends itself to comparison with other ways of getting around, and is easily understood. 

- Bike results are compared to average travel-time by car, penalized by an estimate of how long it might take to park. Parking penalties are based on nearby parking meter usage.

- In the future travel times will be estimated using the Google Maps API. At present that are __very crude__ estimates based on line-of-sight distance.

# Installation

`git clone ...` into a working directory.

On the command line, move into that directory then into the top-level `bike2books` directory. From there type, `pip install -e .`


# Usage

See `ipnyb/example.ipynb`


# Data

- Library locations: http://seshat.datasd.org/sde/library/libraries_datasd.geojson
- Parking meter usage: http://seshat.datasd.org/parking_meters/treas_meters_2016_pole_by_mo_day_datasd.csv
- Bike paths locations: http://seshat.datasd.org/sde/bike_route/bike_routes_datasd.geojson

