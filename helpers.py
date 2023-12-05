import logging
import sqlite3
from datetime import date
import re
from config import DATABASE, LOGGER
from errors import InvalidEntry, InvalidAge, InvalidPublicationYear, IdNotExist, IdAlreadyExists, BookNotAvailable


def regex_check(pattern, text):
    """
    Checks if a given text matches a specified regular expression pattern.

    Args:
        pattern (str): The regular expression pattern to match against.
        text (str): The text to be validated.

    Returns:
        bool: True if the text matches the pattern, False otherwise.
    """
    return bool(re.match(pattern, str(text), re.IGNORECASE))


def check_date(loan_date, date_):
    """
    Validates if a given date falls within a specific range.

    Args:
        loan_date (date): The starting date to compare against.
        date_ (str): The date in string format to be checked.

    Returns:
        bool: True if date_ is after loan_date and before today's date, False otherwise.
    """
    # Comparing the input date (date_) against the loan_date and today's date
    # Ensuring that the date_ is after the loan_date and before today's date
    return bool(loan_date < date.fromisoformat(date_) < date.today())


def check_number(user_input, num_type):
    """
    Validates if a given input falls within the specified numeric range based on type.

    Args:
        user_input (str): The numeric input as a string.
        num_type (str): The type of number to check ('age', 'year', 'month', 'day').

    Returns:
        bool: True if the input is within the specified range, False otherwise.
    """
    mini = None
    maxi = None

    # Setting minimum and maximum values based on num_type
    if num_type == 'age':
        mini, maxi = 4, 120
    elif num_type == 'year':
        mini, maxi = 1700, date.today().year
    elif num_type == 'month':
        mini, maxi = 1, 12
    elif num_type == 'day':
        mini, maxi = 1, 31

    # Checking if the user_input falls within the specified range
    return bool(mini < int(user_input) <= maxi)


def align_input(text, pattern, error, number=None):
    user_input = None
    valid_num = True
    valid_res = False

    while not valid_res or not valid_num:
        user_input = input(f"{text}")  # Prompting user for input
        if user_input == '0':  # Allowing exit option
            return '0'

        valid_res = regex_check(pattern, user_input)  # Validating against regex pattern

        if number and valid_res:  # If additional number check is required
            valid_num = check_number(user_input, number)  # Performing numeric validation

        # Handling invalid input cases with appropriate error messages
        try:
            if not valid_res:
                raise InvalidEntry
        except Exception as e:
            auto_log(f"{error}", e, error=True)
            print(e, error)

        # Additional handling for numeric type errors
        try:
            if not valid_num:
                if number == 'age':
                    raise InvalidAge
                if number == 'year':
                    raise InvalidPublicationYear
        except Exception as e:
            auto_log(f"ERROR: ", e, error=True)
            print(e)

    return user_input


def query_db(query, parameters=None, db=DATABASE, result=False):
    res = None

    with sqlite3.connect(db) as conn:  # Connecting to the database
        c = conn.cursor()
        if parameters:
            c.execute(query, parameters)  # Executing the query with parameters
        else:
            c.execute(query)  # Executing the query without parameters

        if result:
            res = c.fetchall()  # Fetching results if required

        conn.commit()  # Committing the transaction


def auto_log(msg, log_id, error=False):
    """
      Logs a message to a specified log file.

      Args:
          msg (str): The message to log.
          log_id (str): An identifier associated with the log message.
          error (bool): If True, logs as an error; otherwise, logs as info.
      """
    # Setting up logging configuration
    logging.basicConfig(filename=LOGGER, level=logging.DEBUG, format='%(levelname)s:%(asctime)s:%(message)s')
    if error:
        logging.error(f"{msg}: Error: {log_id}")  # Logging error messages
    else:
        logging.info(f"{msg}: ID: {log_id}")  # Logging info messages


def get_by_id(object_id, table):
    """
       Fetches a record by ID from a specified table.

       Args:
           object_id (str): The ID of the record to fetch.
           table (str): The table name to fetch the record from.

       Returns:
           tuple: The fetched record.

       Raises:
           IdNotExist: If the record does not exist.
       """
    # Fetching record by ID and handling non-existence
    query = f"SELECT * FROM {table} WHERE id = ?;"

    res = query_db(query=query, parameters=(object_id,), result=True)[0]

    if len(res) == 0:
        raise IdNotExist

    return res


def check_loans(self):
    """
    Checks if there are any active loans associated with a customer or a book.

    This function is part of both the Customer and Book classes.

    Raises:
        AssertionError: If there are active loans preventing deletion of the item.
    """

    query = None

    # Determining the query based on the class of the object calling this method
    if self.__class__.__name__ == 'Customer':
        # If the object is a Customer, prepare a query to check for loans linked to this customer
        query = f"SELECT l.id, l.custID, l.bookID, l.loandate, l.expected_returndate, l.actual_returndate " \
                f"FROM loans l " \
                f"JOIN customers c ON l.custID = c.id WHERE c.id = {self.id};"

    elif self.__class__.__name__ == 'Book':
        # If the object is a Book, prepare a query to check for loans linked to this book
        query = f"SELECT l.id, l.custID, l.bookID, l.loandate, l.expected_returndate, l.actual_returndate " \
                f"FROM loans l " \
                f"JOIN books b ON l.bookID = b.id WHERE b.id = {self.id};"

    # Executing the query to retrieve data from the database
    data_output = query_db(query=query, result=True)
    final_output = []

    # Loop through each loan record
    for loan in data_output:
        # Check if the loan is still active (not returned)
        if loan[5] == 'Not returned':
            # If the loan is active, add it to the final output list
            final_output.append(loan)

    # Assert that there are no active loans; raise an error if there are
    assert len(final_output) == 0, "Unable to delete. " \
                                   "The item you are trying to delete has open loans related to it."


def check_id(self=None, table=None, object_id=None, test=False):
    """
    Checks if an ID already exists in a specified table.

    Args:
        self: The instance of the object (optional).
        table (str): The table name to check in.
        object_id (str): The ID to check.
        test (bool): If True, checks existence without raising an error.

    Returns:
        bool: True if the ID is not already in use, otherwise raises an exception.

    Raises:
        IdAlreadyExists: If the ID already exists in the table.
    """

    # If the function is called from an object instance, get the ID and table from the object
    if self:
        object_id = self.get_id()
        table = self.get_table()

    # SQL query to check for the existence of the ID in the specified table
    query = f"SELECT * FROM {table} WHERE id = ?;"
    # Executing the query
    data_output = query_db(query=query, parameters=(object_id,), result=True)

    # If not in test mode, check if the ID already exists and raise an exception if it does
    if not test:
        if len(data_output) > 0:
            raise IdAlreadyExists

    return True  # Returning True if the ID does not exist or if in test mode


def is_available(book_id):
    """
    Checks if a book is currently available for loan.

    Args:
        book_id (str): The ID of the book to check.

    Raises:
        BookNotAvailable: If the book is currently on loan and not returned.
    """

    # SQL query to get all loans associated with the given book ID
    query = f"SELECT * FROM loans WHERE bookID = ?;"
    # Executing the query
    loans = query_db(query=query, parameters=(book_id,), result=True)

    # Looping through each loan record to check if the book is currently on loan
    for loan in loans:
        # Checking if the book is not returned yet
        if loan[5] == 'Not returned':
            # If the book is not returned, raise an exception indicating it is not available
            raise BookNotAvailable(f"This book is currently on loan")

    # If the book is not on loan, it is available
