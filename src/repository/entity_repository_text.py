
from src.repository.repository import Repository


class EntityRepositoryText(Repository):
    def __init__(self, validator_class, file_name, entity_class):
        super().__init__(validator_class)
        self.__file_name = file_name
        self.__entity_class = entity_class
        self.__load_data()

    def __load_data(self):
        with open(self.__file_name) as file_pointer:
            for line in file_pointer:
                entity = self.__entity_class().read_from(line)
                super().save(entity)

    def find_by_id(self, entity_id):
        return super().find_by_id(entity_id)

    def save(self, entity):
        super().save(entity)
        self.__save_to_file(entity)

    def delete_by_id(self, entity_id):
        super().delete_by_id(entity_id)
        self.__update_file()

    def update(self, entity_id, entity):
        super().update(entity_id, entity)
        self.__update_file()

    def get_all(self):
        return super().get_all()

    def __save_to_file(self, entity):
        with open(self.__file_name, "a") as file_pointer:
            self.__entity_class().write_to(file_pointer, entity)

    def __update_file(self):
        try:
            entities = self.get_all()
            with open(self.__file_name, "w") as file_pointer:
                for entity in entities:
                    self.__entity_class().write_to(file_pointer, entity)
        except:
            open(self.__file_name, "w").close()

