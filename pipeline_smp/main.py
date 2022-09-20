# load modules
import logging
import psutil
import yaml
import inspect

# load functions
import src.extract as extract
import src.load as load
import conf.config as conf
import utils.validate as validate

# load transform function. Change utils.*** if another transformation
# function is needed. (e.g. change to utils.credit_trans1 if user 
# wants to use another transformation function)
import utils.credit_trans as transform

# logger
logging.basicConfig(filename = 'log/run.log',
    format='%(asctime)s %(name)s L%(lineno)d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

def main(config_db):
    # with open("log.txt", "a") as log:
    try:
        # get yaml data
        CONN_STR = conf.conn_str(config_db, 'db')
        dest = conf.conn_str(config_db, 'sch_tb')
        src = conf.dir_str(config_db)
        tr = conf.opts_str(config_db)[0]
        vl = conf.opts_str(config_db)[1]

        # extract data
        logger.info('Extracting file from ' + src[0])
        if src[1].lower() == 'local':
            df = extract.csv_from_local(src[0])
        logger.info('Extraction CPU usage {}%'.format(psutil.cpu_percent()))

        # transform data
        if tr == True:
            logger.info(f"Setting/transforming data types.")
            df = getattr(transform, 'trans')(df)
        else:
            logger.info(f"No transformation specified, initiating DF load.")
        logger.info('Transform CPU usage {}%'.format(psutil.cpu_percent()))

        # validate data
        tests = [x.__name__ for x in validate.__dict__.values() if inspect.isfunction(x)]
        tests = [test for test in tests if test not in ['test']]
        if vl == True:
            logger.info(f"Validating data.")
            validate.test(df, tests)
        else:
            logger.info(f"No transformation specified, initiating DF load.")
        logger.info('Validation CPU usage {}%'.format(psutil.cpu_percent()))

        # load data
        logger.info(f"Loading data...")
        load.to_tbl(df, dest, CONN_STR)
        logger.info(f"Data succesfully loaded.")
        logger.info('Load CPU usage {}%'.format(psutil.cpu_percent()))
        logger.info("ETL job complete.")

    except Exception as e:
        logger.error('ETL failed. Error: '+ str(e))
        logger.info("ETL job failed.")

if __name__ == '__main__':
    # load yaml
    with open("conf/config.yaml", "r") as file:
        config = yaml.safe_load(file)

    # start etl
    logger.info('Initiating ETL pipeline!')
    main(config)