from dataclasses import dataclass

@dataclass
class BaseEntity:
    id: str = ''

@dataclass
class Movie(BaseEntity):
    title: str = ''
    description: str = ''
    genre: str = ''

@dataclass()
class Client(BaseEntity):
    name: str = ''

@dataclass()
class Rental(BaseEntity):
    movie_id: str = ''
    client_id: str = ''
    rented_date: str = ''
    due_date: str = ''
    returned_date: str = '-'

