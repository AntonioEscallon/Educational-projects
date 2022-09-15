if (!require("rspatial")) devtools::install_github('rspatial/rspatial')
install.packages("gstat")
require(sp)
require(rspatial)

require(dismo)


d <- sp_data('ca_border')

d$prec <- rowSums(d[, c(6:17)])
plot(
  sort(d$prec), 
  main = "CA annual precipitation",
  ylab = 'Annual precipitation (mm)', xlab = 'Stations',
  las = 1 )

dsp <- SpatialPoints(d[,4:3], proj4string = CRS("+proj=longlat +datum=NAD83"))
dsp <- SpatialPointsDataFrame(dsp, d)
CA <- sp_data("counties")

# define groups for mapping
cuts <- c(0,200,300,500,1000,3000)

# set up a palette of interpolated colors
blues <- colorRampPalette(c('yellow', 'orange', 'blue', 'dark blue'))
pols <- list("sp.polygons", CA, fill = "lightgray")
spplot(dsp, 'prec', cuts = cuts, col.regions = blues(5), sp.layout = pols, pch = 20, cex = 2)

TA <- CRS("+proj=aea +lat_1=34 +lat_2=40.5 +lat_0=0
          +lon_0=-120 +x_0=0 +y_0=-4000000 +datum=NAD83
          +units=m +ellps=GRS80 +towgs84=0,0,0")
require(rgdal)
dta <- spTransform(dsp, TA)
cata <- spTransform(CA, TA)

RMSE <- function(observed, predicted) {
  sqrt(mean((predicted - observed)^2, na.rm = TRUE))
}

v <- voronoi(dta)
plot(v)

require(rgeos)
ca <- aggregate(cata)
vca <- intersect(v, ca)
spplot(vca, 'prec', col.regions = rev(get_col_regions()))

par(mfrow = c(1, 2)); plot(cata, main = "cata"); plot(ca, main = "ca")

r <- raster(cata, res = 10000)
vr <- rasterize(vca, r, 'prec')
plot(vr)

require(gstat)
gs <- gstat(
  formula = prec~1,
  locations = dta, 
  nmax = 5, 
  set = list(idp = 0))
nn <- interpolate(r, gs)
nnmsk <- mask(nn, vr)
plot(nnmsk)
