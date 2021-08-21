# packages, functions and times
library(readxl)
library(dplyr)
library(haven)

roundUp <- function(x) ceiling(max(x)/10)*10
apo_greater <- function(df, var) {
  df %>%
    filter(!! rlang::sym("wk_id") >= var)
}

wk_2_t <- function(df){
  temp <- unique(df[,"wk_id"])
  temp <- temp[order(temp)]
  res <- cbind(t = order(temp), wk_id = temp)
  return(as.data.frame(res))
}

bar_ready <- function(df,hi){
  barplot(df, xaxt = "n",
          col = NA, border = NA, axes = FALSE,
          ylim = c(0, hi))
  par(new=TRUE)
  grid(lwd=2)
  par(new=TRUE)
}

apo_nat_fi_la <- function(df, first, last){
  df %>% filter(!! rlang::sym("wk") >= first, 
                !! rlang::sym("wk") <= last) %>% 
    group_by(!! rlang::sym("yr"),
             !! rlang::sym("shop_cd")) %>% 
    summarize(amt = sum(!! rlang::sym("amt")))
}

apo_order <- function(df){
  temp <- order(df[,"shop_cd"])
  df <- df[temp,] %>% group_by(!! rlang::sym("shop_cd"))
  df <- filter(df, n()>1)
  
  yr_check <- as.numeric(unlist(df[,"yr"] %% 2))
  yr_check_cmp <- rep(c(1,0),length(yr_check)/2)

  if(sum(yr_check == yr_check_cmp) == length(yr_check)){
    print("2019 and 2020 are in order!")
    df <- df %>%
      group_by(!! rlang::sym("shop_cd")) %>% 
      arrange(!! rlang::sym("yr"), .by_group = TRUE) %>%
      mutate(pct_change = (!! rlang::sym("amt")/lag(!! rlang::sym("amt")) - 1) * 100)
    
  }else{
    print("2019 and 2020 are not in order!")
  }
  
  return(df)
}