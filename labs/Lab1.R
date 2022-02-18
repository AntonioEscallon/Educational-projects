plot(wyCounty2)
plot(yellowstone, add = TRUE)
wyCounty2 = spTransform(readOGR(here("data", "tl_2016_56_cousub")), proj4string(yellowstone))
wy_intersect_County3 = gIntersection(wyCounty2, yellowstone, byid = TRUE)
plot(wy_intersect_County2)
wy_overlap2  = wyCounty[wy_intersect_County3, ]
plot(wy_intersect_County3)

dev.copy2pdf(file="intersectWithBorders.pdf", width = 7, height = 5)