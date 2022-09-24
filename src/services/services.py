import datetime
import random
from dataclasses import dataclass

from src.domain.domain import Movie, Client, Rental
from src.domain.validators import MovieRentalException


class ServicesException(MovieRentalException):
    pass

class MovieServices:
    def __init__(self, movie_repository, rental_repository):
        self._movie_repository = movie_repository
        self._rental_repository = rental_repository

    def add_movie(self, movie_id, title, description, genre):
        """
        Adds a movie to the movie repository
        """
        new_movie = Movie(movie_id, title, description, genre)
        self._movie_repository.save(new_movie)

    def add_predefined(self):
        """
        Adds 20 randomly generated movie entities to the movie repository
        :return:
        """
        titles = ['Citizen Kane','Casablanca','The Godfather','Gone with the Wind','Lawrence of Arabia',
                  'The Wizard of Oz','The Graduate','On the Waterfront','Schindler s List',	'Singin in the Rain',
                  'Its a Wonderful Life','Sunset Boulevard','The Bridge on the River Kwai','Some Like It Hot',
                  'Star Wars','All About Eve','The African Queen','Psycho','The General','Chinatown',
                  'One Flew Over the Cuckoo s Nest','The Grapes of Wrath','2001: A Space Odyssey','The Maltese Falcon',
                  'Raging Bull','E.T. the Extra-Terrestrial','Dr. Strangelove','Bonnie and Clyde','Apocalypse Now',
                  'Mr. Smith Goes to Washington']
        genres = ['Action', 'Adventure', 'Thriller', 'Horror', 'Drama', 'Romance', 'Comedy']
        descriptions = ['Interesting', 'Pretty dull', 'Very immersive', 'An eventful journey', 'Based on a true story',
                        'Must watch', 'Frightening events', 'True love story', 'Lone wolf on a mission to escape',
                        'Mysterious', 'All out chaos']
        title_list = random.sample(titles, 20)
        for count in range(20):
            movie_id = str(count+1)
            title = title_list[count]
            description = random.choice(descriptions)
            genre = random.choice(genres)
            self.add_movie(movie_id, title, description, genre)

    def check_id_existence(self, movie_id):
        """
        Checks whether a movie exists for a given id and raises an exception otherwise
        """
        if not self._movie_repository.find_by_id(movie_id):
            raise ServicesException("\nMovie id does not exist\n")
        return True

    def remove_movie_by_id(self, movie_id):
        """
        Removes the movie identified by a given id
        """
        self._movie_repository.delete_by_id(movie_id)

    def update_movie_by_id(self, movie_id, title, description, genre):
        """
        Updates the movie identified by a given id
        :param movie_id: Id of movie to be updated
        :param title: Updated title
        :param description: Updated description
        :param genre: Updated genre
        """
        new_movie = Movie(movie_id, title, description, genre)
        self._movie_repository.update(movie_id, new_movie)

    def get_all_movies(self):
        """
        Returns a list of all movie entities
        """
        return self._movie_repository.get_all()

    def movie_search_tool(self, search_string):
        """
        Searches for given string in the movie repository and returns a list of matching entities
        """
        movie_list = self.get_all_movies()
        return_list = []

        for movie in movie_list:
            if search_string.lower() in movie.id.lower():
                return_list.append(movie)
            elif search_string.lower() in movie.title.lower():
                return_list.append(movie)
            elif search_string.lower() in movie.description.lower():
                return_list.append(movie)
            elif search_string.lower() in movie.genre.lower():
                return_list.append(movie)

        if len(return_list) == 0:
            raise ServicesException("\nNo matching results for search\n")

        return return_list


