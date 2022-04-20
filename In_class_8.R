require(rgdal)
require(rgeos)
install.packages("dismo")
require(dismo)
require(sf)
require("here")
require(raster)

ca_cnty = readOGR(here("data", "CA_counties.GPKG"))
ca_ozone = spTransform(readOGR(here("data", "CA_ozone_2017.GPKG")), proj4string(ca_cnty))

ca_voronoi = voronoi(ca_ozone)

plot(ca_voronoi)

ca_crop = crop(ca_voronoi, ca_cnty)
plot(ca_crop)

points(ca_ozone)
