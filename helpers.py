import logging
import sqlite3
from datetime import date
import re
from config import DATABASE, LOGGER
from errors import InvalidEntry, InvalidAge, InvalidPublicationYear, IdNotExist, IdAlreadyExists, BookNotAvailable


def regex_check(pattern, text):
    return bool(re.match(pattern, str(text), re.IGNORECASE))


def check_date(loan_date, date_):
    return bool(loan_date < date.fromisoformat(date_) < date.today())


def check_number(user_input, num_type):
    mini = None
    maxi = None

    if num_type == 'age':
        mini = 4
        maxi = 120
    if num_type == 'year':
        mini = 1700
        maxi = date.today().year
    if num_type == 'month':
        mini = 1
        maxi = 12
    if num_type == 'day':
        mini = 1
        maxi = 31

    return bool(mini < int(user_input) <= maxi)


def align_input(text, pattern, error, number=None):
    user_input = None
    valid_num = True
    valid_res = False

    while not valid_res or not valid_num:
        user_input = input(f"{text}")
        if user_input == '0':
            return '0'
        else:
            valid_res = regex_check(pattern, user_input)

        if number and valid_res:
            valid_num = check_number(user_input, number)

        try:
            if not valid_res:
                raise InvalidEntry
        except Exception as e:
            auto_log(f"{error}", e, error=True)
            print(e, error)

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

    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        if parameters:
            c.execute(query, parameters)
        else:
            c.execute(query)

        if result:
            res = c.fetchall()

        conn.commit()

        return res


def auto_log(msg, log_id, error=False):
    logging.basicConfig(filename=LOGGER, level=logging.DEBUG, format='%(levelname)s:%(asctime)s:%(message)s')
    if error:
        logging.error(f"{msg}: Error: {log_id}")
    else:
        logging.info(f"{msg}: ID: {log_id}")


def get_by_id(object_id, table):
    query = f"SELECT * FROM {table} WHERE id = ?;"

    res = query_db(query=query, parameters=(object_id,), result=True)[0]

    if len(res) == 0:
        raise IdNotExist

    return res


def check_loans(self):
    query = None

    if self.__class__.__name__ == 'Customer':
        query = f"SELECT l.id, l.custID, l.bookID, l.loandate, l.expected_returndate, l.actual_returndate " \
                f"FROM loans l " \
                f"JOIN customers c ON l.custID = c.id WHERE c.id = {self.id};"

    elif self.__class__.__name__ == 'Book':
        query = f"SELECT l.id, l.custID, l.bookID, l.loandate, l.expected_returndate, l.actual_returndate " \
                f"FROM loans l " \
                f"JOIN books b ON l.bookID = b.id WHERE b.id = {self.id};"

    data_output = query_db(query=query, result=True)
    final_output = []

    for loan in data_output:
        if loan[5] == 'Not returned':
            final_output.append(loan)

    assert len(final_output) == 0, "Unable to delete. " \
                                   "The item you are trying to delete has open loans related to it."


def check_id(self=None, table=None, object_id=None, test=False):
    if self:
        object_id = self.get_id()
        table = self.get_table()

    query = f"SELECT * FROM {table} WHERE id = ?;"
    data_output = query_db(query=query, parameters=(object_id,), result=True)

    if not test:
        if len(data_output) > 0:
            raise IdAlreadyExists

    return True


def is_available(book_id):
    query = f"SELECT * FROM loans WHERE bookID = ?;"
    loans = query_db(query=query, parameters=(book_id,), result=True)
    loan = None
    flag = False

    for l in loans:
        if l[5] == 'Not returned':
            flag = True
            loan = l
            break

    if flag:
        raise BookNotAvailable(f"This book is currently on loan")
