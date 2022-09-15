library(tidyverse) # r-package ecosystem
library(MASS) # statistical functions
library(knitr) # fancy tables
library(clifro) # windrose plot
library(scales) # percentages
library(elevatr) # elevation data
library(raster) # geospatial
library(leaflet) # mapping
require("here")
require(ggvis)
require(grid)
require(ggplot2)
library(hrbrthemes)
library(dplyr)
library(tidyr)
library(viridis)

df_list <-list.files("iCons/data/chosen_stations", pattern=NULL, all.files=FALSE, full.names=FALSE)
print(df_list)
val = df_list[11]
val2 = df_list[4]
val3 = df_list[6]
print(val)

df2[df1, on = c('id','dates')]

df <- read.delim(here("iCons", "data", "station_2951449pwr.csv"), sep='\t')
df2 <- read.delim(here("iCons", "data", "chosen_stations", val), sep='\t')
df3 <- read.delim(here("iCons", "data", "chosen_stations", val2), sep='\t')
df4 <- read.delim(here("iCons", "data", "chosen_stations", val3), sep='\t')

head(df2)
head(df)
val2 = ""
val2 = substr(val, 0, 13)

pwr <- c(df2$PWR)
pwr2 <- c(df$PWR)



setkey( df2, df2$Date )
setkey( df3, df3$Date )
combined <- df[ old, roll = "nearest" ]
#df7 = merge(x = df2, y = df3, by = NULL)
#head(df7)

#ggvis(df, props(x = ~Date, y = ~new_wspd)) + layer_line()
#matplot(x = df$Date, y = df$new_wspd,type = "l" )
#a <-ggplot(df,aes(Date,new_wspd, group = 1))+geom_line()+theme_minimal()
#grid.draw(ggplotGrob(a))
#dev.copy2pdf(file=val + "_wind.pdf", width = 7, height = 5)
df = df[!(df$WDIR >360), ]
p.wr2 = windrose(speed = df3$new_wspd,
         direction = df3$WDIR,
         n_directions = 12,
         speed_cuts = seq(0,20,4),
         ggtheme='minimal',
         col_pal = 'YlGn')
p.wr2
dev.copy2pdf(file=paste0(val2,"_windRose.pdf" ), width = 7, height = 5)
#df[df$new_wspd<0,]
#any(is.na(df))
df = df[!(is.na(df$new_wspd) | df$new_wspd=="" | df$new_wspd < 0), ]
head(df)
#weibull_fit<-fitdistr(df$new_wspd,'weibull')
#x<-seq(0,20,.01)
#weibull_density<-tibble(x,y=dweibull(x = x,shape = weibull_fit$estimate[1],scale = weibull_fit$estimate[2]))

#ggplot(df,aes(new_wspd))+
  #geom_histogram(aes(y=..density..),bins=30,color='white')+
  #geom_line(data=weibull_density,aes(x=x,y=y),color='red')+
  #theme_minimal()

ggplot(df,aes(PWR))+
  geom_density(fill='blue')+
  theme_minimal() + ylim(0, 0.001)
+lines(density(df2$PWR))


lines(density(df2$PWR))
plot(density(df$PWR))
dev.copy2pdf(file=paste0(val2,"_pwrDensity.pdf" ), width = 7, height = 5)
#monthly<-df %>%
#  group_by(Month) %>%
#  summarise(hours=n()/12,
#            windspeedat100mms=mean(windspeedat100mms),
#            mwh=sum(kw,na.rm=T)/(1000*12)) %>%
#  mutate(ncf=percent(mwh/(hours*1.5)))
#kable(monthly,digits=1,caption='monthly totals',align='c')
head(diamonds)

ggplot(data=df, aes(x= new_wspd, group=PWR, fill=PWR)) +
  geom_density(adjust=1.5, position="fill") +
  theme_ipsum()

ggplot(data=df3, aes(x= new_wspd, group=PWR, fill=PWR)) +
  geom_density(adjust=1.5, position="fill") +
  theme_ipsum()

dat <- data.frame(dens = c(rnorm(4000), rnorm(4000, 10, 5))
                  , lines = rep(c(df2$PWR_x, df2$PWR_y)))
library(reshape2)
data = melt(df2)
head(data)

data = data[(!data$variable== "X"), ]
head(data)
m = ggplot(data,aes(x=value, fill=variable)) +   geom_density(adjust=1.25, alpha=.25) +
  theme_ipsum() + ggtitle("Power Density: In-land vs Off-Shore") + xlab("Power Output (kW)") +  ylab("Density")
ggplot(data=df2, aes(x=, fill=c(In.Land, Off.Shore))) +
  geom_density(adjust=1.5, alpha=.4) +
  theme_ipsum()
m + scale_fill_manual( values = c("green","darkgreen"))

p <- ggplot(data=data, aes(x=value, group=variable, fill=variable)) +
  geom_density(adjust=1.5, alpha=.4, position="fill") +
  theme_ipsum()  + ggtitle("Power Density Breakdown: In-land vs Off-Shore") + xlab("Power Output (kW)") +  ylab("Density")
p+ scale_fill_manual( values = c("green","darkgreen"))


