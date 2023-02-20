library(tidyverse)
library(validate)

# https://cran.r-project.org/web/packages/validate/vignettes/cookbook.html#1_Introduction_to_validate

loan <- read_csv("src/ds/loan.csv")
account  <- read_csv("src/ds/account.csv")
card  <- read_csv("src/ds/all_card.csv")
client <- read_csv("src/ds/client.csv")
disp <- read_csv("src/ds/disp.csv")
district <- read_csv("src/ds/district.csv")
trans <- read_csv("src/ds/all_trans.csv")


loanValidValues <- validator(loan_id > 0 
                 , account_id > 0
                 , date > 0 
                 , amount > 0
                 , duration > 0
                 , payments > 0
                 , status == -1 || status == 1)

loanMissingValues <- validator(!is.na(loan_id)
                 , !is.na(account_id)
                 , !is.na(date)
                 , !is.na(amount)
                 , !is.na(payments)
                 , !is.na(account_id)
                 , !is.na(status))

loanUniqueValues <- validator(is_unique(account_id))


transValidValues <- validator(trans_id > 0 
                 , account_id > 0
                 , date > 0 
                 , type != ""
                 , operation != ""
                 , amount > 0
                 , balance > 0
                 , k_symbol != ""
                 , field_length(bank,n=2)
                 , bank != ""
                 , account > 0)

transBalanceValues <- validator(balance > 0)


transMissingValues <- validator(!is.na(trans_id)
                 , !is.na(account_id)
                 , !is.na(date)
                 , !is.na(type)
                 , !is.na(operation)
                 , !is.na(amount)
                 , !is.na(balance)
                 , !is.na(k_symbol)
                 , !is.na(bank)
                 , !is.na(account), account != 0)

districtValidValues <- validator(code > 0 
                 , name != ""
                 , region != ""
                 , `no. of inhabitants` > 0
                 , `no. of municipalities with inhabitants < 499` > 0
                 , `no. of municipalities with inhabitants 500-1999` > 0
                 , `no. of municipalities with inhabitants 2000-9999` > 0
                 , `no. of municipalities with inhabitants >10000` > 0
                 , `no. of cities` > 0
                 , `ratio of urban inhabitants` > 0
                 , `average salary` > 0
                 , `unemploymant rate '95` > 0
                 , `unemploymant rate '96` > 0
                 , `no. of enterpreneurs per 1000 inhabitants` > 0
                 , `no. of commited crimes '95 ` > 0
                 , `no. of commited crimes '96 ` > 0)

 

dispValidValues <- validator(disp_id > 0 
                 , client_id > 0
                 , account_id > 0
                 , type != "")

                 
dispUniqueValues <- validator(is_unique(account_id))

clientValidValues <- validator(client_id > 0
                 , birth_number > 0
                 , district_id > 0)


cardValidValues <- validator(card_id > 0
                 , type != ""
                 , issued > 0
                 , disp_id > 0)



out   <- confront(trans, transBalanceValues)
summary(out)
plot(out)