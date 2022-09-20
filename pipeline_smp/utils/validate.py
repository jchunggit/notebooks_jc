import logging

logger = logging.getLogger(__name__)

def REloan_check(df):
    """
    example of a validation test:
    check if real estate loans variable is 
    less than number of open credit lines
    """
    return (df['NumberRealEstateLoansOrLines'] <= df['NumberOfOpenCreditLinesAndLoans']).all()

def test(df, tests):
    res = []
    for test in tests:
        res.append(eval(test + "(df)"))
        if res[-1]:
            logger.info(f'Validation {test} passed.')
        else:
            logger.info(f'Validation {test} did not pass.')
    return sum(res) == len(res)