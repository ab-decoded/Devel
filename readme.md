# DEVEL
### Create pages for web on the web.   

*Platform to easily design webpage using intuitive tools and easy-to-learn interface.*

The aim of the project is to provide an open-source platform for the users to see and make live changes to their web page. Devel provides an interactive UI to select the components to add to the webpage(divs, images, tables, grids, text), styling and arrangement of the components. Devel allows downloading the webpage(HTML file along with css) for use in some project.
The project creates templates using Semantic-UI for grid system, and allows the user to choose from predefined set of mockups. 

#### Tech stack
* Django(Python-2.7) for backend
* MySQL for database
* Semantic-UI, jQuery, Interact.js, jQuery-ui for frontend

#### Features
* Easily insert and edit.
![alt tag](https://s3-us-west-2.amazonaws.com/devel-store/insert.gif)
* Many easy-to-use features like color dropper.
![alt tag](https://s3-us-west-2.amazonaws.com/devel-store/color.gif)

*The project is live at [devel-ab.ml](http://devel-ab.ml)(no machine learning in there :P, just too lazy to get a new domain)* 


#### Installation(Development)
* ```git clone https://github.com/ab-decoded/Devel.git``` (Or using ssh)
* ```cd Devel```
* Setup virtualenv
* ```pip install -r requirements.txt```
* Create database ```devel``` in MYSQL and add your MySQL credentials in devel_main/settings.py
* Create a superuser for django(mainly for adding mockups) ```python manage.py createsuperuser```
* Makemigration(creating new migrations based on the changes you have made to your models): ```python manage.py makemigrations```; 
Migrate( applying migrations, actually making tables in database): ```python manage.py migrate```; To run: ```python manage.py runserver```
* **Setup social login (optional)**: In MySQL, select ```devel``` database

  ```sql
  UPDATE django_site SET DOMAIN = '127.0.0.1:8000', name = 'Vort' WHERE id=1;
  INSERT INTO socialaccount_socialapp (provider, name, secret, client_id, `key`)
  VALUES ("facebook", "Facebook", "--put-your-own-app-secret-here--", "--put-your-own-app-id-here--", '');
  INSERT INTO socialaccount_socialapp_sites (socialapp_id, site_id) VALUES (1,1); 
  ```
##### Any contribution and suggestion is appreciated. 
*The project in no terms is complete and requires many new features. Any contribution in this regard is valuable. Feel free to use and modify as per requirements.*

.
