from customer_menu import customer_menu, find_customer_by_name
from book_menu import book_menu, find_book_by_title
from loan_menu import loan_menu
from sample_data import create_sample_data
import unittest


def main_menu():
    """
    Display the main menu and prompt user for action.

    This function presents the main menu options to the user and captures user input.
    It ensures that the user's input is valid and corresponds to one of the available actions.

    Returns:
        str: The user's chosen action as a string.
    """
    # List of valid actions that can be taken from the main menu.
    possible_actions = ['1', '2', '3', '4', '5', '6', '7', '0']

    # Displaying the main menu options to the user.
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

    # Capturing and validating user input.
    action = input('-->')
    while action not in possible_actions:
        print("Invalid entry. Please choose one of the options in the menu")
        action = input('-->')

    return action

def menu_navigator():
    """
    Navigate through the application's menu system.

    This function utilizes the main_menu function to get the user's choice and
    then navigates to the appropriate functionality based on that choice.
    It's a recursive function that continues to present the main menu after
    each action until the user decides to exit.
    """
    # Get the user's action from the main menu.
    action = main_menu()

    # Match the user's action to the corresponding functionality.
    match action:
        case '1':
            customer_menu()
        case '2':
            book_menu()
        case '3':
            loan_menu()
        case '4':
            find_customer_by_name()
        case '5':
            find_book_by_title()
        case '6':
            # Run unit tests from the 'tester' module.
            unittest.main(module='tester', exit=False)
        case '7':
            create_sample_data()
        case '0':
            print('Goodbye!')
            exit(0)

    # Recall the menu navigator to present the main menu again.
    menu_navigator()