class ClientServices:
    def __init__(self, client_repository):
        self._client_repository = client_repository

    def add_client(self, client_id, name):
        """
        Adds a client to the client repository
        """
        new_client = Client(client_id, name)
        self._client_repository.save(new_client)

    def check_id_existence(self, client_id):
        """
        Checks whether a client exists for a given id and raises an exception otherwise
        """
        if not self._client_repository.find_by_id(client_id):
            raise ServicesException("\nClient id does not exist\n")
        return True

    def remove_client_by_id(self, client_id):
        """
        Removes the client identified by a given id
        """
        self._client_repository.delete_by_id(client_id)

    def update_client_by_id(self, client_id, name):
        """
        Updates the client identified by a given id
        :param client_id: Id of client to be updated
        :param name: Updated name
        """
        new_client = Client(client_id, name)
        self._client_repository.update(client_id, new_client)

    def get_all_clients(self):
        """
        Returns a list of all client entities
        """
        return self._client_repository.get_all()

    def client_search_tool(self, search_string):
        """
        Searches for given string in the client repository and returns a list of matching entities
        """
        client_list = self.get_all_clients()
        return_list = []

        for client in client_list:
            if search_string.lower() in client.id.lower():
                return_list.append(client)
            elif search_string.lower() in client.name.lower():
                return_list.append(client)

        if len(return_list) == 0:
            raise ServicesException("\nNo matching results for search\n")

        return return_list

class RentalServices:
    def __init__(self, rental_repository):
        self._rental_repository = rental_repository

    def add_rental(self, rental_id, movie_id, client_id, rented_date, due_date, returned_date):
        """
        Adds a rental to the client repository
        """
        new_rental = Rental(rental_id, movie_id, client_id, rented_date, due_date, returned_date)
        if len(self._rental_repository._entities) > 0:
            if not self.check_rental_condition(client_id):
                raise ServicesException("\nClient has an active rental that is past its due date but it was not returned\n")
        self._rental_repository.save(new_rental)

    def check_rental_condition(self, client_id):
        """
        Checks if a client is eligible for another rental
        """
        rental_list = filter(lambda rental: rental.client_id == client_id, self.get_all_rentals())
        for rental in rental_list:
            if rental.returned_date == '-' and datetime.datetime.strptime(rental.due_date, "%d/%m/%Y").date() < datetime.date.today():
                return False
        return True

    def return_rental(self, rental_id, returned_date):
        """
        Returns an active rental
        :param rental_id: Id of rental to be returned
        :param returned_date: Date of return
        """
        rental = self._rental_repository.find_by_id(rental_id)
        if not rental.returned_date == '-':
            raise ServicesException("Rental was already returned")
        returned_rental = Rental(rental.id, rental.movie_id, rental.client_id, rental.rented_date, rental.due_date,
                           returned_date)
        self._rental_repository.update(rental_id, returned_rental)

    def check_id_existence(self, rental_id):
        """
        Checks whether a rental exists for a given id and raises an exception otherwise
        """
        if not self._rental_repository.find_by_id(rental_id):
            raise ServicesException("\nRental id does not exist\n")
        return True

    def remove_rental_by_id(self, rental_id):
        """
        Removes the rental identified by a given id
        """
        self._rental_repository.delete_by_id(rental_id)

    def get_all_rentals(self):
        """
        Returns a list of all rental entities
        """
        return self._rental_repository.get_all()


