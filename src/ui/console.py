from src.domain.validators import MovieRentalException
from src.handlers.handlers import UndoHandler, opposite_handler
from src.services.services import UndoManager, EntityPair


class Console:
    def __init__(self, movie_service, client_service, rental_service, statistics_services):
        self._movie_service = movie_service
        self._client_service = client_service
        self._rental_service = rental_service
        self._statistics_service = statistics_services
        self._undo_manager = UndoManager()
        self._redo_manager = UndoManager()

    @staticmethod
    def print_menu():
        print(" 1. Add a movie")
        print(" 2. Remove a movie")
        print(" 3. List all movies")
        print(" 4. Update a movie")
        print(" 5. Add a client")
        print(" 6. Remove a client")
        print(" 7. List all clients")
        print(" 8. Update a client")
        print(" 9. Rent a movie")
        print("10. Return a movie")
        print("11. List all rentals")
        print("12. Search for movie")
        print("13. Search for client")
        print("14. List most rented movies")
        print("15. List most active clients")
        print("16. List all late rentals")
        print("17. Undo last operation")
        print("18. Redo last operation")
        print("19. Exit")

    @staticmethod
    def input_movie():
        movie_id = input("Input movie's id: ")
        title = input("Input movie's title: ")
        description = input("Input movie's description: ")
        genre = input("Input movie's genre: ")
        return movie_id, title, description, genre

    def print_movies(self, movies):
        print('\n')
        for movie in movies:
            print("Id: " + movie.id + "  Title: " + movie.title + "  Description: " + movie.description
                  + "  Genre: " + movie.genre)
        print('\n')

    @staticmethod
    def input_movie_id():
        return input("Input the id of movie desired to be removed: ")

    @staticmethod
    def input_movie_update():
        movie_id = input("Input the id of the movie to be updated: ")
        title = input("Input updated title: ")
        description = input("Input updated description: ")
        genre = input("Input updated genre: ")
        return movie_id, title, description, genre

    @staticmethod
    def input_client():
        client_id = input("Input client's id: ")
        name = input("Input client's name: ")
        return client_id, name

    @staticmethod
    def input_client_id():
        return input("Input the id of client desired to be removed: ")

    def print_clients(self, clients):
        print('\n')
        for client in clients:
            print("Id: " + client.id + "  Name: " + client.name)
        print('\n')

    @staticmethod
    def input_client_update():
        client_id = input("Input the id of the client to be updated: ")
        name = input("Input updated name: ")
        return client_id, name

    @staticmethod
    def input_rental():
        rental_id = input("Input id of rental: ")
        movie_id = input("Input id of movie to be rented: ")
        client_id = input("Input id of renter: ")
        rented_date = input("Input date of rent: ")
        due_date = input("Input due date for rent: ")
        return rental_id, movie_id, client_id, rented_date, due_date

    def print_all_rentals(self):
        rentals = self._rental_service.get_all_rentals()
        print('\n')
        for rental in rentals:
            print("Rental Id: " + rental.id + "  Movie id: " + rental.movie_id + "  Client Id: " + rental.client_id
                  + "  Rented date: " + rental.rented_date + " Due date: " + rental.due_date + " Returned date: "
                  + rental.returned_date )
        print('\n')

    @staticmethod
    def input_rental_return():
        rental_id = input("Input id of rental to return: ")
        returned_date = input("Input date of return: ")
        return rental_id, returned_date

    def print_most_rented_movies(self, movies):
        print('\n')
        for movie in movies:
            print("Movie id: " + movie[0] + " Title: '" + movie[1] + "' Number of rented days: " + str(movie[2]))
        print('\n')

    def print_most_active_clients(self, clients):
        print('\n')
        for client in clients:
            print("Client id: " + client[0] + " Name: '" + client[1] + "' Total rented time in days: " + str(client[2]))
        print('\n')

    def print_late_rentals(self, late_rentals):
        print('\n')
        for movie in late_rentals:
            print("Movie id: " + movie[0] + " Title: '" + movie[1] + "' Number of days of delay: " + str(movie[2]))
        print('\n')

    def run_console(self):
        self._movie_service.add_predefined()
        while True:
            self.print_menu()
            option = input("Choose an option: ")
            try:
                if option == '1':
                    movie_id, title, description, genre = self.input_movie()
                    self._movie_service.add_movie(movie_id, title, description, genre)
                    movie = self._movie_service._movie_repository.find_by_id(movie_id)
                    self._undo_manager.register_operation(self._movie_service, UndoHandler.ADD_MOVIE, movie)
                    self._redo_manager.clear_list()
                if option == '2':
                    movie_id = self.input_movie_id()
                    movie = self._movie_service._movie_repository.find_by_id(movie_id)
                    self._movie_service.remove_movie_by_id(movie_id)
                    self._undo_manager.register_operation(self._movie_service, UndoHandler.DELETE_MOVIE, movie)
                    self._redo_manager.clear_list()
                if option == '3':
                    movies = self._movie_service.get_all_movies()
                    self.print_movies(movies)
                if option == '4':
                    movie_id, title, description, genre = self.input_movie_update()
                    movie1 = self._movie_service._movie_repository.find_by_id(movie_id)
                    self._movie_service.update_movie_by_id(movie_id, title, description, genre)
                    movie2 = self._movie_service._movie_repository.find_by_id(movie_id)
                    self._undo_manager.register_operation(self._movie_service, UndoHandler.UPDATE_MOVIE,
                                                          EntityPair(movie1, movie2))
                    self._redo_manager.clear_list()
                if option == '5':
                    client_id, name = self.input_client()
                    self._client_service.add_client(client_id, name)
                    client = self._client_service._client_repository.find_by_id(client_id)
                    self._undo_manager.register_operation(self._client_service, UndoHandler.ADD_CLIENT, client)
                    self._redo_manager.clear_list()
                if option == '6':
                    client_id = self.input_client_id()
                    client = self._client_service._client_repository.find_by_id(client_id)
                    self._client_service.remove_client_by_id(client_id)
                    self._undo_manager.register_operation(self._client_service, UndoHandler.DELETE_CLIENT, client)
                    self._redo_manager.clear_list()
                if option == '7':
                    clients = self._client_service.get_all_clients()
                    self.print_clients(clients)
                if option == '8':
                    client_id, name  = self.input_client_update()
                    client1 = self._client_service._client_repository.find_by_id(client_id)
                    self._client_service.update_client_by_id(client_id, name)
                    client2 = self._client_service._client_repository.find_by_id(client_id)
                    self._undo_manager.register_operation(self._client_service, UndoHandler.UPDATE_CLIENT,
                                                          EntityPair(client1, client2))
                    self._redo_manager.clear_list()
                if option == '9':
                    rental_id, movie_id, client_id, rented_date, due_date = self.input_rental()
                    self._movie_service.check_id_existence(movie_id)
                    self._client_service.check_id_existence(client_id)
                    self._rental_service.add_rental(rental_id, movie_id, client_id, rented_date, due_date, '-')
                    rental = self._rental_service._rental_repository.find_by_id(rental_id)
                    self._undo_manager.register_operation(self._rental_service, UndoHandler.ADD_RENTAL, rental)
                    self._redo_manager.clear_list()
                if option == '10':
                    rental_id, returned_date = self.input_rental_return()
                    self._rental_service.check_id_existence(rental_id)
                    rental1 = self._rental_service._rental_repository.find_by_id(rental_id)
                    self._rental_service.return_rental(rental_id, returned_date)
                    rental2 = self._rental_service._rental_repository.find_by_id(rental_id)
                    self._undo_manager.register_operation(self._rental_service, UndoHandler.ADD_RETURN,
                                                          EntityPair(rental1, rental2))
                    self._redo_manager.clear_list()
                if option == '11':
                    self.print_all_rentals()
                if option == '12':
                    movies = self._movie_service.movie_search_tool(input("Input search string: "))
                    self.print_movies(movies)
                if option == '13':
                    clients = self._client_service.client_search_tool(input("Input search string: "))
                    self.print_clients(clients)
                if option == '14':
                    movies = self._statistics_service.most_rented_movies()
                    self.print_most_rented_movies(movies)
                if option == '15':
                    clients = self._statistics_service.most_active_clients()
                    self.print_most_active_clients(clients)
                if option == '16':
                    late_rentals = self._statistics_service.late_rentals()
                    self.print_late_rentals(late_rentals)
                if option == '17':
                    operation = self._undo_manager.return_last_operation()
                    self._undo_manager.undo()
                    self._redo_manager.register_operation(operation.target_object, opposite_handler(operation.handler),
                                                          operation.entity)
                if option == '18':
                    operation = self._redo_manager.return_last_operation()
                    self._redo_manager.undo()
                    self._undo_manager.register_operation(operation.target_object, opposite_handler(operation.handler),
                                                          operation.entity)
                if option == '19':
                    break
            except MovieRentalException as exception:
                print(str(exception))