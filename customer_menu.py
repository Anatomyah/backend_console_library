from customers import Customer
from helpers import auto_log, get_by_id, align_input, query_db, check_loans, check_id
from config import RE_PATT_D, ERRORS


def customer_menu():
    """
      Displays the customer menu and handles user interaction for customer-related actions.

      Offers options to add, edit, delete, display all customers, or return to the main menu.
      Validates user input and calls the appropriate functions based on the selected action.
      """

    # Displaying customer-related action choices to the user
    print("\n[1] Add a customer\n"
          "[2] Edit a customer\n"
          "[3] Delete a customer\n"
          "[4] Display all customers\n"
          "[0] Return to Main Menu")
    customer_act = input("-->")

    # Validating user input to ensure it matches one of the available actions
    while customer_act not in ['1', '2', '3', '4', '0']:
        print("Invalid entry. Please choose one of the options in the menu")
        customer_act = input('-->')

    # Matching the user's choice with the corresponding function
    match customer_act:
        case '1':
            add_customer()  # Adding a new customer
            customer_menu()  # Re-displaying the customer menu after the action

        # ... other cases follow similar structure ...
        case '2':
            id_input = align_input('ID number: ', RE_PATT_D['custID'], ERRORS['custID'])
            edit_customer(get_customer(id_input))
            customer_menu()
        case '3':
            id_input = align_input('ID number: ', RE_PATT_D['custID'], ERRORS['custID'])
            delete_customer(get_customer(id_input))
            customer_menu()
        case '4':
            display_all_customers()
            customer_menu()
        case '0':
            return  # Returning to the main menu


def get_customer_d():
    """
    Gathers input from the user for new customer details.

    Prompts for customer ID, first and last name, city, and age.
    Validates the input using regular expressions and custom error messages.
    Returns a dictionary of the inputted customer details or '0' to exit.

    Returns:
        dict or str: Dictionary of customer details or '0' for exit.
    """

    print("Please enter new customer details:")
    # Input gathering and validation loop for each customer attribute
    id_input = align_input('ID number: ', RE_PATT_D['custID'], ERRORS['custID'])
    if id_input == '0':
        return '0'

    while True:
        try:
            check_id(table='customers', object_id=id_input)
        except Exception as e:
            print(e)
            id_input = align_input('ID number: ', RE_PATT_D['custID'], ERRORS['custID'])
        else:
            break

    p_name_input = align_input('First name: ', RE_PATT_D['p_name'], ERRORS['p_name']).title()
    if p_name_input == '0':
        return '0'
    l_name_input = align_input('Last name: ', RE_PATT_D['l_name'], ERRORS['l_name']).title()
    if l_name_input == '0':
        return '0'
    city_input = align_input('City: ', RE_PATT_D['city'], ERRORS['city']).title()
    if city_input == '0':
        return '0'
    age_input = align_input('Age: ', RE_PATT_D['age'], ERRORS['age'], number='age')
    if age_input == '0':
        return '0'

    # Returning a dictionary with the collected customer details
    return {'id': id_input, 'p_name': p_name_input, 'l_name': l_name_input, 'city': city_input, 'age': age_input}


def get_customer(id_num):
    """
    Retrieves a customer object by its ID.

    Args:
        id_num (int): The ID number of the customer to retrieve.

    Handles exceptions and validates the input ID.
    Displays customer details if found, otherwise prompts for re-entry.

    Returns:
        Customer: The customer object corresponding to the given ID.
    """
    customer_data = None

    # Looping until valid customer data is retrieved using the provided ID
    while not customer_data:
        # Attempting to retrieve customer data by ID with exception handling
        try:
            customer_data = get_by_id(id_num, table='customers')
        except Exception as e:
            print(e)
            id_num = align_input('Enter customer ID: ', RE_PATT_D['custID'], ERRORS['custID'])

    # Creating and returning a Customer object with the retrieved data
    try:
        c = Customer(id_=customer_data[0],
                     p_name=customer_data[1],
                     l_name=customer_data[2],
                     city=customer_data[3],
                     age=customer_data[4])
    except Exception as e:
        print(e.__traceback__)
        customer_menu()
        return

    c.show()

    return c


def add_customer():
    """
    Handles the process of adding a new customer to the system.

    Gathers customer details from the user, creates a Customer object, and saves it to the database.
    Logs the action and displays a success message upon completion.
    """

    # Process for adding a new customer with data validation and exception handling
    customer_d = get_customer_d()
    if customer_d == '0':
        return

    try:
        c = Customer(id_=customer_d['id'], p_name=customer_d['p_name'],
                     l_name=customer_d['l_name'], city=customer_d['city'], age=customer_d['age'])
    except Exception as e:
        print(e)
        add_customer()
        return

    c.save()

    auto_log('Customer added', log_id=c.id)
    print("\n*** Customer added successfully! ***\n")


