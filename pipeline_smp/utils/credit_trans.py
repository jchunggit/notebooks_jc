import logging

logger = logging.getLogger(__name__)

def trans(df):
    try:
        df = df.iloc[:,1:].copy()

        for col in df.columns:
            if col in ['RevolvingUtilizationOfUnsecuredLines', 'DebtRatio']:
                df[col] = df[col].astype(float)
            else:
                df[col] = df[col].astype('Int64')
        df = df[df.columns].copy()
        return df

    except Exception as e:
        logger.error('ETL failed during transform. Error: '+ str(e), exc_info=True)
        raise Exception('Data transform failed.')