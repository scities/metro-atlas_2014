# 2014 US Metropolitan Atlas

Ever worked with census data at the metropolitan level? This will save you a lot
of time by exporting shapefiles of cities containing the delineations of
sub-geographies.

As of today, the code contained in this repository allows to output

- Shapefiles
- Adjacency (contiguity) matrix between units
- Surface area of units

For the following levels

- Blockgroups
- Tracts
- Counties


## Use

To output all geographies type in command line

    make

In order to output specific geometries

    make blockgroups

    make tracts
    
    make counties


## License

The code is distributed under BSD License (see LICENSE).

    Copyright (c) Scities
    Rémi Louf <remi@sciti.es>
