import datetime
import time


class MovieRentalException(Exception):
    pass

class MovieIdException(MovieRentalException):
    pass

class ClientIdException(MovieRentalException):
    pass

class RentalException(MovieRentalException):
    pass

class MovieIdValidator:
    @staticmethod
    def validate(movie):
        if not movie.id.isnumeric():
            raise MovieIdException("\nA movie's id must be a number\n")

class ClientIdValidator:
    @staticmethod
    def validate(client):
        if not client.id.isnumeric():
            raise ClientIdException("\nA client's id must be a number\n")

class RentalValidator:
    @staticmethod
    def validate(rental):
        if not rental.id.isnumeric():
            raise RentalException("\nA rental's id must be a number\n")
        try:
            day, month, year = rental.rented_date.split('/')
            if not datetime.datetime(int(year), int(month), int(day)):
                raise RentalException("\nRented date is in invalid format\n")
        except ValueError:
            raise RentalException("\nRented date is in invalid format\n")

        try:
            day, month, year = rental.due_date.split('/')
            if not datetime.datetime(int(year), int(month), int(day)):
                raise RentalException("\nDue date is in invalid format\n")
        except ValueError:
            raise RentalException("\nDue date is in invalid format\n")

        if time.strptime(rental.rented_date, "%d/%m/%Y") > time.strptime(rental.due_date, "%d/%m/%Y"):
            raise RentalException("\nRented date must be older than due date\n")
