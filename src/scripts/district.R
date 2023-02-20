install.packages('readr', dependencies = TRUE, repos='http://cran.rstudio.com/')
install.packages('ggplot2', repos='http://cran.us.r-project.org')
library(readr)
library(dplyr)
library(ggplot2)


district <- read_csv("ds/district.csv")

district <- read_csv("ds/district.csv",
                col_type = list (code = col_integer(),
                                     name = col_character(),
                                     region = col_character(),
                                     `no. of inhabitants` = col_integer(),
                                     `no. of municipalities with inhabitants < 499` = col_integer(),
                                     `no. of municipalities with inhabitants 500-1999` = col_integer(),
                                     `no. of municipalities with inhabitants 2000-9999` = col_integer(),
                                     `no. of municipalities with inhabitants >10000` = col_integer(),
                                     `no. of cities` = col_integer(),
                                     `ratio of urban inhabitants` = col_integer(),
                                     `average salary` = col_integer(),
                                     `no. of enterpreneurs per 1000 inhabitants` = col_integer()))

#unemploymant rate '95 = col_integer(),
#unemploymant rate '96 = col_integer(),
#"no. of commited crimes '95" = col_integer(),
#"no. of commited crimes '96 " = col_integer()



# Verify if data is in a valid format:
#filter(district, code <= 1 | !(is.string(name)) | !(is.string(region)) | 'no. of inhabitants' <= 0 | 'no. of municipalities with inhabitants < 499' <= 0 | 'no. of municipalities with inhabitants 500-1999' <= 0 |'no. of municipalities with inhabitants 2000-9999' <= 0 | 'no. of municipalities with inhabitants >10000' <= 0 | 'no. of cities' <= 0| 'ratio of urban inhabitants' <= 0.0 | 'average salary' <= 0 | "unemploymant rate '95" <= 0.0 | "unemploymant rate '96" <= 0.0 | 'no. of enterpreneurs per 1000 inhabitants' <= 0 | "no. of commited crimes '95" <= 0 | "no. of commited crimes '96 " <= 0)
filter(district, code <= 1 | `no. of inhabitants` <= 0 | `no. of municipalities with inhabitants < 499` <= 0 
                | `no. of municipalities with inhabitants 500-1999` <= 0 
                |`no. of municipalities with inhabitants 2000-9999` <= 0 
                | `no. of municipalities with inhabitants >10000` <= 0 
                | `no. of cities` <= 0| `ratio of urban inhabitants` <= 0.0 
                | `average salary` <= 0 
                | `no. of enterpreneurs per 1000 inhabitants` <= 0)

#"unemploymant rate '95" <= 0.0 | "unemploymant rate '96" <= 0.0 
#| "no. of commited crimes '95" <= 0 | "no. of commited crimes '96 " <= 0


# Check for missing values
sapply(district, function(x) sum(is.na(x)))
summarise(district, avgAm= mean(`no. of enterpreneurs per 1000 inhabitants`), varAm = var(`no. of enterpreneurs per 1000 inhabitants`), sdAm = sd(`no. of enterpreneurs per 1000 inhabitants`), IQRAm = IQR(`no. of enterpreneurs per 1000 inhabitants`))

# Summarize data
#summarise(district, avgSal=mean('average salary'), sdSal=sd('average salary'), avgEnter=mean('no. of enterpreneurs per 1000 inhabitants'), sdEnter=sd('no. of enterpreneurs per 1000 inhabitants'))

# Plot the data
#ggplot(district, aes(sample='average salary')) + geom_qq() + ylab("Average Salary")


#ggplot(disp, aes(x=type)) + geom_bar()
ggplot(district, aes(x = factor(0), y = `average salary`)) + geom_boxplot(fill="darkseagreen4") + theme(axis.title.x=element_blank(),axis.text.x=element_blank(),axis.ticks.x=element_blank()) + ggtitle("Distribution of Average Salary") + coord_cartesian(xlim = c(0.5,1.5))
