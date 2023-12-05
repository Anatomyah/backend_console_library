class InvalidEntry(Exception):
    """
    Exception raised for invalid entries in general.

    Attributes:
        message (str): Explanation of the error
    """
    def __str__(self):
        return "InvalidEntry: "


class InvalidAge(Exception):
    """
    Exception raised for entering an age that is not within the valid range.

    Attributes:
        message (str): Explanation of the error
    """
    def __str__(self):
        return "InvalidAge: Valid age range is between 4-120"


class InvalidPublicationYear(Exception):
    """
    Exception raised for entering a publication year that is not within the valid range.

    Attributes:
        message (str): Explanation of the error
    """
    def __str__(self):
        return "InvalidPublicationYear: Valid range is between 1700-2023"


class InvalidDate(Exception):
    """
    Exception raised for entering a return date that is not within the valid range.

    Attributes:
        message (str): Explanation of the error
    """
    def __str__(self):
        return 'InvalidDate: Return date must be in range between the loan date and today'


class IdNotExist(Exception):
    """
    Exception raised when the entered ID does not exist in the database.

    Attributes:
        message (str): Explanation of the error
    """
    def __str__(self):
        return "IDNotExist: Entered ID does not exist in our database"


class IdAlreadyExists(Exception):
    """
    Exception raised when the entered ID already exists in the database.

    Attributes:
        message (str): Explanation of the error
    """
    def __str__(self):
        return "IdAlreadyExists: Entered ID already exists in our database"


class BookNotAvailable(Exception):
    """
    Exception raised when the requested book is not available for loan.

    Attributes:
        message (str): Explanation of the error
    """
    def __str__(self):
        return f"BookNotAvailable: This book is currently on loan"