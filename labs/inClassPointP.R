install.packages("spatstat")
require(spatstat)

ppp_owin = owin(xrange = c(0, 1), yrange = c(0, 1))
# Set a random seed so we can re-create our results
set.seed(123456789)

lambda_sim = 100
ppp_sim_1 = 
  rpoispp(
    lambda = lambda_sim,
    win = ppp_owin)

plot(ppp_sim_1)

quad_25 = quadratcount(ppp_sim_1, nx = 5, ny = 5)
hist(
  quad_25,
  main = "Histogram of quadrat counts",
  xlab = "count"
)

set.seed(1)
pois_25 = rpois(n = 25, lambda = lambda_sim / 25)
hist(
  pois_25,
  main = "Histogram of random\nPoisson-distributed numbers",
  xlab = "count")

par(mfrow = c(2, 1))

hist(
  quad_25,
  main = "Histogram of quadrat counts",
  xlab = "count"
)
hist(
  pois_25,
  main = "Histogram of random\nPoisson-distributed numbers",
  xlab = "count")

mean(quad_25)

var(c(quad_25))

mean(pois_25)

var(pois_25)


ecdf_pts = ecdf(quad_25)
ecdf_rnd = ecdf(pois_25)
plot(
  ecdf_pts(seq(0, 12)), type = "l",
  main = "Empirical CDFs",
  ylab = "Pr(x < i)", xlab = "i")
lines(ecdf_rnd(seq(0, 12)), lty = 2)

quadrat.test(quad_25)
