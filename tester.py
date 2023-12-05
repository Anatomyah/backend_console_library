import unittest
from customers import Customer
from books import Book
from loans import Loan
from helpers import check_id, check_loans


class MyTestCase(unittest.TestCase):
    """
       Unit tests for the library management system.

       This class contains tests to verify the functionality of the Customer, Book,
       and Loan classes, and their interaction with the database. It also tests
       helper functions like check_id and check_loans to ensure they work correctly.
       """

    def test_customer(self):
        """
              Test the Customer class's creation, saving, retrieval, and deletion.
              """
        # Test customer creation and type.
        c = Customer(id_='123456789', p_name='Test', l_name='Testing', city='Nowhere', age='66')
        # Asserting that the created object is indeed an instance of Customer.
        self.assertIsInstance(c, Customer, "Customer object created successfully")

        # Asserting that the save operation returns True, indicating successful save in the database.
        save_result = c.save()
        self.assertTrue(save_result, "Save Successful")

        # Asserting that the customer can be found in the database after being saved.
        found_customer = check_id(self=c, test=True)
        self.assertTrue(found_customer, "Object found in Database")

        # Asserting that the delete operation returns True, indicating successful deletion from the database.
        delete_result = c.delete()
        self.assertTrue(delete_result, "Delete Successful")

    def test_book(self):
        """
        Test the Book class's creation, saving, retrieval, and deletion.
        """
        # Similar testing structure as for the Customer class.
        b = Book(title='Something', author_pname='Test', author_lname='Testing', year_published='1989', book_type='1')
        self.assertIsInstance(b, Book, "Book object created succesfully")

        save_result = b.save()
        self.assertTrue(save_result, "Save Successful")

        found_book = check_id(self=b, test=True)
        self.assertTrue(found_book, "Object found in Database")

        delete_result = b.delete()
        self.assertTrue(delete_result, "Delete Successful")

    def test_loan(self):
        """
             Test the Loan class's creation, saving, retrieval, and deletion.
             """
        # Testing the creation, saving, retrieval, and deletion for Loan class.
        # Also involves creating and deleting Customer and Book instances.
        c = Customer(id_='123456789', p_name='Test', l_name='Testing', city='Nowhere', age='66')
        c.save()
        b = Book(title='Something', author_pname='Test', author_lname='Testing', year_published='1989', book_type='1')
        b.save()
        l = Loan(customer_id='123456789', book_id='1')

        self.assertIsInstance(l, Loan, "loan object created succesfully")

        save_result = l.save()
        self.assertTrue(save_result, "Save Successful")

        found_loan = check_id(self=l, test=True)
        self.assertTrue(found_loan, "Object found in Database")

        delete_result = l.delete()
        self.assertTrue(delete_result, "Delete Successful")
        b.delete()
        c.delete()

    def test_del_customer_with_loan(self):
        """
               Test the behavior of trying to delete a customer who has an active loan.
               """
        # Tests if an AssertionError is raised when attempting to delete
        # a customer with an active loan.
        c = Customer(id_='123456789', p_name='Test', l_name='Testing', city='Nowhere', age='66')
        c.save()
        b = Book(title='Something', author_pname='Test', author_lname='Testing', year_published='1989', book_type='1')
        b.save()
        l = Loan(customer_id='123456789', book_id='1')
        l.save()

        # Attempting to delete a customer with an active loan.
        # This should raise an AssertionError according to the business logic.
        with self.assertRaises(AssertionError):
            check_loans(b)

        # Cleaning up by deleting the loan, book, and customer from the database.
        l.delete()
        b.delete()
        c.delete()

    def test_del_book_with_loan(self):
        """
              Test the behavior of trying to delete a book that is currently on loan.
              """
        # Tests if an Exception is raised when attempting to delete
        # a book that is currently on loan.
        c = Customer(id_='123456789', p_name='Test', l_name='Testing', city='Nowhere', age='66')
        c.save()
        b = Book(title='Something', author_pname='Test', author_lname='Testing', year_published='1989',
                 book_type='1')
        b.save()
        l = Loan(customer_id='123456789', book_id='1')
        l.save()

        # Attempting to delete a book on loan.
        # This should raise a generic Exception according to the business logic.
        with self.assertRaises(Exception):
            check_loans(b)

        # Cleaning up by deleting the loan, book, and customer from the database.
        l.delete()
        b.delete()
        c.delete()


if __name__ == '__main__':
    unittest.main()
