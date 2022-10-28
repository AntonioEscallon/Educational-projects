require("here")
install.packages("stats")                            # Install dplyr
library("dplyr")
data_dir = here(
  "data")
require("stats")


dat_catrate <- data.frame(read.csv(here("data","catrate.csv")))
dat_delomys <- data.frame(read.csv(here("data", "delomys.csv")))
dat_rope <- data.frame(read.csv(here("data", "rope.csv")))



head(dat_catrate)

select_catrate <- select_if(dat_catrate, is.numeric)
select_delomys <- select_if(dat_delomys, is.numeric)
select_rope <- select_if(dat_rope, is.numeric)

plot(select_catrate$years, select_catrate$pond, main= "Antonio: Years vs Pond")

#What is the probability of observing a value less than 7.5 in a normal 
#distribution with mean 10 and standard deviation 3?
pnorm(7.5, mean = 10, sd = 3)

pnorm(-0.75)
pnorm(78, mean = 74, sd = 2, lower.tail = FALSE)

dbinom(3, 4, 0.75)

pbinom(3,4,0.75)

1 - pbinom(3, 5, 0.75)

pnorm(3.2, mean = 2, sd = 2) - pnorm(1.2, mean = 2, sd = 2)
pnorm(3.2, mean = 2, sd = 2)

log(dbinom(2, 6, 0.368))
sum(log(dbinom(2, 6, 0.368)))
set.seed(1)
vec_rnorm = rnorm(n = 10, mean = 0, sd = 1)

like = dnorm(vec_rnorm, 0, 0.1)

log_vec = sum(log(like))

log_vec
