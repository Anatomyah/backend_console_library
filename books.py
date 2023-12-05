from dbhandler import DataBaseHandler
from config import BOOKS_FIELDNAMES, RE_PATT_D, ERRORS
from helpers import query_db, regex_check, check_number, auto_log
from errors import InvalidEntry, InvalidPublicationYear
from datetime import timedelta


class Book(DataBaseHandler):
    def __init__(self, title, author_pname, author_lname, year_published, book_type, id_=None, override_id=False):
        self.title = title
        self.auth_pname = author_pname
        self.auth_lname = author_lname
        self.published = year_published
        self.book_type = book_type

        if override_id is False:
            rowid = query_db(query="SELECT MAX(rowid) FROM books", result=True)[0][0]
            if not rowid:
                self.id = 1
            else:
                self.id = str(int(rowid) + 1)
        if override_id:
            self.id = id_

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_val):
        valid_res = regex_check(RE_PATT_D['title'], new_val)

        if not valid_res:
            auto_log(f"{InvalidEntry}", f"{ERRORS['title']}", error=True)
            raise InvalidEntry(f"{ERRORS['title']}")
        else:
            self._title = new_val

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
        duration = None

        if str(self._book_type) == '1':
            duration = 10
        elif str(self._book_type) == '2':
            duration = 5
        elif str(self._book_type) == '3':
            duration = 2

        return timedelta(days=duration)

    def obj_to_values(self):
        return (f'{self.id}', f'{self.title}', f'{self.auth_pname}', f'{self._auth_lname}',
                f'{self.published}', f'{self.book_type}')

    def get_table(self):
        return 'books'

    def get_fieldnames(self):
        return BOOKS_FIELDNAMES

    def get_id(self):
        return self.id

    def show(self):
        print(f"\n*** Book Details ***\n"
              f"ID: {self.id}\n"
              f"Name: {self._title}\n"
              f"Author: {self._auth_pname} {self._auth_lname}\n"
              f"Publication Year: {self._published}\n"
              f"Type: {self._book_type}")

    @classmethod
    def load_from_db(cls):
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
