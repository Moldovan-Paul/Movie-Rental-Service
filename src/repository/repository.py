from src.domain.validators import MovieRentalException

class RepositoryException(MovieRentalException):
    pass

class Repository(object):
    def __init__(self, validator_class):
        self._validator_class = validator_class
        self._entities = {}

    def find_by_id(self, entity_id):
        """
        Search for an entity by id
        :param entity_id: Entity's id
        :return: Entity if found, None otherwise
        """
        if entity_id in self._entities:
            return self._entities[entity_id]
        return None

    def save(self, entity):
        """
        Adds entity to entity list
        :param entity: Entity to be added
        """
        if self.find_by_id(entity.id) is not None:
            raise RepositoryException(f"\nId already in use {entity.id}\n")
        self._validator_class.validate(entity)
        self._entities[entity.id] = entity

    def update(self, entity_id, entity):
        """
        Updates an entity identified by a given id
        :param entity_id: Id of entity to be modified
        :param entity: New entity to replace the old one
        """
        if self.find_by_id(entity_id) is None:
            raise RepositoryException("\nId does not exist\n")
        self._entities[entity_id] = entity

    def delete_by_id(self, entity_id):
        """
        Deletes an entity identified by a given id
        :param entity_id: Id of entity to be removed
        """
        if self.find_by_id(entity_id) is None:
            raise RepositoryException("\nId does not exist\n")
        del self._entities[entity_id]

    def get_all(self):
        """
        Returns a list of values of all entities in the entity dictionary
        """
        if len(list(self._entities.values())) == 0:
            raise RepositoryException("\nNo entities in memory\n")
        return sorted(list(self._entities.values()), key=lambda entity: int(entity.id))


