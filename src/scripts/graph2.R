library(readr)
library(dplyr)
library(ggplot2)


loan <- read_csv("loan.csv")

ggplot(all_data, aes(x = loan$duration, y = loan$amount, color = status)) + geom_point() + labs(title = "Scatterplot of loan duration and loan amount", x = "Loan duration", y = "Loan amount")
