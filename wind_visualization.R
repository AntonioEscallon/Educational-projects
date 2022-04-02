# Download and install "rWind" package from CRAN:  
install.packages("shape")  

# You should install also "raster" package if you do not have it   
require(raster)
library(rWind)  
require(rWind)
library(raster)  
require(rworldmap)
library(gdistance)
library(shape)
library(rgdal)
library(dplyr)

packageDescription("rWind")  
help(package="rWind")  

# "rWind" is a package with several tools for downloading, editing and transforming wind data from Global Forecast   
# System (GFS, see <https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-forcast-system-gfs>) of the USA's  
# National Weather Service (NWS, see <http://www.weather.gov/>).  

citation("rWind")  

# > Javier Fernández-López (2016). rWind: Download, Edit and Transform Wind Data from GFS. R package version 0.1.3.  
# > https://CRAN.R-project.org/package=rWind  

# First, we can download a wind dataset of a specified date from GFS using wind.dl function  
# help(wind.dl)  

# Download wind for Spain region at 2015, February 12, 00:00  
help(wind.dl)  

wind.dl(2015,2,12,0,-10,5,38,45)  

# By default, this function generates an R object with downloaded data. You can store it...  

wind_data<-wind.dl(2015,2,12,0,-75,-66,38,45)  
#https://pae-paha.pacioos.hawaii.edu/erddap/griddap/ncep_global.csv?ugrd10m[(2015-2-12T0:00:00Z)][(-91):(-66)][(30):(359.5)],vgrd10m[(2015-2-12T0:00:00Z)][(-91):(-66)][(30):(359.5)]&.draw=vectors&.vars=longitude|latitude|ugrd10m|vgrd10m&.color=0x000000

head(wind_data)


# or download a CVS file into your work directory with the data using type="csv" argument:  

getwd()  
wind.dl(2015,2,12,0,-75,-66,35,45, type="csv")  


# If you inspect inside wind_data object, you can see that data are organized in a weird way, with  
# to rows as headers, a column with date and time, longitude data expressed in 0/360 notation and wind  
# data defined by the two vector components U and V. You can transform these data in a much more nice format
# using "wind.fit" function:  
#help(wind.fit)  

#wind_data<-wind.fit_int(wind_data)  

head(wind_data) 

r_wind <- wind2raster(wind_data)  

writeRaster(r_wind,'r_wind_raster.tif',options=c('TFW=YES'))

library(rworldmap)   
newmap <- getMap(resolution = "low")

writeRaster(newmap,'newmap.tif',options=c('TFW=YES'))
map <- subset(world, LON>-43.41 | LON < -43.1 & LAT>- 23.05 | LAT< -22.79)
writeOGR(map, ".", "map", 
         driver = "ESRI Shapefile")
plot(newmap)

par(mfrow=c(1,2)) 
print(proj4string(newmap))
print(proj4string(r_wind))
plot(subset(r_wind,1), main="Wind") 
alpha <- arrowDir(wind_data)

Arrowhead(wind_data$lon, wind_data$lat, angle=alpha, arr.length = 0.04, arr.type="curved")

lines(newmap, lwd=0.5)  



