# Fletcher and Fortin 2018 Chapter 3: Land-cover pattern and change ----
# UPDATED USING LANDSCAPEMETRICS & NLMR PACKAGE

# Packages and Data Directory ----
library(raster)           #for raster covariate data; version 3.5_2 used
library(rasterVis)         #for plotting rasters;  version 0.51.1 used
library(rgdal)             #for raster data, projections; version 1.5-27 used
library(landscapemetrics)  #for most landscape metrics; version 1.5.4 used
library(rgeos)             #for some patch metrics; version 0.5-8 used
library(igraph)            #for some landscape metrics; version 1.2.8 used
library(Voss)              #for neutral landscapes; version 0.1-4 used
library(secr)              #for neutral landscapes; version 4.4.8 used
library(NLMR)              #for neutral landscapes; version 1.1 used
library(reshape2)          #for re-formatting data; version 1.4.4 used

data_dir = here(
  "data",
  "Fletcher_Fortin-2018-Supporting_Files",
  "data")


# 3.3.3 Land-cover at different scales ----

#set working directory where you downloaded the data
# setwd(choose.dir())

#load landscape data
nlcd <- raster(file.path(data_dir, "nlcd2011gv2sr"))

#check projection/crs
proj4string(nlcd)

#grain and extent
res(nlcd)
extent(nlcd)

#nlcd categories
levels(nlcd)
unique(nlcd)

#------------------------------------------#
## land-cover type (nlcd original categories) ----
#1 = forest:41-43
#2 = developed:21-24
#3 = agriculture:81,82
#4 = herbaceous:71-74
#5 = open:51-52
#6 = wetland:90,95
#7 = water:11-12
#------------------------------------------#

#convert land-cover integers to factor levels (categories)
nlcd <- as.factor(nlcd)

#add names of categories to raster layer
land_cover <- levels(nlcd)[[1]]
land_cover[,"landcover"] <- c("forest","developed", "ag","grass","open","wetland")
levels(nlcd) <- land_cover

#plot
land_col <- c("green","orange","yellow","brown","white","blue")
plot(nlcd, legend = T, col = land_col)

#plot with rasterVis
levelplot(nlcd, col.regions=land_col, xlab="", ylab="")

#create a reclassification matrix
nlcd.cat <- unique(nlcd)
nlcd.cat.for <- c(1,0,0,0,0,0)                #if we want binary landscape (forest and non-forest)
nlcd.cat.for.only <- c(1,NA,NA,NA,NA,NA)      #if we only want to interpret forest

reclass.mat <- cbind(nlcd.cat, nlcd.cat.for)
reclass.mat                                   #first col: orginal; second: change to

#forest binary layer from reclassification matrix
nlcd.forest <- reclassify(nlcd, reclass.mat)
plot(nlcd.forest)

# 3.3.3.1 patch-level quantification ----

#4-neighbor rule
forest.patchID4 <- clump(nlcd.forest, directions = 4)  #patch delineation with raster package
cellStats(forest.patchID4, max)                        #number of patches identified
plot(forest.patchID4)

#8-neighbor rule
forest.patchID8 <- clump(nlcd.forest, directions = 8) #patch delineation with raster package
cellStats(forest.patchID8, max)                       #number of patches identified
plot(forest.patchID8)

#-----------------------------------------------#
## Patch-level metrics with landscapemetrics ----
#-----------------------------------------------#

#check landscape 
check_landscape(nlcd.forest)

#check options: 12 options
list_lsm(level = "patch")

#Note: below both forest/non-forest patches will be summarized
#if you want only output of forest, can either subset output based on 'class' column or pass raster where 0 (non-forest) is converted to NA
#However, if NA instead of 0, some care should be taken as some metrics may be inappropriately calculated

#a single metric of patch area: 4-neighbor rule:
lsm_p_area(nlcd.forest, 
           directions = 4)

#a single metric of patch area: 8-neighbor rule
lsm_p_area(nlcd.forest, 
           directions = 8)


#bind multiple metrics
for.pstat_area_core <- calculate_lsm(nlcd.forest, 
                           directions = 8,
                           what = c("lsm_p_area", "lsm_p_core"))

#inspect: tibble in long format
head(for.pstat_area_core)
unique(for.pstat_area_core$metric)

#all patch metrics: both forest/non-forest patches summarized
for.pstat <- calculate_lsm(nlcd.forest, 
                           directions = 8,
                           level = c("patch"))

