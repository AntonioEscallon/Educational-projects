library(dplyr)
library(ggplot2)
library(caTools)
library(corrgram)

df <- read.csv('data/LMP_data/station4000.csv', sep='\t')
any(is.na(df))
head(df)
corrgram(df, lower.panel=panel.shade, upper.panel=panel.cor)

set.seed(42)

sampleSplit <- sample.split(Y=df$Locational.Marginal.Price, SplitRatio=0.7)
trainSet <- subset(x=df, sampleSplit==TRUE)
testSet <- subset(x=df, sampleSplit==FALSE)

model <- lm(formula=Locational.Marginal.Price ~prev_hour, data=trainSet)
model2 <- lm(formula=Locational.Marginal.Price ~Hour.Ending, data=trainSet)
summary(model)
summary(model2)

preds = predict(model, testSet)

modelEval <- cbind(testSet$Locational.Marginal.Price, preds)
colnames(modelEval) <- c('Actual', 'Predicted')
modelEval <- as.data.frame(modelEval)

head(modelEval)

modelResiduals <- as.data.frame(residuals(model)) 
ggplot(modelResiduals, aes(residuals(model))) +
  geom_histogram(fill='deepskyblue', color='black')

#Mean squared error
mse <- mean((modelEval$Actual - modelEval$Predicted)^2)
print(mse)
#Root of the mean square value
rmse <- sqrt(mse)
print(rmse)
#On average we are wrong by 7.951 LMP units