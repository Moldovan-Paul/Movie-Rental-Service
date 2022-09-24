from enum import Enum

from src.domain.domain import Rental


def add_movie_handler(movie_service, movie):
    movie_service.remove_movie_by_id(movie.id)

def delete_movie_handler(movie_service, movie):
    movie_service.add_movie(movie.id, movie.title, movie.description, movie.genre)

def update_movie_handler(movie_service, movies):
    movie_service.update_movie_by_id(movies.entity1.id, movies.entity1.title, movies.entity1.description, movies.entity1.genre)

def op_update_movie_handler(movie_service, movies):
    movie_service.update_movie_by_id(movies.entity2.id, movies.entity2.title, movies.entity2.description, movies.entity2.genre)

def add_client_handler(client_service, client):
    client_service.remove_client_by_id(client.id)

def delete_client_handler(client_service, client):
    client_service.add_client(client.id, client.name)

def update_client_handler(client_service, clients):
    client_service.update_client_by_id(clients.entity1.id, clients.entity1.name)

def op_update_client_handler(client_service, clients):
    client_service.update_client_by_id(clients.entity2.id, clients.entity2.name)

def add_rental_handler(rental_service, rental):
    rental_service.remove_rental_by_id(rental.id)

def remove_rental_handler(rental_service, rental):
    rental_service.add_rental(rental.id, rental.movie_id, rental.client_id, rental.rented_date,
                              rental.due_date, rental.returned_date)

def add_return_handler(rental_service, rentals):
    rental = Rental(rentals.entity1.id, rentals.entity1.client_id,rentals.entity1.movie_id, rentals.entity1.rented_date,
                    rentals.entity1.due_date, rentals.entity1.returned_date, )
    rental_service._rental_repository.update(rentals.entity1.id, rental)

def op_add_return_handler(rental_service, rentals):
    rental = Rental(rentals.entity2.id, rentals.entity2.client_id, rentals.entity2.movie_id,rentals.entity2.rented_date,
                    rentals.entity2.due_date, rentals.entity2.returned_date)
    rental_service._rental_repository.update(rentals.entity2.id, rental)

def opposite_handler(handler):
    if handler == UndoHandler.ADD_MOVIE:
        return UndoHandler.DELETE_MOVIE
    if handler == UndoHandler.DELETE_MOVIE:
        return UndoHandler.ADD_MOVIE
    if handler == UndoHandler.UPDATE_MOVIE:
        return UndoHandler.OP_UPDATE_MOVIE
    if handler == UndoHandler.OP_UPDATE_MOVIE:
        return UndoHandler.UPDATE_MOVIE
    if handler == UndoHandler.ADD_CLIENT:
        return UndoHandler.DELETE_CLIENT
    if handler == UndoHandler.DELETE_CLIENT:
        return UndoHandler.ADD_CLIENT
    if handler == UndoHandler.UPDATE_CLIENT:
        return UndoHandler.OP_UPDATE_CLIENT
    if handler == UndoHandler.OP_UPDATE_CLIENT:
        return UndoHandler.UPDATE_CLIENT
    if handler == UndoHandler.ADD_RENTAL:
        return UndoHandler.REMOVE_RENTAL
    if handler == UndoHandler.REMOVE_RENTAL:
        return UndoHandler.ADD_RENTAL
    if handler == UndoHandler.ADD_RETURN:
        return UndoHandler.REMOVE_RETURN
    if handler == UndoHandler.REMOVE_RETURN:
        return UndoHandler.ADD_RETURN

class UndoHandler(Enum):
    ADD_MOVIE = add_movie_handler
    DELETE_MOVIE = delete_movie_handler
    UPDATE_MOVIE = update_movie_handler
    OP_UPDATE_MOVIE = op_update_movie_handler
    ADD_CLIENT = add_client_handler
    DELETE_CLIENT = delete_client_handler
    UPDATE_CLIENT = update_client_handler
    OP_UPDATE_CLIENT = op_update_client_handler
    ADD_RENTAL = add_rental_handler
    REMOVE_RENTAL = remove_rental_handler
    ADD_RETURN = add_return_handler
    REMOVE_RETURN = op_add_return_handler
