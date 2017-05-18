# Wild (Item-Catalog)
Wild is a video game catalog where users can view a catalog of games, view games by genre, add new games, or edit/delete a game. A user must be logged in to do anything more than view game information, and they can only modify the games that they have entered into the site.

## Installation
In order to run this application, users will need to have Python and Git installed on their machines.

They will then need to clone this Github Repo by running the following command in their terminal:

    $ git clone https://github.com/toriancrane/item-catalog.git

Use the terminal to navigate into the folder where the application files are housed.

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
