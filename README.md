# Setup instructions

* Clone repository from your own fork::
    
        git clone git@github.com:your_user_name/BHDigitalCollection.git

* Create a virtualenv:

        mkvirtualenv bh

* Upgrade pip:

        pip install -U pip

* Install requirements:

        pip install -r requirements.txt

* Migrate latest changes::

        python manage.py migrate

* Create sample data for testing::

        python manage.py create_artifacts 20

* Create a superuser::

        python manage.py createsuperuser

* Run the server::

        python manage.py runserver
