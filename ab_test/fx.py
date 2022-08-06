def ab_t(df, push, mess):
    
    from scipy.stats import shapiro
    import scipy.stats as stats
    import pandas as pd
    import numpy as np
    
    # Split A/B
    groupA = df[(df['change'] == "before")&(df['push_cnt'] == push)&\
        (df['msg_type'] == mess)]
    groupB = df[(df['change'] == "after")&(df['push_cnt'] == push)&\
        (df['msg_type'] == mess)]

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
    temp["Test Type"] = np.where((ntA == False) & (ntB == False), "Parametric", "Non-Parametric")
    temp["AB Hypothesis"] = np.where(temp["AB Hypothesis"] == False, "Cannot reject H0", "Reject H0")
    temp["Comment"] = np.where(temp["AB Hypothesis"] == "Cannot reject H0", "A/B groups are similar", "A/B groups are not similar")
    
    # create column
    if (ntA == False) & (ntB == False):
        temp["Homogeneity"] = np.where(leveneTest == False, "Yes", "No")
        temp = temp[["Test Type", "Homogeneity","AB Hypothesis", "p-value", "Comment"]]
    else:
        temp = temp[["Test Type", "AB Hypothesis", "p-value", "Comment"]]
    
    # print hypothesis
    print("# A/B Testing Hypothesis")
    print("H0: A == B")
    print("H1: A != B", "\n")
    
    return temp