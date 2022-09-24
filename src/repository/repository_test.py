import unittest

from src.domain.domain import Movie, Client, Rental
from src.domain.validators import RentalValidator, ClientIdValidator, MovieIdValidator, MovieRentalException
from src.repository.repository import Repository

class RepositoryTest(unittest.TestCase):

    def setUp(self) -> None:
        """
        Runs before every test method
        """
        self._movie_repo = Repository(MovieIdValidator)
        self._client_repo = Repository(ClientIdValidator)
        self._rental_repo = Repository(RentalValidator)

    def test_empty_movie_repository(self):
        self.assertEqual(len(self._movie_repo._entities), 0)
        self.assertEqual(len(self._client_repo._entities), 0)
        self.assertEqual(len(self._rental_repo._entities), 0)

    def test_movie_add(self):
        self._movie_repo.save(Movie('1234', 'Frozen', 'abcdefg', 'Comedy'))
        self.assertEqual(len(self._movie_repo._entities), 1)
        with self.assertRaises(MovieRentalException):
            self._movie_repo.save(Movie('1234', 'Frozen', 'abcdefg', 'Comedy'))

    def test_client_add(self):
        self._client_repo.save(Client('1234', 'John Wick'))
        self.assertEqual(len(self._client_repo._entities), 1)

    def test_rental_add(self):
        self._rental_repo.save(Rental('1234', '1234', '1234', '01/12/2002', '01/12/2005', '-'))
        self.assertEqual(len(self._rental_repo._entities), 1)

    def test_find_by_id(self):
        self._movie_repo.save(Movie('1234', 'Frozen', 'abcdefg', 'Comedy'))
        self.assertEqual(self._movie_repo.find_by_id('1234'), self._movie_repo._entities['1234'])
        self.assertEqual(self._movie_repo.find_by_id('1'), None)

    def test_update_by_id(self):
        self._movie_repo.save(Movie('1234', 'Frozen', 'abcdefg', 'Comedy'))
        updated_movie = Movie('1234', 'Alien', 'abcdefg', 'Thriller')
        self._movie_repo.update('1234', updated_movie)
        self.assertEqual(self._movie_repo._entities['1234'], updated_movie)
        with self.assertRaises(MovieRentalException,):
            self._movie_repo.update('5555', updated_movie)

    def test_remove_by_id(self):
        self._movie_repo.save(Movie('1234', 'Frozen', 'abcdefg', 'Comedy'))
        self._movie_repo.delete_by_id('1234')
        self.assertEqual(len(self._movie_repo._entities), 0)
        with self.assertRaises(MovieRentalException):
            self._movie_repo.delete_by_id('1234')

    def test_get_all(self):
        with self.assertRaises(MovieRentalException):
            list = self._movie_repo.get_all()
        self._movie_repo.save(Movie('1234', 'Frozen', 'abcdefg', 'Comedy'))
        self._movie_repo.save(Movie('5555', 'Frozen', 'abcdefg', 'Comedy'))
        list = self._movie_repo.get_all()
        self.assertEqual(list[0].id, '1234')
        self.assertEqual(list[1].id, '5555')