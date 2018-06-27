# Dota Ward Analysis

library(ggplot2)
library(tibble)
library(caret)
library(dplyr)
library(rjson)
library(png)

json_data <- fromJSON(file="versions_test/7.17/3944571593.json")

# Get player name
json_data$players[[1]]$personaname

# Get the players observer ward log
json_data$players[[1]]$obs_log
json_data$players[[1]]$sen_log

x_obs <- integer()
y_obs <- integer()
x_sent <- integer()
y_sent <- integer()

for (i in 1:length(json_data$eventData$wardEvents)) {
    if (json_data$eventData$wardEvents[[i]]$x != 0) {
      if (json_data$eventData$wardEvents[[i]]$wardType == 0) {
        x_obs <- c(x_obs,json_data$eventData$wardEvents[[i]]$x)
        y_obs <- c(y_obs,json_data$eventData$wardEvents[[i]]$y)
      } else if (json_data$eventData$wardEvents[[i]]$wardType == 1) {
        x_sent <- c(x_sent,json_data$eventData$wardEvents[[i]]$x)
        y_sent <- c(y_sent,json_data$eventData$wardEvents[[i]]$y)
      }
    }
}

ima <- readPNG("analysis/TeamWardAnalysis/detailed_707.png")
#69:186 ratio does the best for the plot
sizes <- 69:186
plot(sizes,sizes, type='n')
lim <- par()
rasterImage(ima, lim$usr[1], lim$usr[3], lim$usr[2], lim$usr[4])
points(x_obs,y_obs, col="green")
points(x_sent,y_sent,col="blue")
   
