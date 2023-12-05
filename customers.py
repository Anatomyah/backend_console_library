from dbhandler import DataBaseHandler
from config import CUSTOMERS_FIELDNAMES, RE_PATT_D, ERRORS
from helpers import query_db, regex_check, auto_log, check_number, check_id
from errors import InvalidEntry, InvalidAge


class Customer(DataBaseHandler):

    def __init__(self, id_, p_name, l_name, city, age):
        self.id = id_
        self.p_name = p_name
        self.l_name = l_name
        self.city = city
        self.age = age

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_val):
        valid_res = regex_check(RE_PATT_D['custID'], str(new_val))

        if not valid_res:
            auto_log(f"{InvalidEntry}", f"{ERRORS['custID']}", error=True)
            raise InvalidEntry(f"{ERRORS['custID']}")

        self._id = new_val

    @property
    def p_name(self):
        return self._p_name

    @p_name.setter
    def p_name(self, new_val):
        valid_res = regex_check(RE_PATT_D['p_name'], new_val)

        if not valid_res:
            auto_log(f"{InvalidEntry}", f"{ERRORS['p_name']}", error=True)
            raise InvalidEntry(f"{ERRORS['p_name']}")
        else:
            self._p_name = new_val

    @property
    def l_name(self):
        return self._l_name

    @l_name.setter
    def l_name(self, new_val):
        valid_res = regex_check(RE_PATT_D['l_name'], new_val)

        if not valid_res:
            auto_log(f"{InvalidEntry}", f"{ERRORS['l_name']}", error=True)
            raise InvalidEntry(f"{ERRORS['l_name']}")
        else:
            self._l_name = new_val

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, new_val):
        valid_res = regex_check(RE_PATT_D['age'], str(new_val))
        valid_num = check_number(new_val, 'age')

        if not valid_res:
            auto_log(f"{InvalidEntry}", f"{ERRORS['age']}", error=True)
            raise InvalidEntry(f"{ERRORS['age']}")
        elif not valid_num:
            auto_log(f"Error: {InvalidAge}", InvalidAge, error=True)
            raise InvalidAge
        else:
            self._age = new_val

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, new_val):
        valid_res = regex_check(RE_PATT_D['city'], new_val)

        if not valid_res:
            auto_log(f"{InvalidEntry}", f"{ERRORS['city']}", error=True)
            raise InvalidEntry(f"{ERRORS['city']}")
        else:
            self._city = new_val

    def obj_to_values(self):
        return (f'{self._id}', f'{self._p_name}', f'{self.l_name}',
                f'{self._city}', f'{self._age}')

    def get_table(self):
        return 'customers'

    def get_fieldnames(self):
        return CUSTOMERS_FIELDNAMES

    def get_id(self):
        return self.id

    def show(self):
        print(f"\n*** Customer Details ***\n"
              f"ID: {self._id}\n"
              f"First name: {self._p_name}\n"
              f"Last name: {self._l_name}\n"
              f"City: {self._city}\n"
              f"Age: {self._age}")

    @classmethod
    def load_from_db(cls):
        client_data = cls.load(table='customers')

        objects = []
        for row in client_data:
            objects.append(cls(id_=row[0],
                               p_name=row[1],
                               l_name=row[2],
                               city=row[3],
                               age=row[4],
                               ))

        return objects

    @classmethod
    def create_customer_table(cls):
        query = """
        CREATE TABLE IF NOT EXISTS customers  \
            (id TEXT PRIMARY KEY,  \
            p_name TEXT NOT NULL, \
            l_name TEXT NOT NULL, \
            city TEXT NOT NULL, \
            age INTEGER NOT NULL 
        );
        """

        query_db(query=query)
