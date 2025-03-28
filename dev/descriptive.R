library(dplyr)
data <- read.csv("dat/processed/data_all.csv",
                 header = T,
                 sep = ",",
                 dec = ".",
                 stringsAsFactors=FALSE)
data_set <- data %>% filter(profile == 4, Wood==20)
mean(data_set$v)
sd(data_set$v)
mean(data_set$h)
sd(data_set$h)
mean(data_set$Froude)
sd(data_set$Froude)
