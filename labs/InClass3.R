require(raster)
require(rgdal)
require(rgeos)
require(rasterVis)

temperature = raster(here::here("data", "temperature", "temperature.tif"))

wy_cnty = spTransform(
  readOGR(here("data", "wy_counties")),
  projection(temperature))

projection(wy_cnty)

plot(temperature)

plot(wy_cnty, add = T)

temp_wy = crop(temperature, wy_cnty)

par(mar = c(0.1, 0.1, 0.1, 1))

plot(temp_wy, axes = F); plot(wy_cnty, add = T)

wy_counties_temp_mean = raster::extract(temp_wy, wy_cnty, fun = mean)

class(wy_counties_temp_mean)

wy_counties_temp_spdf = raster::extract(
  temp_wy, wy_cnty, fun = mean, sp = TRUE)

class(wy_counties_temp_spdf)

names(wy_counties_temp_spdf)

wy_counties_temp_list = raster::extract(
  temp_wy, wy_cnty)

sapply(wy_counties_temp_list, mean)

sapply(wy_counties_temp_list, mean, na.rm = T)

class(wy_counties_temp_list)

str(wy_counties_temp_list, 1)

# Mean of annual temperature.
wy_cnty$mean_temp = sapply(wy_counties_temp_list, mean, na.rm = TRUE)

# Standard deviation of annual temperature:
wy_cnty$sd_temp = sapply(wy_counties_temp_list, sd, na.rm = TRUE)

spplot(
  wy_cnty, zcol = "mean_temp")

spplot(wy_cnty, zcol = "sd_temp")

dsn = here("data", "Iowa_County_Boundaries-shp")
layer = "IowaCounties"

temperature = raster(here::here("data", "temperature", "temperature.tif"))

temperature = raster(here::here("data","PRISM_ppt_30yr_normal_4kmM3_all_bil", "PRISM_ppt_30yr_normal_4kmM3_01_bil.bil"))
other = raster(here::here("data","PRISM_tmean_30yr_normal_4kmM3_annual_bil", "PRISM_tmean_30yr_normal_4kmM3_annual_bil.bil"))


plot(temperature)
plot(other)
ia_cnty = spTransform(
  readOGR(dsn),
  projection(temperature))
plot(ia_cnty, add=T)

other_ia = crop(other, ia_cnty)
plot(other_ia)

ia_counties_temp_mean = raster::extract(temp_ia, ia_cnty, fun = mean)
ia_counties_temp_other = raster::extract(other_ia, ia_cnty, fun = mean)
class(ia_counties_temp_mean)

plot( 
  ia_counties_temp_other ~ ia_counties_temp_mean, data = ia_cnty@data,
  main = "IA Counties\n Mean Annual Precipitation and Temperature",
  xlab = "Mean annual temperature", ylab = "Mean annual precipitation"
)

