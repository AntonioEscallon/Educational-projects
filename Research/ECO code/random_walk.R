# Random walk 1

n_steps = 4

data_steps = matrix(0, ncol= 2, nrow = n_steps + 1)

step_length = 1

x_0 = 0
y_0 = 0

for( i in 1:n_steps){
  direction_i = rbinom(1,1,0.5)

  #Before step, set x_1 to x_0 and y_1 to y_0

  x_i = x_0; y_i = y_0
  #Horizontal
  if(direction_i == 0 ){
  
    x_i = x_i + sample(c(-1,1), 1)
  
  }

  if(direction_i == 1){
  
    y_i = y_i + sample(c(-1,1), 1)
  
  }
}


x_i
y_i

i = 1

data_steps[i+1, 1] = x_i
data_steps[i+1, 1] = y_i
plot(data_steps[,1], data_steps[,2], type = "l")
