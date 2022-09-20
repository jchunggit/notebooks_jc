import logging

logger = logging.getLogger(__name__)

def conn_str(config, type):
    try:
        conf = config['DATABASE']
        if all(len(str(value)) > 0 for value in conf.values()) == True:
            if type == 'db':
                db_str = conf['DB_TYPE'] + '://' + conf['USERNAME'] + \
                    ':' + conf['PASSWORD'] + '@' + conf['HOST'] + \
                        ':' + str(conf['PORT']) + '/' + conf['DB_NAME']
            elif type == 'sch_tb':
                db_str = conf['DB_NAME'] + '.' + conf['SCHEMA'] + '.' + conf['TABLE']
            return db_str
    except Exception as e:
        logger.error('YAML parsing for DB connection failed. Is there a missing value on the YAML file? Error: '+ str(e))

def dir_str(config):
    try:
        conf = config['DATA_SOURCE']
        if all(len(value) > 0 for value in conf.values()) == True:
            dir_str = conf['FULL_DIR']
            src_type = conf['TYPE']
            return [dir_str, src_type]
    except Exception as e:
        logger.error('YAML parsing for data source parsing failed. Is there a missing value on the YAML file? Error: '+ str(e))

def opts_str(config):
    try:
        conf = config['OPTIONS']
        opts_out = conf['TRANSFORM'], conf['VALIDATE']
        if True or False in opts_out:
            return opts_out
    except Exception as e:
        logger.error('YAML parsing for DB transform failed. Is there a missing value on the YAML file? Error: '+ str(e))