require("here")
require("ggplot2")

data_dir = here(
  "data")

dat <- data.frame(read.csv(here("data","ginkgo_data_2022.csv")))

names(dat)

dat <- unique(dat$site_id)
print(dat)
sum(dat$seeds_present == T)

ggplot(dat, aes(x = max_width, y = notch_depth, colour = seeds_present)) +
  geom_point() +
  xlab("Max Leaf Width (mm)") +
  ylab("Notch Depth (mm)") 

