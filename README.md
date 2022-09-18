# About this project

<img width="400" src="https://user-images.githubusercontent.com/98110966/190910122-a5d7303c-0ce1-4b21-a9f3-c561661502db.png">

# Overview

**Movie Rental Service** is a desktop application that allows its user to manage a movie rental service. It is written in **Python**. This project was done as an assignment for University and should be treated as a display of the ability to juggle with object-oriented programming concepts, rather than as a tool that is innovative. **Unit tests** are performed for repository and service layers.

# Functionalities

Movie entity - id, title, description, genre
Client entity - id, name
Rental entity - rental id, movie id, client id, rent date, due date

All information is input by the user from the keyboard.

1. Add a movie - adds a movie to the local repository
2. Remove a movie - removes a movie from the local repository; the movie is identified by title
3. List all movies - prints all movies within the local repository to the console
4. Update a movie - updates information about a movie within the local repository; the movie is identified by title
5. Add a client - adds a client to the local repository
6. Remove a client - removes a client from the local repository; the client is identified by name
7. List all clients - prints all clients within the local repository to the console
8. Update a client - updates information about a client within the local repository; the client is identified by name
9. Rent a movie - given a movie id, client id, rent date and due date, a rental entity will be added
10. Return a movie - given the rental id, the rental entity will be removed
11. List all rentals - prints all active rentals within the local repository to the console
12. Search for movie - given a string
13. Search for client
14. List most rented movies
15. List most active clients
16. List all late rentals
17. Undo last operation
18. Redo last operation
19. Exit
