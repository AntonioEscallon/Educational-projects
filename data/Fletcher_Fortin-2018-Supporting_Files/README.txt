Spatial Ecology and Conservation Modeling
Fletcher and Fortin (2018)
4/5/2019

Below we provide a brief summary fo the code and data files used in Fletcher and Fortin (2018). 
Some data files are used in > 1 chapter.
Data files will be updated as needed and re-posted.
Note that some spatial data use > 1 file (e.g. rasters have .gri and .grd files); below we only mention the file called in the text.

If you have any problems, please email: robert.fletcher@ufl.edu.

Data and code files used for each chapter:

Ch2:

Ch2_code.R: complete R code used in Chapter 2.
nlcd2011SE: raster National Landcover Dataset from 2011, truncated to the SE United States.
reptiledata: Folder containing spatial data regarding site information of drift-fence arrays across the SE United States. Taken from Gottlieb et al. (2017).
reptiles_flsk.csv: comma-delimited file of data for southeastern five-lined skinks taken from drift-fence arrays across the SE United States.

Ch3:

Ch3_code.R: complete R code used in Chapter 3.
nlcd2011gv2sr: raster National Landcover Dataset from 2011. One landscape considered in Ch2 that has been re-classified to fewer landcover categories.

Ch4:

Ch4_code.R: complete R code used in Chapter 4.
cactus.csv: text file of Opuntia distribution in one plot at the Ordway-Swisher Biological Station, taken from Fletcher et al. (2018).
cactus_boundary.csv: comma-delimited file of coordinates for the plot extent, taken from Fletcher et al. (2018).
cactus_boundary.shp: spatial polygon file for the plot extent, taken from Fletcher et al. (2018).
cactus_matrix.csv: comma-delimited file (note, book shows use of raster derived from this file) that quantifies the vegetation height surrounding Opuntia in the plot from Ch 4, with measurements taken every 2 m, taken from Fletcher et al. (2018).

Ch5:

Ch5_code.R: complete R code used in Chapter 5.
cactus_matrix.csv: comma-delimited file that quantifies the vegetation height surrounding Opuntia in the plot from Ch 4, with measurements taken every 2 m, taken from Fletcher et al. (2018).

Ch6:

Ch6_code.R: complete R code used in Chapter 6, excluding one function used (icorrelogram).
icorrelogram.R: code that provides a custom function for fitting a correlogram and getting null envelopes for the correlogram.
vath_2004.csv: comma-delimited file on varied thrush occurrence in the year 2004, taken from the Northern Region Landbird Monitoring Program (Hutto and Young 2002).
elev.gri: raster file of elevation (a digital elevation model) for the study region.

Ch7:

Ch7_code.R: complete R code used in Chapter 7.
vath_2004.csv: comma-delimited file on varied thrush occurrence in the year 2004, taken from the Northern Region Landbird Monitoring Program (Hutto and Young 2002).
vath_VALIDATION.csv: comma-delimited file on varied thrush occurrence in the years 2007-2008, taken from the Northern Region Landbird Monitoring Program (Hutto and Young 2002).
elev.gri: raster file of elevation (a digital elevation model) for the study region.
cc2.gri: raster file of canopy cover, taken from a PCA using the USFS R1-VMP map, for the study region. See McCarty et al. (2012).
mesic.gri: raster file of mesic forest, taken from the USFS R1-VMP map, for the study region. See McCarty et al. (2012).
precip.gri: raster file of mean annual precipitation, taken from the PRISM group (www.prismclimate.org), for the study region. See McCarty et al. (2012).

Ch8:

Ch8_code.R: complete R code used in Chapter 8.
panthers.shp: spatial point (.shp) file of panther locations for 6 panthers in southern Florida. Taken from Florida Fish and Wildlife Conservation Commission.
panther_landcover.gri: raster land-cover data for southern Florida in 2003. Taken from Florida Fish and Wildlife Conservation Commission.

Ch9:

Ch9_code.R: complete R code used in Chapter 9.
panther_landcover.gri: raster land-cover data for southern Florida in 2003. Taken from Florida Fish and Wildlife Conservation Commission.
panther_publicland.shp:
resistance_reclass.txt: text file for reclassifying land-cover data, based loosely on Kautz et al. (2006).
kite_movement.csv: comma-delimited file of annual snail kite movements between wetlands, taken from Reichert et al. (2016).
kite_nodes.csv: comma-delimited file of wetland attributes used in kite_movement.csv.

Ch10:

Ch10_code.R: complete R code used in Chapter 10.
orchid.csv: comma-delimited file of orchid data, including survey data and site attributes. 

Ch11:

Ch11_code.R: complete R code used in Chapter 11.
birdcommunity: comma-delimited file on occurrence of 114 bird species at point locations, pooling data from 3 years (2000, 2002, 2004). Taken from the Northern Region Landbird Monitoring Program (Hutto and Young 2002).
elev.gri: raster file of elevation (a digital elevation model) for the study region.
cc2.gri: raster file of canopy cover, taken from a PCA using the USFS R1-VMP map, for the study region. See McCarty et al. (2012).
precip.gri: raster file of mean annual precipitation, taken from the PRISM group (www.prismclimate.org), for the study region. See McCarty et al. (2012).

Appendix

Appendix_code.R: complete R code used in Appendix.
vath_2004.csv: comma-delimited file on varied thrush occurrence in the year 2004, taken from the Northern Region Landbird Monitoring Program (Hutto and Young 2002).
vath_covariates: comma-delimited file characteristics at sampling locations in vath_2004.csv.
water: Folder containing spatial data (polygon data) for watersheds in region.
elev.gri: raster file of elevation (a digital elevation model) for the study region.
mesic.gri: raster file of mesic forest, taken from the USFS R1-VMP map, for the study region. See McCarty et al. (2012).

