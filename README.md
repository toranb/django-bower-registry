## Bower registry (the python/django edition)

I wrote this bower registry so you could run it on the raspberry pi

## Install the dependencies

    mkvirtualenv registry
    pip install -r requirements.txt

## Sync your database and run migrations

    python manage.py dev syncdb --migrate --noinput

## Run the webserver locally

    python manage.py dev runserver

## Create package

    curl http://localhost:8000/packages/ -v -F 'name=jquery' -F 'url=git://github.com/jquery/jquery.git'

## Find package

    curl http://localhost:8000/packages/jquery/

## Development

    python manage.py test test
      
## License

Copyright © 2013 Toran Billups

Licensed under the MIT License
