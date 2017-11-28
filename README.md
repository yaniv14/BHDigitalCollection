# Setup instructions

* Clone this repo.
* Create a virtualenv:

        mkvirtualenv diaspora

* Install requirements:

        pip install -r requirements.txt

* Migrate tables

	    m migrate
	    m makemigrations artifacts
	    m sqlmigrate artifacts 0001

* Create tables:

        m migrate

* Run your server:

        m runserver

* Enjoy: http://localhost:8000/