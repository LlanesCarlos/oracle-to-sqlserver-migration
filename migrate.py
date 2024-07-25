import cx_Oracle
import jaydebeapi
import jpype
from datetime import datetime
import progressbar as pbar2

# ANSI escape codes for colored output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Oracle DB connection configuration
config_db = {
    'user': 'your_username',
    'password': 'your_password',
    'dsn': 'your_dsn',
    'host': 'your_host',
    'port': 'your_port',
    'service_name': 'your_service_name'
}

# Oracle DB connection
print(f"{bcolors.WARNING}Connecting to Oracle database...{bcolors.ENDC}")
oracle_dsn = cx_Oracle.makedsn(config_db['host'], config_db['port'], service_name=config_db['service_name'])
oracle_conn = cx_Oracle.connect(user=config_db['user'], password=config_db['password'], dsn=oracle_dsn)
oracle_cursor = oracle_conn.cursor()
print(f"{bcolors.WARNING}Oracle database connection established.{bcolors.ENDC}")

# JDBC driver and connection details
driver_class = 'com.database.jdbc.Driver'
driver_path = '/path/to/your/jdbc_driver.jar'  # Update with your JDBC driver path
url = 'jdbc:database://your_host;databaseName=your_database;trustServerCertificate=true'
user = 'your_username'
password = 'your_password'

# Start the JVM with the driver
print(f"{bcolors.WARNING}Starting JVM...{bcolors.ENDC}")
jpype.startJVM(classpath=[driver_path])
print(f"{bcolors.WARNING}JVM started.{bcolors.ENDC}")

# SQL Server DB connection
print(f"{bcolors.WARNING}Connecting to SQL Server database...{bcolors.ENDC}")
sql_server_conn = jaydebeapi.connect(driver_class, url, [user, password], driver_path)
sql_server_cursor = sql_server_conn.cursor()
print(f"{bcolors.WARNING}SQL Server database connection established.{bcolors.ENDC}")

# Mapping of Oracle tables to SQL Server tables
table_mapping = {
    'ORACLE_SCHEMA.TABLE1': 'SQL_SERVER_SCHEMA.TABLE1',
    'ORACLE_SCHEMA.TABLE2': 'SQL_SERVER_SCHEMA.TABLE2',
    'ORACLE_SCHEMA.TABLE3': 'SQL_SERVER_SCHEMA.TABLE3'
}

# Mapping of column names between Oracle and SQL Server, excluding columns that should not be migrated
column_mapping = {
    'ORACLE_SCHEMA.TABLE1': {
        'COLUMN1': 'COLUMN1',
        'COLUMN2': 'COLUMN2',
        'COLUMN3': 'COLUMN3'
    },
    'ORACLE_SCHEMA.TABLE2': {
        'COLUMN1': 'COLUMN1',
        'COLUMN2': 'COLUMN2',
        'COLUMN3': 'COLUMN3'
    },
    'ORACLE_SCHEMA.TABLE3': {
        'COLUMN1': 'COLUMN1',
        'COLUMN2': 'COLUMN2',
        'COLUMN3': 'COLUMN3'
    }
}

# Function to convert datetime objects to strings
def convert_datetime_to_str(row):
    return [
        val.strftime('%Y-%m-%d %H:%M:%S') if isinstance(val, datetime) else val
        for val in row
    ]

# Function to truncate tables in SQL Server
def truncate_table(sql_server_table):
    print(f"{bcolors.WARNING}Truncating table {sql_server_table}...{bcolors.ENDC}")
    sql_server_cursor.execute(f"TRUNCATE TABLE {sql_server_table}")
    sql_server_conn.commit()

# Function to insert data into SQL Server
def insert_data(oracle_table, sql_server_table):
    print(f"{bcolors.WARNING}Starting data insertion into {sql_server_table}...{bcolors.ENDC}")
    try:
        # SELECT from Oracle
        print(f"{bcolors.WARNING}Executing SELECT query on Oracle table {oracle_table}...{bcolors.ENDC}")
        oracle_cursor.execute(f"SELECT * FROM {oracle_table}")
        oracle_columns = [desc[0] for desc in oracle_cursor.description]
        oracle_rows = oracle_cursor.fetchall()
        oracle_rows = [convert_datetime_to_str(row) for row in oracle_rows]

        # Map columns
        sql_server_columns = column_mapping[oracle_table]
        columns = ', '.join(sql_server_columns.values())
        placeholders = ', '.join(['?'] * len(sql_server_columns))
        insert_query = f"INSERT INTO {sql_server_table} ({columns}) VALUES ({placeholders})"

        # Insert data into SQL Server
        print(f"{bcolors.WARNING}Executing inserts on SQL Server table {sql_server_table}...{bcolors.ENDC}")
        total_rows = len(oracle_rows)
        widgets = [f'{bcolors.OKGREEN}Progress of table {sql_server_table}:{bcolors.ENDC}', pbar2.Percentage(), ' ', pbar2.Bar(marker='#', left='[', right=']'), ' ', pbar2.ETA()]
        progress_bar = pbar2.ProgressBar(widgets=widgets, maxval=total_rows).start()
        for idx, row in enumerate(oracle_rows, 1):
            sql_server_cursor.execute(insert_query, [row[oracle_columns.index(col)] for col in sql_server_columns])
            progress_bar.update(idx)
        progress_bar.finish()

        # Commit changes
        sql_server_conn.commit()
        print(f"{bcolors.OKGREEN}Data insertion into {sql_server_table} completed.{bcolors.ENDC}")
    except Exception as e:
        print(f"{bcolors.FAIL}Error inserting data into {sql_server_table}: {e}{bcolors.ENDC}")

# List of tables to truncate and insert data into, in the specified order
tables_to_truncate = [
    'SQL_SERVER_SCHEMA.TABLE1',
    'SQL_SERVER_SCHEMA.TABLE2',
    'SQL_SERVER_SCHEMA.TABLE3'
]

tables_to_insert = [
    ('ORACLE_SCHEMA.TABLE1', 'SQL_SERVER_SCHEMA.TABLE1'),
    ('ORACLE_SCHEMA.TABLE2', 'SQL_SERVER_SCHEMA.TABLE2'),
    ('ORACLE_SCHEMA.TABLE3', 'SQL_SERVER_SCHEMA.TABLE3')
]

# Truncate tables
for table in tables_to_truncate:
    truncate_table(table)

# Insert data
for oracle_table, sql_server_table in tables_to_insert:
    insert_data(oracle_table, sql_server_table)

# Close database connections
oracle_cursor.close()
oracle_conn.close()
sql_server_cursor.close()
sql_server_conn.close()
jpype.shutdownJVM()
print(f"{bcolors.OKGREEN}Truncate and insert process completed.{bcolors.ENDC}")
