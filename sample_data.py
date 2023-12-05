from customers import Customer
from books import Book
from loans import Loan
from helpers import query_db

CUSTOMER_LST = [('123456789', 'Tom', 'Kedar', 'Jerusalem', '33'), ('123456788', 'Moshe', 'Cohen', 'Jerusalem', '28'),
                ('123456787', 'Refael', 'Bitton', 'Jerusalem', '45'),
                ('123456786', 'Avishai', 'Derii', 'Jerusalem', '12'),
                ('123456785', 'Tal', 'Karo', 'Jerusalem', '8')]

BOOK_LST = [('The Fellowship of the ring', 'J.R.R.', 'Tolkien', '1954', '1'), ('1984', 'Aldus', 'Huxley', '1949', '1'),
            ('Moby Dick', 'Herman', 'Melville', '1851', '2'),
            ('Harry Potter', 'J.K.', 'Rowling', '1997', '2'),
            ('Animal Farm', 'George', 'Orwell', '1945', '3'),
            ('Alice in Wonderland', 'Louis', 'Carolle', '1865', '2'),
            ('Le Petit Prince', 'Antoine', 'de Saint-Exupery', '1865', '3')]

LOAN_LST = [('123456789', '1'), ('123456788', '2'), ('123456787', '3'), ('123456786', '4'), ('123456785', '5')]


def create_sample_data():
    for customer in CUSTOMER_LST:
        c = Customer(id_=customer[0], p_name=customer[1], l_name=customer[2], city=customer[3], age=customer[4])
        c.save()

    for book in BOOK_LST:
        b = Book(title=book[0], author_pname=book[1], author_lname=book[2], year_published=book[3],
                 book_type=book[4])
        b.save()

    for loan in LOAN_LST:
        l = Loan(customer_id=loan[0], book_id=loan[1])
        l.save()

    query_db(query = "INSERT INTO loans (id, custID, bookID, loandate, expected_returndate, actual_returndate)"
                     " VALUES (6, 123456789, 6, '2023-04-05', '2023-04-10', 'Not returned');")

    query_db(query= "INSERT INTO loans (id, custID, bookID, loandate, expected_returndate, actual_returndate)"
                     " VALUES (7, 123456789, 7, '2023-04-12', '2023-04-14', 'Not returned');")


