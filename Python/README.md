# Python

But this is not a development course!

...

.....

FINE!

## main.py

Nothing fancy. Just run Flask in port 8666 with the application.

## Flask 3.1.1

The flask structure is divided into blue-prints to allow a logical separation (or realms if you like).

## Jinja

All HTML pages are Jinja templates to allow dynamic filling-in.

## MVC structure

Because WEB programming lessons made it clear that it is a must.

### main

The main page. As basic as base can base. A single route to the index.

### inventory

GET functionalities:
1. Display the current inventory

POST functionalities:
1. Add a new item
2. Edit existing item
3. Delete an item

### projects

GET functionalities:
1. Display the current projects

POST functionalities:
1. Add a new project
2. Edit an existing project
3. Delete a project

### statistics

GET functionalities:
1. Display the statistics

## The application is hardcoded to port 8666 because why not

# Docker

Not much to say. Trying to decrease the image size, implement additionas that Flask need and compile the project in a standard python app docker file manner.

