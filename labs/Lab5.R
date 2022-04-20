
# load packages
library(spatstat)         #for point pattern analyses; version 2.2-0 used
library(raster)           #for raster covariate data; version 3.5_2 used
require(here)

data_dir = here(
  "data",
  "Fletcher_Fortin-2018-Supporting_Files",
  "data")

#import the data from directory
cactus <- read.csv(file.path(data_dir, "cactus.csv"))
boundary <- read.csv(
  file.path(data_dir, "cactus_boundaries.csv"), header=T)

#create spatstat objects
ppp.window <- owin(
  xrange=c(boundary$Xmin, boundary$Xmax),
  yrange=c(boundary$Ymin, boundary$Ymax))
ppp.cactus <- ppp(
  cactus$East,
  cactus$North,
  window=ppp.window)

#plot raw data
plot(ppp.cactus)

#summary information
summary(ppp.cactus)

# density plots: density() function from stats package (terra
# and raster density() methods ultimately call stats::density())
plot(stats::density(ppp.cactus))
plot(raster::density(ppp.cactus,1))  #alter smoothing parameter

#contour plot
contour(density(ppp.cactus, 1))

#quadrat counts
Q <- quadratcount(ppp.cactus, nx = 4, ny = 4)#counts in 12.5x12.5m quadrats

# Does it look like a Poisson distribution?
hist(Q)


#plot
plot(ppp.cactus, cex = 2)
plot(Q, add = TRUE, cex = 1)

#chi-sq test for complete spatial randomness, CSR
quadrat.test(ppp.cactus, nx = 4, ny = 4, method="Chisq")

pp.xy <- ppm(ppp.cactus, ~ x + y)
pp.xy2 <- ppm(ppp.cactus, ~ polynom( x, y, 2))
pp.xy.pred <- predict.ppm(pp.xy2, type = "trend")

#get intensity, lambda, from our point pattern
intensity(ppp.cactus)

#Simulate a homogeneous point pattern 4 times
sim.pp <- rpoispp(lambda=intensity(ppp.cactus), nsim=4, win=ppp.window)

#plot
plot(sim.pp)

#access the x-y coords for simulation 1
sim.pp[[1]]$x
sim.pp[[1]]$y

pp.xy <- ppm(ppp.cactus, ~ x + y)
pp.xy2 <- ppm(ppp.cactus, ~ polynom( x, y, 2))
pp.xy.pred <- predict.ppm(pp.xy2, type = "trend")

#inhomogeneous point pattern
summary(pp.xy2)#summary of best ppm model

#function based on ppm coefficients
pp2.fun <- function(x, y) {exp(pp.xy2$coef[1] + 
                                 pp.xy2$coef[2]*x + pp.xy2$coef[3]*y +
                                 pp.xy2$coef[4]*I(x^2) + pp.xy2$coef[5]*x*y + pp.xy2$coef[6]*I(y^2))}

#simulate using function
pp2.sim <- rpoispp(pp2.fun, nsim=2, win=ppp.window)

#Simulate from a pixel image of expected value from the ppm
pp2.sim.exp <- rpoispp(pp.xy.pred, nsim=2)

#plot
plot(pp2.sim)
plot(pp2.sim.exp)

ppp.window <- owin(
  xrange=c(0, 100),
  yrange=c(0, 100))

ppp.cactus <- ppp(
  cactus$East,
  cactus$North,
  window=ppp.window)

#re-fit with rescaled coordinates and window
pp.xy <- ppm(ppp.cactus, ~ x + y)
summary(pp.xy)
AIC(pp.xy)

pp.xy2 <- ppm(ppp.cactus, ~ polynom(x, y, 2))
summary(pp.xy2)
AIC(pp.xy2)

pp.xy.pred <- predict.ppm(pp.xy2, type="trend")
Lxycsr <- envelope(ppp.cactus, Linhom, nsim=99, rank=1, correction="translate", simulate=expression(rpoispp(pp.xy.pred)), global=FALSE)
head(Lxycsr)
Dense_CRS_pattern <- rpoispp(180, win=ppp.window)
plot(Dense_CRS_pattern ,pch=16, col= rgb(0.2, 0.2, 1.0, 0.2))


