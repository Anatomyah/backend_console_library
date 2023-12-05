from abc import abstractmethod, ABCMeta
import helpers


class DataBaseHandler(metaclass=ABCMeta):
    @abstractmethod
    def obj_to_values(self):
        pass

    @abstractmethod
    def get_table(self):
        pass

    @abstractmethod
    def get_fieldnames(self):
        pass

    @abstractmethod
    def get_id(self):
        pass

    def load(self=None, table=None, condition=None):
        if condition:
            query = f'SELECT * FROM {table} WHERE {condition};'
        else:
            query = f'SELECT * FROM {table};'

        data_output = helpers.query_db(query=query, result=True)

        return data_output

    def delete(self):
        object_id = self.get_id()
        table = self.get_table()

        query = f"DELETE FROM {table} WHERE id = {object_id};"

        helpers.query_db(query=query)

        return True

    def edit(self, set_clauses: tuple, values):
        object_id = self.get_id()
        table = self.get_table()
        placeholders = ", ".join(clause for clause in set_clauses)

        query = f"UPDATE {table} SET {placeholders} WHERE id = {object_id};"
        helpers.query_db(query=query, parameters= values)

        return True

    def save(self):
        table = self.get_table()
        columns = self.get_fieldnames()
        values = self.obj_to_values()
        placeholders = ', '.join('?' for _ in values)

        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders});"

        helpers.query_db(query=query, parameters=values)

        return True
