require(readxl)
require(tidyverse)
require(haven)
require(writexl)

setwd("~/10 work/covid19")

# data load
data_orig <- read_xlsx("covid_otc_raw.xlsx")
scok <- read_xlsx("scok_pool.xlsx") %>% 
  mutate(Institution_ID = paste0("F",sprintf("%08d", one_key)))
apotar <- read_sas("apothekentargeting.sas7bdat")
instpool <- read_sas("onekey_instpool.sas7bdat") %>% 
  filter(substr(Institution_ID,1,1)=="F")
spiegel <- read_sas("apothekenspiegel.sas7bdat")

data <- scok %>% left_join(data_orig, by = "shop_cd") %>% 
  select(-shop_cd) %>% drop_na() %>% mutate(q2q1_20 = (q2_20/q1_20) - 1)
data$q2q1_20_cat <- cut(data$q2q1_20, 
                        breaks=c(-Inf, -.4, -.3, -.2, -.15, Inf), 
                        include.lowest=TRUE)
data <- data %>% left_join(apotar, by = "Institution_ID") %>% drop_na()
brks <- with(data, quantile(q2q1_20, probs = c(0, 0.2, 0.4, 0.6, 0.8, 1)))
# temp <- within(data, quartile <- cut(q2q1_20, breaks = brks, labels = 1:4, 
#                                      include.lowest = TRUE))

## train stations + airports
bahnhof_flugs <- function(df){
  sum(grepl("ahnhof", df$Institution_Long_Name)|
        grepl("Im Bahnhof", df$Address)|
        grepl("Am Bahnhof", df$Address)|
        grepl("lugh", df$Institution_Long_Name)|
        grepl("Aero", df$Institution_Long_Name)|
        grepl("aero", df$Institution_Long_Name)|
        grepl("flug", df$Institution_Long_Name)|
        grepl("Flug", df$Institution_Long_Name)|
        grepl("lugh", df$Address)|
        grepl("Terminal", df$Address)|
        grepl("Terminal", df$Institution_Long_Name)|
        grepl("Ankunft", df$Address)|
        grepl("Ebene", df$Address)|
        grepl("airport", df$Institution_Long_Name))
}
df_bhf_flgs <- function(df){
  df[grepl("ahnhof", df$Institution_Long_Name)|
       grepl("Im Bahnhof", df$Address)|
       grepl("Am Bahnhof", df$Address)|
       grepl("lugh", df$Institution_Long_Name)|
       grepl("Aero", df$Institution_Long_Name)|
       grepl("aero", df$Institution_Long_Name)|
       grepl("flug", df$Institution_Long_Name)|
       grepl("Flug", df$Institution_Long_Name)|
       grepl("lugh", df$Address)|
       grepl("Terminal", df$Address)|
       grepl("Terminal", df$Institution_Long_Name)|
       grepl("Ankunft", df$Address)|
       grepl("Ebene", df$Address)|
       grepl("airport", df$Institution_Long_Name),]
}
bahnhof_address <- function(df){
  sum(grepl("Im Bahnhof", df$Address)|
        grepl("Am Bahnhof", df$Address))
}

FindOutliers <- function(data) {
  lowerq = quantile(data)[2]
  upperq = quantile(data)[4]
  iqr = upperq - lowerq
  extreme.threshold.upper = (iqr * 3) + upperq
  extreme.threshold.lower = lowerq - (iqr * 3)
  result <- which(data > extreme.threshold.upper | data < extreme.threshold.lower)
}
rowIndx <- function(df, n) {
  n <- paste0(n)
  df <- mutate(df, !!n := 1:dim(df)[1])
  
}

# percent flux
data_1 <- data %>% filter(q2q1_20_cat == "[-Inf,-0.4]")
data_2 <- data %>% filter(q2q1_20_cat == "(-0.4,-0.3]")
data_3 <- data %>% filter(q2q1_20_cat == "(-0.3,-0.2]")
data_4 <- data %>% filter(q2q1_20_cat == "(-0.2,-0.15]")
data_5 <- data %>% filter(q2q1_20_cat == "(-0.15, Inf]")

