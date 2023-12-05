from books import Book
from customers import Customer
from loans import Loan
from primary_menu import menu_navigator


# This is the main entry point of the library management program.
# The program initializes by creating tables for customers, books, and loans,
# and then launches the primary menu for user interaction.
#
# The script relies on the following modules:
# - books: Contains the Book class and related methods.
# - customers: Contains the Customer class and related methods.
# - loans: Contains the Loan class and related methods.
# - primary_menu: Manages the primary user interface and navigation.

if __name__ == '__main__':
    # Create tables for customers, books, and loans in the database.
    # These methods are responsible for setting up the initial database schema,
    # ensuring that the application has the necessary structure to store and
    # retrieve data effectively.

    Customer.create_customer_table()  # Creates the customer table.
    Book.create_book_table()          # Creates the book table.
    Loan.create_loan_table()          # Creates the loan table.

    # Launch the primary menu of the application.
    # The menu_navigator function handles user inputs and navigates through
    # different functionalities of the library management system, such as
    # adding books, registering customers, and managing loans.
    menu_navigator()
