
from jproperties import Properties

from src.domain.validators import MovieIdValidator, ClientIdValidator, RentalValidator
from src.repository.entities_data_access import MovieDataAccess, RentalDataAccess, ClientDataAccess
from src.repository.entity_repository_bin import EntityRepositoryBin
from src.repository.entity_repository_text import EntityRepositoryText
from src.repository.repository import Repository
from src.services.services import MovieServices, ClientServices, RentalServices, Statistics
from src.ui.console import Console

config = Properties()
with open('settings.properties', 'rb') as config_file:
    config.load(config_file)

movie_validator = MovieIdValidator
rental_validator = RentalValidator
client_validator = ClientIdValidator

repo_type = config.get('repository')[0]
if repo_type == 'inmemory':
    movie_repository = Repository(movie_validator)
    rental_repository = Repository(rental_validator)
    client_repository = Repository(client_validator)
elif repo_type == 'textfiles':
    movie_repository = EntityRepositoryText(movie_validator, config.get('movies')[0], MovieDataAccess)
    rental_repository = EntityRepositoryText(rental_validator, config.get('rentals')[0], RentalDataAccess)
    client_repository = EntityRepositoryText(client_validator, config.get('clients')[0], ClientDataAccess)
else:
    movie_repository = EntityRepositoryBin(movie_validator, config.get('movies')[0])
    rental_repository = EntityRepositoryBin(rental_validator, config.get('rentals')[0])
    client_repository = EntityRepositoryBin(client_validator, config.get('clients')[0])



movie_services = MovieServices(movie_repository, rental_repository)
client_services = ClientServices(client_repository)
rental_services = RentalServices(rental_repository)

statistics_services = Statistics(movie_repository, client_repository, rental_repository)

console = Console(movie_services, client_services, rental_services, statistics_services)

console.run_console()

