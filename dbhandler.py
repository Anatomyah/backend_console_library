from abc import abstractmethod, ABCMeta
import helpers


class DataBaseHandler(metaclass=ABCMeta):
    """
    Abstract base class for handling database operations.

    This class defines the structure for database handlers including methods
    for object value extraction, query execution, and basic CRUD (Create, Read, Update, Delete) operations.

    Methods defined as abstract must be implemented by subclasses.
    """

    @abstractmethod
    def obj_to_values(self):
        """
        Abstract method to convert an object to a tuple of values for database operations.
        """
        pass

    @abstractmethod
    def get_table(self):
        """
        Abstract method to get the name of the database table associated with the object.
        """
        pass

    @abstractmethod
    def get_fieldnames(self):
        """
        Abstract method to get the field names of the database table associated with the object.
        """
        pass

    @abstractmethod
    def get_id(self):
        """
        Abstract method to get the unique identifier of the object for database operations.
        """
        pass

    def load(self=None, table=None, condition=None):
        """
        Load data from the database.

        Parameters:
            table (str): Name of the database table to query.
            condition (str): Condition for filtering the data.

        Returns:
            list: Data retrieved from the database.
        """
        # Constructing the query based on the presence of a condition
        if condition:
            query = f'SELECT * FROM {table} WHERE {condition};'
        else:
            query = f'SELECT * FROM {table};'

        # Executing the query and returning the result
        data_output = helpers.query_db(query=query, result=True)
        return data_output

    def delete(self):
        """
        Delete the current object from the database.

        Returns:
            bool: True if the operation is successful.
        """
        # Retrieving the object ID and table
        object_id = self.get_id()
        table = self.get_table()

        # Constructing and executing the delete query
        query = f"DELETE FROM {table} WHERE id = {object_id};"
        helpers.query_db(query=query)

        return True

    def edit(self, set_clauses: tuple, values):
        """
        Edit the current object in the database.

        Parameters:
            set_clauses (tuple): Tuple of clauses for setting new values.
            values: New values to be set.

        Returns:
            bool: True if the operation is successful.
        """
        # Retrieving the object ID and table
        object_id = self.get_id()
        table = self.get_table()
        placeholders = ", ".join(clause for clause in set_clauses)

        # Constructing and executing the update query
        query = f"UPDATE {table} SET {placeholders} WHERE id = {object_id};"
        helpers.query_db(query=query, parameters=values)

        return True

    def save(self):
        """
        Save the current object to the database.

        Returns:
            bool: True if the operation is successful.
        """
        # Retrieving table name, field names, and values from the object
        table = self.get_table()
        columns = self.get_fieldnames()
        values = self.obj_to_values()
        placeholders = ', '.join('?' for _ in values)

        # Constructing and executing the insert query
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders});"
        helpers.query_db(query=query, parameters=values)

        return True
