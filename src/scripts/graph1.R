library(readr)
library(dplyr)
library(ggplot2)


loan <- read_csv("loan.csv")

trans <- read_csv("trans.csv")

nr_trans <- trans %>% group_by(account_id) %>% summarise(nr = n())

all_data <- inner_join(nr_trans, loan, by="account_id")

ggplot(all_data, aes(x = amount, y = nr, color = status)) + geom_point() + labs(title = "Scatterplot of loan amount and number of transactions", x = "Loan amount", y = "Number of transactions")
