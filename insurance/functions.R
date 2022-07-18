merge_after_aggregate <- function(df_from_t_col_name, df_from_by_col_name,
                                  df_to, by_col_name, t_col_name, 
                                  c_col_name, FUN, t_na=NULL){
  
  agg_df_temp <- aggregate(df_from_t_col_name, 
                           by=list(df_from_by_col_name), 
                           FUN=FUN)
  
  colnames(agg_df_temp) <- c(by_col_name, c_col_name)
  
  ret_df <- merge(x = df_to, y = agg_df_temp, by = by_col_name, all=TRUE)
  
  if(!is.null(t_na)){
    ret_df[is.na(ret_df[, c_col_name]), c_col_name] <- t_na
  }
  
  return (ret_df)
}

is.not.na <- function(x){ sum(!is.na(x)) }

print_missing_count <- function(df, all = FALSE){
  num_data <- nrow(df)
  for (name in colnames(df)){
    sum_col <- sum(is.na(df[, name]))
    if (all == TRUE || sum_col > 0) {
      cat(name, "(", class(df[, name]), ")" , "====", sum_col, "\t\trate = ", round(sum_col/num_data*100, 1))
      cat("\n")
    }
  }
}
remove_missing_data_column <- function(df, threshold = 100){
  num_data <- nrow(df)
  for (name in colnames(df)){
    sum_mis_row <- sum(is.na(df[, name]))
    if (sum_mis_row > 0) {
      rate <- round(sum_mis_row/num_data*100, 1)
      cat(name, "(", class(df[, name]), ")" , "====", sum_mis_row, "\t\trate = ", rate)
      cat("\n")
      if(rate > threshold) {
        df[, name] <- NULL
      }
    }
  }
  return(df)
}

remove_missing_data_row <- function(df){
  num_data <- nrow(df)
  for (name in colnames(df)){
    sum_mis_row <- sum(is.na(df[, name]))
    if (sum_mis_row > 0) {
      df[is.na(df[, name]),] <- NULL
    }
  }
  return(df)
}

add_count_of_value_by_colname <- function(df_from, df_from2, df_to, t_col_name, by_col_name, t_na=NULL){
  
  df_from[, t_col_name] <- factor(df_from[, t_col_name])
  df_from2[, t_col_name] <- factor(df_from2[, t_col_name])
  
  #t_col_arr <- levels(df_from[, t_col_name])
  t_col_arr <- unique(c(levels(df_from[, t_col_name]), levels(df_from2[, t_col_name])))
  levels(df_from[, t_col_name]) <- t_col_arr
  cat("levels(df_from[, t_col_name])", levels(df_from[, t_col_name]), "\n")
  cat("levels(df_from2[, t_col_name])", levels(df_from2[, t_col_name]), "\n")
  cat(t_col_arr, "\n")
  
  for (t_val in t_col_arr){
    
    col_temp <- paste(t_col_name, "_", t_val, sep="")
    
    if(nrow(df_from[which(df_from[, t_col_name]== t_val), ]) > 0){
      
      agg_temp <- aggregate(df_from[which(df_from[, t_col_name]== t_val), t_col_name], by=list(df_from[which(df_from[, t_col_name] == t_val), by_col_name]), FUN=function(x){ sum(!is.na(x))
      })
      
      colnames(agg_temp) <- c(by_col_name, col_temp)
      
      df_to <- merge(x = df_to, y = agg_temp, by = by_col_name, all=TRUE)
      
      #NA 
      if(!is.null(t_na)){
        df_to[is.na(df_to[, col_temp]), col_temp] <- t_na
      }
    }else{
      
      df_to[, col_temp] <- NA
      
      #NA 
      if(!is.null(t_na)){
        df_to[is.na(df_to[, col_temp]), col_temp] <- t_na
      }
    }
  }
  return (df_to)
}