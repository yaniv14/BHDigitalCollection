# Setup instructions

* Clone repository from your own fork::
    
        git clone git@github.com:your_user_name/JewishDiaspora.git

* Create a virtualenv:

        mkvirtualenv diaspora

* Upgrade pip:

        pip install -U pip

* Install requirements:

        pip install -r requirements.txt

* Migrate latest changes::

        python manage.py migrate

* Create a superuser::

        python manage.py createsuperuser myname

* Run the server::

        python manage.py runserver
