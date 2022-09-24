import unittest

from src.domain.domain import Movie
from src.domain.validators import MovieIdValidator, RentalValidator, MovieRentalException, ClientIdValidator
from src.repository.repository import Repository
from src.services.services import MovieServices, RentalServices, ClientServices, Statistics


class ServicesTest(unittest.TestCase):

    def setUp(self) -> None:
        """
        Runs before every test method
        """
        movie_repository = Repository(MovieIdValidator)
        rental_repository = Repository(RentalValidator)
        self._movie_service = MovieServices(movie_repository, rental_repository)
        self._rental_service = RentalServices(rental_repository)
        client_repository = Repository(ClientIdValidator)
        self._client_service = ClientServices(client_repository)
        self._statistics_service = Statistics(movie_repository, client_repository, rental_repository)

    def test_add(self):
        self._movie_service.add_movie('1234','Frozen','abcdefg','Drama')
        self.assertEqual(len(self._movie_service._movie_repository._entities), 1)
        self._rental_service.add_rental('1234', '1234', '1234', '01/12/2002', '01/12/2005', '-')
        self.assertEqual(len(self._rental_service._rental_repository._entities), 1)
        with self.assertRaises(MovieRentalException):
            self._rental_service.add_rental('5555', '5555', '1234', '01/12/2021', '05/12/2021', '-')

    def test_check_id_existence(self):
        self._movie_service.add_movie('1234', 'Frozen', 'abcdefg', 'Drama')
        self.assertEqual(self._movie_service.check_id_existence('1234'), 1)
        with self.assertRaises(MovieRentalException):
            self._movie_service.check_id_existence('5555')

    def test_remove_by_id(self):
        self._movie_service.add_movie('1234', 'Frozen', 'abcdefg', 'Drama')
        self._movie_service.remove_movie_by_id('1234')
        self.assertEqual(len(self._movie_service._movie_repository._entities), 0)

    def test_check_update_by_id(self):
        self._movie_service.add_movie('1234', 'Frozen', 'abcdefg', 'Drama')
        update = Movie('1234', 'Alien', 'ABDCDG', 'Comedy')
        self._movie_service.update_movie_by_id('1234', 'Alien', 'ABDCDG', 'Comedy')

    def test_check_get_all(self):
        self._movie_service.add_movie('1234', 'Frozen', 'abcdefg', 'Drama')
        self._movie_service.add_movie('5555', 'Frozen 2', 'abcdefg', 'Drama')
        list = self._movie_service.get_all_movies()
        self.assertEqual(list[0].id, '1234')
        self.assertEqual(list[1].id, '5555')

    def test_check_rental_condition(self):
        self._rental_service.add_rental('1', '1', '1', '02/10/2021', '04/11/2021', '05/10/2021')
        self.assertEqual(self._rental_service.check_rental_condition('1'), True)
        self._rental_service.add_rental('2', '2', '1', '01/10/2021', '01/11/2021', '-')
        self.assertEqual(self._rental_service.check_rental_condition('1'), False)

    def test_rental_return(self):
        self._rental_service.add_rental('1', '1', '1', '02/10/2021', '04/11/2021', '05/10/2021')
        with self.assertRaises(MovieRentalException):
            self._rental_service.return_rental('1', '01/02/2021')
        self._rental_service.add_rental('2', '1', '1', '02/10/2021', '04/11/2021', '-')
        self._rental_service.return_rental('2', '01/02/2021')
        self.assertEqual(self._rental_service._rental_repository._entities['2'].returned_date, '01/02/2021')

    def test_search_tool(self):
        self._movie_service.add_movie('1234', 'Frozen', 'abcdefg', 'Drama')
        self._movie_service.add_movie('5555', 'Frozen 2', 'abcdefg', 'Horror')
        list = self._movie_service.movie_search_tool('fR')
        self.assertEqual(list[0].id, '1234')
        self.assertEqual(list[1].id, '5555')
        list = self._movie_service.movie_search_tool('hor')
        self.assertEqual(list[0].id, '5555')

    def test_movie_id_with_rented_time_descending(self):
        self._movie_service.add_movie('1', 'Frozen', 'abcdefg', 'Drama')
        self._movie_service.add_movie('2', 'Alien', 'abcdefg', 'Horror')
        self._rental_service.add_rental('1', '1', '1', '05/11/2021', '20/11/2021', '-')
        self._rental_service.add_rental('2', '2', '2', '01/11/2021', '20/11/2021', '-')
        list1 = self._statistics_service.movie_id_with_rented_time_descending()
        list2 = [('2', 321), ('1', 317)]
        self.assertEqual(list1,list2)

    def test_most_rented_movies(self):
        self._movie_service.add_movie('1', 'Frozen', 'abcdefg', 'Drama')
        self._movie_service.add_movie('2', 'Alien', 'abcdefg', 'Horror')
        self._rental_service.add_rental('1', '1', '1', '05/11/2021', '20/11/2021', '-')
        self._rental_service.add_rental('2', '2', '2', '01/11/2021', '20/11/2021', '-')
        list1 = self._statistics_service.most_rented_movies()
        list2 = [['2', 'Alien', 321], ['1', 'Frozen', 317]]
        self.assertEqual(list1, list2)

    def test_movie_id_with_delay_descending(self):
        self._movie_service.add_movie('1', 'Frozen', 'abcdefg', 'Drama')
        self._movie_service.add_movie('2', 'Alien', 'abcdefg', 'Horror')
        self._rental_service.add_rental('1', '1', '1', '05/11/2021', '20/11/2021', '-')
        self._rental_service.add_rental('2', '2', '2', '01/11/2021', '20/11/2021', '-')
        list1 = self._statistics_service.movie_id_with_delay_descending()
        list2 = [('2', 321), ('1', 317)]
        self.assertEqual(list1, list2)

    def test_late_rentals(self):
        self._movie_service.add_movie('1', 'Frozen', 'abcdefg', 'Drama')
        self._movie_service.add_movie('2', 'Alien', 'abcdefg', 'Horror')
        self._rental_service.add_rental('1', '1', '1', '05/11/2021', '20/11/2021', '-')
        self._rental_service.add_rental('2', '2', '2', '01/11/2021', '20/11/2021', '-')
        list1 = self._statistics_service.late_rentals()
        list2 = [['2', 'Alien', 321], ['1', 'Frozen', 317]]
        self.assertEqual(list1, list2)

