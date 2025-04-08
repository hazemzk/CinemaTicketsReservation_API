🎟️ Cinema Tickets Reservation API
This project is an API built using Django REST Framework for managing and reserving cinema tickets.

🚀 Features
View available movies and showtimes

Reserve a ticket for a specific movie

Manage guests and reservations through a RESTful API

Full support for CRUD operations (Create, Read, Update, Delete)

Simple login system using Basic Authentication

Clean code structure using CBVs and ViewSets

📁 Project Structure
View all available movies and their showtimes

Reserve a ticket for a specific movie

Edit or cancel your reservation

All operations are done through a REST API (can be used in mobile or web apps)

Protected access using Basic Authentication (login required)

Folders and Files:

project/: Contains Django settings (database, URLs, installed apps)

tickets/: The core app that includes:

Models (database tables)

Views (handles request logic)

Serializers (convert data between JSON and Python objects)

manage.py: Project launcher script

requirements.txt: Lists all required libraries

📡 Endpoints
Examples:

/api/movies/ ➜ Lists all movies

/api/reservations/ ➜ Lists all reservations

Use POST to create a reservation

Use PUT / DELETE to update or delete a reservation

Developed by:
@hazemzk 🎉
