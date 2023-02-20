install.packages('readr', dependencies = TRUE, repos='http://cran.rstudio.com/')
install.packages('ggplot2', repos='http://cran.us.r-project.org')
library(readr)
library(dplyr)
library(ggplot2)

trans <- read_csv("ds/trans_train.csv",
                col_type = list (trans_id = col_integer(),
                                     account_id = col_integer(),
                                     date = col_integer(),
                                     type = col_factor(),
                                     operation = col_factor(),
                                     amount = col_double(),
                                     balance = col_double(),
                                     k_symbol = col_factor(),
                                     bank = col_factor(),
                                     account = col_character()))

filter(trans, trans_id <= 0 | account_id <= 0 | date <= 0 | amount <= 0.0 | balance%%1==0 | type != "")

sapply(trans, function(x) sum(is.na(x)))

summarise(trans, avgBal= mean(balance), varBal = var(balance), sdBal = sd(balance), IQRBal = IQR(balance))
summarise(trans, avgAm= mean(amount), varAm = var(amount), sdAm = sd(amount), IQRAm = IQR(amount))

transgraph <- ggplot(trans, aes(x=type)) + geom_bar(fill="darkseagreen4")
transgraph + labs( title = "Type of Transactions",
                     tag = "Figure 3",
                     x = "Type of Transactions",
                     y = "Number of Transactions",
                     colour = "Gears"
                     )


 transgraph + theme_classic()

trans2 <- na.omit(trans)
transgraph2 <- ggplot(trans2, aes(x=operation)) + geom_bar(fill="darkseagreen4") + theme(axis.text.x=element_text(angle=50, size=6, vjust=0.5))

transgraph2 + labs( title = "Operations",
                     tag = "Figure 4",
                     x = "Operations",
                     y = "Number of Transactions",
                     colour = "Gears"
                     )


 transgraph2 + theme_classic()