import os.path
import pickle

from src.repository.repository import Repository


class EntityRepositoryBin(Repository):
    def __init__(self, validator_class, file_name):
        super().__init__(validator_class)
        self.__file_name = file_name
        self.__load_data()

    def __get_data(self):
        return super().get_all()

    def __load_data(self):
        if os.path.getsize(self.__file_name) > 0:
            with open(self.__file_name, "rb") as file_pointer:
                while True:
                    try:
                        entity = pickle.load(file_pointer)
                        super().save(entity)
                    except (EOFError, pickle.UnpicklingError):
                        break

    def __save_to_file(self):
        try:
            entities = self.__get_data()
            with open(self.__file_name, "wb") as file_pointer:
                for entity in entities:
                    pickle.dump(entity, file_pointer)
        except:
            open(self.__file_name, "w").close()

    def find_by_id(self, entity_id):
        return super().find_by_id(entity_id)

    def save(self, entity):
        super().save(entity)
        self.__save_to_file()

    def delete_by_id(self, entity_id):
        super().delete_by_id(entity_id)
        self.__save_to_file()

    def update(self, entity_id, entity):
        super().update(entity_id, entity)
        self.__save_to_file()



