#Given list of latitude and longitude coordinates,
#plot the points in 2-D cartesian points and plot

#Equirectangular projection:
# x = (lat)*R*cos(lon)
# y = (lat)*R
# center of XY grid is (0,0)

library(devtools)
#install_github("ggbiplot", "vqv")
library(ggbiplot)


latlonXY <- function(lats, lons, scaling = 6371){
  phi0 = mean(lats)
  x = numeric(length = length(lats)); y = x
  lats = lats*pi/180; lons = lons*pi/180
  for (jj in 1:length(lats)){
    x[jj] = scaling*lons[jj]*cos(phi0)
  }
  y = lats*scaling
  plot(x,y, main = "lat/lon to x,y centered at (0,0)", xlab = "x", ylab = "y")
  return(list(x=x, y=y))
}
  
plotPCA <- function(XY){
  XY <- as.data.frame(XY)
  fit <- prcomp(XY, scale. = T, center = T)
  g <- ggbiplot(fit, #obs.scale = 1, var.scale = 1,
                ellipse = TRUE, 
                circle = F)
  g <- g + scale_color_discrete(name = '')
  g <- g + theme(legend.direction = 'horizontal', 
                 legend.position = 'top')
  print(g)
}



