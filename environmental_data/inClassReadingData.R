require("here")
install.packages("here")                            # Install dplyr
library("dplyr")
data_dir = here(
  "data")


dat_catrate <- data.frame(read.csv(here("data","catrate.csv")))
dat_delomys <- data.frame(read.csv(here("data", "delomys.csv")))
dat_rope <- data.frame(read.csv(here("data", "rope.csv")))



head(dat_catrate)

select_catrate <- select_if(dat_catrate, is.numeric)
select_delomys <- select_if(dat_delomys, is.numeric)
select_rope <- select_if(dat_rope, is.numeric)

plot(select_catrate$years, select_catrate$pond, main= "Antonio: Years vs Pond")
