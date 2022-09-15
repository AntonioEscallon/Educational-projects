require(sp)
require(ggplot2)
require(rgdal)
states = rgdal::readOGR(
  dsn = here("data", "NY8_utm18"))
states$AREANAME
sy_sp = subset(states, AREANAME == "Syracuse city")
sy_sp$AREANAME
sy_nb = poly2nb(sy_sp, queen = T)
sy_nb_w = nb2listw(sy_nb)
par(mar = c(0,0,0,0))
plot(sy_sp, border = gray(0,0.9), lwd=1)
# You can use $ to subset a brick with named layers
elev_spdf = rasterToPoints(layers$elev)

# rasterToPoints returns a matrix, but ggplot()
# expects a data.frame
elev_df = data.frame(elev_spdf)
head(elev_df)
# The geom_raster() method does the work by 'tiling' squares.
# It can be a little bit slow.
ggplot(elev_df) +
  geom_raster(aes(x = x, y = y, fill = elev))
require(sf)
data_dir = here(
  "data",
  "NY8_utm18")
head(point.data)

ny_8 = readOGR()

point_sf = st_as_sf(point.data, coords = c("EASTING", "NORTHING"))

# We happen to know the coordinate systems are the same
st_crs(point_sf) = crs(layers)

ggplot() +
  geom_raster(data = elev_df, mapping = aes(x = x, y = y, fill = elev)) +
  geom_sf(data = point_sf)

ggplot() +
  geom_raster(data = elev_df, mapping = aes(x = x, y = y, fill = elev)) +
  geom_sf(data = point_sf) +
  scale_fill_viridis_c()


moran.test(sy_sp$Cases, listw = sy_nb_w)

sy_sp = subset(ny_)

fit_spatial_1 = lm(Z ~ PCTAGE65P + PCTOWNHOME + PEXPOSURE, data = sy_sp)

summary(fit_spatial_1)


syr_me = ME(Z ~ PCTAGE65P +  PCTOWNHOME + PEXPOSURE, data = sy_sp, listw = sy_nb_w)
moran.test(residuals(fit_spatial_1), listw = sy_nb_w)
fit_spatial_2 = lm(Z ~ PCTAGE65P + PCTOWNHOME + PEXPOSURE + fitted(syr_me), data = sy_sp)

summary(fit_spatial_2)

 moran.test(residuals(fit_spatial_2), listw = sy_nb_w)

fit_sar_3 = spautolm(Z ~ PCTAGE65P + PCTOWNHOME + PEXPOSURE, data = sy_sp, listw = sy_nb_w)

summary(fit_sar_3)
fit_sar_3$fit$residuals
moran.test(residuals(fit_sar_3), listw = sy_nb_w)

fit_lag_1 = lagsarlm(Z ~ PCTAGE65P + PCTOWNHOME + PEXPOSURE, data = sy_sp, listw = sy_nb_w)

summary(fit_lag_1)

moran.test(residuals(fit_lag_1), listw = sy_nb_w)

rmse = function(fit) return (sqrt(mean(residuals(fit)^2)))

fits_rmse = data.frame( model = c("aspatial", "SAR", "Lag", "Filter"),
                        rmse = round(c(rmse(fit_spatial_1),
                                       rmse(fit_sar_3),
                                       rmse(fit_lag_1),
                                       rmse(fit_spatial_2)), 2
                                       ))
fits_rmse

par(mfrow = c(2, 2))
par(oma=c(0,0,2,0))
hist(fit_spatial_1$residuals, main = "Histogram of Aspatial residuals")
hist(fit_spatial_2$residuals, main = "Histogram of Filter residuals")
hist(fit_sar_3$fit$residuals, main = "Histogram of SAR residuals")
hist(fit_lag_1$residuals, main = "Histogram of Lag residuals")