def edit_customer(customer):
    """
     Provides options to edit different attributes of a given customer.

     Args:
         customer (Customer): The customer object to be edited.

     Allows editing of the customer's name, city, and age.
     Validates the user's choices and updates the customer details accordingly.
     """

    # Possible actions a user can take within the edit customer menu
    possible_actions = ['1', '2', '3', '4', '0']
    values = []  # List to store new values for customer attributes
    clauses_lst = []  # List to store SQL clauses for updating customer attributes

    while True:
        # Displaying the edit menu options to the user
        print("\n[1] Edit first name\n"
              "[2] Edit last name\n"
              "[3] Edit City\n"
              "[4] Edit Age\n"
              "[0] Return to Customer Menu")
        edit_customer_act = input("-->")

        # Validating user input to match available edit actions
        while edit_customer_act not in possible_actions:
            edit_customer_act = input("-->")

        # Handling user's choice for editing specific customer attributes
        match edit_customer_act:
            case '1':
                # Editing customer's first name
                while True:
                    p_name_input = align_input('First name: ', RE_PATT_D['p_name'], ERRORS['p_name']).title()
                    if p_name_input == '0':
                        return  # Exiting if input is '0'
                    try:
                        customer.p_name = p_name_input  # Setting new first name
                    except Exception as e:
                        print(e)  # Handling exceptions
                        continue
                    else:
                        clauses_lst.append("p_name = ?")  # Preparing SQL clause
                        values.append(customer._p_name)  # Adding new value
                        break

            # Similar structures follow for editing customer's last name, city and age
            case '2':
                while True:
                    l_name_input = align_input('Last name: ', RE_PATT_D['l_name'], ERRORS['l_name']).title()
                    if l_name_input == '0':
                        return
                    try:
                        customer.l_name = l_name_input
                    except Exception as e:
                        print(e)
                        continue
                    else:
                        clauses_lst.append("l_name = ?")
                        values.append(customer._l_name)
                        break
            case '3':
                while True:
                    city_input = align_input('City: ', RE_PATT_D['city'], ERRORS['city']).title()
                    if city_input == '0':
                        return
                    try:
                        customer.city = city_input
                    except Exception as e:
                        print(e)
                        continue
                    else:
                        clauses_lst.append("city = ?")
                        values.append(customer._city)
                        break
            case '4':
                while True:
                    age_input = align_input('Age: ', RE_PATT_D['age'], ERRORS['age'], number='age')
                    if age_input == '0':
                        return
                    try:
                        customer.age = age_input
                    except Exception as e:
                        print(e)
                        continue
                    else:
                        clauses_lst.append("age = ?")
                        values.append(customer._age)
                        break
            case '0':
                return  # Returning to the customer menu

                # Prompting user if they want to make additional edits
        print("Anything else to edit?\n"
              "[1] Yes\n"
              "[2] No")

        edit_act = input("-->")
        match edit_act:
            case '1':
                pass  # Continuing the loop if there are more edits to be made
            case '2':
                # Finalizing edits and updating the customer in the database
                customer.edit(set_clauses=tuple(clauses_lst), values=values)
                break

        # Logging the edit action and displaying a success message
        auto_log('Customer edited', log_id=customer.id)
        print("\n*** Customer edited successfully! ***\n")


def delete_customer(customer):
    """
       Handles the deletion of a customer from the system.

       Args:
           customer (Customer): The customer object to be deleted.

       Asks for user confirmation before deletion.
       Checks if the customer has any active loans and prevents deletion if so.
       Logs the action and displays a success message upon completion.
       """

    # Prompting the user for confirmation before proceeding with deletion
    print("\nConfirm delete?\n"
          "[1] Yes\n"
          "[2] No")
    while True:
        del_customer_act = input("-->")
        # Ensuring valid input for confirmation
        if del_customer_act in ['1', '2']:
            break

    match del_customer_act:
        case '1':
            # If user confirms deletion
            try:
                # Checking if the customer has any active loans
                check_loans(customer)
            except AssertionError as e:
                # If there are active loans, show error and return to customer menu
                print(e)
                customer_menu()
                return

            # Deleting the customer from the database
            customer.delete()
            # Logging the deletion action
            auto_log('Customer deleted', log_id=customer.id)
            # Displaying a success message
            print("\n*** Customer deleted successfully ***")
            return

        case '2':
            # If user decides not to delete, return to the customer menu
            customer_menu()


def display_all_customers():
    """
      Retrieves and displays details of all customers in the system.

      Fetches customers from the database and prints their details.
      """

    # Logic to retrieve and display all customers
    customers = Customer.load_from_db()

    for c in customers:
        c.show()


def find_customer_by_name():
    """
       Searches for customers based on a name keyword.

       Allows the user to input a search keyword.
       Queries the database for customers with names matching the keyword.
       Displays the search results.
       """

    while True:
        print('\n')
        # Prompting the user to enter a search keyword for customer name
        keyword = f"%{input('Enter search keyword: ')}%"
        if keyword == '%0%':
            return  # Allowing the user to exit the search

        # SQL query to find customers whose first or last name matches the keyword
        query = "SELECT * FROM customers WHERE p_name LIKE ? or l_name like ?;"
        # Executing the query and storing the result
        res_lst = query_db(query=query, parameters=(keyword, keyword), result=True)

        if len(res_lst) == 0:
            # If no matching results are found, inform the user
            print("\n *** No matching results found*** ")
        else:
            # If matching results are found, display each customer's details
            print(f"************************************"
                  f"\nFOUND {len(res_lst)} RESULT(S): ")
            for customer in res_lst:
                # Creating Customer objects for each matching record
                c = Customer(id_=customer[0],
                             p_name=customer[1],
                             l_name=customer[2],
                             city=customer[3],
                             age=customer[4])
                c.show()  # Displaying customer details
            print('*************************************')
