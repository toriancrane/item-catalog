# Wild (Item-Catalog)
Wild is a video game catalog where users can view a catalog of games, view games by genre, add new games, or edit/delete a game. A user must be logged in to do anything more than view game information, and they can only modify the games that they have entered into the site.

A live version of this site can be found [here](http://wildapp.herokuapp.com/).

## Installation and Usage
In order to run this application, users will need to have Python and Git installed on their machines.

They will then need to clone this Github Repo by running the following command in their terminal:

    $ git clone https://github.com/toriancrane/item-catalog.git

Use the terminal to navigate into the folder where the application files are housed.

The contents of the folder include a number of files:

* project.py is used to run the web server
* requirements.txt is used to help users install all of the necessary requirements to run the application
* database_setup.py is used to initalize the database
* lotsofgames.py is used to populate the database with dummy information
* db_methods.py houses the database queries that are used to manipulate the CRUD database functions
* the templates folder holds all of the HTML templates used to render the application
* the static folder holds all of the css files used for styling

To install the requirements necessary to run the application, enter:

    $ pip install -r requirements.txt

To set up the database that will keep track of game information, enter:

    $ python database_setup.py

A list of games and game info has been provided for users to pre-populate the database with some dummy information

To populate the database with dummy information, enter:

    $ python lotsofgames.py

To run the server and browse the application, enter:

    $ python project.py

Then, navigate to localhost:8000 in your browser.
