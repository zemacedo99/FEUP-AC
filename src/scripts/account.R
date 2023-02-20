library(tidyverse)

dsaccount <- read_csv("src/ds/account.csv",
                    col_type = list (account_id = col_integer(),
                                    district_id = col_integer(),
                                    frequency = col_factor(),
                                    date = col_integer()))




filter(dsaccount, account_id <= 0 | district_id <= 0 | date <= 0 )


sapply(dsaccount, function(x) sum(is.na(x)))

accountplot <- ggplot(dsaccount, aes(x=frequency))  + geom_bar(fill="darkseagreen4")


accountplot + labs( title = "Distribution of frequency of issuance of statements",
                    tag = "Figure 1",
                    x = "Frequency of issuance",
                    y = "Number of accounts",
                    colour = "Gears"
                    )


accountplot + theme_classic()

frequencytable <- table(dsaccount$frequency)
