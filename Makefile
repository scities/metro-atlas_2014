# Author: Remi Louf <remilouf@sciti.es>
# Date:   24/03/2016

all: counties tracts blockgroups

blockgroups: download_blockgroups  shapefile_blockgroups adjacency_blockgroups surface_blockgroups
tracts: download_tracts  shapefile_tracts adjacency_tracts surface_tracts
counties: download_counties  shapefile_counties adjacency_counties surface_counties


#################
# DOWNLOAD DATA #
#################

# Reconstitute 2014 American Community Survey CBSA
data/gz/List1.xls:
	mkdir -p $(dir $@)
	curl "http://www.census.gov/population/metro/files/lists/2013/$(notdir $@)" -o $@.download
	mv $@.download $@





# Download the shapefiles of the different areal units
## Download census blockgroups
data/gz/tl_2014_%_bg.zip:
	mkdir -p $(dir $@)
	curl 'http://www2.census.gov/geo/tiger/TIGER2014/BG/$(notdir $@)' -o $@.download
	mv $@.download $@

data/shp/state/%/blockgroups.shp: data/gz/tl_2014_%_bg.zip
	rm -rf $(basename $@)
	mkdir -p $(basename $@)
	unzip -d $(basename $@) $<
	for file in $(basename $@)/*; do chmod 644 $$file; mv $$file $(basename $@).$${file##*.}; done
	rmdir $(basename $@)
	touch $@

download_blockgroups: data/shp/state/01/blockgroups.shp data/shp/state/02/blockgroups.shp data/shp/state/04/blockgroups.shp data/shp/state/05/blockgroups.shp data/shp/state/06/blockgroups.shp data/shp/state/08/blockgroups.shp data/shp/state/09/blockgroups.shp data/shp/state/10/blockgroups.shp data/shp/state/11/blockgroups.shp data/shp/state/12/blockgroups.shp data/shp/state/13/blockgroups.shp data/shp/state/15/blockgroups.shp data/shp/state/16/blockgroups.shp data/shp/state/17/blockgroups.shp data/shp/state/18/blockgroups.shp data/shp/state/19/blockgroups.shp data/shp/state/20/blockgroups.shp data/shp/state/21/blockgroups.shp data/shp/state/22/blockgroups.shp data/shp/state/23/blockgroups.shp data/shp/state/24/blockgroups.shp data/shp/state/25/blockgroups.shp data/shp/state/26/blockgroups.shp data/shp/state/27/blockgroups.shp data/shp/state/28/blockgroups.shp data/shp/state/29/blockgroups.shp data/shp/state/30/blockgroups.shp data/shp/state/31/blockgroups.shp data/shp/state/32/blockgroups.shp data/shp/state/33/blockgroups.shp data/shp/state/34/blockgroups.shp data/shp/state/35/blockgroups.shp data/shp/state/36/blockgroups.shp data/shp/state/37/blockgroups.shp data/shp/state/38/blockgroups.shp data/shp/state/39/blockgroups.shp data/shp/state/40/blockgroups.shp data/shp/state/41/blockgroups.shp data/shp/state/42/blockgroups.shp data/shp/state/44/blockgroups.shp data/shp/state/45/blockgroups.shp data/shp/state/46/blockgroups.shp data/shp/state/47/blockgroups.shp data/shp/state/48/blockgroups.shp data/shp/state/49/blockgroups.shp data/shp/state/50/blockgroups.shp data/shp/state/51/blockgroups.shp data/shp/state/53/blockgroups.shp data/shp/state/54/blockgroups.shp data/shp/state/55/blockgroups.shp data/shp/state/56/blockgroups.shp data/shp/state/60/blockgroups.shp data/shp/state/66/blockgroups.shp data/shp/state/69/blockgroups.shp data/shp/state/72/blockgroups.shp data/shp/state/78/blockgroups.shp 



## Download census tracts
data/gz/tl_2014_%_tract.zip:
	mkdir -p $(dir $@)
	curl 'http://www2.census.gov/geo/tiger/TIGER2014/TRACT/$(notdir $@)' -o $@.download
	mv $@.download $@

data/shp/state/%/tracts.shp: data/gz/tl_2014_%_tract.zip
	rm -rf $(basename $@)
	mkdir -p $(basename $@)
	unzip -d $(basename $@) $<
	for file in $(basename $@)/*; do chmod 644 $$file; mv $$file $(basename $@).$${file##*.}; done
	rmdir $(basename $@)
	touch $@

download_tracts: data/shp/state/01/tracts.shp data/shp/state/02/tracts.shp data/shp/state/04/tracts.shp data/shp/state/05/tracts.shp data/shp/state/06/tracts.shp data/shp/state/08/tracts.shp data/shp/state/09/tracts.shp data/shp/state/10/tracts.shp data/shp/state/11/tracts.shp data/shp/state/12/tracts.shp data/shp/state/13/tracts.shp data/shp/state/15/tracts.shp data/shp/state/16/tracts.shp data/shp/state/17/tracts.shp data/shp/state/18/tracts.shp data/shp/state/19/tracts.shp data/shp/state/20/tracts.shp data/shp/state/21/tracts.shp data/shp/state/22/tracts.shp data/shp/state/23/tracts.shp data/shp/state/24/tracts.shp data/shp/state/25/tracts.shp data/shp/state/26/tracts.shp data/shp/state/27/tracts.shp data/shp/state/28/tracts.shp data/shp/state/29/tracts.shp data/shp/state/30/tracts.shp data/shp/state/31/tracts.shp data/shp/state/32/tracts.shp data/shp/state/33/tracts.shp data/shp/state/34/tracts.shp data/shp/state/35/tracts.shp data/shp/state/36/tracts.shp data/shp/state/37/tracts.shp data/shp/state/38/tracts.shp data/shp/state/39/tracts.shp data/shp/state/40/tracts.shp data/shp/state/41/tracts.shp data/shp/state/42/tracts.shp data/shp/state/44/tracts.shp data/shp/state/45/tracts.shp data/shp/state/46/tracts.shp data/shp/state/47/tracts.shp data/shp/state/48/tracts.shp data/shp/state/49/tracts.shp data/shp/state/50/tracts.shp data/shp/state/51/tracts.shp data/shp/state/53/tracts.shp data/shp/state/54/tracts.shp data/shp/state/55/tracts.shp data/shp/state/56/tracts.shp data/shp/state/60/tracts.shp data/shp/state/66/tracts.shp data/shp/state/69/tracts.shp data/shp/state/72/tracts.shp data/shp/state/78/tracts.shp 



## Download census counties
data/gz/tl_2012_us_countyec.zip:
	mkdir -p $(dir $@)
	curl 'http://www2.census.gov/geo/tiger/TIGER2014/COUNTYEC/$(notdir $@)' -o $@.download
	mv $@.download $@

data/shp/us/counties.shp: data/gz/tl_2012_us_countyec.zip
	rm -rf $(basename $@)
	mkdir -p $(basename $@)
	unzip -d $(basename $@) $<
	for file in $(basename $@)/*; do chmod 644 $$file; mv $$file $(basename $@).$${file##*.}; done
	rmdir $(basename $@)
	touch $@

download_counties: data/shp/us/counties.shp





##################
## Prepare data ##
##################

# Extract CBSA names
data/misc/cbsa_names.txt: data/gz/List1.xls
	mkdir -p $(dir $@)
	python2 bin/names/cbsa_names.py



# Blockgroups
## Crosswalk blockgroups and CBSA
data/crosswalks/cbsa_blockgroup.txt: data/crosswalks/cbsa_county.txt
	mkdir -p $(dir $@)
	python2 bin/crosswalks/cbsa_blockgroup.py

## Shapefile blockgroups for each CBSA
shapefile_blockgroups: data/misc/cbsa_names.txt data/crosswalks/cbsa_blockgroup.txt
	mkdir -p data/shp/cbsa
	python2 bin/shp/blockgroups.py

## Adjacency matrix for blockgroups
adjacency_blockgroups:
	mkdir -p  data/adjacency/cbsa
	python2 bin/adjacency/blockgroups.py

## Compute the surface area of blockgroups
surface_blockgroups:
	mkdir -p data/surface_area/cbsa
	python2 bin/surface/blockgroups.py



# Tracts
## Crosswalk tracts and CBSA
data/crosswalks/cbsa_tract.txt: data/crosswalks/cbsa_county.txt
	mkdir -p $(dir $@)
	python2 bin/crosswalks/cbsa_tract.py

## Shapefile tracts for each CBSA
shapefile_tracts: data/misc/cbsa_names.txt data/crosswalks/cbsa_tract.txt
	mkdir -p data/shp/cbsa
	python2 bin/shp/tracts.py

## Adjacency matrix for tracts
adjacency_tracts:
	mkdir -p  data/adjacency/cbsa
	python2 bin/adjacency/tracts.py

## Compute the surface area of tracts
surface_tracts:
	mkdir -p data/surface_area/cbsa
	python2 bin/surface/tracts.py



# Counties
## Crosswalk counties and CBSA
data/crosswalks/cbsa_county.txt: data/gz/List1.xls
	mkdir -p $(dir $@)
	python2 bin/crosswalks/cbsa_county.py

## Shapefile counties for each CBSA
shapefile_counties:
	mkdir -p data/shp/cbsa
	python2 bin/shp/counties.py

## Adjacency matrix for counties
adjacency_counties:
	mkdir -p  data/adjacency/cbsa
	python2 bin/adjacency/counties.py

## Compute the surface area of counties
surface_counties:
	mkdir -p data/surface_area/cbsa
	python2 bin/surface/counties.py






#########
# CLEAN #
#########
clean:
	find data ! -name 'states_list.txt' -type d -exec rm -rf {} +
