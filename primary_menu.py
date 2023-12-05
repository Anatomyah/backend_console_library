from customer_menu import customer_menu, find_customer_by_name
from book_menu import book_menu, find_book_by_title
from loan_menu import loan_menu
from sample_data import create_sample_data
import unittest


def main_menu():
    possible_actions = ['1', '2', '3', '4', '5', '6', '7', '0']
    print('\n*** Welcome to LiberBook! **\n'
          '\n*** Enter [0] at any time to return to the previous menu***\n'
          '\n[1] Customer menu\n'
          '[2] Book menu\n'
          '[3] Loan menu\n'
          '[4] Find customer by name\n'
          '[5] Find book by name\n'
          '[6] Run Unit Testing\n'
          '[7] Create sample data\n'
          '[0] Exit')
    action1 = input('-->')

    while action1 not in possible_actions:
        print("Invalid entry. Please choose one of the options in the menu")
        action1 = input('-->')

    return action1


def menu_navigator():
    action = main_menu()
    match action:
        case '1':
            customer_menu()
            menu_navigator()
        case '2':
            book_menu()
            menu_navigator()
        case '3':
            loan_menu()
            menu_navigator()
        case '4':
            find_customer_by_name()
            menu_navigator()
        case '5':
            find_book_by_title()
            menu_navigator()
        case '6':
            unittest.main(module='tester', exit=False)
            menu_navigator()
        case '7':
            create_sample_data()
            menu_navigator()
        case '0':
            'Goodbye!'
            exit(0)
