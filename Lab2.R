require(raster)
require(here)
#Q1:A plot of the original 6 by 6 raster. ----
#Plots of resampled rasters of various dimensions. 
#You should include as many figures as you need to help 
#illustrate your answer to the next questions.

#Q2: Explain your intuitive understanding of what happens when ----
#you resample raster data to dimensions that are not whole 
#number multiples of the original.
#Specifically address what happens when you make rasters with 
#coarser and finer grains from the original. You should reference 
#the figures you included in the first question.

#Q3: Explain what happened when you tried to recover your ----
#original 6 by 6 raster. Make sure you explain why your end product does 
#or does not look like your starting raster. Include at least one figure 
#to illustrate your answer.

#Q4: Propose one or more strategies to minimize distortions.

#Q5: Identify at least one good reason for using simulated data when you’re 
#learning new concepts or techniques.

dat_dir = here("data", "Fletcher_Fortin-2018-Supporting_Files", "data")
nlcd = raster(file.path(dat_dir, "nlcd2011SE.nc"))

#Creating the first template raster
raster_temp <- raster(ncol=6, nrow=6, xmn=1, xmx=6, ymn=1, ymx=6)
raster_temp[] <- rpois(ncell(raster_temp), lambda=3)
plot(raster_temp, axes=F, box=F)

#Creating a second template raster
rast_6 <- raster(ncol=6, nrow=6, xmn=1, xmx=6, ymn=1, ymx=6)
rast_6[] <- rpois(ncell(raster_temp), lambda=10)
plot(rast_6, axes=F, box=F)
text(toy2, digits=2)
dev.copy2pdf(file="raster_6.pdf", width = 7, height = 5)

#Creating a second template raster
rast_7 <- raster(ncol=7, nrow=7, xmn = 1, xmx = 6, ymn = 1, ymx = 6)
rast_7[] <- rpois(ncell(raster_temp), lambda=10)
plot(rast_7, axes=F, box=F)


temp1 = resample(rast_6, rast_7)
plot(temp1, axes=F, box= F)
dev.copy2pdf(file="raster_7.pdf", width = 7, height = 5)
temp11 = rast_templ(11,11)
temp2 = resample(rast_6, temp11)
plot(temp2, axes = F, box = F)
dev.copy2pdf(file="raster_11.pdf", width = 7, height = 5)
plot(rast_6)
plot(rast_7)
temp5 = rast_templ(5,5)
temp3 = resample(rast_6, temp5)
plot(temp3, axes = F, box = F)
dev.copy2pdf(file="raster_5.pdf", width = 7, height = 5)

temp60 = resample(temp3, rast_6)
plot(temp60, axes = F, box = F)
dev.copy2pdf(file="raster_Rec.pdf", width = 7, height = 5)

temp61 = resample(temp2, rast_6)
plot(temp61, axes = F, box = F)
dev.copy2pdf(file="raster_Rec2.pdf", width = 7, height = 5)

#Building a template raster
rast_templ = function(nrows, ncols, xmn = 1, xmx = 6, ymn = 1, ymx = 6)
{
  return(raster(
    ncol = ncols, nrow = nrows, 
    xmx = xmx, xmn = xmn, 
    ymx = ymx, ymn = ymn))
}

template1= rast_templ(5, 5)
template1[] <- rpois(ncell(template1), lambda=10)
template2 = resample(template1, rast_7)
plot(template2)

dat_dir = here("data", "Fletcher_Fortin-2018-Supporting_Files", "data")
nlcd = raster(file.path("data", "nlcd2011SE.nc"))

require(rgdal)
# site and reptile data
sites = readOGR(file.path(dat_dir, "reptiledata"))
#inspect
class(sites)
proj4string(sites)
proj4string(sites) <- nlcd_proj #set projection
summary(sites)
head(sites, 2)

#plot with custom color scheme
my_col <- c("black","blue","darkorange","red","darkred","grey30","grey50", "lightgreen",
            "green", "darkgreen", "yellow", "goldenrod", "purple", "orchid","lightblue", "lightcyan")
states = rgdal::readOGR(dsn = here("data", "tl_2018_us_state"))
southernStates = subset(states, STUSPS %in% c("AL", "FL", "GA", "AR", "KN", "SC", "LA", "TN", "MS", "NC", "VA", "WV"))
plot(southernStates, add = TRUE)
#plot
plot(nlcd, col=my_col, axes=F, box=F)
plot(sites, add=T)

