from abc import ABC, abstractmethod

from src.domain.domain import Movie, Client, Rental


class DataAccessEntity(ABC):
    @abstractmethod
    def write_to(self, file_pointer, entity):
        pass

    @abstractmethod
    def read_from(self, line):
        pass

class MovieDataAccess(Movie, DataAccessEntity):
    def write_to(self, file_pointer, movie):
        file_pointer.write(f"{movie.id},{movie.title},{movie.description},{movie.genre},\n")

    def read_from(self, line):
        movie_data = line.split(",")
        movie = Movie(movie_data[0],movie_data[1],movie_data[2],movie_data[3])
        return movie

class ClientDataAccess(Client, DataAccessEntity):
    def write_to(self, file_pointer, client):
        file_pointer.write(f"{client.id},{client.name},\n")

    def read_from(self, line):
        client_data = line.split(",")
        client = Client(client_data[0],client_data[1])
        return client

class RentalDataAccess(Rental, DataAccessEntity):
    def write_to(self, file_pointer, rental):
        file_pointer.write(f"{rental.id},{rental.movie_id},{rental.client_id},{rental.rented_date},{rental.due_date},"
                           f"{rental.returned_date},\n")

    def read_from(self, line):
        rental_data = line.split(",")
        rental = Rental(rental_data[0],rental_data[1],rental_data[2],rental_data[3],rental_data[4])
        return rental