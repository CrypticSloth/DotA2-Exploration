# Dota Ward Analysis

library(ggplot2)
library(tibble)
library(caret)
library(dplyr)
library(rjson)
library(png)

setwd("C:/Users/lizar/Google Drive (erik.sorensen20@houghton.edu)/DotaAnalysis/versions_test/7.17")
json_data <- fromJSON(file="3944571593.json")

# Get player name
json_data$players[[1]]$personaname

# Get the players observer ward log
json_data$players[[1]]$obs_log
json_data$players[[1]]$sen_log

x <- integer()
y <- integer()

for (i in 1:length(json_data$eventData$wardEvents)) {
    if (json_data$eventData$wardEvents[[i]]$x != 0) {
        x <- c(x,json_data$eventData$wardEvents[[i]]$x)
        y <- c(y,json_data$eventData$wardEvents[[i]]$y)
    }
}

ima <- readPNG("C:/Users/lizar/Pictures/dota_minimap.png")
plot(75:190,75:190, type='n')
lim <- par()
rasterImage(ima, lim$usr[1], lim$usr[3], lim$usr[2], lim$usr[4])
points(x,y, col="white")
   