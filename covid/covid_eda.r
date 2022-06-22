# creation of cov_shop_ok joint csv
cov_shop <- read.csv("shopcd_covid.csv")
cov_shop_ok <- read_xlsx("scok_pool.xlsx")
cov_shop <- cov_shop %>% left_join(cov_shop_ok, by = "shop_cd")
write.csv(cov_shop, "shopcd_covid_join.csv")

# coordinate join
sasdat <- read_sas("\\\\internal.imsglobal.com\\ffmvdfs01\\Departments\\Consulting\\Intern\\daten\\Automation\\OneKey\\apothekenspiegel_202006.sas7bdat")
pandat <- read_sas("\\\\internal.imsglobal.com\\ffmvdfs01\\Departments\\Consulting\\Intern\\daten\\Automation\\Panadress\\apothekentargeting_2020_03.sas7bdat")
sasdat_f <- sasdat %>% select(Institution_ID, XCOOR_WGS, YCOOR_WGS) %>% 
  mutate(one_key = as.numeric(substr(Institution_ID,2,10))) %>%
  select(one_key, XCOOR_WGS, YCOOR_WGS) %>% na.omit

cov_shop_xy <- cov_shop %>% left_join(sasdat_f, by = "one_key")
write.csv(cov_shop_xy, "shopcd_ok_covid_xy.csv")

## national level wk 10-26
apo_nat_10_26 <- apo_sales %>% filter(wk < 27, wk > 9) %>% 
  group_by(yr) %>% summarize(trans_amt = sum(trans_amt))

# 10-26
# 14-26
# 18-26

# pharmacy level
apo_nat_per_10_26 <- apo_sales %>% filter(wk < 27, wk > 9) %>% 
  group_by(yr, shop_cd) %>% summarize(trans_amt = sum(trans_amt)) 
apo_nat_per_10_26 <- apo_nat_per_10_26 %>% group_by(shop_cd) %>% 
  filter(n()==2) %>% arrange(shop_cd)
apo_nat_per_10_26_chng <- apo_nat_per_10_26 %>% group_by(shop_cd) %>% 
  arrange(yr, .by_group = TRUE) %>% 
  mutate(pct_change = (trans_amt/lag(trans_amt) - 1) * 100)
pcts_temp <- apo_nat_per_10_26_chng$pct_change
pcts <- pcts_temp[!is.na(pcts_temp)]


