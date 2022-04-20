library(tidyverse) # r-package ecosystem
library(MASS) # statistical functions
library(knitr) # fancy tables
library(clifro) # windrose plot
library(scales) # percentages
library(elevatr) # elevation data
library(raster) # geospatial
library(leaflet) # mapping
require("here")
install.packages("ggvis")
require(ggvis)
require(grid)
require(ggplot2)

df_list <-list.files("iCons/data/chosen_stations", pattern=NULL, all.files=FALSE, full.names=FALSE)
print(df_list)
val = df_list[28]
print(val)

df <- read.delim(here("iCons", "data", "chosen_stations", val))

head(df)
val2 = ""
val2 = substr(val, 0, 13)

#ggvis(df, props(x = ~Date, y = ~new_wspd)) + layer_line()
#matplot(x = df$Date, y = df$new_wspd,type = "l" )
#a <-ggplot(df,aes(Date,new_wspd, group = 1))+geom_line()+theme_minimal()
#grid.draw(ggplotGrob(a))
#dev.copy2pdf(file=val + "_wind.pdf", width = 7, height = 5)
df = df[!(df$WDIR >360), ]
windrose(speed = df$new_wspd,
         direction = df$WDIR,
         n_directions = 12,
         speed_cuts = seq(0,20,4),
         ggtheme='minimal',
         col_pal = 'YlGn')
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
  theme_minimal()
dev.copy2pdf(file=paste0(val2,"_pwrDensity.pdf" ), width = 7, height = 5)
#monthly<-df %>%
#  group_by(Month) %>%
#  summarise(hours=n()/12,
#            windspeedat100mms=mean(windspeedat100mms),
#            mwh=sum(kw,na.rm=T)/(1000*12)) %>%
#  mutate(ncf=percent(mwh/(hours*1.5)))
#kable(monthly,digits=1,caption='monthly totals',align='c')
