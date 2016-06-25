# US Metropolitan atlas 2014

Provides an Atlas of the US Metropolitan areas delineated for the 2014 American
Community Survey. Inspired by Mike Bostock's [us-atlas](https://github.com/mbostock/us-atlas).

## Features available

Data tabulation geographical levels for the 2014 US Census:

* Census Block Groups boundaries (blockgroups)
* Census Tracts boundaries (tracts)
* Counties boundaries (countries)

## Use

In the commande line, go in the folder where you cloned the repository, and type
(to get the blockgroups)

```bash
make blockgroups
```

The program will download the necessary data, and the shapefiles will be
available in the folder `data/shp/cbsa_id.

To get other geographies, type the name of other geographies in parenthesis
above instead of 'blockgroups'. If you type `make` alone, the program will
download and prepare all geographies.

CBSA Ids can be obtained by typing


```bash 
cat data/misc/cbsa_names.txt | grep a_few_letters_of_city_name
```

## License

The code is distributed under the BSD License, see LICENSE.txt for more details.

```
Copyright (c) Scities
Rémi Louf <remi.louf@sciti.es>
```
