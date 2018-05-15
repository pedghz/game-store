**Project plan Web Software Development**

**Project name: Django unchained**

**Project Information:**

**Name of the project: wsd17-Django Unchained**

**Communication Application: djangounchained-group.slack.com**

**Version control system: https://gitlab.rd.tut.fi/ghazi/Web\_development\_project.git**

**Scope of the project:**

The objective of the project is to implement a game store where players can play their favorite online games and developers can upload games to the store.

For this project, we plan to implement the following features:

- Create an authentication system so that players and developers may login, logout and register,
- The players will have the possibility to buy and explore games. They will also be able to check high-scores and save their own high-scores (provide some game-service interaction),
- The developers will be allowed to upload games to their inventory and see the list of game sales,

**Detail of functionalities:**

We will now give more details about the different points:

The authentication system will use an email validation scheme to make sure that new users are real.(Update: We have not implemented the email verification)

For paying games, we will use a mockup payment service. Having to buy games implies that players may only play games they purchased. The exploration of games may be done through a search bar.

Deletion and update of games may be done by the developer. The developer should also have the ability to see his selling statistics.

As for security restrictions, we will make sure that developers are only allowed to modify, delete and add their own games (modify their own inventory).

As for additional functionalities, we will update this document as we advance.

For the functionalities, since we are just starting in the field, we only know that we will be using Javascript, HTML/CSS and Django plus one or two third-party APIs. As a result, we will enrich this part later on i.e when we start doing actual coding.

**Organization of the groupwork**

The organization of the groupwork will be done as follows: we will meet on a weekly basis to keep each other up to date. During the week, we will communicate through Slack where we already created a group. As for, version control, since our repository is in Gitlab, we will be using Git.



**UPDATES:**

**Javascript games:**
We have developed 2 javascript games which can send/recive save/load-request/load/score/settings messages and act properly accordingly.


**Apps:**
We have thre different apps dealing with the store tasks:
1- authentication: In this app we deal with the registration, login, edit account, game upload, edit or remove game
2- playing_area: This is somehow the main app which is responsible for the hompage, the page in which we have games' list, and the page that someone can play a game.
3- purchase: In this app we implement the parts related to placing orders and buying games.

**The models:**
* Profile - Which is extended form User and it has two more fields, one is a charfield for the account type and another one is a manytomany field for the games people have purchased.
* Game - A table for storing games' information 
* GameState - A table to store game states which has foreign keys to User and Game table
* Order - Which stores the data about different orders.

**The views:**

**In authentication app:**
- login_register_page(only loading the page for login and register)
- login_view(dealing with login)
- logout_view(dealing with logout)
- register_view(dealing with register)
- add_game(dealing with adding a game)
- my_profile(dealing with users profile page and changing the info about the user)
- reset_password(dealing with changing the password)
- developer_games(dealing with the developers page, showing the games he\she has developed)
- edit_game(dealing with changin one game's info)

**In playing_area app:**
- my_index(dealing with the homepage)
- my_gameslist(dealing with the page that has list of games and user is able to filter by genre or search a game's name)
- playing_game(dealing with the page that user plays a game)

**In purchase app:**
- owned_game(dealing with list of purchased games)
- shopping_cart(dealing with the page of shopping cart and items in the basket)
- order(checks if the game is in the purchased games or not and it checks if the status of order and finally insert the order in coresponding table)
- order_details(sends/recieves info from the payment service and creates the structure of payment)
- payment_result(deals with the payment and its result if it validated the payment. finally it deletes the related session for the coresponding order)
- finish_payment(if the payment was successful it redirects list of purchased games.)


Extra Features: We also have also tried to implement 3rd party login and Restful api


Link of the project on Heroku(without restful api):
https://game-store-django.herokuapp.com/

Link of the project on Heroku(with restful api):
https://floating-mesa-39921.herokuapp.com/


Link to the Project Demonstration Document:
https://docs.google.com/document/d/12rStTj5OB8pHWQCZLCn5SQtm9VuP7aGVIM4bOsFyyOY/edit#
