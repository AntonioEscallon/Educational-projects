require(rgdal)
require(here)
require(sp)
require(terra)
require(sf)
require(ggplot2)
require(raster)
#install.packages("RColorBrewer")
require(RColorBrewer)
require(gstat)
require(cowplot)
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
aqi_gs = gstat(
  formula = AQI ~ 1,
  locations = ca_ozone)

# Build empirical variogram:
aqi_vgm_emp = variogram(aqi_gs)
plot(aqi_vgm_emp, pch = 21, cex = 1.2, main = "Antonios varirogram of AQI")
# Parameterize initial spherical and exponential variograms.
# These contain the starting parameters for optimizations.
vgm_mod_exp = vgm(
  model = "Exp",
  nugget = 1e-5,
  range = 2e5)
vgm_mod_sph = vgm(
  model = "Sph",
  nugget = 1e-5,
  range = 2e5)

# Use fit.variogram() to optimize the variogram parameters...
vgm_fit_sph = fit.variogram(
  aqi_vgm_emp, vgm_mod_sph)

vgm_fit_exp = fit.variogram(
  aqi_vgm_emp, vgm_mod_exp)

# and plot them!
par(mfrow = c(2, 1))
plot(vgm_emp, vgm_fit_mat, main = "Antonio's Matérn Variogram (AQI)") 

plot(vgm_emp, vgm_fit_sph, main = "Antonio's Spherical Variogram (AQI)")

preds_exp = variogramLine(
  vgm_fit_exp,
  maxdist = max(aqi_vgm_emp$dist),
  n = 200)

preds_sph = variogramLine(
  vgm_fit_sph,
  maxdist = max(aqi_vgm_emp$dist),
  n = 200)

g_exp = ggplot(vgm_emp, aes(x = dist, y = gamma)) +
  geom_point() +
  geom_line(data = preds_exp) +
  ggtitle("Antonio's awesome exponential variogram (Sorry Mike)", "feat. ggplot2")

g_sph = ggplot(vgm_emp, aes(x = dist, y = gamma)) +
  geom_point() +
  geom_line(data = preds_sph) +
  ggtitle("Antonio's awesome spherical variogram (Sorry Mike)", "feat. ggplot2")

g_exp
g_sph

plot_grid(g_exp, g_sph, nrow = 2)

aqi_krig_exp =  gstat::krige(
  AQI ~ 1,
  locations = ca_ozone,
  newdata = temp_grid_sp,
  model = vgm_fit_exp)

aqi_krig_sph =  gstat::krige(
  AQI ~ 1,
  locations = ca_ozone,
  newdata = temp_grid_sp,
  model = vgm_fit_sph)

# CA county borders:
g_ca = geom_sf(
  data = ca_sf,
  lwd = 0.1, fill = "transparent")

# Fill gradients for the interpolated values and the sample variance

# Modify the name and limits for AQI
g_fill_aqi_pred = scale_fill_gradientn(
  colours = heat.colors(10),
  name = "AQI", limits = c(0, 80))

# Modify the name and limits for AQI
g_fill_aqi_var =   scale_fill_gradientn(
  colours = rainbow(10),
  name = "Sample\nVariance",
  limits = c(0, 170))

# For plotting the raster layers for interpolated values and sample variances:
g_r_pred = geom_raster(mapping = aes(x = x, y = y, fill = var1.pred))
g_r_var = geom_raster(mapping = aes(x = x, y = y, fill = var1.var))

# Ggplot objects
g_k_exp_oz = ggplot(as.data.frame(aqi_krig_exp)) +
  g_r_pred + g_fill_aqi_pred + g_ca +
  ggtitle("Kriged AQI Values", "Exponential Variogram")
g_k_exp_var = ggplot(as.data.frame(aqi_krig_exp)) +
  g_r_var + g_fill_aqi_var + g_ca +
  ggtitle("Sample Variance", "Exponential Variogram")

g_k_sph_oz = ggplot(as.data.frame(aqi_krig_sph)) +
  g_r_pred + g_fill_aqi_pred + g_ca +
  ggtitle("Kriged AQI Values", "Spherical Variogram")
g_k_sph_var = ggplot(as.data.frame(aqi_krig_sph)) +
  g_r_var + g_fill_aqi_var + g_ca +
  ggtitle("Sample Variance", "Spherical Variogram")

cowplot::plot_grid(
  g_k_sph_oz, g_k_sph_var, g_k_exp_oz, g_k_exp_var,
  nrow = 2)


