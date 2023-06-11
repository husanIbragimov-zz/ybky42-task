## How to Use

---

```bash
    # Clone this repository
    $ https://github.com/husanIbragimov/impact.t.git 
    
    # Go into the repository
    $ cd impact.t
    
    # Create two files
    $ mkdir static
    $ mkdir media
    
    # Create a virtual environment
    # Linux & Mac                         # Windows 
    $ virtualenv venv                     $ py -m venv venv  
    
    
    # Active your virtual environment 
    # Linux & Mac                          # Windows
    $ source venv/bin/activate             $ venv\Scripts\activate
    
    
    # Install dependencies
    $ pip install -r requirements.txt
    
    # Migrate the original database schema to the SQLite3 database using the management script:
    # Linux & Mac                          # Windows
    $ python manage.py makemigrations      $ py manage.py makemigrations
    $ python manage.py migrate             $ py manage.py migrate
    
    
    # Create an administrative user for the project by typing:
    # Linux & Mac                          # Windows
    $ python manage.py createsuperuser     $ py manage.py createsuperuser
    
    
    # Collect all static content into the directory that has been configured:
    # Linux & Mac                          # Windows
    $ python manage.py collectstatic       $ py manage.py collectstatic
    
    
    # Run the app
    # Linux & Mac                          # Windows
    $ python manage.py runserver           $ py manage.py runserver
    
    
    # Welcome :)
```

