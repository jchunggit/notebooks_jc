def ab_t(df, type1, type2):
    
    from scipy.stats import shapiro
    import scipy.stats as stats
    import pandas as pd
    import numpy as np
    
    # Split A/B
    groupA = df[df['type'] == type1]['mean']
    groupB = df[df['type'] == type2]['mean']

    # check normality
    ntA = shapiro(groupA)[1] < 0.05
    ntB = shapiro(groupB)[1] < 0.05
    
    if (ntA == False) & (ntB == False): 
        leveneTest = stats.levene(groupA, groupB)[1] < 0.05
        # H0 - variances are equivalent
        # H1 - variances are not equivalent
        
        if leveneTest == False:
            # if equivalent perform t test
            ttest = stats.ttest_ind(groupA, groupB, equal_var=True)[1]
        else:
            ttest = stats.ttest_ind(groupA, groupB, equal_var=False)[1]
    else:
        # Non-Parametric Test
        ttest = stats.mannwhitneyu(groupA, groupB)[1]
        
    temp = pd.DataFrame({
        "AB Hypothesis":[ttest < 0.05], 
        "p-value":[ttest]
    })
    temp["Scenario"] = type1 + " vs. " + type2
    temp["Test Type"] = np.where((ntA == False) & (ntB == False), "Parametric", "Non-Parametric")
    temp["AB Hypothesis"] = np.where(temp["AB Hypothesis"] == False, "Cannot reject H0", "Reject H0")
    temp["Comment"] = np.where(temp["AB Hypothesis"] == "Cannot reject H0", "A/B groups are similar", "A/B groups are not similar")
    
    # create column
    if (ntA == False) & (ntB == False):
        temp["Homogeneity"] = np.where(leveneTest == False, "Yes", "No")
        temp = temp[["Scenario", "Test Type", "Homogeneity","AB Hypothesis", "p-value", "Comment"]]
    else:
        temp = temp[["Scenario", "Test Type", "AB Hypothesis", "p-value", "Comment"]]
    
    return temp

def shapiro_df(df, col):
    from scipy.stats import shapiro
    import pandas as pd
    
    temp = pd.DataFrame({
    })

    # check normality
    col_vals = df[col].unique()
    
    for i in range(len(col_vals)):
        
        temp1 = pd.DataFrame({
            "Scenario":[""],
            "n":[0],
            "p-value":[0],
            "Normality?":[""]
        })

        ntA = shapiro(df[df[col] == col_vals[i]]['mean'])[1]

        temp1['Scenario'] = col_vals[i]
        temp1['n'] = len(df[df[col] == col_vals[i]]['mean'])
        temp1['p-value'] = ntA
        temp1['Normality?'] = "Not of normal distribution" if ntA < 0.05 \
            else "Of normal distribution"
        
        temp = pd.concat((temp, temp1), axis = 0)

    return temp

def df_id(df_i, status):

    df = df_i[df_i['type']=='0/None/before'][df_i[df_i['type']==\
        '0/None/before']['user_id'].isin(df_i[df_i['type']==\
            status]['user_id'])]
    return df