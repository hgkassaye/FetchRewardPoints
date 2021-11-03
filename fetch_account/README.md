Date: 11/03/2021

# Fetch Rewards Points

This application is built using Django's web framework to allow users to see view thier available rewards points and/or redeem what they need. 

## Required Packages

Packages required: 
* python = 3.8.5
* Django = 3.2.6

You can use a virtual enviroment to install these Packages. Make sure you use the versions specified above as 
the application is not tested for forward and backward compatibailities with other versions. Install as follows:
1. brew install python==3.8.5
2. pip3 install Django==3.2.6

## Run Development Server
Once you have insalled the package (activate virtual env if needed), clone this repository and navigate into project directory in your terminal window. 

Run the followings commands to start a development server:
1. cd fetch_account (make sure you are on the top fetch_account directory since there are two directories with the same name)
2. python3 manage.py migrate
3. python3 mamage.py makemigrations account_app
4. python3 manage.py migrate
5. python3 manage.py runserver

At this point the development server is started. Copy the link provided into your browser (use Google Chrome). Use the navigation menu to add transactions, redeem points and
get points summary

