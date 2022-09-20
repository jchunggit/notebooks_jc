import logging
import pandas as pd
from os.path import exists

logger = logging.getLogger(__name__)

def csv_from_local(path):
    try:
        if exists(path):
            logger.info(path + ' exists. ')
            return pd.read_csv(path, low_memory=False)
    except Exception as e:
        logger.error('ETL failed during extraction. Error: '+ str(e), exc_info=True)
        raise Exception('Data extract failed.')