from helpers import auto_log, get_by_id, align_input, is_available
from config import RE_PATT_D, ERRORS
from loans import Loan
from datetime import date


def loan_menu():
    """
    Presents a menu for managing loans, including options to open, close, or display loans.

    This function prints out a menu with options for the user to select from.
    It checks the user's input for validity and calls the appropriate function based on the selection.

    The options include:
    - Open a new loan
    - Close a loan
    - Display all loans
    - Display all late loans
    - Return to the Main Menu

    No parameters or return values.
    """
    # Initialize valid action choices
    loan_actions = ['1', '2', '3', '4', '0']

    # Display menu options
    print("\n[1] Open a new loan\n"
          "[2] Close a loan\n"
          "[3] Display all loans\n"
          "[4] Display all late loans\n"
          "[0] Return to the Main Menu")
    loan_act = input("-->")

    # Validate user input and prompt until a valid option is chosen
    while loan_act not in loan_actions:
        print("Invalid entry. Please choose one of the options in the menu")
        loan_act = input('-->')

    # Match the user's choice with corresponding action
    match loan_act:
        case '1':
            add_loan()
            loan_menu()
        case '2':
            loan_id = align_input('Enter loan ID: ', RE_PATT_D['loanID'], ERRORS['loanID'])
            delete_loan(get_loan(loan_id))
            loan_menu()
        case '3':
            display_all_loans()
            loan_menu()
        case '4':
            display_all_loans(late_loans=True)
            loan_menu()
        case '0':
            return


def get_loan_d():
    """
    Prompts the user for new loan details, including customer ID and book ID.

    The function ensures that the customer ID and book ID exist and are valid.
    It checks for the existence of the customer and book in the respective databases
    and ensures the book is available for loan.

    Returns:
        dict: A dictionary with customer and book IDs if successful, None otherwise.
    """
    print("Please enter new loan details:")

    # Customer ID Input and Validation
    cust_id_input = align_input('Enter customer ID: ', RE_PATT_D['custID'], ERRORS['custID'])
    if cust_id_input == '0':
        return

    # Loop to ensure valid customer ID
    cust_id_exist = None
    while not cust_id_exist:
        try:
            cust_id_exist = get_by_id(cust_id_input, 'customers')
        except Exception as e:
            # Logging and handling exceptions
            auto_log("Error: ", e, error=True)
            print(e)
            cust_id_input = align_input('Enter customer ID: ', RE_PATT_D['custID'], ERRORS['custID'])

    # Book ID Input and Validation
    book_id_input = align_input('Enter book ID: ', RE_PATT_D['bookID'], ERRORS['bookID'])
    if book_id_input == '0':
        return

    # Loop to ensure valid and available book ID
    book_id_exist = None
    book_available = None
    while not book_id_exist and not book_available:
        try:
            book_id_exist = get_by_id(book_id_input, 'books')
        except Exception as e:
            # Handling book ID related exceptions
            auto_log("Error: ", e, error=True)
            print(e)
            book_id_input = align_input('Enter book ID: ', RE_PATT_D['bookID'], ERRORS['bookID'])

        try:
            # Check for book availability
            is_available(book_id_input)
        except Exception as e:
            # Handling availability related exceptions
            print(e)
            loan_menu()
            return

    return {'custID': cust_id_input, 'bookID': book_id_input}


def get_loan(id_num):
    """
    Retrieves loan information based on the loan ID.

    The function continuously prompts for a valid loan ID until it successfully retrieves
    the corresponding loan data from the 'loans' table.

    Args:
        id_num (str): The loan ID.

    Returns:
        Loan: An instance of the Loan class populated with the retrieved loan data.
    """
    loan_data = None

    # Loop to ensure valid loan data is retrieved
    while not loan_data:
        try:
            loan_data = get_by_id(id_num, table='loans')
        except Exception as e:
            # Handling exceptions during loan data retrieval
            print(e)
            id_num = align_input('Enter loan ID: ', RE_PATT_D['loanID'], ERRORS['loanID'])

    # Creating a Loan instance with the retrieved data
    l = Loan(customer_id=loan_data[1], book_id=loan_data[2], loan_date=loan_data[3],
             expected_return_date=loan_data[4], actual_return_date=loan_data[5],
             loan_id=loan_data[0], override_id=True)

    # Displaying loan details
    l.show()

    return l


def add_loan():
    """
    Facilitates the addition of a new loan.

    The function prompts the user for loan details using `get_loan_d()` and creates
    a new Loan instance. If successful, the loan is saved to the database.

    No parameters or return values. Prints confirmation upon successful loan addition.
    """
    loan_d = get_loan_d()

    try:
        # Creating a new Loan instance
        l = Loan(customer_id=loan_d['custID'], book_id=loan_d['bookID'])
    except Exception as e:
        # Handling exceptions during Loan instance creation
        print(e)
        add_loan()
        return

    # Saving the new loan and logging the action
    l.save()
    auto_log('New loan added', log_id=l.id)
    print("\n*** Loan added successfully! ***\n")


def delete_loan(loan):
    """
    Deletes a given loan after user confirmation.

    The function prompts the user to confirm the deletion of the loan.
    If confirmed, the loan is deleted from the system.

    Args:
        loan (Loan): The Loan object to be deleted.

    No return value. Prints confirmation upon successful deletion.
    """
    print("\nConfirm delete?\n"
          "[1] Yes\n"
          "[2] No")
    while True:
        del_loan_act = input("-->")
        if del_loan_act == '1' or '2':
            break

    # Matching user's choice for deletion confirmation
    match del_loan_act:
        case '1':
            # Deleting the loan and logging the action
            loan.delete()
            auto_log('Loan deleted', log_id=loan.id)
            print("\n*** Loan deleted successfully ***\n")

        case '2':
            return


def display_all_loans(late_loans=False):
    """
    Displays all loans, with an option to show only late loans.

    This function retrieves all loans from the database and prints their details.
    If the `late_loans` flag is set to True, it filters and shows only the loans that are late.

    Args:
        late_loans (bool, optional): Flag to display only late loans. Defaults to False.

    No return value. Prints details of loans or late loans based on the flag.
    """
    loans = Loan.load_from_db()

    for l in loans:
        if late_loans:
            # Comparing loan return dates to filter late loans
            temp = date.fromisoformat(l.expected_return_date)
            if date.today() > temp:
                l.show()
        else:
            # Displaying all loans
            l.show()
