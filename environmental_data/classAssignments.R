"Hello World, it's Antonio Escallon"

getwd()
data(iris)

head(iris)

iris$Sepal.Width

mean(iris$Sepal.Length)

sd(iris$Sepal.Width)

plot(x = iris$Sepal.Width, y = iris$Sepal.Length)

data_center_x = mean(iris$Sepal.Width)
data_center_y = mean(iris$Sepal.Length)
c(data_center_x, data_center_y)

print(data_center_x)
print(data_center_y)

plot(x = iris$Sepal.Width, y = iris$Sepal.Length)
points(x = data_center_x, y = data_center_y, col = "red")

line_point_slope = function(x, x1, y1, slope)
{
  get_y_intercept = 
    function(x1, y1, slope) 
      return(-(x1 * slope) + y1)
  
  linear = 
    function(x, yint, slope) 
      return(yint + x * slope)
  
  return(linear(x, get_y_intercept(x1, y1, slope), slope))
}

line_point_slope(2, 4, 4, -2)

plot(x = iris$Sepal.Width, y = iris$Sepal.Length) + title(main = "Antonios Plot")
points(x = data_center_x, y = data_center_y, col = "blue")
curve(
  line_point_slope(
    x, 
    data_center_x, 
    data_center_y,
    2), 
  add = TRUE)

data(CO2)

head(CO2)

data_center_xCO2 = mean(CO2$uptake)
data_center_yCO2 = mean(CO2$conc)
c(data_center_xCO2, data_center_yCO2)

plot(x = CO2$uptake, y = CO2$conc) + title(main = " Plot of Uptake vs Conc")
points(x = data_center_xCO2, y = data_center_yCO2, col = "green")
curve(
  line_point_slope(
    x, 
    data_center_xCO2, 
    data_center_yCO2,
    2), 
  add = TRUE)
