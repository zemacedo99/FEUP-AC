library(readr)
library(dplyr)
library(ggplot2)

loan <- read_csv("all_loan.csv")
disp <- read_csv("disp.csv")

# Mode function
getmode <- function(v) {
   uniqv <- unique(v)
   uniqv[which.max(tabulate(match(v, uniqv)))]
}

# Verify if data is in a valid format:
filter(loan, loan_id <= 0 | account_id <= 0 | date <=0 | amount <= 0 | duration <= 0 | payments <= 0 |( status != -1 & status != 1))


# Check for missing values
sapply(loan, function(x) sum(is.na(x)))

# Summarize data
summarise(loan, avgAmount = mean(amount), varAmount = var(amount), sdAmount = sd(amount), IQRAmount = IQR(amount))

summarise(loan, avgDuration=mean(duration), varDuration = var(duration), sdDuration=sd(duration), IQRDuration = IQR(duration))

summarise(disp, getmode(type))

summarise(disp, getmode(type))


# Plot the data
ggplot(loan, aes(x = factor(0), y = amount)) + geom_boxplot(fill="darkseagreen4") + coord_cartesian(xlim = c(0.5, 1.5)) + theme(axis.title.x=element_blank(),axis.text.x=element_blank(),axis.ticks.x=element_blank()) + labs(title="Distribution of loan amounts", y="Amount")
ggplot(loan, aes(x = factor(0), y = duration)) + geom_boxplot(fill="darkseagreen4") + coord_cartesian(xlim = c(0.5, 1.5)) + theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank()) + labs(title="Distribution of loan duration", y="Duration")
ggplot(loan, aes(sample = amount)) + geom_qq(geom = "point", fill="darkseagreen4") + stat_qq_line() +  labs(title="QQPlot of the loan amount values", y="Amount value")
ggplot(loan, aes(x=factor(amount), y=amount, color=status)) + geom_dotplot()
 
ggplot(disp, aes(x=type)) + geom_bar(fill="darkseagreen4") + labs(title="Disposition types", x="Types", y="")

all_data %>% ggplot(aes(Age)) + geom_histogram(binwidth=1, color="darkseagreen4", fill = 'white')