class Statistics:
    def __init__(self, movie_repository, client_repository, rental_repository):
        self._movie_repository = movie_repository
        self._client_repository = client_repository
        self._rental_repository = rental_repository

    def movie_id_with_rented_time_descending(self):
        """
            Creates and returns a dictionary in which the dictionary keys represent movie ids and their corresponding
        values represent the number of days the movie was rented. This dictionary is sorted in descending order by
        number of days rented.
        """
        rental_list = self._rental_repository.get_all()
        rented_time_dict = {}
        for rental in rental_list:
            if rental.returned_date == '-':
                if rental.movie_id in rented_time_dict:
                    rented_time_dict[rental.movie_id] += (datetime.date.today() - datetime.datetime.strptime(rental.due_date, "%d/%m/%Y").date()).days
                else:
                    rented_time_dict[rental.movie_id] = (datetime.date.today() - datetime.datetime.strptime(rental.due_date, "%d/%m/%Y").date()).days
            else:
                if rental.movie_id in rented_time_dict:
                    rented_time_dict[rental.movie_id] += (datetime.datetime.strptime(rental.returned_date,"%d/%m/%Y").date()
                                                          - datetime.datetime.strptime(rental.due_date,"%d/%m/%Y").date()).days
                else:
                    rented_time_dict[rental.movie_id] = (datetime.datetime.strptime(rental.returned_date, "%d/%m/%Y").date()
                                                          - datetime.datetime.strptime(rental.due_date, "%d/%m/%Y").date()).days

        return sorted(rented_time_dict.items(), key=lambda x: int(x[1]), reverse=True)

    def most_rented_movies(self):
        """
        Creates and returns a list containing the most rented movies ordered descending based on number of days rented
        :return:
        """
        most_rented_movies_list = []
        rented_time_dict = self.movie_id_with_rented_time_descending()
        for key, value in rented_time_dict:
            most_rented_movies_list.append([key, self._movie_repository.find_by_id(key).title, value])

        return most_rented_movies_list

    def client_id_with_rented_time_descending(self):
        """
            Creates and returns a dictionary in which the dictionary keys represent client ids and their corresponding
        values represent the number of days they rented movies. This dictionary is sorted in descending order by
        total rental time.
        """
        rental_list = self._rental_repository.get_all()
        rented_time_dict = {}
        for rental in rental_list:
            if rental.returned_date == '-':
                if rental.client_id in rented_time_dict:
                    rented_time_dict[rental.client_id] += (datetime.date.today() - datetime.datetime.strptime(rental.due_date, "%d/%m/%Y").date()).days
                else:
                    rented_time_dict[rental.client_id] = (datetime.date.today() - datetime.datetime.strptime(rental.due_date, "%d/%m/%Y").date()).days
            else:
                if rental.client_id in rented_time_dict:
                    rented_time_dict[rental.client_id] += (datetime.datetime.strptime(rental.returned_date,"%d/%m/%Y").date()
                                                           - datetime.datetime.strptime(rental.due_date,"%d/%m/%Y").date()).days
                else:
                    rented_time_dict[rental.client_id] = (datetime.datetime.strptime(rental.returned_date, "%d/%m/%Y").date()
                                                          - datetime.datetime.strptime(rental.due_date, "%d/%m/%Y").date()).days

        return sorted(rented_time_dict.items(), key=lambda x: int(x[1]), reverse=True)

    def most_active_clients(self):
        """
        Creates and returns a list containing the most active clients ordered descending based on total rented time
        """
        most_active_clients_list = []
        rented_time_dict = self.client_id_with_rented_time_descending()
        for key, value in rented_time_dict:
            most_active_clients_list.append([key, self._client_repository.find_by_id(key).name, value])

        return most_active_clients_list

    def movie_id_with_delay_descending(self):
        """
            Creates and returns a dictionary in which the dictionary keys represent movie ids and their corresponding
        values represent the number of days of rental return delay. This dictionary is sorted in descending order by
        delay time.
        """
        rental_list = self._rental_repository.get_all()
        rented_time_dict = {}
        for rental in rental_list:
            if rental.returned_date == '-' and datetime.datetime.strptime(rental.due_date, "%d/%m/%Y").date() < datetime.date.today():
                if rental.movie_id in rented_time_dict:
                    rented_time_dict[rental.movie_id] += (datetime.date.today() - datetime.datetime.strptime(rental.due_date, "%d/%m/%Y").date()).days
                else:
                    rented_time_dict[rental.movie_id] = (datetime.date.today() - datetime.datetime.strptime(rental.due_date, "%d/%m/%Y").date()).days

        return sorted(rented_time_dict.items(), key=lambda x: int(x[1]), reverse=True)

    def late_rentals(self):
        """
        Creates and returns a list containing all late rentals ordered descending based on total rent time
        """
        late_rentals_list = []
        rented_time_dict = self.movie_id_with_delay_descending()
        for key, value in rented_time_dict:
            late_rentals_list.append([key, self._movie_repository.find_by_id(key).title, value])

        return late_rentals_list


@dataclass
class UndoOperation:
    target_object: object
    handler: object
    entity: object

@dataclass
class EntityPair:
    entity1: object
    entity2: object

class UndoManager:
    def __init__(self):
        self.__undo_operations = []

    def register_operation(self, target_object, handler, entity):
        self.__undo_operations.append(UndoOperation(target_object, handler, entity))

    def return_last_operation(self):
        if len(self.__undo_operations) == 0:
            raise ServicesException("\nOperation cannot be performed\n")
        return self.__undo_operations[-1]

    def clear_list(self):
        self.__undo_operations.clear()

    def undo(self):
        if len(self.__undo_operations)  == 0:
            raise ServicesException("\nOperation cannot be performed\n")
        undo_operation = self.__undo_operations.pop()
        undo_operation.handler(undo_operation.target_object, undo_operation.entity)