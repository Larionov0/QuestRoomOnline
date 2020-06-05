import MySQLdb
from .misc import db_user_password
from GameObjects.Exceptions import SingletoneException


class ISaveble:
    """
    Interface
    """
    def save(self):
        pass


class DatabaseManager:
    """
    Singletone
    """
    instance = None

    def __init__(self, host='localhost', user='test_user', passwd=db_user_password, database='QuestRoomOnline', use_this_out_of_class=True):
        if use_this_out_of_class:
            raise SingletoneException("Using out of Class (Singletone)")
        try:
            self._database = MySQLdb.connect(
                host=host,
                user=user,
                passwd=passwd,
                database=database
            )
        except MySQLdb._exceptions.OperationalError as e:
            print(f"Error with connecting: {e}")
            return
        self.cursor = self._create_cursor()
        DatabaseManager.instance = self

    @staticmethod
    def get_instance():
        if DatabaseManager.instance is None:
            return DatabaseManager(use_this_out_of_class=False)
        else:
            return DatabaseManager.instance

    def _create_cursor(self):
        return self._database.cursor()

    def execute(self, query, fetchall=False, commit=False):
        try:
            self.cursor.execute(query)
        except MySQLdb._exceptions.ProgrammingError as e:
            print(f"SQL error: ")
            print(query)
            raise e
            return False
        if fetchall:
            return self.fetchall()
        if commit:
            self.cursor.connection.commit()

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    @staticmethod
    def python_value_to_db_string(value):
        type_ = type(value)
        if type_ is int:
            return str(value)
        elif type_ is str:
            return f"'{value}'"
        elif type_ is bool:
            if value is True:
                return 'true'
            else:
                return 'false'
        elif value is None:
            return 'NULL'

    def insert_row(self, table_name, update_dict):
        query = f"""
        INSERT INTO {table_name} ({', '.join(list(update_dict.keys()))})
        VALUES ({','.join([self.python_value_to_db_string(value) for value in update_dict.values()])})
        """
        self.execute(query, commit=True)

    def get_row(self, table_name, id, primary_str='id'):
        query = f"""
                SELECT *
                FROM {table_name}
                WHERE {primary_str} = {id}
                """
        result = self.execute(query, True)
        if len(result) != 1 or len(result[0]) == 0:
            return None

        return result[0]

    def get_table(self, table_name, columns, where=None):
        columns_str = ",".join(columns)
        query = f"""
                        SELECT {columns_str}
                        FROM {table_name}
                 """
        if where:
            query += "WHERE "+where
        result = self.execute(query, True)
        return result

    def update_row(self, update_dict, table_name, id, primary_str='id'):
        query = f"""
        UPDATE {table_name} 
        SET
        
        """
        for key in update_dict:
            query += f"{key} = {self.python_value_to_db_string(update_dict[key])},\n"
        query = query[:-2]

        query += f"\n WHERE {primary_str} = {id}"
        self.execute(query, commit=True)

    def get_one_value_of_one_table(self, table_name, column_name, id, primary_str='id', ignore_errors=False):
        query = f"""
        SELECT {column_name}
        FROM {table_name}
        WHERE {primary_str} = {id}
        """
        result = self.execute(query, True)
        if len(result) != 1 or len(result[0]) != 1:
            if ignore_errors is False:
                raise Exception("Not one value after executing")
            else:
                return None

        return result[0][0]

    def update_one_value_of_one_table(self, table_name, column_name, value, id, primary_str='id'):
        query = f"""
                UPDATE {table_name}
                SET {column_name} = {self.python_value_to_db_string(value)}
                WHERE {primary_str} = {id}
                """
        self.execute(query, commit=True)

    def many_to_many_set(self, table_name, many_to_many_table_name, target_table_name, id_):
        query = f"""
                SELECT {target_table_name}.id FROM
                (
                SELECT * FROM {many_to_many_table_name}
                WHERE {many_to_many_table_name}.{self.clear__(table_name)}_id = {id_}
                ) as temp
                JOIN {target_table_name} ON temp.{self.clear__(target_table_name)}_id = {target_table_name}.id
                """
        result = self.execute(query, True)
        lst = []
        for row in result:
            lst.append(row[0])
        return lst

    @staticmethod
    def clear__(word):
        if word[-1] == '_':
            return word[:-1]
        else:
            return word
