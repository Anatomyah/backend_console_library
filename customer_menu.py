from customers import Customer
from helpers import auto_log, get_by_id, align_input, query_db, check_loans, check_id
from config import RE_PATT_D, ERRORS


def customer_menu():
    customer_actions = ['1', '2', '3', '4', '0']
    print("\n[1] Add a customer\n"
          "[2] Edit a customer\n"
          "[3] Delete a customer\n"
          "[4] Display all customers\n"
          "[0] Return to Main Menu")
    customer_act = input("-->")

    while customer_act not in customer_actions:
        print("Invalid entry. Please choose one of the options in the menu")
        customer_act = input('-->')

    match customer_act:
        case '1':
            add_customer()
            customer_menu()
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
            return


def get_customer_d():
    print("Please enter new customer details:")

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

    return {'id': id_input, 'p_name': p_name_input, 'l_name': l_name_input, 'city': city_input, 'age': age_input}


def get_customer(id_num):
    customer_data = None

    while not customer_data:
        try:
            customer_data = get_by_id(id_num, table='customers')
        except Exception as e:
            print(e)
            id_num = align_input('Enter customer ID: ', RE_PATT_D['custID'], ERRORS['custID'])

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
    possible_actions = ['1', '2', '3', '4', '0']
    values = []
    clauses_lst = []

    while True:
        print("\n[1] Edit first name\n"
              "[2] Edit last name\n"
              "[3] Edit City\n"
              "[4] Edit Age\n"
              "[0] Return to Customer Menu")
        edit_customer_act = input("-->")

        while edit_customer_act not in possible_actions:
            edit_customer_act = input("-->")

        match edit_customer_act:
            case '1':
                while True:
                    p_name_input = align_input('First name: ', RE_PATT_D['p_name'], ERRORS['p_name']).title()
                    if p_name_input == '0':
                        return
                    try:
                        customer.p_name = p_name_input
                    except Exception as e:
                        print(e)
                        continue
                    else:
                        clauses_lst.append("p_name = ?")
                        values.append(customer._p_name)
                        break
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
                return

        print("Anything else to edit?\n"
              "[1] Yes\n"
              "[2] No")

        edit_act = input("-->")
        match edit_act:
            case '1':
                pass
            case '2':
                customer.edit(set_clauses=tuple(clauses_lst), values=values)

                break

    auto_log('Customer edited', log_id=customer.id)
    print("\n*** Customer edited successfully! ***\n")


def delete_customer(customer):
    print("\nConfirm delete?\n"
          "[1] Yes\n"
          "[2] No")
    while True:
        del_customer_act = input("-->")
        if del_customer_act == '1' or '2':
            break

    match del_customer_act:
        case '1':
            try:
                check_loans(customer)
            except AssertionError as e:
                print(e)
                customer_menu()
                return

            auto_log('Customer deleted', log_id=customer.id)
            print("\n*** Customer deleted successfully ***")
            return

        case '2':
            customer_menu()


def display_all_customers():
    customers = Customer.load_from_db()

    for c in customers:
        c.show()


def find_customer_by_name():
    while True:
        print('\n')
        keyword = f"%{input('Enter search keyword: ')}%"
        if keyword == '%0%':
            return

        query = "SELECT * FROM customers WHERE p_name LIKE ? or l_name like ?;"
        res_lst = query_db(query=query, parameters=(keyword, keyword), result=True)
        if len(res_lst) == 0:
            print("\n *** No matching results found*** ")
        else:
            print(f"************************************"
                  f"\nFOUND {len(res_lst)} RESULT(S): ")
            for customer in res_lst:
                c = Customer(id_=customer[0],
                             p_name=customer[1],
                             l_name=customer[2],
                             city=customer[3],
                             age=customer[4])

                c.show()
            print('*************************************')