data_1_sum <- data_1 %>% summarise_if(is.numeric, mean)
data_2_sum <- data_2 %>% summarise_if(is.numeric, mean)
data_3_sum <- data_3 %>% summarise_if(is.numeric, mean)
data_4_sum <- data_4 %>% summarise_if(is.numeric, mean)
data_5_sum <- data_5 %>% summarise_if(is.numeric, mean)

data_1_50_sum <- data_1_50 %>% summarise_if(is.numeric, mean)
data_5_50_sum <- data_5_50 %>% summarise_if(is.numeric, mean)

data_sum <- rbind(data_5_sum,data_4_sum,data_3_sum,data_2_sum,data_1_sum)

pos <- lapply(data_sum, FindOutliers)
View(pos[lapply(pos,length)>0])

# sales flux
data$sal_change <- data$q2_20 - data$q1_20
brks_q1q2 <- with(data, quantile(sal_change, probs = c(0, 0.1, 0.25, 0.5, 0.75, 1)))
data$q2q1_20_sal_cat <- cut(data$sal_change, 
                            breaks=c(-Inf, -100000, -50000, -25000, -10000, Inf), 
                            include.lowest=TRUE)
data_1 <- data %>% filter(q2q1_20_sal_cat == "[-Inf,-1e+05]")
data_2 <- data %>% filter(q2q1_20_sal_cat == "(-1e+05,-5e+04]")
data_3 <- data %>% filter(q2q1_20_sal_cat == "(-5e+04,-2.5e+04]")
data_4 <- data %>% filter(q2q1_20_sal_cat == "(-2.5e+04,-1e+04]")
data_5 <- data %>% filter(q2q1_20_sal_cat == "(-1e+04, Inf]")

data_1_sum <- data_1 %>% summarise_if(is.numeric, mean)
data_2_sum <- data_2 %>% summarise_if(is.numeric, mean)
data_3_sum <- data_3 %>% summarise_if(is.numeric, mean)
data_4_sum <- data_4 %>% summarise_if(is.numeric, mean)
data_5_sum <- data_5 %>% summarise_if(is.numeric, mean)

data_sum_sal <- rbind(data_5_sum,data_4_sum,data_3_sum,data_2_sum,data_1_sum)

pos_sal <- lapply(data_sum_sal, FindOutliers)
View(pos_sal[lapply(pos_sal,length)>0])





# identify top 100s from Q1-2019
top_no <- 50
setwd("~/10 work/covid19/Output")
qq <- c(201913, 201926, 201939, 201952, 202013, 202026)
for(i in 5:6){
  q_xl <- read_xlsx(paste0("others_Market_1_",qq[i],"_R2_output.xlsx"), 
                    sheet = "INPUT_Apothekenliste")
  q_xl <- q_xl %>% select(Institution_Id, zip_code, location_name, Market_1)
  q_xl <- rowIndx(q_xl, qq[i])
  
  if(i == 1){
    q_xl_fin <- head(q_xl, top_no)
    plot(unlist(q_xl_fin["201913"])~rep(i,dim(q_xl_fin)[1]), 
         xlim = c(1,6),
         ylim = rev(range(1:100)),
         xaxt = "n", pch = 20, cex = 0.5,
         xlab = "YYYYMM", ylab = "Rank of pharmacy")
    legend("bottomleft", c("?? = Less than 50 or increased", "?? = 50-100", 
                           "?? = 100-500", "?? = Greater than 500"),
           col = c("white", "darkorange", "red", "darkmagenta"), lty = 1)
    axis(1, at = 1:6, labels = qq)
  }else{
    q_xl <- q_xl[,c(1,5)]
    q_xl_fin <- q_xl_fin %>% left_join(q_xl, by = "Institution_Id")
    points(unlist(q_xl_fin[as.character(qq[i])])~rep(i,dim(q_xl_fin)[1]),
           pch = 20, cex = 0.5)
    for(ii in 1:top_no){
      q_diff <- unlist(q_xl_fin[as.character(qq[i])])[ii] - 
        unlist(q_xl_fin[as.character(qq[i-1])])[ii]
      if(q_diff > 50){
        color = "darkorange"
      }
      if(q_diff > 100){
        color = "red"
      }
      if(q_diff > 500){
        color = "darkmagenta"
      }
      if(q_diff < 51){
        next
      }
      lines(x = c(i-1, i), 
            y = c(unlist(q_xl_fin[as.character(qq[i-1])])[ii],
                  unlist(q_xl_fin[as.character(qq[i])])[ii]),
            col = color)
    }
  }
}

