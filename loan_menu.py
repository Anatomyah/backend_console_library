from helpers import auto_log, get_by_id, align_input, is_available
from config import RE_PATT_D, ERRORS
from loans import Loan
from datetime import date


def loan_menu():
    loan_actions = ['1', '2', '3', '4', '0']
    print("\n[1] Open a new loan\n"
          "[2] Close a loan\n"
          "[3] Display all loans\n"
          "[4] Display all late loans\n"
          "[0] Return to the Main Menu")
    loan_act = input("-->")

    while loan_act not in loan_actions:
        print("Invalid entry. Please choose one of the options in the menu")
        loan_act = input('-->')

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
    print("Please enter new loan details:")

    cust_id_input = align_input('Enter customer ID: ', RE_PATT_D['custID'], ERRORS['custID'])
    if cust_id_input == '0':
        return

    cust_id_exist = None
    while not cust_id_exist:
        try:
            cust_id_exist = get_by_id(cust_id_input, 'customers')
        except Exception as e:
            auto_log("Error: ", e, error=True)
            print(e)
            cust_id_input = align_input('Enter customer ID: ', RE_PATT_D['custID'], ERRORS['custID'])

    book_id_input = align_input('Enter book ID: ', RE_PATT_D['bookID'], ERRORS['bookID'])
    if book_id_input == '0':
        return

    book_id_exist = None
    book_available = None
    while not book_id_exist and not book_available:
        try:
            book_id_exist = get_by_id(book_id_input, 'books')
        except Exception as e:
            auto_log("Error: ", e, error=True)
            print(e)
            book_id_input = align_input('Enter book ID: ', RE_PATT_D['bookID'], ERRORS['bookID'])

        try:
            is_available(book_id_input)
        except Exception as e:
            print(e)
            print(e)
            loan_menu()
            return

    return {'custID': cust_id_input, 'bookID': book_id_input}


def get_loan(id_num):
    loan_data = None

    while not loan_data:
        try:
            loan_data = get_by_id(id_num, table='loans')
        except Exception as e:
            print(e)
            id_num = align_input('Enter loan ID: ', RE_PATT_D['loanID'], ERRORS['loanID'])

    l = Loan(customer_id=loan_data[1], book_id=loan_data[2], loan_date=loan_data[3], expected_return_date=loan_data[4],
             actual_return_date=loan_data[5], loan_id=loan_data[0], override_id=True)

    l.show()

    return l


def add_loan():
    loan_d = get_loan_d()

    try:
        l = Loan(customer_id=loan_d['custID'], book_id=loan_d['bookID'])
    except Exception as e:
        print(e)
        add_loan()
        return

    l.save()

    auto_log('New loan added', log_id=l.id)
    print("\n*** Loan added successfully! ***\n")


def delete_loan(loan):
    print("\nConfirm delete?\n"
          "[1] Yes\n"
          "[2] No")
    while True:
        del_loan_act = input("-->")
        if del_loan_act == '1' or '2':
            break

    match del_loan_act:
        case '1':
            loan.delete()

            auto_log('Loan deleted', log_id=loan.id)
            print("\n*** Loan deleted successfully ***\n")

        case '2':
            return


def display_all_loans(late_loans=False):
    loans = Loan.load_from_db()

    for l in loans:
        if late_loans:
            temp = date.fromisoformat(l.expected_return_date)
            if date.today() > date.fromisoformat(l.expected_return_date):
                l.show()
        else:
            l.show()
