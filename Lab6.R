require(rgdal)
require(here)
require(sp)
require(terra)
require(sf)
require(ggplot2)
require(raster)
ca_cnty = readOGR(here("data", "ca_Counties.GPKG"))

ca_ozone = spTransform(readOGR(here("data", "CA_ozone_2017.GPKG")), proj4string(ca_cnty))

crs(ca_ozone) = crs(ca_cnty)

ca_sf = st_as_sf(ca_cnty)
oz_sf = st_as_sf(ca_ozone)

ggplot() +
  geom_sf(data = ca_sf, lwd = 0.1, fill = gray(0.5, 0.5)) +
  geom_sf(data = oz_sf, mapping = aes(colour = ozone), cex = 2) +
  scale_color_gradientn(colours = heat.colors(10), name = "Ozone") +
  theme_minimal() +
  ggtitle("Annual ozone levels: 2017")

# Create a template raster
temp_rast = raster(
  ca_cnty, nrow = 200, ncol = 180)

# Use the crs() trick to avoid any potential headaches
crs(temp_rast) = crs(ca_cnty)

# Convert the raster to a SpatialPointsDataFrame
temp_grid_sp = as(temp_rast, "SpatialPoints")

# Crop to the outline of California
temp_grid_sp = crop(temp_grid_sp, ca_cnty)


# Create gstat object
oz_gs = gstat(
  formula = ozone ~ 1,
  locations = ca_ozone)

# Build empirical variogram:
vgm_emp = variogram(oz_gs)
plot(vgm_emp, pch = 16, cex = 1.2)