ggplot() +
  geom_sf(data = ca_sf, lwd = 0.1, fill = gray(0.5, 0.5)) +
  geom_sf(data = oz_sf, mapping = aes(colour = AQI), cex = 2) +
  scale_color_gradientn(colours = c("red","yellow","green","lightblue","darkblue"), name = "AQI") +
  theme_minimal() +
  ggtitle("Antonio's Awesome AQI Map: 2017")

#CORRELATION PART ----

require(sf)
require(ggplot2)
data_dir = here(
  "data",
  "Fletcher_Fortin-2018-Supporting_Files",
  "data")
cactus_matrix = read.csv(file.path(data_dir, "cactus_matrix.csv"))
cactus_coords <- cbind(cactus_matrix$x, cactus_matrix$y)

# note the names of the x- and y-coordinate columns
head(cactus_matrix, 3)

cactus_matrix_sf = 
  st_as_sf(
    cactus_matrix, 
    # provide the names of the x- and y-coordinate columns:
    coords = c("x", "y"))

# Note there's no coordinate reference (see the book's comment on this).
# st_as_sf() knew to use the Height column as the data corresponding
# to the coordinates in the x and y columns
head(cactus_matrix_sf)

gg_cactus = ggplot(cactus_matrix_sf) +
  geom_sf(aes(colour = Height), cex = 5) +
  # I used the topo.colors color gradient:
  scale_colour_gradientn(colours = topo.colors(10)) +
  ggtitle("Cactus height matrix")

plot(gg_cactus)

require(spdep)

distmat = as.matrix(dist(cactus_matrix[, 1:2]))
maxdist = (2/3) * max(distmat)

# Spdep
correlog.sp <- data.frame(
  dist=seq(5, maxdist, by=5),
  Morans.i=NA,
  Null.lcl=NA,
  Null.ucl=NA,
  Pvalue=NA)

#inspect (it should be empty)
head(correlog.sp)

for (i in 1:nrow(correlog.sp))
{
  d.start <- correlog.sp[i,"dist"]-5
  d.end <- correlog.sp[i,"dist"]
  
  neigh <- dnearneigh(
    x=cactus_coords,
    d1=d.start,
    d.end,
    longlat=F)
  
  wts <- nb2listw(
    neighbours=neigh,
    style='W',
    zero.policy=T)
  
  mor.i <- moran.mc(
    x=cactus_matrix$Height,
    listw=wts,
    nsim=99,
    alternative="greater",
    zero.policy=T)
  
  #summarize results from spdep
  correlog.sp[i, "dist"] <- (d.end+d.start)/2
  #mean dist
  correlog.sp[i, "Morans.i"] <- mor.i$statistic 
  #observed Moran's I
  correlog.sp[i, "Null.lcl"] <- 
    quantile(
      mor.i$res,
      probs = 0.025,
      na.rm = TRUE)  #lower null envelope
  correlog.sp[i, "Null.ucl"] <- 
    quantile(
      mor.i$res,
      probs = 0.975,
      na.rm = TRUE)  #upper null envelope
  correlog.sp[i, "Pvalue"] <- mor.i$p.value                                                      #p-value for Moran's I at that distance category
}

#plot
plot(
  y=correlog.sp$Morans.i,
  x=correlog.sp$dist,
  xlab="Lag Distance(m)",
  ylab="Moran's I",
  ylim=c(-0.3,0.3))
#ylim provides limit on y-axis between -1 and 1

abline(h=0)                                                              #0 reference
lines(correlog.sp$dist, correlog.sp$Null.lcl,col = "red")                  #add the null lcl to the plot
lines(correlog.sp$dist, correlog.sp$Null.ucl,col = "red")                  #add the null ucl to the plot

ggplot(data.frame(correlog.sp)) +
  geom_smooth(aes(x = dist, y = Morans.i), se = FALSE) +
  geom_point(aes(x = dist, y = Morans.i)) +
  geom_ribbon(aes(
    x = dist,
    ymin = Null.lcl,
    ymax = Null.ucl),
    fill = adjustcolor("steelblue", 0.2)) +
  ggtitle("Spdep correlogram", "cactus vegetation matrix")

fit_1 = lm(ozone ~ AQI, data = ca_ozone)
summary(fit_1)

plot(fit_1, which = 1)

plot(fit_1, which = 2)

ca_ozone$resids = residuals(fit_1)


