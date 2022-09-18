# About this project

<p align="center">
<img width="400" src="https://user-images.githubusercontent.com/98110966/190915808-83c9296e-9a8a-4e19-9b2f-951a85cf2b04.png">
</p>

# Overview

**Movie Rental Service** is a console-based desktop application that allows its user to manage a movie rental service. It is written in **Python**. This project was done as an assignment for University and should be treated as a display of the ability to juggle with **object-oriented programming concepts**, rather than as a tool that is innovative. **Unit tests** are performed for repository and service layers. A particularity of this project is the implementation of **undo** and **redo** functionalities using a **reverse operation** approach.

FOR **VIDEO DEMONSTRATION** PLEASE REFER TO THE FOLLOWING ANCHORS:

[Video Demonstration](#video-demonstration)

# Functionalities

**Movie entity** - id, title, description, genre

**Client entity** - id, name

**Rental entity** - rental id, movie id, client id, rent date, due date

All information is input by the user from the keyboard. The user is informed at each step regarding what information should be provided.

 1. **Add a movie** - adds a movie to the local repository
 2. **Remove a movie** - removes a movie from the local repository; the movie is identified by id
 3. **List all movies** - prints all movies within the local repository to the console
 4. **Update a movie** - updates information about a movie within the local repository; the movie is identified by id
 5. **Add a client** - adds a client to the local repository
 6. **Remove a client** - removes a client from the local repository; the client is identified by id
 7. **List all clients** - prints all clients within the local repository to the console
 8. **Update a client** - updates information about a client within the local repository; the client is identified by id
 9. **Rent a movie** - given a movie id, client id, rent date and due date, a rental entity will be added
10. **Return a movie** - given the rental id, the rental entity will be removed
11. **List all rentals** - prints all active rentals within the local repository to the console
12. **Search for movie** - given a string, performs a search and prints to the console all movies containing said string within their title
13. **Search for client** - given a string, performs a search and prints to the console all clients containing said string within their name
14. **List most rented movies** - prints all movies ordered descending based on number of days rented to the console
15. **List most active clients** - prints all clients ordered descending based on total rented time to the console
16. **List all late rentals** - prints all active rental entities that have a due date that has passed, sorted descending by amount of time since their due date
17. **Undo last operation** - undo functionality for data altering operations
18. **Redo last operation** - redo functionality for data altering operations
19. **Exit** - closes the application

A client that has a not returned a rental that is passed its due date cannot rent any other movie until returning the first one.

# Input Validation

All user input is validated. Attempting to print an empty local repository will show an appropriate message. This is also the case if a search function has found no matching results. Here are a few examples:

<p align="center">
<img width="250" src="https://user-images.githubusercontent.com/98110966/190916098-1f47ea21-efeb-4388-bb38-23413adb222f.png">
</p>

<p align="center">
<img width="200" src="https://user-images.githubusercontent.com/98110966/190916132-6bc303c6-6db7-4f95-ae86-4ce4f8698a6e.png">
</p>

<p align="center">
<img width="250" src="https://user-images.githubusercontent.com/98110966/190916174-c7f6b608-6c7d-4499-92d6-d182405ffd10.png">
</p>

# Save File

Each entity repository can be saved either **in memory**, **to a text file** or **to a binary file**. The file type can be changed through the `settings.properties` file. For in memory storage, assign "inmemory" to the `repository` property. For saving to a text file, assign "textfiles" to the `repository` property. For saving to a binary file, assign "binaryfiles" to the `repository` property. Destination file is chosen by assigning a filepath to the `movies`, `clients` and `rentals` properties. A method adds mock data in memory on application startup; this method should be commented out if in memory storage is not used to avoid a duplicate id exception.

<p align="center">
<img width="400" src="https://user-images.githubusercontent.com/98110966/190916882-0af2ae09-701b-4e47-bc14-e5a8c4851d30.png">
</p>



# Video Demonstration

Mock data was added beforehand in order to be able to show functionalities.