states2 = raster(states)
plot(states)

states = spTransform(readOGR(here("data", "tl_2018_us_state")), proj4string(nlcd))
southernStates = subset(states, STUSPS %in% c("AL", "FL", "GA", "AR", "KN", "SC", "LA", "TN", "MS", "NC", "VA", "WV"))

plot(southernStates)
plot(nlcd, add = TRUE)
nlcd_states = spTransform(
  raster(file.path(dat_dir, "nlcd2011SE.nc")),
  proj4string(states2))

Object2reprojected <- spTransform(states,crs(nlcd))
dev.copy2pdf(file="graph_forest_density.pdf", width = 7, height = 5)
new_nlcd = extent(nlcd)
extent(c(0, 7, 0, 7))
my_col = adjustcolor(c("red", "orange", "#004040a0"), alpha.f = 0.25)
par(bg=my_col)
plot(new_nlcd, add = TRUE,  col="black")

dev.copy2pdf(file="forestMap.pdf", width = 7, height = 5)

##  alpha = 1/2 * previous alpha --> opaque colors
x <- palette(adjustcolor(palette(), 0.5))

matplot(new_nlcd, type = "b", pch = 21:23, col = 2:5, bg = 2:5,
        main = "Using an 'opaque ('translucent') color palette")

#create a binary forest layer using nlcd as template
forest <- nlcd
values(forest) <- 0 #set to zero

#reclassify:
#with raster algebra; this is slow

forest[nlcd==41 | nlcd==42 | nlcd==43] <- 1  #locations with evergreen + mixed forest + deciduous forest

#reclassify with reclassify function is faster
reclass <- c(rep(0,7), rep(1,3), rep(0,6))
nlcd.levels <- levels(nlcd)[[1]]

#create reclassify matrix: first col: orginal; second: change to
reclass.mat <- cbind(levels(nlcd)[[1]], reclass)
reclass.mat

#reclassify
forest <- reclassify(nlcd, reclass.mat)

#plot
plot(forest)
plot(sites, pch=21, col="white", add=T)

grainarea <- res(forest)[[1]]^2/10000#in ha
bufferarea <- (3.14159*buf1km^2)/10000#pi*r^2
forestcover1km <- cellStats(buffer.forest1.1km, 'sum')*grainarea
percentforest1km <- forestcover1km/bufferarea*100

plot(new_nlcd, add = TRUE, col="")

sites = rast_templ(8,8)
sites[] <- rpois(ncell(sites), lambda=10)
              
empty_vec = rep(NA, length = nrow(sites))


cover_data = data.frame(
  f100m = empty_vec,
  f500m = empty_vec,
  f1000m = empty_vec,
  f1500m = empty_vec,
  f2000m = empty_vec,
  f2500m = empty_vec,
  f3000m = empty_vec,
  f3500m = empty_vec
)



BufferCover <- function(coords, size, landcover, grain){
  
  bufferarea.i <- pi*size^2/10000                             #ha; size must be in m
  coords.i <- SpatialPoints(cbind(coords[i, 1],coords[i, 2])) #create spatial points from coordinates
  buffer.i <- gBuffer(coords.i, width=size)                   #buffer from rgeos
  crop.i <- crop(landcover, buffer.i)                         #crop with raster function
  crop.NA <- setValues(crop.i, NA)                            #empty raster for the rasterization
  buffer.r <- rasterize(buffer.i, crop.NA)                    #rasterize buffer
  land.buffer <- mask(x=crop.i, mask=buffer.r)                #mask by putting NA outside the boundary
  coveramount<-cellStats(land.buffer, 'sum')*grain            #calculate area
  percentcover<-100*(coveramount/bufferarea.i)                #convert to %
  
  return(percentcover)
}

f1km <- rep(NA, length = nrow(sites))
f2km <- rep(NA, length = nrow(sites))

#with for loop (all five buffers: 910s; <=3km: 228s)
for(i in 1:nrow(sites)) {
  f1km[i] <- BufferCover(coords=sites,size=1000,landcover=forest,grain=grainarea)
  f2km[i] <- BufferCover(coords=sites,size=2000,landcover=forest,grain=grainarea)
  print(i)
}

#make a data frame
forest.scale <- data.frame(site=sites$site,
                           x=sites$coords_x1, y=sites$coords_x2,
                           f1km=f1km, f2km=f2km)

#plot
plot(f1km, f2km)
