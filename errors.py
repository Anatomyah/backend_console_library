class InvalidEntry(Exception):
    def __str__(self):
        return "InvalidEntry: "


class InvalidAge(Exception):
    def __str__(self):
        return "InvalidAge: Valid age range is between 4-120"


class InvalidPublicationYear(Exception):
    def __str__(self):
        return "InvalidPublicationYear: Valid range is between 1700-2023"


class InvalidDate(Exception):
    def __str__(self):
        return 'InvalidDate: Return date must be in range between the loan date and today'


class IdNotExist(Exception):
    def __str__(self):
        return "IDNotExist: Entered ID does not exist in our database"


class IdAlreadyExists(Exception):
    def __str__(self):
        return "IdAlreadyExists: Entered ID already exists in our database"


class BookNotAvailable(Exception):
    def __str__(self):
        return f"BookNotAvailable: This book is currently on loan"