# WindRose.R
require(ggplot2)
require(RColorBrewer)

plot.windrose <- function(data,
                          spd,
                          dir,
                          spdres = 2,
                          dirres = 30,
                          spdmin = 2,
                          spdmax = 30,
                          spdseq = NULL,
                          palette = "YlGnBu",
                          countmax = NA,
                          debug = 0){
  
  
  # Look to see what data was passed in to the function
  if (is.numeric(spd) & is.numeric(dir)){
    # assume that we've been given vectors of the speed and direction vectors
    data <- data.frame(spd = spd,
                       dir = dir)
    spd = "spd"
    dir = "dir"
  } else if (exists("data")){
    # Assume that we've been given a data frame, and the name of the speed 
    # and direction columns. This is the format we want for later use.    
  }  
  
  # Tidy up input data ----
  n.in <- NROW(data)
  dnu <- (is.na(data[[spd]]) | is.na(data[[dir]]))
  data[[spd]][dnu] <- NA
  data[[dir]][dnu] <- NA
  
  # figure out the wind speed bins ----
  if (missing(spdseq)){
    spdseq <- seq(spdmin,spdmax,spdres)
  } else {
    if (debug >0){
      cat("Using custom speed bins \n")
    }
  }
  # get some information about the number of bins, etc.
  n.spd.seq <- length(spdseq)
  n.colors.in.range <- n.spd.seq - 1
  
  # create the color map
  spd.colors <- colorRampPalette(brewer.pal(min(max(3,
                                                    n.colors.in.range),
                                                min(9,
                                                    n.colors.in.range)),                                               
                                            palette))(n.colors.in.range)
  
  if (max(data[[spd]],na.rm = TRUE) > spdmax){    
    spd.breaks <- c(spdseq,
                    max(data[[spd]],na.rm = TRUE))
    spd.labels <- c(paste(c(spdseq[1:n.spd.seq-1]),
                          '-',
                          c(spdseq[2:n.spd.seq])),
                    paste(spdmax,
                          "-",
                          max(data[[spd]],na.rm = TRUE)))
    spd.colors <- c(spd.colors, "grey50")
  } else{
    spd.breaks <- spdseq
    spd.labels <- paste(c(spdseq[1:n.spd.seq-1]),
                        '-',
                        c(spdseq[2:n.spd.seq]))    
  }
  data$spd.binned <- cut(x = data[[spd]],
                         breaks = spd.breaks,
                         labels = spd.labels,
                         ordered_result = TRUE)
  # clean up the data
  data. <- na.omit(data)
  
  # figure out the wind direction bins
  dir.breaks <- c(-dirres/2,
                  seq(dirres/2, 360-dirres/2, by = dirres),
                  360+dirres/2)  
  dir.labels <- c(paste(360-dirres/2,"-",dirres/2),
                  paste(seq(dirres/2, 360-3*dirres/2, by = dirres),
                        "-",
                        seq(3*dirres/2, 360-dirres/2, by = dirres)),
                  paste(360-dirres/2,"-",dirres/2))
  # assign each wind direction to a bin
  dir.binned <- cut(data[[dir]],
                    breaks = dir.breaks,
                    ordered_result = TRUE)
  levels(dir.binned) <- dir.labels
  data$dir.binned <- dir.binned
  
  # Run debug if required ----
  if (debug>0){    
    cat(dir.breaks,"\n")
    cat(dir.labels,"\n")
    cat(levels(dir.binned),"\n")       
  }  
  
  # deal with change in ordering introduced somewhere around version 2.2
  if(packageVersion("ggplot2") > "2.2"){    
    cat("Hadley broke my code\n")
    data$spd.binned = with(data, factor(spd.binned, levels = rev(levels(spd.binned))))
    spd.colors = rev(spd.colors)
  }
  
  # create the plot ----
  p.windrose <- ggplot(data = data,
                       aes(x = dir.binned,
                           fill = spd.binned)) +
    geom_bar() + 
    scale_x_discrete(drop = FALSE,
                     labels = waiver()) +
    coord_polar(start = -((dirres/2)/360) * 2*pi) +
    scale_fill_manual(name = "Wind Speed (m/s)", 
                      values = spd.colors,
                      drop = FALSE) +
    theme(axis.title.x = element_blank())
  
  # adjust axes if required
  if (!is.na(countmax)){
    p.windrose <- p.windrose +
      ylim(c(0,countmax))
  }
  
  # print the plot
  print(p.windrose)  
  
  # return the handle to the wind rose
  return(p.windrose)
}



df3 = df3[!(is.na(df3$WDIR)), ]
sum(is.na(df4$new_wspd))
# recreate p.wr2, so that includes the new data
p.wr2 <- plot.windrose(data = df3,
                       spd = "new_wspd",
                       dir = "WDIR")
# now generate the faceting
p.wr3 <- p.wr2 + facet_wrap(~month)
# and remove labels for clarity
p.wr3 <- p.wr3 + theme(axis.text.x = element_blank(),
                       axis.title.x = element_blank()) 
p.wr3 + ggtitle("Windrose Per Month: Station 44020")