csr_env_cactus = envelope(
  ppp.cactus, 
  Lest,
  nsim = 99,
  rank = 1,
  corection = "translate",
  global = FALSE,
  savefuns = TRUE)
attr(csr_env_cactus, "simfuns")
envelope_sims = data.frame(attr(csr_env_cactus, "simfuns"))
head(envelope_sims)[, 1:5]
envelope_sims2 = envelope_sims
envelope_sims2[, -1] = envelope_sims[, -1] - envelope_sims2$r

matlines(x = envelope_sims2$r, y = envelope_sims2[, -1][, -1], 
        type = "l", ylab = "L(r)", xlab = "r", col=gray(.65, .1))
matlines(Lcsr$obs,Lcsr$obs - Lcsr$r,  type = "l",
         col = 2, lwd = 2,
         lty = 1)
head(Lcsr)
lines(Lcsr$hi,col=2)
head(Lcsr)
plot(Lcsr$obs, Lcsr$obs - Lcsr$r, col = 2, type = "l")
lines(Lcsr$obs, )
plot(Lcsr, . - r~r, shade=c("lo", "lo"), col = (2), legend=F)

#makes a new object with marks, amenable to analysis in spatstat
ppp.area <- ppp(waka$x, waka$y, window=waka$window, marks=waka$marks)

#inspect
summary(ppp.area)

#plot
plot(ppp.area)

#mark correlation function
mcf.area <- markcorr(ppp.area)

#plot
plot(mcf.area, legend=F)

#Monte Carlo simulations for confidence envelope
MCFenv <- envelope(ppp.area, markcorr, nsim=99, correction="iso", global=F)

#plot with envelope
plot(MCFenv,  shade=c("hi", "lo"), legend=F)


# kappa is the intensity (lambda) of the parent points
kappa_1 = 1

# scale is the radius of the offspring clusters
scale_1 = 0.8

# mean number of points per cluster.
# (I think the final count is Poisson-distributed -- have to dig into the code to see.)
mu_1 = 4

# Different sized windows for scale comparison
win_small = owin(xrange = c(0, 10), yrange = c(0, 10))
win_large = owin(xrange = c(0, 30), yrange = c(0, 30))

# plotting parameters
pch_mat = 16
cex_mat = 0.8

mat_pp_small = rMatClust(kappa_1, scale_1, mu_1, win = win_small)
mat_pp_large = rMatClust(kappa_1, scale_1, mu_1, win = win_large)

e_lest_mat_small =  envelope(
  mat_pp_small, 
  fun = Lest,
  nsim = 99,
  rank = 1,
  correction = "isotropic",
  global = FALSE)


e_lest_mat_large =  envelope(
  mat_pp_large,
  fun = Lest,
  nsim = 99, 
  rank = 1, 
  correction = "isotropic", 
  global = FALSE, funargs = list("rmax" = 20))

e_lest_mat_small =  envelope(
  mat_pp_small,
  fun = Lest,
  nsim = 99,
  rank = 1,
  correction = "isotropic",
  global = FALSE,
  funargs = list("rmax" = 5))

plot(e_lest_mat_small, . - r ~ r, main = "Small Point Pattern")
plot(e_lest_mat_large, . - r ~ r, main = "Large Point Pattern")

par(mfrow = c(2, 1))
plot(
  mat_pp_small,
  pch = pch_mat, cex = cex_mat,
  main = "Matern Process - 10 by 10 window ")
plot(
  mat_pp_large,
  pch = pch_mat, cex = 0.3 * cex_mat,
  "Matern Process - 100 by 100 window ")

L1 <- Lest(mat_pp_large, rmax=35, correction="none") 
L2 <-Lest(mat_pp_small, rmax = 35, correction="none")
plot(L1, main = "Large Scale")
plot(L2, main = "Small Scale")
