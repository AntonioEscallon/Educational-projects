require("here")
install.packages("RColorBrewer")
require(dplyr); require(RColorBrewer); require(ggplot2)
require(mapdata); require(maptools)
require("maps")
require("usmap")
data <- read.csv(here("iCons", "Buoy - Sheet1.csv"))
df <- data.frame(data)
head(df)
# Load the required libraries
library(maps)
map(database = "NorthAmerica")
plot_usmap()
# marking points on map
points(x = df$Latitdue.[1:10], y = -df$Longitdue.[1:10], col = "Green")
usa <- map_data("usa")
canada <- map_data("worldHires", "Canada")
mexico <- map_data("worldHires", "Mexico")

NAmap <- ggplot() + geom_polygon(data = usa, 
                                 aes(x=long, y = lat, group = group), 
                                 fill = "white", 
                                 color="black") +
  geom_polygon(data = canada, aes(x=long, y = lat, group = group), 
               fill = "white", color="black") + 
  geom_polygon(data = mexico, aes(x=long, y = lat, group = group), 
               fill = "white", color="black") +
  coord_fixed(xlim = c(-75, -65),  ylim = c(35, 50), ratio = 1.2)

NAmap

NAmap <- NAmap + geom_point(data=df, aes(x=-Longitdue., y=Latitdue.),
                            fill="Green", color = "black", 
                            shape=21, size=5.0) +
  geom_point(data=df, aes(x=-Longitdue., y=Latitdue.), 
             fill="Dark Green", color = "black", shape=21, size=5.0) +
  geom_point(data=df, aes(x=-Longitdue., y=Latitdue.), 
             fill="Dark Green", color = "black", shape=21, size=5.0) +
  geom_point(data=df, aes(x=-Longitdue., y=Latitdue.), 
             fill="Dark Green", color = "black", shape=21, size=5.0)
NAmap <- NAmap + ggtitle("Buoy Location")
NAmap <- NAmap +theme(
  plot.title = element_text(color="Green", size=14, face="bold.italic"))
NAmap
