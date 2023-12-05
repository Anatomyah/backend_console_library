from books import Book
from customers import Customer
from loans import Loan
from primary_menu import menu_navigator


if __name__ == '__main__':
    Customer.create_customer_table()
    Book.create_book_table()
    Loan.create_loan_table()

    menu_navigator()
