import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import datetime
class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'

    def query(self, query = "SELECT CURDATE()", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def about(self, nested=False):    
        query = """select concat(col.table_schema, '.', col.table_name) as 'table',
                          col.column_name                               as column_name,
                          col.column_key                                as is_key,
                          col.column_comment                            as column_comment,
                          kcu.referenced_column_name                    as fk_column_name,
                          kcu.referenced_table_name                     as fk_table_name
                    from information_schema.columns col
                    join information_schema.tables tab on col.table_schema = tab.table_schema and col.table_name = tab.table_name
                    left join information_schema.key_column_usage kcu on col.table_schema = kcu.table_schema
                                                                     and col.table_name = kcu.table_name
                                                                     and col.column_name = kcu.column_name
                                                                     and kcu.referenced_table_schema is not null
                    where col.table_schema not in('information_schema','sys', 'mysql', 'performance_schema')
                                              and tab.table_type = 'BASE TABLE'
                    order by col.table_schema, col.table_name, col.ordinal_position;"""
        results = self.query(query)
        if nested == False:
            return results

        table_info = {}
        for row in results:
            table_info[row['table']] = {} if table_info.get(row['table']) is None else table_info[row['table']]
            table_info[row['table']][row['column_name']] = {} if table_info.get(row['table']).get(row['column_name']) is None else table_info[row['table']][row['column_name']]
            table_info[row['table']][row['column_name']]['column_comment']     = row['column_comment']
            table_info[row['table']][row['column_name']]['fk_column_name']     = row['fk_column_name']
            table_info[row['table']][row['column_name']]['fk_table_name']      = row['fk_table_name']
            table_info[row['table']][row['column_name']]['is_key']             = row['is_key']
            table_info[row['table']][row['column_name']]['table']              = row['table']
        return table_info



    def createTables(self, purge=False, data_path='flask_app/database/'):
        if purge:
            drop_order = ['feedback', 'skills', 'experiences', 'positions', 'institutions']
            for table in drop_order:
                self.query(f"DROP TABLE IF EXISTS `{table}`;")

        sql_file_order = ['institutions.sql', 'positions.sql', 'experiences.sql', 'skills.sql', 'feedback.sql']
        for sql_file_name in sql_file_order:
            with open(f"{data_path}create_tables/{sql_file_name}", 'r') as file:
                sql_script = file.read()
                self.query(sql_script)

        csv_file_order = ['institutions.csv', 'positions.csv', 'experiences.csv', 'skills.csv']
        for csv_file_name in csv_file_order:
            with open(f"{data_path}initial_data/{csv_file_name}", 'r', newline='', encoding='utf-8-sig') as file:
                csv_data = list(csv.reader(file))
                if not csv_data:
                    continue
                headers = csv_data[0]
                rows = csv_data[1:]
                rows = [row for row in rows if any(field.strip() for field in row)]
                if not rows:
                    continue
                self.insertRows(table=csv_file_name.split('.')[0], columns=headers, parameters=rows)

    
    def insertRows(self, table='table', columns=['x', 'y'], parameters=[['v11', 'v12'], ['v21', 'v22']]):
        sql = f"INSERT INTO `{table}` ({', '.join([f'`{col}`' for col in columns])}) VALUES ({', '.join(['%s'] * len(columns))})"
        cnx = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=self.database,
            charset='latin1'
        )
        cur = cnx.cursor()
        cleaned_parameters = [[None if val.strip().upper() == 'NULL' else val for val in row] for row in parameters if len(row) == len(columns)]
        cur.executemany(sql, cleaned_parameters)
        cnx.commit()
        cur.close()
        cnx.close()

    def getResumeData(self):
        resume_data = {}
        institutions = self.query("SELECT * FROM institutions")
        for institution in institutions:
            inst_id = institution['inst_id']
            resume_data[inst_id] = institution
            resume_data[inst_id]['positions'] = {}
            positions = self.query("SELECT * FROM positions WHERE inst_id = %s", parameters=[inst_id])
            for position in positions:
                position_id = position['position_id']
                resume_data[inst_id]['positions'][position_id] = position
                resume_data[inst_id]['positions'][position_id]['experiences'] = {}
                experiences = self.query("SELECT * FROM experiences WHERE position_id = %s", parameters=[position_id])
                for experience in experiences:
                    experience_id = experience['experience_id']
                    resume_data[inst_id]['positions'][position_id]['experiences'][experience_id] = experience
                    resume_data[inst_id]['positions'][position_id]['experiences'][experience_id]['skills'] = {}
                    skills = self.query("SELECT * FROM skills WHERE experience_id = %s", parameters=[experience_id])
                    for skill in skills:
                        skill_id = skill['skill_id']
                        resume_data[inst_id]['positions'][position_id]['experiences'][experience_id]['skills'][skill_id] = skill
        return resume_data