# this fx is NOT used - just a demo file to show that
# another transformation function can be used
import logging

logger = logging.getLogger(__name__)

def trans(df):
    try:
        
        df['SeriousDlqin2yrs'] = df['SeriousDlqin2yrs'].astype('Int64')
        df['age'] = df['age'].astype('Int64')
        df['NumberOfTime30-59DaysPastDueNotWorse'] = df['NumberOfTime30-59DaysPastDueNotWorse'].astype('Int64')
        df['MonthlyIncome'] = df['MonthlyIncome'].astype('Int64')
        df['NumberOfOpenCreditLinesAndLoans'] = df['NumberOfOpenCreditLinesAndLoans'].astype('Int64')
        df['NumberOfTimes90DaysLate'] = df['NumberOfTimes90DaysLate'].astype('Int64')
        df['NumberRealEstateLoansOrLines'] = df['NumberRealEstateLoansOrLines'].astype('Int64')
        df['NumberOfTime60-89DaysPastDueNotWorse'] = df['NumberOfTime60-89DaysPastDueNotWorse'].astype('Int64')
        df['NumberOfDependents'] = df['NumberOfDependents'].astype('Int64')
        df['RevolvingUtilizationOfUnsecuredLines'] = df['RevolvingUtilizationOfUnsecuredLines'].astype(float)
        df['DebtRatio'] = df['DebtRatio'].astype(float)
        columns = [
            'SeriousDlqin2yrs',
            'RevolvingUtilizationOfUnsecuredLines',
            'age',
            'NumberOfTime30-59DaysPastDueNotWorse',
            'DebtRatio',
            'MonthlyIncome',
            'NumberOfOpenCreditLinesAndLoans',
            'NumberOfTimes90DaysLate',	
            'NumberRealEstateLoansOrLines',
            'NumberOfTime60-89DaysPastDueNotWorse',
            'NumberOfDependents']
        df = df[columns].copy()
        return df

    except Exception as e:
        logger.error('ETL failed during transform. Error: '+ str(e), exc_info=True)
        raise Exception('Data transform failed.')