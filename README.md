## How to Use

---
### Clone this repository
```
    $ https://github.com/husanIbragimov/impact.t.git 
```
    
### Go into the repository
```
    $ cd impact.t
```
### Create two files
```
    $ mkdir static
    $ mkdir media
```
### Create a virtual environment 
#### Linux & Mac 
```
    $ virtualenv venv 
```
#### Windows
        $ py -m venv venv  
    
    
### Active your virtual environment 
#### Linux & Mac
        $ source venv/bin/activate             
#### Windows
        $ venv\Scripts\activate
    
### Install dependencies
        $ pip install -r requirements.txt
    
### Migrate the original database schema to the SQLite3 database using the management script:
#### Linux & Mac
        $ python manage.py makemigrations      
        $ python manage.py migrate     
#### Windows
        $ py manage.py makemigrations
        $ py manage.py migrate
    
### Create an administrative user for the project by typing:
#### Linux & Mac                         
        $ python manage.py createsuperuser     
#### Windows   
        $ py manage.py createsuperuser
    
### Collect all static content into the directory that has been configured:
#### Linux & Mac                         
        $ python manage.py collectstatic
#### Windows
        $ py manage.py collectstatic
    
### Run the app
#### Linux & Mac                          
        $ python manage.py runserver           
#### Windows
``` 
    $ py manage.py runserver
```


## Swagger UI

---

![Screenshot](static/Screenshot%20from%202023-06-11%2000-38-06.png)


## Read the documentation

---

__If you want to use the [API](https://xusandev.pythonanywhere.com/), firstly, you should read the [Postman documentation](https://documenter.getpostman.com/view/21553790/2s93sXdFP4#049bf4c6-1894-450d-bfde-a42f582b3b4b)__





