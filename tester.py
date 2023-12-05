import unittest
from customers import Customer
from books import Book
from loans import Loan
from helpers import check_id, check_loans


class MyTestCase(unittest.TestCase):
    def test_customer(self):
        c = Customer(id_='123456789', p_name='Test', l_name='Testing', city='Nowhere', age='66')
        self.assertIsInstance(c, Customer, "Customer object created successfully")

        save_result = c.save()
        self.assertTrue(save_result, "Save Successful")

        found_customer = check_id(self=c, test=True)
        self.assertTrue(found_customer, "Object found in Database")

        delete_result = c.delete()
        self.assertTrue(delete_result, "Delete Successful")

    def test_book(self):
        b = Book(title='Something', author_pname='Test', author_lname='Testing', year_published='1989', book_type='1')
        self.assertIsInstance(b, Book, "Book object created succesfully")

        save_result = b.save()
        self.assertTrue(save_result, "Save Successful")

        found_book = check_id(self=b, test=True)
        self.assertTrue(found_book, "Object found in Database")

        delete_result = b.delete()
        self.assertTrue(delete_result, "Delete Successful")

    def test_loan(self):
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
        c = Customer(id_='123456789', p_name='Test', l_name='Testing', city='Nowhere', age='66')
        c.save()
        b = Book(title='Something', author_pname='Test', author_lname='Testing', year_published='1989', book_type='1')
        b.save()
        l = Loan(customer_id='123456789', book_id='1')
        l.save()

        with self.assertRaises(AssertionError):
            check_loans(b)

        l.delete()
        b.delete()
        c.delete()

    def test_del_book_with_loan(self):
        c = Customer(id_='123456789', p_name='Test', l_name='Testing', city='Nowhere', age='66')
        c.save()
        b = Book(title='Something', author_pname='Test', author_lname='Testing', year_published='1989',
                 book_type='1')
        b.save()
        l = Loan(customer_id='123456789', book_id='1')
        l.save()

        with self.assertRaises(Exception):
            check_loans(b)

        l.delete()
        b.delete()
        c.delete()


if __name__ == '__main__':
    unittest.main()