q_xl_xy <- q_xl_fin %>% left_join(instpool, by = c("Institution_Id" = "Institution_ID"))

q120_xl <- read_xlsx(paste0("others_Market_1_",202013,"_R2_output.xlsx"), 
                     sheet = "INPUT_Apothekenliste") %>% 
  rename(Q1 = Market_1) %>% arrange(desc(Q1)) %>% mutate(Q1_RK = 1:n())
q220_xl <- read_xlsx(paste0("others_Market_1_",202026,"_R2_output.xlsx"), 
                     sheet = "INPUT_Apothekenliste") %>% 
  rename(Q2 = Market_1) %>% arrange(desc(Q2)) %>% mutate(Q2_RK = 1:n())
q1q2_xl <- q220_xl %>% left_join(q120_xl %>% select(Institution_Id, Q1, Q1_RK), 
                                 by = "Institution_Id") %>% 
  mutate(per_change = Q2/Q1 - 1, sal_change = Q2-Q1) %>% arrange(Q1_RK)

q1q2_50 <- head(q1q2_xl, 50)
sum(q1q2_50$Q2_RK %in% 1:50)
q1q2_100 <- head(q1q2_xl, 100)
sum(q1q2_100$Q2_RK %in% 1:100)
q1q2_200 <- head(q1q2_xl, 200)
sum(q1q2_200$Q2_RK %in% 1:200)
q1q2_500 <- head(q1q2_xl, 500)
sum(q1q2_500$Q2_RK %in% 1:500)
q1q2_1k <- head(q1q2_xl, 1000)
sum(q1q2_1k$Q2_RK %in% 1:1000)/1000
q1q2_2k <- head(q1q2_xl, 2000)
sum(q1q2_2k$Q2_RK %in% 1:2000)/2000
q1q2_5k <- head(q1q2_xl, 5000)
sum(q1q2_5k$Q2_RK %in% 1:5000)/5000
q1q2_10k <- head(q1q2_xl, 10000)
sum(q1q2_10k$Q2_RK %in% 1:10000)/10000

brks_q1q2 <- with(q1q2_xl, quantile(sal_change, probs = c(0, 0.25, 0.5, 0.75, 1)))


#swiss borders
maps::map('world', xlim = c(4,16), ylim = c(46, 55))
points(q_xl_xy$XCOOR_WGS,q_xl_xy$YCOOR_WGS, pch = 16, col = "red", cex = 0.5)
q_xl_xy[(q_xl_xy$XCOOR_WGS < 10 & q_xl_xy$YCOOR_WGS > 47)&
          (q_xl_xy$XCOOR_WGS > 7.5 & q_xl_xy$YCOOR_WGS < 48),]






json_raw <- FROM_GeoJson(url_file_string = "export.geojson")

for(i in 1:461){
  json_raw$features 
}

bhfs <- c(bahnhof_flugs(data_1),bahnhof_flugs(data_2),
          bahnhof_flugs(data_3),bahnhof_flugs(data_4),
          bahnhof_flugs(data_5))
bhfs_add <- c(bahnhof_address(data_1),bahnhof_address(data_2),
              bahnhof_address(data_3),bahnhof_address(data_4),
              bahnhof_address(data_5))

mean(df_bhf_flgs(data_)$EW)

data$q2_20
head(data)

## concentration curve
data_curv <- data[order(-data$q1_20),]
data_curv <- data_curv %>% mutate(q1_20_curv = cumsum(q1_20/sum(q1_20)),
                                  q2_20_curv = cumsum(q2_20/sum(q2_20))) %>%
  mutate(apo = 1/dim(data_curv)[1]) %>% mutate(cumapo = cumsum(apo))
plot(data_curv$cumapo, data_curv$q1_20_curv,  typ = "p", pch = 16,
     xlab = "% Apo Anteil", ylab = "% Apo Potentiell", col = "red", cex = 0.25)
points(data_curv$cumapo, data_curv$q2_20_curv, pch = 16, 
       col = "blue", cex = 0.25)
legend("bottomright", legend = c("Q1-2020", "Q2-2020"), col = c("red", "blue"),
       lwd = 2)