#inspect: tibble in long format
head(for.pstat)
unique(for.pstat$metric)

#subset the forest summary (remove non-forest)
for.pstat <- for.pstat[for.pstat$class==1,]

#convert from long to wide format with reshape2 package
for.pstat.wide <- dcast(for.pstat, id ~ metric, value.var = "value")
head(for.pstat.wide)

#number of patches
nrow(for.pstat.wide)

#mean patch metrics
for.pstat.mean <- colMeans(for.pstat.wide[,2:ncol(for.pstat.wide)])
round(for.pstat.mean, 2)

#SD of patch metrics with apply function
for.pstat.sd <- apply(for.pstat.wide[,2:ncol(for.pstat.wide)], 2, sd)
round(for.pstat.sd, 2)

#correlation matrix
round(cor(for.pstat.wide[,2:ncol(for.pstat.wide)]),2)

#plot
pairs(for.pstat.wide[,2:ncol(for.pstat.wide)])                    #all, but hard to see
pairs(for.pstat.wide[,c("area","core","cai", "ncore", "contig")]) #area/core area
pairs(for.pstat.wide[,c("shape","contig", "para", "frac")])       #shape/edge

# 3.3.3.2 Class-level quantification ----

#check class-level metric possibilities: 55 options!
list_lsm(level = "class")

#calculation based on forest layer
#if we use forest layer with NAs, then some metrics will not be calculated appropriately
for.cstat <- calculate_lsm(nlcd, 
                           directions = 8,
                           level = c("class"))

#check against patch-level calculations:

#mean patch size
for.cstat[for.cstat$class==1 & for.cstat$metric== "area_mn", "value"]
for.pstat.mean["area"]#mean patch size

#standard deviation of patch shape
for.cstat[for.cstat$class==1 & for.cstat$metric== "shape_sd", "value"]
for.pstat.sd["shape"]

#make wide format
for.cstat.wide <- dcast(for.cstat, class ~ metric, value.var = "value")
head(for.cstat.wide, 2)

#correlation matrix
cor(for.cstat.wide[,c("area_mn", "cai_mn", "core_mn")])#subset of area/core area metrics

#plot subset of metrics
pairs(for.cstat.wide[,c("area_mn", "cai_mn", "core_mn")])

#-----------------------------#
## distance-related metrics ----
#-----------------------------#

#create polygon layer using patchIDs calculated above
forest.poly <- rasterToPolygons(forest.patchID8, dissolve = T)

#plot
plot(forest.poly)

#----------------------------------#
## core area and edge distances ----
#----------------------------------#

#manual calculation of core area
core.poly <- gBuffer(forest.poly, width = -100, byid = T)
core.area <- gArea(core.poly, byid = T)

#plot
plot(forest.poly, col = "grey30")
plot(core.poly, col = "grey80", add = T)

#map distance to edge with raster package
nlcd.forestNA <- nlcd.forest
nlcd.forestNA[nlcd.forestNA == 1] <- NA
forest.dist <- raster::distance(nlcd.forestNA)

#plot distance to forest edge
plot(forest.dist)

#centroids of polygons
forest.centroid <- gCentroid(forest.poly, byid = T)

#plot centroids
plot(forest.poly, col = "grey80")
plot(forest.centroid, add = T)

#edge-edge distance matrix using rgeos package
edge.dist <- gDistance(forest.poly, byid = T)

#centroid-centroid distance matrix
cent.dist <- gDistance(forest.centroid, byid = T)

#patch-level nearest-neighbor distance
diag(cent.dist) <- NA
diag(edge.dist) <- NA

nnd.cent <- apply(cent.dist, 1, min, na.rm = T)
nnd.edge <- apply(edge.dist, 1, min, na.rm = T)

plot(nnd.cent, nnd.edge)
cor(nnd.cent, nnd.edge)

#compare with enn from landscape metrics
cor(nnd.edge, for.pstat.wide$enn)

#Why so different? landscapemetrics labels patches in different orders:
lm_patches <- get_patches(nlcd.forest, 
                          class = 1, 
                          directions = 8)

plot(lm_patches$layer_1$class_1)
plot(lm_patches[[1]])
plot(forest.patchID8)

#--------------------#
## proximity index ----
#--------------------#

#patch area
patch.area <- data.frame(id = for.pstat.wide$id, area = for.pstat.wide$area)