res_vgm_emp = variogram(resids~1, data=ca_ozone)
plot(res_vgm_emp, pch = 21, cex = 1.2, main = "Antonios varirogram of residuals")

# Parameterize initial spherical and exponential variograms.
# These contain the starting parameters for optimizations.
vgm_mod_exp = vgm(
  model = "Mat",
  nugget = 1e-5,
  range = 2e5)
vgm_mod_sph = vgm(
  model = "Sph",
  nugget = 1e-5,
  range = 2e5)

# Use fit.variogram() to optimize the variogram parameters...
vgm_fit_sph = fit.variogram(
  res_vgm_emp, vgm_mod_sph)

vgm_fit_exp = fit.variogram(
  res_vgm_emp, vgm_mod_exp)

# and plot them!
par(mfrow = c(2, 1))
#Varirogram of Residuals----
plot(res_vgm_emp, vgm_fit_sph, main = "Antonio's Varirogram of Residuals 2")



# Calculate the maximum distance for ozone points in CA
distmat_ca = dist(as.matrix(coordinates(ca_ozone)))

# Since CA is an elongated shape, we'll use 1/2 the max distance
maxdist_ca = 0.5 * max(distmat_ca)

# What's the minimum distance?
# This will be helpful for neighborhood building.
mindist_ca = min(distmat_ca)

# make a sequence of 10 distance classes between the min and max distances:
n_dist_class = 10
ca_nb_dists = seq(mindist_ca, maxdist_ca, length.out = n_dist_class)

# dnearneigh() accepts a sp or sf object as its x argument
ca_nbh_1 = dnearneigh(
  x = ca_ozone,
  #d1 is minimum distance, d2 is max distance
  d1 = ca_nb_dists[1],
  d2 = ca_nb_dists[2],
  longlat=F)

# Make a weights object
wts_ca = nb2listw(
  neighbours=ca_nbh_1,
  #W = row-standardized weights
  style='W',
  zero.policy=T)

#Moran's I test with normal approximation versus Monte Carlo permutation test
#Monte Carlo
mor_mc_ca = moran.mc(
  ca_ozone$resids,
  listw =wts_ca,
  nsim=999,
  zero.policy=T)

#normal approximation
mor_norm_ca = moran.test(
  ca_ozone$resids,
  listw =wts_ca,
  randomisation=F,
  zero.policy=T)

#inspect
mor_mc_ca

mor_norm_ca

#Model Residuals Correogram----

# make a sequence of 10 distance classes between the min and max distances:
n_dist_class = 10
ca_nb_dists = seq(mindist_ca, maxdist_ca, length.out = n_dist_class)

# Create data frames for storing output
ca_correlog_aqi =
  data.frame(
    dist=ca_nb_dists[-n_dist_class],
    Morans.i=NA,
    Null.lcl=NA,
    Null.ucl=NA,
    Pvalue=NA)

# then use a for loop to calculate Moran's I for lag distances
for (i in 1:(length(ca_nb_dists) - 1))
{
  d.start = ca_nb_dists[i]
  d.end = ca_nb_dists[i + 1]
  
  # dnearneigh() accepts a sp or sf object as its x argument
  neigh_i = dnearneigh(x = ca_ozone, d1 = d.start, d2 = d.end)
  
  # Make a weights object
  wts_i = nb2listw(
    neighbours = neigh_i,
    #W = row-standardized weights
    style='W',zero.policy=T)
  
  mor.i_aqi <- moran.mc(ca_ozone$ozone, listw =wts_i,nsim=999, zero.policy=T)
  
  #summarize results from spdep
  ca_correlog_aqi[i, "Morans.i"] = mor.i_aqi$statistic
  ca_correlog_aqi[i, "Null.lcl"] = quantile(mor.i_aqi$res, 0.025, na.rm = TRUE)
  ca_correlog_aqi[i, "Null.ucl"] = quantile(mor.i_aqi$res, probs = 0.975, na.rm = TRUE)
  ca_correlog_aqi[i, "Pvalue"] = mor.i_aqi$p.value
}

ggplot(data.frame(ca_correlog_aqi)) +
  geom_smooth(aes(x = dist, y = Morans.i), se = FALSE) +
  geom_point(aes(x = dist, y = Morans.i)) +
  geom_ribbon(aes(
    x = dist,
    ymin = Null.lcl,
    ymax = Null.ucl),
    fill = adjustcolor("steelblue", 0.2)) +
  ggtitle("Antonio's spdep Correlogram", "Ozone")

