library(dplyr)
library(ggplot2)
library(caTools)
library(corrgram)
install.packages("reshape")
require(reshape)

rm(list = ls())
#Creating a data frame from the stations csv
df <- read.csv('data/LMP_data/station4000.csv', sep='\t')
df2 <- read.csv('data/LMP_data/new_calc.csv')
#Making sure no null values are in this document
any(is.na(df))
head(df2)
head(df)
scatter.smooth(x=df$Locational.Marginal.Price, y=df2$new_calc, main="Actual vs prediction")

corrgram(df, lower.panel=panel.shade, upper.panel=panel.cor)

set.seed(42)
df2 <- df2[ -c(0:5) ]

sampleSplit <- sample.split(Y=df$Locational.Marginal.Price, SplitRatio=0.7)
sampleSplit2 <- sample.split(Y=df2$Locational.Marginal.Price, SplitRatio=0.7)
newCalc <- subset(x=df2, sampleSplit2==T)
trainSet <- subset(x=df, sampleSplit==TRUE)
testSet <- subset(x=df, sampleSplit==FALSE)

model <- lm(formula=Locational.Marginal.Price ~prev_hour, data=trainSet)
model2 <- lm(formula=Locational.Marginal.Price ~new_calc, data=newCalc)
model3 <- lm(formula=Locational.Marginal.Price ~1, data=trainSet)

summary(model)
summary(model2)

preds = predict(model, testSet)

modelEval2 <- cbind(df$Locational.Marginal.Price, df2$new_calc)
modelEval <- cbind(df$Locational.Marginal.Price, df$prev_hour)
colnames(modelEval2) <- c('Actual', 'Predicted')
colnames(modelEval) <- c('Actual', 'Prev_hour')
modelEval <- as.data.frame(modelEval)
modelEval2 <- as.data.frame(modelEval2)

## Create a list
linear.model.list <- list(prev_hour = model, increase_hour = model2, null= model3)

## Model summaries
lapply(linear.model.list,function(x) {r.sq <- summary(x)$r.squared})
head(modelEval)

modelResiduals <- as.data.frame(residuals(model)) 
ggplot(modelResiduals, aes(residuals(model))) +
  geom_histogram(fill='deepskyblue', color='black')

#Mean squared error
mse <- mean((modelEval$Actual - modelEval$Predicted)^2)
mse2 <- mean((modelEval$Actual - modelEval$new_calc)^2)
print(mse)
print(mse2)
#Root of the mean square value
rmse <- sqrt(mse)
print(rmse)
#On average we are wrong by 7.951 LMP units

#Plotting predicted vs actual 
dat.m <- melt(modelEval, id.vars = "Actual")
ggplot(dat.m,                                     # Draw plot using ggplot2 package
       aes(Actual, value, colour = variable)) +
  geom_point()+
  scale_colour_manual(values = c("red", "darkred")) +
  geom_abline(intercept = 0,
              slope = 1,
              color = "orange",
              size = 2)
