require(rgeos)
require(rgdal)
require(raster)
wy_counties = readOGR(file.path("data", "wy_counties"))
temperature = raster(here("data", "temperature", "temperature.tif"))

wy_counties = spTransform(readOGR(here("data", "wy_counties")), proj4string(temperature))

plot(temperature)

plot(wy_counties, add= TRUE)

temperature = crop(temperature, buffer(wy_counties, width = 10000))
plot(temperature)


carbon_cnty = subset(wy_counties, COUNTYNAME == "Carbon")
carbon_cnty_rst = crop(temperature, buffer(carbon_cnty, width = 10000))
plot(carbon_cnty_rst)
plot(carbon_cnty, add = T, lwd = 2)
plot(mask(carbon_cnty_rst, carbon_cnty))
plot(carbon_cnty, add = T)

wy_rasters = rasterize(wy_counties, temperature)

plot(wy_rasters)