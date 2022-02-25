require(here)
require(raster)
install.packages("landscapemetrics")
require(rasterVis)
require(igraph)
require(landscapemetrics)

data_dir = here(
  "data",
  "Fletcher_Fortin-2018-Supporting_Files",
  "data")

nlcd = raster(file.path(
  data_dir, "nlcd2011gv2sr"
))

#Creating a plot with levelplot----
nlcd <- as.factor(nlcd)

land_cover <- levels(nlcd)[[1]]
land_cover[,"landcover"] <- c("forest","developed", "ag","grass","open","wetland")
levels(nlcd) <- land_cover

land_col <- c("green","orange","yellow","brown","white","blue")
plot(nlcd, legend = T, col = land_col)

levelplot(nlcd, col.regions=land_col, xlab="", ylab="")

#Creating a forest Mask----
nlcd.cat <- unique(nlcd)
nlcd.cat.for <- c(1,0,0,0,0,0)                #if we want binary landscape (forest and non-forest)
nlcd.cat.for.only <- c(1,NA,NA,NA,NA,NA)      #if we only want to interpret forest

reclass.mat <- cbind(nlcd.cat, nlcd.cat.for)
reclass.mat                                   

#forest binary layer from reclassification matrix
nlcd.forest <- reclassify(nlcd, reclass.mat)
plot(nlcd.forest)

#Patch characteristics 4-neighbor and 8-neighbor rule----
forest.patchID4 <- clump(nlcd.forest, directions = 4)  
cellStats(forest.patchID4, max)                        
plot(forest.patchID4)

forest.patchID8 <- clump(nlcd.forest, directions = 8) #patch delineation with raster package
cellStats(forest.patchID8, max)                       #number of patches identified
plot(forest.patchID8)

#Let's try out the patch area stats using the 4- and 8-neighbor rules:
patches_area_4 = lsm_p_area(nlcd.forest, directions = 4)
patches_area_8 = lsm_p_area(nlcd.forest, directions = 8)

#You can plot histograms, noting that the area is held in the value column using log:
par(mfrow = c(1, 2))
hist(
  log(patches_area_8$value),
  main = "8-neighbor rule", xlab = "Patch Area")
hist(
  log(patches_area_4$value),
  main = "4-neighbor rule", xlab = "Patch Area")

#Placing our new data into a raster
carver = raster(here(
  "data", "carver_bogs",
  "NLCD_2001_Land_Cover_L48_20210604_twhHnv7eGwpL3DLaGf2I.tiff"))

tomah = raster(here(
  "data", "tomah_bogs",
  "NLCD_2001_Land_Cover_L48_20210604_X6xxWhgNuPvZI4ZjRai9.tiff"))

carver_f = as.factor(carver)
tomah_f = as.factor(tomah)

plot(tomah)

carver_levels = read.csv(
  here(
    "data", "carver_bogs", 
    "NLCD_landcover_legend_2018_12_17_twhHnv7eGwpL3DLaGf2I.csv"),
  na.strings = "")
head(carver_levels)

tomah_levels = read.csv(
  here(
    "data", "tomah_bogs", 
    "NLCD_landcover_legend_2018_12_17_X6xxWhgNuPvZI4ZjRai9.csv"),
  na.strings = "")
head(tomah_levels)

complete.cases(carver_levels)
complete.cases(tomah_levels)

carver_lvl_rows = 
  which(complete.cases(carver_levels))

tomah_lvl_rows = 
  which(complete.cases(tomah_levels))

colnames(carver_levels)[2] <- "Landcover"
colnames(tomah_levels)[2] <- "Landcover"
colnames(carver_levels)[1] <- "ID"
colnames(tomah_levels)[1] <- "ID"

levels(carver_f) = carver_levels[carver_lvl_rows, ]
levels(tomah_f) = tomah_levels[tomah_lvl_rows, ]

levels(carver_f)
levels(tomah_f)

col_tomah = colortable(tomah_f)[tomah_lvl_rows]
col_carver = colortable(carver_f)[carver_lvl_rows]

levels(tomah_f) = tomah_levels[tomah_lvl_rows, ]

levelplot(
  tomah_f,
  col.regions = col_tomah,
  main = "Landcover Classes in Tomah, WI",
  scales = list(draw = F))

levelplot(
  carver_f,
  col.regions = col_carver,
  main = "Landcover Classes in Carver, MA",
  scales = list(draw = F))
levels(carver_f)[[1]]
levels(tomah_f)[[1]]

#We can use the reclassify function to create our binary raster
#we just need a reclassification raster first.

reclass_cultivated_c = cbind(
  levels(carver_f)[[1]][, 1],
  levels(carver_f)[[1]][, 2] == "Cultivated Crops")

reclass_cultivated_t = cbind(
  levels(tomah_f)[[1]][, 1],
  levels(tomah_f)[[1]][, 2] == "Cultivated Crops")

tomah_reclass_f = as.factor(reclassify(tomah_f, reclass_cultivated_t))
carver_reclass_f = as.factor(reclassify(carver_f, reclass_cultivated_c))

levels(carver_reclass_f)[[1]]$Cover = c("Other", "Cultivated")
levels(tomah_reclass_f)[[1]]$Cover = c("Other", "Cultivated")

levelplot(
  tomah_reclass_f,
  main = "Antonio's plot of Tomah, WI",
  col.regions = c("white", "forestgreen"),
  # This suppresses the axes:
  scales = list(draw = F))

levelplot(
  carver_reclass_f,
  main = "Antonio's plot of Carver, MA",
  col.regions = c("white", "forestgreen"),
  # This suppresses the axes:
  scales = list(draw = F))

list_lsm(level = "patch")


tomah_ncore = lsm_p_ncore(tomah_reclass_f)
carver_ncore = lsm_p_ncore(carver_reclass_f)

tomah_area = lsm_p_area(tomah_reclass_f)
carver_area = lsm_p_area(carver_reclass_f)
lsm_p_area(tomah_reclass_f)


hist(
  log(tomah_area$value),
  main = "Tomah Area", xlab = "Value")

hist(
  log(carver_area$value),
  main = "Carver Area", xlab = "Value")

hist(
  log(tomah_ncore$value),
  main = "Tomah NCore", xlab = "Value")

hist(
  log(carver_ncore$value),
  main = "Carver NCore", xlab = "Value")
#Both areas look somewhat similar, with Carver having a clear peak on the lower side of area,
#and somewhat of a similar amount of patches in the same area. In Tomah, we see a more varied
#amount of areas, with two values being very close to each other when cosnidering the max value
#In addition to this, both of the second largest areas end at 6. Interestingly enough, Carver has
#a larger area patch than Tomah, even though in total it has smaller patches

#As for the core areas, it is puzzling to see that they look so similar, especially when the Tomah
#area has a larger total area and the breakdown of its patches look like perfect squares. This similarity
#could be because there are many small patches in Tomah that make the data look more similar to Carver, and
#Carver seems to have a lot of large patches with a large core area. 