#neighborhood for proximity index to be calculated
#NOTE: using 4-neighbor rule results in some 0 distances, which requires a correction in formula

h <- edge.dist
h2 <- 1/h^2
h2[edge.dist > 1000] <- 0
diag(h2) <- 0

#proximity index
patch.prox <- rowSums(sweep(h2, 2, patch.area$area, "*"))

#correlation of metrics
cor(cbind(patch.prox, area=patch.area$area, nnd.cent, nnd.edge))

# 3.3.3.3 landscape-level quantification ----

#check landscape-level metric possibilities
list_lsm(level = "landscape") #65 options!

#calculate a subset of landscape metrics
for.lstat <- calculate_lsm(nlcd, 
                           directions = 8,
                           level = c("landscape"))

#compare with some summary metrics derived from class-level metrics
land.NP <- sum(for.cstat.wide$np)                            #number of patches
land.PD <- sum(for.cstat.wide$pd)                            #patch density
land.LPI <- max(for.cstat.wide$lpi)                          #largest patch index
land.TE <- sum(for.cstat.wide$te)/2                          #total edge
land.ED <- sum(for.cstat.wide$ed)/2                          #edge density
land.AI <- sum(for.cstat.wide$pland/100 * for.cstat.wide$ai) #aggregation index

#check
land.AI
for.lstat[for.lstat$metric == "ai",]

#-----------------------------------#
## some diversity-related metrics ----
#-----------------------------------#

#richness
richness <- length(unique(values(nlcd)))
richness

#a function richness
richness <- function(x) length(unique(na.omit(x)))

#diversity,D, and evenness, E
table(values(nlcd))

C <- table(values(nlcd))
P <- C / sum(C)
D <- -sum(P * log(P))
E <- D/log(length(C))

#----------------------------------#
## contagion ----
#----------------------------------#

#from raster; identifies adjacent cells
adj <- adjacent(nlcd, 1:ncell(nlcd), directions=4, pairs=T, include=T)
head(adj, 2)

#contigency table of pairwise adjacencies; should include ii
N <- table(nlcd[adj[,1]], nlcd[adj[,2]])
N

#contagion and related metrics come from this table
subset(for.lstat, metric =="contag") #contagion
subset(for.lstat, metric =="pladj")  #proportion of like adjacencies

# ----------------------------------#
# 3.3.3.4 Moving window analysis ----
# ----------------------------------#

#focal buffer matrix for moving windows
buffer.radius <- 100
fw.100m <- focalWeight(nlcd, buffer.radius, 'circle')#buffer in CRS units
round(fw.100m, 3)

#re-scale weight matrix to 0,1
fw.100m <- ifelse(fw.100m > 0, 1, 0)
fw.100m

#weight matrix for a Gaussian kernel
round(focalWeight(nlcd, c(50,100), type = "Gaus"), 2)

#forest cover moving window; number of cells
forest.100m <- focal(nlcd.forest, w=fw.100m, fun="sum", na.rm=T)

#proportion of forest
forest.prop.100m <-forest.100m/sum(fw.100m,na.rm=T)#proportion: divide by buffer size
plot(forest.prop.100m)

#richness moving window (took 0.61s on my laptop)
rich.100m <- focal(nlcd, fw.100m, fun=richness)
plot(rich.100m)

#diversity moving window function
diversity <- function(landcover, radius) {

  n <- length(unique(landcover))

  #Create focal weights matrix
  fw.i <- focalWeight(landcover, radius, type="circle")

  #Compute focal means of indicators
  D <- landcover
  values(D) <- 0
  log.i <- function(x) ifelse(x==0, 0, x*log(x))#log(p)*p

  #for each landcover, create a moving window map and make calculations
  for (i in 1:length(n)) {
    focal.i <- focal(landcover == i, fw.i)
    D <- D + calc(focal.i, log.i)#take log(p)*p
  }

  D <- calc(D, fun=function(x){x * -1})#take negative
  return(D)
}

#calculate diversity moving window
diversity.100m <- diversity(landcover = nlcd, radius = 100)
plot(diversity.100m)

cor(values(diversity.100m), values(rich.100m), use="complete.obs")

#-----------------------------------------#
## moving window with landscapemetrics ----
#-----------------------------------------#

#calculate richness (currently only landscape-level metrics allowed)
lm_richness100m <- window_lsm(nlcd, 
                           window = fw.100m, 
                           what = c("lsm_l_pr"))

