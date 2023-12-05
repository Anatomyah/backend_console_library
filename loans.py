from dbhandler import DataBaseHandler
from config import LOAN_FIELDNAMES, RE_PATT_D, ERRORS
from helpers import get_by_id, query_db, auto_log, regex_check, check_date
from errors import InvalidEntry, InvalidDate
from datetime import date
from customers import Customer
from books import Book


class Loan(DataBaseHandler):
    """
        Represents a loan record in the library system.

        This class provides functionalities to manage loan records, including creation,
        retrieval, update, and deletion of loan records in the database.

        Inherits from DataBaseHandler and implements its abstract methods.

        Attributes:
            id (str): Unique identifier of the loan.
            _customer (Customer): Customer object associated with the loan.
            _book (Book): Book object associated with the loan.
            loan_date (date): Date when the loan was made.
            expected_return_date (date): Expected date for returning the loaned book.
            _actual_return_date (date or str): Actual return date of the loaned book or 'Not returned'.
        """

    def __init__(self, customer_id, book_id, loan_date=None, expected_return_date=None,
                 actual_return_date=None, loan_id=None, override_id=False):
        """
        Initializes a new Loan object.

        Parameters:
            customer_id (str): ID of the customer.
            book_id (str): ID of the book.
            loan_date (date, optional): Date when the loan was made. Defaults to today's date if not provided.
            expected_return_date (date, optional): Expected return date. Calculated based on book type if not provided.
            actual_return_date (date or str, optional): Actual return date of the book. Defaults to 'Not returned'.
            loan_id (str, optional): Unique identifier for the loan. Auto-generated if not provided.
            override_id (bool): Flag to indicate whether to use the provided loan_id or generate a new one.
        """

        self.customer = customer_id
        self.book = book_id

        if override_id is False:
            rowid = query_db(query="SELECT MAX(rowid) FROM loans", result=True)[0][0]
            if not rowid:
                self.id = 1
            else:
                self.id = str(int(rowid) + 1)
            self.loan_date = date.today()
            self.expected_return_date = self.loan_date + self._book.get_book_type_duration()
            self.actual_return_date = 'Not returned'
        if override_id:
            self.id = loan_id
            self.loan_date = loan_date
            self.expected_return_date = expected_return_date
            self.actual_return_date = actual_return_date

    # Property definitions for customer, book, and actual_return_date...
    @property
    def customer(self):
        return self._customer

    @customer.setter
    def customer(self, new_val):
        valid_res = regex_check(RE_PATT_D['custID'], new_val)

        if not valid_res:
            auto_log(f"{InvalidEntry}", f"{ERRORS['custID']}", error=True)
            raise InvalidEntry(f"{ERRORS['custID']}")
        else:
            data = get_by_id(new_val, table='customers')

        self._customer = Customer(id_=data[0], p_name=data[1], l_name=data[2], city=data[3], age=data[4])

    @property
    def book(self):
        return self._book

    @book.setter
    def book(self, new_val):
        valid_res = regex_check(RE_PATT_D['bookID'], new_val)

        if not valid_res:
            auto_log(f"{InvalidEntry}", f"{ERRORS['bookID']}", error=True)
            raise InvalidEntry(f"{ERRORS['bookID']}")
        else:
            data = get_by_id(new_val, table='books')

        self._book = Book(title=data[1], author_pname=data[2], author_lname=data[3],
                          year_published=data[4], book_type=data[5], id_=data[0], override_id=True)

    @property
    def actual_return_date(self):
        return self._actual_return_date

    @actual_return_date.setter
    def actual_return_date(self, new_val):
        if new_val == 'Not returned':
            self._actual_return_date = 'Not returned'
        else:
            valid_res = regex_check(RE_PATT_D['date'], new_val)
            valid_date = check_date(loan_date=self.loan_date, date_=new_val)

            if not valid_res:
                auto_log(f"{InvalidEntry}", f"{ERRORS['date']}", error=True)
                raise InvalidEntry(f"{ERRORS['date']}")
            elif not valid_date:
                auto_log(f"{InvalidDate}", InvalidDate.__name__, error=True)
                raise InvalidDate
            else:
                date_object = date.fromisoformat(new_val)

            self._actual_return_date = date_object

    def obj_to_values(self):
        return (f'{self.id}', f'{self._customer._id}', f'{self._book.id}',
                f'{self.loan_date}', f'{self.expected_return_date}', f'{self._actual_return_date}')

    # Implementation of abstract methods from DataBaseHandler...
    def get_table(self):
        return 'loans'

    def get_fieldnames(self):
        return LOAN_FIELDNAMES

    def get_id(self):
        return self.id

    def show(self):
        """
               Display the details of the loan record.
               """
        print(f"\n*** Loan Details ***\n"
              f"ID: {self.id}\n"
              f"Customer: {self._customer.id}\n"
              f"Book: ID: {self._book.id}, Title: {self._book._title}\n"
              f"Loan date: {self.loan_date}\n"
              f"Expected return date: {self.expected_return_date}\n"
              f"Actual return date: {self._actual_return_date}")

    @classmethod
    def load_from_db(cls):
        """
             Class method to load loan records from the database and create Loan objects.

             Returns:
                 list: A list of Loan objects loaded from the database.
             """
        client_data = cls.load(table='loans')

        objects = []
        for row in client_data:
            objects.append(cls(customer_id=row[1],
                               book_id=row[2],
                               loan_date=row[3],
                               expected_return_date=row[4],
                               actual_return_date=row[5],
                               loan_id=row[0], override_id=True
                               ))

        return objects

    @classmethod
    def create_loan_table(cls):
        """
               Class method to create the 'loans' table in the database if it does not exist.
               """
        query = """
        CREATE TABLE IF NOT EXISTS loans (
            id TEXT PRIMARY KEY,
            custID TEXT NOT NULL,
            bookID TEXT NOT NULL,
            loandate TEXT NOT NULL,
            expected_returndate TEXT NOT NULL,
            actual_returndate TEXT NOT NULL,
            FOREIGN KEY (custID) REFERENCES customers (id) ON DELETE RESTRICT,
            FOREIGN KEY (bookID) REFERENCES books (id) ON DELETE RESTRICT
        );
        """

        foreign_key_query = "PRAGMA foreign_keys = ON;"

        query_db(query=query)
        query_db(query=foreign_key_query)
