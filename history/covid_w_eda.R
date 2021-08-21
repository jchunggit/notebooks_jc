q1_19 <- read.csv("q1_19.csv", row.names = "X")
q2_19 <- read.csv("q2_19.csv", row.names = "X")
q3_19 <- read.csv("q3_19.csv", row.names = "X")
q4_19 <- read.csv("q4_19.csv", row.names = "X")
q1_20 <- read.csv("q1_20.csv", row.names = "X")
q2_20 <- read.csv("q2_20.csv", row.names = "X")

q1_19 <- q1_19 %>% left_join(scok, by = "shop_cd") %>% group_by(shop_cd, one_key) %>% 
  summarise(trans_amt = sum(trans_amt, na.rm =TRUE)) %>% 
  left_join(q1_19_out, by = "one_key") %>% rename(trans_est = Market_1_est) %>% 
  arrange(desc(trans_amt)) %>% replace_na(list(trans_amt = 0, trans_est = 0))
q2_19 <- q2_19 %>% left_join(scok, by = "shop_cd") %>% group_by(shop_cd, one_key) %>% 
  summarise(trans_amt = sum(trans_amt, na.rm =TRUE)) %>% 
  left_join(q2_19_out, by = "one_key") %>% rename(trans_est = Market_1_est) %>% 
  arrange(desc(trans_amt)) %>% replace_na(list(trans_amt = 0, trans_est = 0))
q3_19 <- q3_19 %>% left_join(scok, by = "shop_cd") %>% group_by(shop_cd, one_key) %>% 
  summarise(trans_amt = sum(trans_amt, na.rm =TRUE)) %>% 
  left_join(q3_19_out, by = "one_key") %>% rename(trans_est = Market_1_est) %>% 
  arrange(desc(trans_amt)) %>% replace_na(list(trans_amt = 0, trans_est = 0))
q4_19 <- q4_19 %>% left_join(scok, by = "shop_cd") %>% group_by(shop_cd, one_key) %>% 
  summarise(trans_amt = sum(trans_amt, na.rm =TRUE)) %>% 
  left_join(q4_19_out, by = "one_key") %>% rename(trans_est = Market_1_est) %>% 
  arrange(desc(trans_amt)) %>% replace_na(list(trans_amt = 0, trans_est = 0))
q1_20 <- q1_20 %>% left_join(scok, by = "shop_cd") %>% group_by(shop_cd, one_key) %>% 
  summarise(trans_amt = sum(trans_amt, na.rm =TRUE)) %>% 
  left_join(q1_20_out, by = "one_key") %>% rename(trans_est = Market_1_est) %>% 
  arrange(desc(trans_amt)) %>% replace_na(list(trans_amt = 0, trans_est = 0))
q2_20 <- q2_20 %>% left_join(scok, by = "shop_cd") %>% group_by(shop_cd, one_key) %>% 
  summarise(trans_amt = sum(trans_amt, na.rm =TRUE)) %>% 
  left_join(q1_20_out, by = "one_key") %>% rename(trans_est = Market_1_est) %>% 
  arrange(desc(trans_amt)) %>% replace_na(list(trans_amt = 0, trans_est = 0))

q1_19_20 <- q1_19 %>% rename(amt19 = trans_amt) %>%
  left_join(q1_20, by = "shop_cd") %>% rename(amt20 = trans_amt) %>%
  select(shop_cd, amt19, amt20) %>% mutate(dif_19_20 = amt20/amt19 - 1)
q2_19_20 <- q2_19 %>% rename(amt19 = trans_amt) %>%
  left_join(q2_20, by = "shop_cd") %>% rename(amt20 = trans_amt) %>%
  select(shop_cd, amt19, amt20) %>% mutate(dif_19_20 = amt20/amt19 - 1)
q4_19_20 <- q4_19 %>% rename(amt19 = trans_amt) %>%
  left_join(q1_20, by = "shop_cd") %>% rename(amt20_1 = trans_amt) %>%
  left_join(q2_20, by = "shop_cd") %>% rename(amt20_2 = trans_amt) %>%
  select(shop_cd, amt19, amt20_1, amt20_2) %>% 
  mutate(dif_19_20_1 = amt20_1/amt19 - 1, dif_19_20_2 = amt20_2/amt19 - 1)
q1_q2_20 <- q1_20  %>% rename(amtq1 = trans_amt) %>%
  left_join(q2_20, by = "shop_cd") %>% rename(amtq2 = trans_amt) %>%
  select(shop_cd, amtq1, amtq2) %>% mutate(dif_q1_q2 = amtq2/amtq1 - 1)

q1_q2_19_20 <- q1_19 %>% group_by(shop_cd) %>% 
  summarise(trans_amt = sum(trans_amt, na.rm =TRUE)) rename(amtq1_19 = trans_amt) %>%
  left_join(q2_19, by = "shop_cd") %>% rename(amtq2_19 = trans_amt) %>%
  left_join(q1_20, by = "shop_cd") %>% rename(amtq1_20 = trans_amt) %>%
  left_join(q2_20, by = "shop_cd") %>% rename(amtq2_20 = trans_amt)

bins <- c(-Inf, -.8, -.5, -.25, -.05, 0.05, 0.25, 0.5, 0.8, Inf)
bins_cov19 <- c(-Inf, -.8, -.5, -.25, -.05, 0.05, Inf)
q1_19_20$damage <- cut(q1_19_20$dif_19_20, breaks = bins)
q2_19_20$damage <- cut(q2_19_20$dif_19_20, breaks = bins)
q4_19_20$damageq1 <- cut(q4_19_20$dif_19_20_1, breaks = bins_cov19)
q4_19_20$damageq2 <- cut(q4_19_20$dif_19_20_2, breaks = bins_cov19)
q1_q2_20$damage <- cut(q1_q2_20$dif_q1_q2, breaks = bins_cov19)
table(q1_19_20$damage) # Quarter 1 2019 vs 2020
table(q2_19_20$damage) # Quarter 2 2019 vs 2020
table(q4_19_20$damageq1) # Quarter 4 2019 vs Quarter 1 2020
table(q4_19_20$damageq2) # Quarter 4 2019 vs Quarter 2 2020
hist(table(q1_q2_20$damage)) # Quarter 1 2020 vs Quarter 2 2020