from dbhandler import DataBaseHandler
from config import BOOKS_FIELDNAMES, RE_PATT_D, ERRORS
from helpers import query_db, regex_check, check_number, auto_log
from errors import InvalidEntry, InvalidPublicationYear
from datetime import timedelta


class Book(DataBaseHandler):
    """
    Represents a book in the library system.

    Inherits from the DataBaseHandler class and manages book-related data.

    Args:
        title (str): Title of the book.
        author_pname (str): Author's first name.
        author_lname (str): Author's last name.
        year_published (int): Year the book was published.
        book_type (str): Type of the book.
        id_ (int, optional): ID of the book. Auto-generated if not provided.
        override_id (bool, optional): Whether to use the provided id_ or auto-generate.

    Attributes are managed through Python properties to enforce data validation and integrity.
    """

    def __init__(self, title, author_pname, author_lname, year_published, book_type, id_=None, override_id=False):
        # Initializing book attributes
        self.title = title
        self.auth_pname = author_pname
        self.auth_lname = author_lname
        self.published = year_published
        self.book_type = book_type

        # ID assignment logic - auto-generate if not overridden
        if override_id is False:
            rowid = query_db(query="SELECT MAX(rowid) FROM books", result=True)[0][0]
            self.id = str(int(rowid) + 1) if rowid else 1
        if override_id:
            self.id = id_

    @property
    def title(self):
        # Getter for book's title
        return self._title

    @title.setter
    def title(self, new_val):
        # Setter for book's title with validation
        valid_res = regex_check(RE_PATT_D['title'], new_val)

        if not valid_res:
            auto_log(f"{InvalidEntry}", f"{ERRORS['title']}", error=True)
            raise InvalidEntry(f"{ERRORS['title']}")
        else:
            self._title = new_val

    # Similar structure for other properties like author's name, publication year, and book type
    @property
    def auth_pname(self):
        return self._auth_pname

    @auth_pname.setter
    def auth_pname(self, new_val):
        valid_res = regex_check(RE_PATT_D['p_name'], new_val)

        if not valid_res:
            auto_log(f"{InvalidEntry}", f"{ERRORS['p_name']}", error=True)
            raise InvalidEntry(f"{ERRORS['p_name']}")
        else:
            self._auth_pname = new_val

    @property
    def auth_lname(self):
        return self._auth_lname

    @auth_lname.setter
    def auth_lname(self, new_val):
        valid_res = regex_check(RE_PATT_D['l_name'], new_val)

        if not valid_res:
            auto_log(f"{InvalidEntry}", f"{ERRORS['p_name']}", error=True)
            raise InvalidEntry(f"{ERRORS['p_name']}")
        else:
            self._auth_lname = new_val

    @property
    def published(self):
        return self._published

    @published.setter
    def published(self, new_val):
        valid_res = regex_check(RE_PATT_D['pub_year'], new_val)
        valid_num = check_number(new_val, 'year')

        if not valid_res:
            auto_log(f"{InvalidEntry}", f"{ERRORS['pub_year']}", error=True)
            raise InvalidEntry(f"{ERRORS['pub_year']}")
        elif not valid_num:
            auto_log(f"Error: {InvalidPublicationYear}", InvalidPublicationYear.__name__, error=True)
            raise InvalidPublicationYear
        else:
            self._published = new_val

    @property
    def book_type(self):
        return self._book_type

    @book_type.setter
    def book_type(self, new_val):
        valid_res = regex_check(RE_PATT_D['book_type'], new_val)

        if not valid_res:
            auto_log(f"{InvalidEntry}", f"{ERRORS['book_type']}", error=True)
            raise InvalidEntry(f"{ERRORS['book_type']}")
        else:
            self._book_type = new_val

    def get_book_type_duration(self):
        """
              Determines the loan duration based on the book type.

              Returns:
                  timedelta: The duration for which the book can be loaned.
              """
        # Logic to determine loan duration based on book type
        duration = None

        if str(self._book_type) == '1':
            duration = 10
        elif str(self._book_type) == '2':
            duration = 5
        elif str(self._book_type) == '3':
            duration = 2

        return timedelta(days=duration)

    def obj_to_values(self):
        # Convert book object attributes to a tuple for database operations
        return (f'{self.id}', f'{self.title}', f'{self.auth_pname}', f'{self._auth_lname}',
                f'{self.published}', f'{self.book_type}')

    def get_table(self):
        # Method to specify the database table name
        return 'books'

    def get_fieldnames(self):
        # Method to provide the field names for the database table
        return BOOKS_FIELDNAMES

    def get_id(self):
        # Getter for the book's ID
        return self.id

    def show(self):
        """
              Class method to load book data from the database and create book objects.

              Returns:
                  list: A list of Book objects loaded from the database.
              """
        # Loading book data from the database and creating book objects
        print(f"\n*** Book Details ***\n"
              f"ID: {self.id}\n"
              f"Name: {self._title}\n"
              f"Author: {self._auth_pname} {self._auth_lname}\n"
              f"Publication Year: {self._published}\n"
              f"Type: {self._book_type}")

    @classmethod
    def load_from_db(cls):
        """
               Class method to load book data from the database and create book objects.

               Returns:
                   list: A list of Book objects loaded from the database.
               """
        # Loading book data from the database and creating book objects
        client_data = cls.load(table='books')

        objects = []
        for row in client_data:
            objects.append(cls(title=row[1],
                               author_pname=row[2],
                               author_lname=row[3],
                               year_published=row[4],
                               book_type=row[5],
                               id_=row[0], override_id=True
                               ))

        return objects

    @classmethod
    def create_book_table(cls):
        """
               Class method to create the books table in the database if it does not exist.
               """
        # SQL query to create the books table
        query = """
        CREATE TABLE IF NOT EXISTS books (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author_pname TEXT NOT NULL,
            author_lname TEXT NOT NULL,
            publication_year INTEGER NOT NULL,
            type INTEGER NOT NULL
        );
        """

        query_db(query=query)
