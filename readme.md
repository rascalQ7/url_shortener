1. Generate database objects:

    `python manage.py makemigrations`

    `python manage.py migrate`
    
1. Generate config items from fixtures:
    
    `python manage.py loaddata tiny_urls/fixtures/config_items.json`

1. Create superuser:

    `python manage.py createsuperuser`

1. Start url shortener service locally:

    `pip install -r requirements.txt`
    
    `python manage.py runserver`

    Or as docker container:

    `docker-compose up`