#compare
plot(lm_richness100m[[1]]$lsm_l_pr)
plot(rich.100m)

#-----------------------------#
# 3.3.4 Neutral Landscapes ----
#-----------------------------#

#neutral landscape dimensions
dimX <- 128
dimY <- 128

#-------------------------------#
## Simple random landscapes ----
#-------------------------------#

#simple random with 10% habitat
sr.30 <- raster(ncol=dimX, nrow=dimY, xmn=0, xmx=dimX, ymn=0, ymx=dimY)
sr.30[] <- rbinom(ncell(sr.30), prob=0.3, size=1)#random values from a bernoulli distribution
plot(sr.30)

#simple random with 30% habitat
sr.10 <- raster(ncol=dimX, nrow=dimY, xmn=0, xmx=dimX, ymn=0, ymx=dimY)
sr.10[] <- rbinom(ncell(sr.30), prob=0.1, size=1)#random values from a bernoulli distribution
plot(sr.10)

#------------------------------------#
## Fractal landscapes ----
#------------------------------------#

voss <- voss2d(g = 7, H = 0.7)#g sets dimensions; g=4: 16x16; g=7: 128 x 128
str(voss)

voss1.thres <- quantile(voss$z, prob=0.1)
voss3.thres <- quantile(voss$z, prob=0.3)

voss$z1 <- ifelse(voss$z<voss1.thres, 1, 0)
voss$z3 <- ifelse(voss$z<voss3.thres, 1, 0)

image(voss$x, voss$y, voss$z1, xlab="x", ylab="y",main="parameter H=0.7")#white is habitat
image(voss$x, voss$y, voss$z3, xlab="x", ylab="y",main="parameter H=0.7")#white is habitat

#plot with raster
voss.raster <- raster(as.matrix(voss$z))
plot(voss.raster,axes=F, box=F, legend=F)

voss3.raster <- raster(as.matrix(voss$z3))
plot(voss3.raster,axes=F, box=F, legend=F)

voss1.raster <- raster(as.matrix(voss$z1))
plot(voss1.raster,axes=F, box=F, legend=F)

#------------------------------------#
## Modified random clusters ----
#------------------------------------#

tempmask <- make.mask(nx = dimX, ny = dimX, spacing = 1)

p55A3 <- randomHabitat(tempmask, p = 0.55, A = 0.3)
p55A1 <- randomHabitat(tempmask, p = 0.55, A = 0.1)

str(p55A3)
plot(p55A3, dots = FALSE, col = "green")
plot(p55A1, dots = FALSE, col = "green")

#-----------------------------------#
# Alternative with NLMR package ----
#-----------------------------------#

#random landscape: draws uniform distribution between 0-1
nlm_uniform <- nlm_random(ncol = 128, nrow = 128)

#inspect
class(nlm_uniform)
dim(nlm_uniform)
plot(nlm_uniform)

#threshold to 10% habitat
nlm_uniform_0.1 <- nlm_uniform
values(nlm_uniform_0.1) <- 0
nlm_uniform_0.1[nlm_uniform < 0.1] <- 1  

#plot
plot(nlm_uniform_0.1)

#fractal: midpoint displacement: H = 0.7
nlm_H0.7 <- nlm_mpd(ncol = 128, nrow = 128,
                    roughness = 0.7)

#inspect
nlm_H0.7
dim(nlm_H0.7)

#plot
plot(nlm_H0.7)

#threshold to 10% habitat
nlm_H0.7.thres <- quantile(values(nlm_H0.7), prob=0.1)
nlm_H0.7_0.1 <- nlm_H0.7
values(nlm_H0.7_0.1) <- 0
nlm_H0.7_0.1[nlm_H0.7 < nlm_H0.7.thres] <- 1  

#plot
plot(nlm_H0.7_0.1)

#random cluster for p = 0.55, A = 0.3
p55A3_nlm <- nlm_randomcluster(ncol = 128, nrow = 128,
                  p = 0.55,
                  ai = c(0.7, 0.3))

#inspect and plot
dim(p55A3_nlm)
plot(p55A3_nlm)

#with 3 types
p55A3_3_nlm <- nlm_randomcluster(ncol = 128, nrow = 128,
                               p = 0.55,
                               ai = c(0.2, 0.5, 0.3))

#plot
plot(p55A3_3_nlm)
