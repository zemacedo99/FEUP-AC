library(tidyverse)

dscard <- read_csv("src/ds/all_card.csv")

cardplot <- ggplot(dscard, aes(x=type)) + geom_bar(fill="darkseagreen4")

cardplot + labs( title = "Distribution of diferent card types",
                    tag = "Figure 2",
                    x = "Card Type",
                    y = "Number of cards",
                    colour = "Gears"
                    )


cardplot + theme_classic()



frequencytable <- table(dscard$type)


x <- c(147,10,45)
labels <- c("Classic", "Gold","Junior")

# Plot the chart.
pie(x,labels)

# Categorical data
cat_var <- factor(c(rep("Classic", 147),
                    rep("Gold", 10),
                    rep("Junior", 45)))

# Create a table from the data
cat <- table(cat_var)

# Pie
pie(cat,
    col = hcl.colors(length(cat), "BluYl")) 
