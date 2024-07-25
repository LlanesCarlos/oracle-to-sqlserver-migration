```markdown
# Database Migration Script

This script migrates data from an Oracle database to a SQL Server database using the `cx_Oracle` and `jaydebeapi` libraries. It handles the truncation of existing data in SQL Server tables and inserts new data fetched from Oracle tables. 

## Requirements

- Python 3.x
- `cx_Oracle` library
- `jaydebeapi` library
- `jpype` library
- Oracle client
- JDBC driver for SQL Server
- Progressbar2 library

## Installation

1. Install the required Python libraries:

    ```bash
    pip install cx_Oracle jaydebeapi jpype1 progressbar2
    ```

2. Ensure you have the Oracle client installed and properly configured on your system.

3. Download the JDBC driver for SQL Server and note its path.

## Configuration

Update the `config_db` dictionary with your Oracle database connection details:

```python
config_db = {
    'user': 'your_username',
    'password': 'your_password',
    'dsn': 'your_dsn',
    'host': 'your_host',
    'port': 'your_port',
    'service_name': 'your_service_name'
}
```

Update the JDBC driver details and connection URL for your SQL Server database:

```python
driver_class = 'com.database.jdbc.Driver'
driver_path = '/path/to/your/jdbc_driver.jar'
url = 'jdbc:database://your_host;databaseName=your_database;trustServerCertificate=true'
user = 'your_username'
password = 'your_password'
```

## Table and Column Mapping

Define the mapping of Oracle tables to SQL Server tables in the `table_mapping` dictionary:

```python
table_mapping = {
    'ORACLE_SCHEMA.TABLE1': 'SQL_SERVER_SCHEMA.TABLE1',
    'ORACLE_SCHEMA.TABLE2': 'SQL_SERVER_SCHEMA.TABLE2',
    'ORACLE_SCHEMA.TABLE3': 'SQL_SERVER_SCHEMA.TABLE3'
}
```

Define the mapping of columns for each table in the `column_mapping` dictionary:

```python
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
```

## Usage

1. Ensure that the Oracle and SQL Server databases are accessible.

2. Run the script:
   
    ```bash
    python migrate.py
    ```

## Notes

- The script starts by truncating the specified tables in SQL Server.
- It then fetches data from the corresponding Oracle tables and inserts it into the SQL Server tables.
- Progress of the data insertion is displayed using a progress bar.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [cx_Oracle](https://oracle.github.io/python-cx_Oracle/) library for connecting to Oracle databases.
- [jaydebeapi](https://pypi.org/project/JayDeBeApi/) library for connecting to SQL Server using JDBC.
- [progressbar2](https://pypi.org/project/progressbar2/) library for displaying progress bars.
```

Save this content as `README.md` in the same directory as your script. This file provides an overview of the script, installation instructions, configuration steps, and usage guidelines.
