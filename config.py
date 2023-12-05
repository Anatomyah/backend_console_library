# Database file path configuration
DATABASE = r'system_files\library.db'  # Path to the library database file
LOGGER = r'system_files\logger'        # Path to the logger file

# Fieldnames for different tables in the database
BOOKS_FIELDNAMES = 'id, title, author_pname, author_lname, publication_year, type'  # Column names for books table
CUSTOMERS_FIELDNAMES = 'id, p_name, l_name, city, age'  # Column names for customers table
LOAN_FIELDNAMES = 'id, custID, bookID, loandate, expected_returndate, actual_returndate'  # Column names for loan table

# Regular expression patterns for data validation
RE_PATT_D = {
    'custID': r'^\d{6,9}$',  # Pattern for customer ID
    'p_name': r'^[a-z][a-z- .]{1,19}$',  # Pattern for person's first name
    'l_name': r"^[a-z][a-z- .']{1,19}$",  # Pattern for person's last name
    'age': r'^\d{1,3}$',  # Pattern for age
    'city': r'^[a-z][a-z- ]{1,19}$',  # Pattern for city
    'bookID': r'^\d{1,5}$',  # Pattern for book ID
    'title': r"^[a-z0-9][a-z0-9- ,.':]{1,59}$",  # Pattern for book title
    'pub_year': r'^\d{4}$',  # Pattern for publication year
    'book_type': r'^[1-3]$',  # Pattern for book type
    'date': r'^\d{4}-\d{2}-\d{2}$',  # Pattern for date
    'loanID': r'^\d{1,5}$'  # Pattern for loan ID
}

# Custom error messages corresponding to the validation patterns
ERRORS = {'custID': 'Invalid ID number. Must only contain 6-9 numbers.',
          'p_name': 'Invalid first name. Must only contain up to 20 letters.',
          'l_name': 'Invalid last name. Must only contain up to 20 letters.',
          'city': 'Invalid city name. Must only contain up to 20 letters.',
          'age': 'Invalid age. Must only contain between 1-3 numbers.',
          'bookID': 'Invalid book ID. Must only contain 1-5 numbers.',
          'title': 'Invalid book name. Must only contain up to 60 letters.',
          'pub_year': 'Invalid publication year. Must only contain 4 numbers (Example: 1989).',
          'book_type': 'Invalid book type. Valid types: 1, 2, 3',
          'date': 'Invalid date. Date must be in the (YYYY-MM-DD) format.',
          'loanID': 'Invalid loan ID. Must only contain 1-5 numbers.'}
