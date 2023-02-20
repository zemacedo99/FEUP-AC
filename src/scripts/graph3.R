pkgs <- c("ggplot2", "dplyr", "plyr", "readr", "GGally", "tidyverse")
install.packages(pkgs, repos = "http://cran.us.r-project.org")
library(readr)
library(dplyr)
library(ggplot2)
library(GGally)
library(tidyverse)

loans <- read_csv("ds/loan.csv", show_col_types = FALSE)
account <- read_csv("ds/account.csv", show_col_types = FALSE)
district <- read_csv("ds/district.csv", show_col_types = FALSE)

nr_loans <- loans %>% group_by(account_id) %>% summarise(nr = n())
all_data <- inner_join(loans, account, by="account_id")
all_data2 <- inner_join(all_data, district, by = c("district_id" = "code"))

ggplot(all_data2, aes(x = amount, y = `average salary`, color = status))  +  geom_point() + labs(title = "Scatterplot of loan amount and average salary", x = "Loan amount", y = "Average Salary")

all_data2 %>%  mutate(status = factor(status)) %>% 
                ggpairs(columns = c("amount", "average salary", "no. of enterpreneurs per 1000 inhabitants", "unemploymant rate \'96"), aes(color = status), upper = list(continuous = wrap('cor', size = 5)), lower = list(combo = wrap('facethist', bins = 30)), diag = list(continuous = wrap('densityDiag', alpha = 5)))