import csv
from io import StringIO
import logging
import sqlalchemy
import datetime

logger = logging.getLogger(__name__)
today_date = datetime.datetime.now().strftime("%Y%m%d")

def psql_insert_copy(table, conn, keys, data_iter):
    
    """
    Reference: https://pandas.pydata.org/docs/user_guide/io.html#io-sql-method
    """

    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:

        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ', '.join('"{}"'.format(k) for k in keys)
        if table.schema:
            table_name = '{}.{}'.format(table.schema, table.name)
        else:
            table_name = table.name

        sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(
            table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)

# def schema_exists(engine, schema):
#     with engine.connect() as conn:
#         sql = '''
#             SELECT schema_name
#             FROM information_schema.schemata
#             WHERE table_schema = %s;
#         '''
#         return conn.execute(sql, schema).rowcount

# def db_exists(engine, db):
#     with engine.connect() as conn:
#         sql = '''
#             SELECT exists(SELECT datname 
#             FROM pg_catalog.pg_database 
#             WHERE lower(datname) = lower(%s));
#         '''
#         return conn.execute(sql, db).rowcount

def tbl_exists(engine, schema, table):
    """
    engine: engine defined via sqlalchemy
    schema: schema
    table: table name
    """
    with engine.connect() as conn:
        sql = '''
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = %s
            AND table_name = %s;
        '''
        return conn.execute(sql, schema, table).rowcount


def truncate_tbl(engine, schema, table):
    """
    engine: engine defined via sqlalchemy
    schema: schema
    table: table name
    """
    with engine.connect() as conn:
        sql = f'''
            TRUNCATE TABLE "{schema}"."{table}";
        '''
        conn.execute(sql)

def to_tbl(df, destination, conn_str):
    """
    df: dataframe
    destination: string defined as schema.table
    conn_str: postgres connection str
    """
    try:
        # setup postgres connection
        if conn_str is None:
            raise ValueError("Postgres connection string must be specified.")
        db, schema, table = destination.split(".")
        engine = sqlalchemy.create_engine(conn_str)
        table = table + "_" + today_date

        # check if schema exists
        with engine.connect() as conn:
            if not conn.dialect.has_schema(conn, schema):
                logger.info(f"Schema {schema} does not exist - creating schema {schema}.")
                conn.execute(sqlalchemy.schema.CreateSchema(schema))
            else:
                logger.info(f"Schema {schema} found.")

        # check if table exists, if exists then truncates and will reupload data
        if tbl_exists(engine, schema, table):
            truncate_tbl(engine, schema, table)
            logger.info(f"Table {table} exists! Appending if there is any new data.")
            if_exists = 'append'
        else:
            if_exists = 'fail'
            logger.info(f"Table {table} does not exist. Creating {table}.")

        # write to Postgres database
        with engine.connect() as conn:
            conn.execute("SET statement_timeout = 300000;")
            df.to_sql(table, conn, schema, if_exists=if_exists,
            index=False
            # ,
            # method=psql_insert_copy
            )

    except Exception as e:
        logger.error('ETL failed during load. Error: '+ str(e), exc_info=True)
        raise Exception('Data load failed.')